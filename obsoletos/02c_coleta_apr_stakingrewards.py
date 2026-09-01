# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "pandas",
# ]
# ///
"""
Script 02c: Coleta do reward_rate (rendimento médio de staking) do ETH
Fonte: Staking Rewards API (GraphQL) -- https://www.stakingrewards.com/data-api
Saída:
  scripts_e_dados/Dados/apr_direto_stakingrewards.csv

POR QUE ESTE SCRIPT EXISTE
---------------------------
Alternativa à Beaconcha.in (que deixou de ter acesso gratuito irrestrito em
26/05/2026) e à derivação puramente algébrica do APR direto em
02_coleta_apr.py. A Staking Rewards tem um TIER GRATUITO explícito para
estudantes/hobbyistas (não é um trial que expira), GraphQL com suporte
nativo a consulta histórica, e trata o ETH como um "asset" de mercado --
não vinculado a nenhum provedor específico como a Lido -- que é
exatamente o benchmark independente de "staking direto" necessário para
calcular o ΔYield de forma empírica (seção 3.4.3).

COMO OBTER A API KEY
-----------------------
1. https://www.stakingrewards.com/data-api -> solicitar chave do tier
   gratuito ("hobbyists, enthusiasts, students, and startups")
2. export STAKINGREWARDS_API_KEY="sua_chave_aqui"

RECOMENDAÇÃO ANTES DE RODAR
-------------------------------
Teste a query abaixo primeiro no Playground deles
(api-docs.stakingrewards.com/playground), sem precisar de código, pra
confirmar que "reward_rate" traz valores plausíveis pro ETH (~3-6% ao
ano) antes de gastar créditos com a coleta automatizada.

LIMITAÇÕES CONHECIDAS (não pude testar contra a API ao vivo)
-----------------------------------------------------------------
1. Não confirmei o limite exato de créditos do tier gratuito nem o teto
   de linhas por requisição -- os exemplos da documentação usam limits
   diferentes em contextos diferentes. O script pagina em lotes
   moderados (BATCH_SIZE) e salva incrementalmente, então funciona
   independente de qual seja o teto real.
2. O filtro createdAt_gt pode ser "estritamente maior que" em nível de
   timestamp completo (não só a data) -- se você notar um dia faltando
   sistematicamente entre lotes consecutivos no CSV final, é esse o
   motivo; me avise que ajusto o avanço do cursor.
3. Não confirmei se "reward_rate" no nível de asset (em vez de
   "provider") é de fato o rendimento médio de rede, e não de um
   provedor específico -- os exemplos da documentação sugerem que sim,
   mas vale conferir os primeiros valores retornados contra alguma
   fonte que você já confie.
"""
import os
import sys
import time
import pandas as pd
import requests
from datetime import datetime

API_KEY = os.environ.get("STAKINGREWARDS_API_KEY")
ENDPOINT = "https://api.stakingrewards.com/public/query"
ASSET_SLUG = "ethereum-2-0"
METRIC_KEY = "reward_rate"

OUTPUT_DIR = os.path.join("scripts_e_dados", "Dados")
OUTPUT_FILE = "apr_direto_stakingrewards.csv"

# Recorte temporal -- manter em sincronia com o resto do pipeline
DATA_INICIO = "2022-05-01"
DATA_FIM = "2026-04-30"

BATCH_SIZE = 200  # pontos por requisição


def montar_query(created_at_gt: str, created_at_lt: str, limit: int) -> str:
    return f"""
    {{
      assets(where: {{ slugs: ["{ASSET_SLUG}"] }}, limit: 1) {{
        name
        metrics(
          where: {{
            metricKeys: ["{METRIC_KEY}"]
            createdAt_gt: "{created_at_gt}"
            createdAt_lt: "{created_at_lt}"
          }}
          order: {{ createdAt: asc }}
          limit: {limit}
        ) {{
          defaultValue
          createdAt
        }}
      }}
    }}
    """


def buscar_lote(created_at_gt: str, created_at_lt: str, session: requests.Session,
                 max_retries: int = 5) -> list:
    query = montar_query(created_at_gt, created_at_lt, BATCH_SIZE)
    for attempt in range(max_retries):
        try:
            resp = session.post(
                ENDPOINT,
                json={"query": query},
                headers={"Content-Type": "application/json", "X-API-KEY": API_KEY},
                timeout=20,
            )
        except requests.RequestException as e:
            print(f"  [ERRO DE REDE] {e}")
            return []

        if resp.status_code == 429:
            wait = min(2 ** attempt, 30)
            print(f"  [429] Rate limit, aguardando {wait}s...")
            time.sleep(wait)
            continue
        if resp.status_code != 200:
            print(f"  [ERRO] HTTP {resp.status_code}: {resp.text[:300]}")
            return []

        payload = resp.json()
        if "errors" in payload:
            print(f"  [ERRO GraphQL] {payload['errors']}")
            return []

        assets = payload.get("data", {}).get("assets", [])
        if not assets:
            print("  [AVISO] Nenhum asset retornado -- confira ASSET_SLUG.")
            return []
        return assets[0].get("metrics", [])

    print(f"  [ERRO] Excedeu {max_retries} tentativas")
    return []


def main():
    print("=" * 60)
    print("SCRIPT 02c -- Coleta: reward_rate ETH (Staking Rewards)")
    print(f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    if not API_KEY:
        print("\n[ERRO] Variável STAKINGREWARDS_API_KEY não definida.")
        print("       1. Peça uma chave gratuita em https://www.stakingrewards.com/data-api")
        print("       2. export STAKINGREWARDS_API_KEY='sua_chave_aqui'")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    registros_existentes = []
    cursor = DATA_INICIO
    if os.path.exists(out_path):
        df_existente = pd.read_csv(out_path)
        registros_existentes = df_existente.to_dict("records")
        if len(df_existente) > 0:
            cursor = str(df_existente["data"].max())
            print(f"\n[Retomada] {len(df_existente)} linhas já coletadas, "
                  f"retomando a partir de {cursor}")

    session = requests.Session()
    todos_registros = list(registros_existentes)
    primeira_resposta_ok = False

    while cursor < DATA_FIM:
        metrics = buscar_lote(cursor, DATA_FIM, session)
        if not metrics:
            print(f"  [Fim] Nenhum dado novo a partir de {cursor}")
            break

        if not primeira_resposta_ok:
            print(f"  [Debug] Primeiro registro bruto: {metrics[0]}")
            primeira_resposta_ok = True

        for m in metrics:
            data_str = str(m.get("createdAt", ""))[:10]
            valor = m.get("defaultValue")
            todos_registros.append({
                "data": data_str,
                "apr_pct": round(float(valor) * 100, 4) if valor is not None else None,
            })

        novo_cursor = str(metrics[-1].get("createdAt", ""))[:10]
        print(f"  -> lote de {len(metrics)} pontos, até {novo_cursor}")

        if not novo_cursor or novo_cursor <= cursor:
            print("  [AVISO] Cursor não avançou -- parando para evitar loop infinito. "
                  "Provavelmente item 2 das limitações conhecidas no topo do arquivo.")
            break
        cursor = novo_cursor

        df_parcial = pd.DataFrame(todos_registros).drop_duplicates(
            subset=["data"], keep="last"
        ).sort_values("data").reset_index(drop=True)
        df_parcial.to_csv(out_path, index=False)

        time.sleep(0.5)

    if not todos_registros:
        print("\n[ERRO] Nenhum dado coletado. Confira a API key, e teste a query "
              "manualmente no Playground (api-docs.stakingrewards.com/playground) "
              "antes de rodar de novo.")
        sys.exit(1)

    df_final = pd.DataFrame(todos_registros).drop_duplicates(
        subset=["data"], keep="last"
    ).sort_values("data").reset_index(drop=True)
    df_final.to_csv(out_path, index=False)

    print(f"\n[OK] Salvo em {out_path} ({len(df_final)} linhas)")
    if "apr_pct" in df_final.columns and df_final["apr_pct"].notna().any():
        print(f"  -> APR mínimo: {df_final['apr_pct'].min():.2f}% | "
              f"Máximo: {df_final['apr_pct'].max():.2f}% | "
              f"Médio: {df_final['apr_pct'].mean():.2f}%")

    print("\n[OK] Script 02c concluído!")
    print("=" * 60)


if __name__ == "__main__":
    main()
