# -*- coding: utf-8 -*-
"""
MODULO 2c: APR Teorico de Consenso via Formula de Emissao do Protocolo Ethereum
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Frequencia Diaria UTC)

Objetivo:
  Calcular um APR de staking direto GENUINAMENTE INDEPENDENTE do numero divulgado
  pela Lido, resolvendo a circularidade apontada na revisao anterior (onde
  apr_rede_direto_total_pct era derivado algebricamente de apr_lido_liquido_pct
  via uma taxa fixa assumida, fazendo delta_apr_pct/taxa_retencao_efetiva_pct
  darem sempre exatamente essa taxa, por construcao).

Formula:
  A camada de consenso do Ethereum paga um reward TEORICO MAXIMO (100% de
  efetividade) que e uma funcao determinística e publica do total de ETH em
  stake — nao depende de nenhum protocolo de staking especifico. Fonte: Ben
  Edgington, "Upgrading Ethereum" (eth2book.info), formula original em funcao
  do numero de validadores N (cada um com saldo efetivo de 32 ETH):

      APR_max(%) = 2940.21 / sqrt(N)

  Reescrita em funcao do TOTAL DE ETH EM STAKE (S, em ETH) em vez de N — mais
  robusta, porque desde o hard fork Pectra (2025) o teto de saldo efetivo por
  validador subiu de 32 para ate 2048 ETH (consolidacao), entao N*32 deixou de
  equivaler exatamente ao total real em stake:

      APR_max(%) = 16632.3 / sqrt(S)

  (constante conferida por calculo direto a partir dos parametros originais de
  Edgington: 100 * 82181.25 * 64 / sqrt(1e9) ~= 16632.3 — ver comentario no
  codigo abaixo). O valor REALISTA (nao o teorico maximo) e obtido multiplicando
  pela efetividade media observada dos validadores (mesma premissa documentada
  no Modulo 2, EFETIVIDADE_ASSUMIDA_PCT).

Por que isso resolve a circularidade:
  apr_consenso_teorico_pct nao usa NENHUM numero publicado pela Lido — so o
  total de ETH em stake na rede (dado publico, independente de qualquer LST) e
  uma formula do proprio protocolo. Combinado com o MEV real amostrado do
  Modulo 2b (taxa_mev_execucao_apr_pct), da um apr_rede_direto_total_pct
  genuinamente independente, que o Modulo 4 usa para SUBSTITUIR a versao
  derivada da Lido nos dias em que os dois componentes estiverem disponiveis.

Dependencia (voce precisa fornecer, nao e coletado automaticamente aqui):
  scripts_e_dados/Dados/total_eth_staked.csv, com colunas Date,total_eth_staked.
  Essa serie CRESCE DEVAGAR E DE FORMA MONOTONICA (bem diferente de preco ou
  MEV, que sao volateis dia a dia) — por isso NAO faz sentido montar um raspador
  automatizado aqui. O caminho mais pratico e um download manual, uma unica vez,
  de um dashboard publico do Dune Analytics ("ethereum total staked") ou do
  grafico beaconcha.in/charts/validators (se tiver opcao de exportar), cobrindo
  o periodo inteiro numa tacada so.

Saidas:
  - dados_consenso_teorico.csv (diretorio raiz)
  - scripts_e_dados/Dados/dados_consenso_teorico.csv
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Dados")
os.makedirs(DADOS_DIR, exist_ok=True)

DATA_INICIO = "2022-04-01"
DATA_FIM = "2026-05-31"

# Constante derivada dos parametros de consenso do protocolo Ethereum (Ben
# Edgington, "Upgrading Ethereum" / eth2book.info): base_reward_factor=64,
# base_rewards_per_epoch=4, epocas/ano=82181.25 (slots de 12s, 32 slots/epoca).
# Formula original: APR_max(%) = 100 * 82181.25 * 64 / sqrt(32e9 * N)
# Reescrita em funcao do total de ETH em stake S (em ETH, nao em Gwei):
#   APR_max(%) = 100 * 82181.25 * 64 / sqrt(S * 1e9) = 16632.3 / sqrt(S)
CONSTANTE_FORMULA_EMISSAO = (100 * 82181.25 * 64) / np.sqrt(1e9)

# Mesma premissa de efetividade media documentada no Modulo 2 — se ajustar la,
# ajuste aqui tambem para manter consistencia entre os dois modulos.
EFETIVIDADE_ASSUMIDA_PCT = 99.45


def main():
    print("=" * 70)
    print("MODULO 2c: APR Teorico de Consenso via Formula de Emissao do Protocolo")
    print(f"Janela Temporal: {DATA_INICIO} a {DATA_FIM}")
    print(f"Constante da formula (verificar contra eth2book.info se necessario): {CONSTANTE_FORMULA_EMISSAO:.1f}")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    staked_file = os.path.join(DADOS_DIR, "total_eth_staked.csv")
    if not os.path.exists(staked_file):
        print("\n[ERRO] scripts_e_dados/Dados/total_eth_staked.csv nao encontrado.")
        print("       Esse arquivo (colunas Date,total_eth_staked) precisa existir antes de")
        print("       rodar este modulo. Ver instrucoes no cabecalho do arquivo — normalmente")
        print("       um download manual, uma unica vez, de um dashboard publico (Dune/beaconcha.in).")
        return

    print("\n[1/3] Carregando total_eth_staked.csv...")
    try:
        df_staked = pd.read_csv(staked_file)
    except Exception as e:
        print(f"  [ERRO] Nao foi possivel ler o arquivo: {e}")
        return

    if "Date" not in df_staked.columns or "total_eth_staked" not in df_staked.columns:
        print("  [ERRO] O arquivo precisa ter exatamente as colunas Date,total_eth_staked.")
        print(f"         Colunas encontradas: {list(df_staked.columns)}")
        return

    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df = pd.DataFrame({"Date": grid_datas})
    df = pd.merge(df, df_staked[["Date", "total_eth_staked"]], on="Date", how="left")

    n_pontos_reais = df["total_eth_staked"].notna().sum()
    print(f"  -> {n_pontos_reais} dia(s) com total_eth_staked informado no CSV fornecido.")

    # Para uma serie monotonica de crescimento lento como esta, densidade de pontos
    # (% de dias com valor direto) NAO e o risco relevante — poucos pontos bem
    # distribuidos bastam. O que importa e (a) as bordas do periodo estarem
    # cobertas (senao viramos ffill/bfill extrapolando "no escuro" nas pontas) e
    # (b) nao haver um hiato longo demais entre dois pontos reais consecutivos
    # (a interpolacao linear ai vira uma aposta sobre o formato do crescimento
    # no meio do caminho — arriscado perto de inflexoes conhecidas, como o salto
    # de depositos logo apos o Shapella).
    datas_reais = pd.to_datetime(df.loc[df["total_eth_staked"].notna(), "Date"]).sort_values()
    if not datas_reais.empty:
        cobre_inicio = datas_reais.iloc[0] <= pd.to_datetime(DATA_INICIO) + pd.Timedelta(days=30)
        cobre_fim = datas_reais.iloc[-1] >= pd.to_datetime(DATA_FIM) - pd.Timedelta(days=30)
        if not cobre_inicio or not cobre_fim:
            print("  [AVISO] O CSV nao chega perto de uma ou ambas as pontas do periodo")
            print(f"          ({DATA_INICIO} a {DATA_FIM}) — os dias fora do alcance dos pontos")
            print("          reais serao preenchidos por propagacao (ffill/bfill), nao interpolacao.")
        if len(datas_reais) >= 2:
            maior_hiato_dias = int(datas_reais.diff().max().days)
            print(f"  -> Maior hiato entre pontos reais consecutivos: {maior_hiato_dias} dia(s).")
            if maior_hiato_dias > 180:
                print("  [AVISO] Hiato de mais de 180 dias entre pontos reais — a interpolacao linear")
                print("          nesse trecho e uma aposta sobre o formato do crescimento no meio do")
                print("          caminho. Considere acrescentar mais pontos nesse intervalo se possivel.")

    if n_pontos_reais < 2:
        print("\n[ERRO] Pontos insuficientes em total_eth_staked para interpolar com confianca")
        print("       (precisa de pelo menos 2 datas reais). Nada foi salvo.")
        return

    # Total de ETH em stake e uma serie monotonica de crescimento lento — diferente
    # de preco ou MEV, aqui interpolar/propagar lacunas e uma premissa segura,
    # DESDE QUE haja pontos reais suficientes ancorando a serie (checado acima).
    df["total_eth_staked"] = df["total_eth_staked"].interpolate(method="linear").ffill().bfill()

    print("\n[2/3] Aplicando formula de emissao do protocolo...")
    df["apr_consenso_teorico_max_pct"] = (CONSTANTE_FORMULA_EMISSAO / np.sqrt(df["total_eth_staked"])).round(4)
    df["apr_consenso_teorico_pct"] = (df["apr_consenso_teorico_max_pct"] * (EFETIVIDADE_ASSUMIDA_PCT / 100.0)).round(4)
    df["fonte_consenso_teorico"] = "formula_emissao_protocolo"
    df["qualidade_dado_consenso_teorico"] = "independente_formula_protocolo"

    print("\n[3/3] Salvando dados_consenso_teorico.csv...")
    saida_raiz = os.path.join(ROOT_DIR, "dados_consenso_teorico.csv")
    saida_dados = os.path.join(DADOS_DIR, "dados_consenso_teorico.csv")
    df.to_csv(saida_raiz, index=False)
    df.to_csv(saida_dados, index=False)

    print(f"  -> Salvo com sucesso em: {saida_raiz}")
    print(f"  -> Copia sincronizada em: {saida_dados}")
    print(f"  -> apr_consenso_teorico_pct medio: {df['apr_consenso_teorico_pct'].mean():.4f}%")
    print(f"  -> Minimo: {df['apr_consenso_teorico_pct'].min():.4f}% | Maximo: {df['apr_consenso_teorico_pct'].max():.4f}%")
    print("=" * 70)
    print("MODULO 2c CONCLUIDO!\n")


if __name__ == "__main__":
    main()
