# -*- coding: utf-8 -*-
"""
MODULO 4: Consolidacao do Master Dataset do TCC (2022-2026)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Frequencia Diaria UTC)

Objetivo:
  - Merge (outer join) de todas as tabelas intermediarias pela coluna de data (Date YYYY-MM-DD).
  - Tratamento de lacunas com interpolacao linear suave e preenchimento progressivo (ffill).
  - Calculo da variavel principal de spread de retornos:
    Delta_APR_t = APR_Rede_Direto_t - APR_Lido_Liquido_t
  - Engenharia de atributos financeiros e classificacao de regimes tecnologicos.

Saidas:
  - dataset_master_tcc_2022_2026.csv (diretorio raiz)
  - scripts_e_dados/Dados/dataset_master_tcc_2022_2026.csv
"""
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DADOS_DIR = os.path.join(BASE_DIR, "Dados")
os.makedirs(DADOS_DIR, exist_ok=True)

DATA_INICIO = "2022-04-01"
DATA_FIM = "2026-05-31"


def carregar_tabela(nome_arquivo: str) -> pd.DataFrame:
    caminho_raiz = os.path.join(BASE_DIR, nome_arquivo)
    caminho_dados = os.path.join(DADOS_DIR, nome_arquivo)

    caminho = caminho_raiz if os.path.exists(caminho_raiz) else caminho_dados
    if not os.path.exists(caminho):
        print(f"  [AVISO] Arquivo {nome_arquivo} nao encontrado!")
        return pd.DataFrame()

    df = pd.read_csv(caminho)
    date_cols = [c for c in df.columns if c.lower() in ("date", "data")]
    if date_cols:
        col = date_cols[0]
        df["Date"] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
        if col != "Date":
            df = df.drop(columns=[col])
    return df


def classificar_regime_historico(dt_str: str) -> str:
    dt = pd.to_datetime(dt_str)
    if dt < pd.to_datetime("2022-09-15"):
        return "Pre-Merge"
    elif dt < pd.to_datetime("2023-04-12"):
        return "Post-Merge_Pre-Shapella"
    else:
        return "Post-Shapella"


def main():
    print("=" * 70)
    print("MODULO 4: Consolidacao do Master Dataset do TCC (2022-2026)")
    print(f"Janela Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    # 1. Carregar tabelas parciais
    print("\n[1/4] Carregando datasets intermediarios...")
    df_precos = carregar_tabela("dados_precos_mercado.csv")
    df_consenso = carregar_tabela("dados_rated_consenso.csv")
    df_defillama = carregar_tabela("dados_defillama_curve.csv")

    print(f"  -> Precos e Volatilidade: {len(df_precos)} linhas")
    print(f"  -> Camada de Consenso:   {len(df_consenso)} linhas")
    print(f"  -> DefiLlama & Curve:     {len(df_defillama)} linhas")

    # 2. Outer Join pelo grid continuo de datas
    print("\n[2/4] Realizando Full Outer Join temporal...")
    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df_master = pd.DataFrame({"Date": grid_datas})

    if not df_precos.empty:
        df_master = pd.merge(df_master, df_precos, on="Date", how="left")

    if not df_consenso.empty:
        df_master = pd.merge(df_master, df_consenso, on="Date", how="left")

    if not df_defillama.empty:
        df_master = pd.merge(df_master, df_defillama, on="Date", how="left")

    # 3. Tratamento de dados e cálculo de features
    print("\n[3/4] Aplicando interpolacao, ffill e engenharia de features financeiras...")

    # Interpolação linear para colunas numéricas
    num_cols = df_master.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df_master[col] = df_master[col].interpolate(method="linear").ffill().bfill()

    # --- Proxy modelado da proporcao de reservas ETH/stETH da pool Curve ---
    # Ver NOTA DE CORRECAO no Modulo 3: nao ha fonte gratuita verificada de
    # split historico ETH/stETH da pool (precisaria de leitura on-chain
    # bloco a bloco, nao testada neste ambiente). Por decisao explicita do
    # autor do TCC, este bloco constroi um PROXY MODELADO -- nao um dado
    # observado -- calibrado com o unico ponto real disponivel:
    #
    #   ratio_steth_pct(t) = 50.0 + k * (-depeg_pct(t))   [limitado a 15%-85%]
    #
    # Racional: quando stETH negocia com desconto (depeg_pct < 0), quem
    # precisa de liquidez vende stETH na pool em troca de ETH, deixando a
    # pool mais concentrada em stETH -- por isso a relacao e negativa em
    # depeg_pct (mais desconto -> maior fatia de stETH). O parametro k NAO e
    # arbitrado: e calibrado usando o dia mais recente da serie, onde temos
    # tanto o ratio real (snapshot da Curve API, Modulo 3) quanto o depeg
    # real (Modulo 1) para o mesmo dia. Se o depeg desse dia estiver perto
    # de zero (sem sinal pra calibrar), cai num k padrao documentado abaixo.
    #
    # A profundidade da pool usa o TVL HISTORICO REAL (tvl_pool_curve_usd,
    # corrigido no Modulo 3) e os PRECOS REAIS de ETH e stETH (Modulo 1) pra
    # resolver a contagem de tokens de forma consistente com o ratio modelado:
    #   TVL_usd(t) = N(t) * [(1-r(t))*preco_eth(t) + r(t)*preco_steth(t)]
    # Ou seja: so a DIVISAO entre os dois tokens e modelada -- o tamanho
    # total da pool e os precos usados sao dado real.
    #
    # LIMITACAO A DEIXAR EXPLICITA NO TCC: isso e um proxy, nao uma
    # observacao. 'reserva_eth_curve', 'reserva_steth_curve' e
    # 'ratio_reserva_steth_pct' devem ser tratados como ESTIMATIVAS, e a
    # coluna 'fonte_reserva_curve' = 'proxy_modelado_via_depeg' documenta
    # isso no proprio dataset. Os valores originais do snapshot real (o
    # unico ponto observado) ficam preservados em
    # 'reserva_eth_curve_snapshot_atual' / 'reserva_steth_curve_snapshot_atual'.
    colunas_necessarias_proxy = {
        "reserva_eth_curve", "reserva_steth_curve", "ratio_reserva_steth_pct",
        "depeg_pct", "tvl_pool_curve_usd", "preco_eth_usd", "preco_steth_usd",
    }
    if colunas_necessarias_proxy.issubset(df_master.columns):
        K_SENSIBILIDADE_DEFAULT = 3.0  # pp de fatia stETH por 1pp de depeg negativo; so usado se a ancora nao calibrar

        ratio_ancora_pct = float(df_master["ratio_reserva_steth_pct"].iloc[-1])
        depeg_ancora_pct = float(df_master["depeg_pct"].iloc[-1])

        if abs(depeg_ancora_pct) > 0.05:
            k_calibrado = (ratio_ancora_pct - 50.0) / (-depeg_ancora_pct)
        else:
            k_calibrado = K_SENSIBILIDADE_DEFAULT
            print(f"  [PROXY RESERVA CURVE] Depeg de ancora perto de zero ({depeg_ancora_pct:.4f}%) "
                  f"-- usando k padrao ({K_SENSIBILIDADE_DEFAULT}) em vez de calibrar.")

        print(f"  [PROXY RESERVA CURVE] Ancora real: ratio_steth={ratio_ancora_pct:.2f}% "
              f"em depeg={depeg_ancora_pct:.4f}% -> k calibrado = {k_calibrado:.4f}")
        if k_calibrado < 0:
            print("  [AVISO] k calibrado ficou negativo -- o ponto de ancora (snapshot real) contraria "
                  "a direcao esperada do modelo (mais desconto -> mais stETH na pool). Revise manualmente "
                  "antes de usar este proxy no TCC; pode ser ruido pontual do dia do snapshot.")

        df_master["reserva_eth_curve_snapshot_atual"] = df_master["reserva_eth_curve"]
        df_master["reserva_steth_curve_snapshot_atual"] = df_master["reserva_steth_curve"]

        df_master["ratio_reserva_steth_pct"] = (50.0 + k_calibrado * (-df_master["depeg_pct"])).clip(15.0, 85.0)

        r_frac = df_master["ratio_reserva_steth_pct"] / 100.0
        preco_medio_ponderado = (1.0 - r_frac) * df_master["preco_eth_usd"] + r_frac * df_master["preco_steth_usd"]
        total_reserva_tokens = df_master["tvl_pool_curve_usd"] / preco_medio_ponderado

        df_master["reserva_steth_curve"] = r_frac * total_reserva_tokens
        df_master["reserva_eth_curve"] = (1.0 - r_frac) * total_reserva_tokens

        if "fonte_reserva_curve" in df_master.columns:
            df_master["fonte_reserva_curve"] = "proxy_modelado_via_depeg"
    else:
        faltando = colunas_necessarias_proxy - set(df_master.columns)
        print(f"  [AVISO] Colunas ausentes para o proxy de reserva da Curve ({faltando}) "
              f"-- mantendo snapshot constante do Modulo 3.")

    # Garantir consistência entre séries de APR
    if "apr_rede_direto_total_pct" not in df_master.columns and "apr_consenso_bruto_pct" in df_master.columns:
        df_master["apr_rede_direto_total_pct"] = df_master["apr_consenso_bruto_pct"] + df_master.get("taxa_mev_execucao_apr_pct", 0.0)

    if "apr_lido_liquido_pct" not in df_master.columns and "apr_lido_consenso_pct" in df_master.columns:
        df_master["apr_lido_liquido_pct"] = df_master["apr_lido_consenso_pct"]

    # VARIÁVEL PRINCIPAL DO TCC:
    # Delta_APR_t = APR_Rede_Direto_t - APR_Lido_Liquido_t
    df_master["delta_apr_pct"] = df_master["apr_rede_direto_total_pct"] - df_master["apr_lido_liquido_pct"]

    # Taxa de Retenção Efetiva da Lido DAO (% cobrada sobre o staking)
    df_master["taxa_retencao_efetiva_pct"] = np.where(
        df_master["apr_rede_direto_total_pct"] > 0,
        (df_master["delta_apr_pct"] / df_master["apr_rede_direto_total_pct"]) * 100.0,
        10.0
    )

    # Classificação de Regimes Tecnológicos
    df_master["regime_ethereum"] = df_master["Date"].apply(classificar_regime_historico)

    # Eventos de Estresse e Hard Forks
    df_master["evento_terra_luna"] = (df_master["Date"].between("2022-05-08", "2022-05-31")).astype(int)
    df_master["evento_merge"] = (df_master["Date"].between("2022-09-15", "2022-09-22")).astype(int)
    df_master["evento_ftx"] = (df_master["Date"].between("2022-11-06", "2022-11-30")).astype(int)
    df_master["evento_shapella"] = (df_master["Date"].between("2023-04-12", "2023-04-30")).astype(int)

    # Custo de Oportunidade Acumulado
    df_master["custo_oportunidade_diario_pct"] = df_master["delta_apr_pct"] / 365.0
    df_master["custo_oportunidade_acumulado_pct"] = df_master["custo_oportunidade_diario_pct"].cumsum()

    # Recorte temporal estrito
    df_master["Date_dt"] = pd.to_datetime(df_master["Date"])
    df_master = df_master[(df_master["Date_dt"] >= pd.to_datetime(DATA_INICIO)) & (df_master["Date_dt"] <= pd.to_datetime(DATA_FIM))]
    df_master = df_master.drop(columns=["Date_dt"]).sort_values("Date").reset_index(drop=True)

    # Ordenação de colunas estratégicas
    cols_ordenadas = [
        "Date",
        "regime_ethereum",
        "preco_eth_usd",
        "preco_steth_usd",
        "preco_steth_eth",
        "liquid_staking_basis",
        "depeg_pct",
        "retorno_log_eth",
        "retorno_log_steth",
        "volatilidade_7d_anual_eth",
        "volatilidade_30d_anual_eth",
        "volatilidade_7d_anual_steth",
        "volatilidade_30d_anual_steth",
        "apr_rede_direto_total_pct",
        "apr_lido_liquido_pct",
        "delta_apr_pct",
        "taxa_retencao_efetiva_pct",
        "custo_oportunidade_acumulado_pct",
        "apr_consenso_bruto_pct",
        "taxa_mev_execucao_apr_pct",
        "efetividade_operadores_lido_pct",
        "slashing_eventos_qtd",
        "slashing_volume_eth",
        "tvl_lido_total_usd",
        "tvl_lido_ethereum_usd",
        "reserva_eth_curve",
        "reserva_steth_curve",
        "ratio_reserva_steth_pct",
        "tvl_pool_curve_usd",
        "volume_diario_curve_usd",
        "evento_terra_luna",
        "evento_merge",
        "evento_ftx",
        "evento_shapella"
    ]
    cols_finais = [c for c in cols_ordenadas if c in df_master.columns] + [c for c in df_master.columns if c not in cols_ordenadas]
    df_master = df_master[cols_finais]

    # Arredondamentos acadêmicos
    for col in df_master.select_dtypes(include=[np.number]).columns:
        if "usd" in col or "reserva" in col or "tvl" in col:
            df_master[col] = df_master[col].round(2)
        elif "ratio" in col or "preco_steth_eth" in col or "retorno_log" in col or "volatilidade" in col or "basis" in col:
            df_master[col] = df_master[col].round(6)
        elif "pct" in col or "apr" in col or "depeg" in col:
            df_master[col] = df_master[col].round(4)

    # 4. Salvar Master Dataset
    print("\n[4/4] Salvando dataset_master_tcc_2022_2026.csv...")
    saida_raiz = os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv")
    saida_dados = os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv")

    df_master.to_csv(saida_raiz, index=False)
    df_master.to_csv(saida_dados, index=False)

    print(f"  -> Salvo com sucesso em: {saida_raiz}")
    print(f"  -> Copia sincronizada em: {saida_dados}")
    print(f"  -> Dimensao: {df_master.shape[0]} linhas x {df_master.shape[1]} colunas")
    print(f"  -> Periodo estrito: {df_master['Date'].iloc[0]} a {df_master['Date'].iloc[-1]}")
    print(f"  -> Delta APR medio (Comissao Lido): {df_master['delta_apr_pct'].mean():.4f}%")
    print(f"  -> Depeg medio: {df_master['depeg_pct'].mean():.4f}% | Depeg minimo: {df_master['depeg_pct'].min():.4f}%")
    print(f"  -> Taxa de Retencao media: {df_master['taxa_retencao_efetiva_pct'].mean():.2f}%")
    print("=" * 70)
    print("MODULO 4 CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()