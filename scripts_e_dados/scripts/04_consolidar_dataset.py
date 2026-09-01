# -*- coding: utf-8 -*-
"""
MODULO 4: Consolidacao do Master Dataset do TCC (2022-2026)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)

Objetivo:
  - Consolidar apenas variaveis 100% empiricas e diretas (sem aproximacoes constantes de efetividade,
    sem registros ilustrativos de slashing e sem modelagem sintetica de reservas da Curve).
  - Variavel Principal: Delta_APR_t = APR_Rede_Direto_t - APR_Lido_Liquido_t
"""
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Dados") if "scripts" not in ROOT_DIR else os.path.join(os.path.dirname(ROOT_DIR), "Dados")
os.makedirs(DADOS_DIR, exist_ok=True)

DATA_INICIO = "2022-05-05"
DATA_FIM = "2026-05-31"

COLUNAS_DISCRETAS = [
    "evento_terra_luna",
    "evento_merge",
    "evento_ftx",
    "evento_shapella"
]

COLUNAS_JANELA_MOVEL = [
    "retorno_log_eth",
    "retorno_log_steth",
    "volatilidade_7d_anual_eth",
    "volatilidade_30d_anual_eth",
    "volatilidade_7d_anual_steth",
    "volatilidade_30d_anual_steth",
    "mev_valor_medio_bloco_eth",
    "mev_total_diario_estimado_eth"
]


def carregar_tabela(nome_arquivo: str) -> pd.DataFrame:
    for local in [
        os.path.join(DADOS_DIR, nome_arquivo),
        os.path.join(ROOT_DIR, nome_arquivo),
        os.path.join(ROOT_DIR, "scripts_e_dados", "scripts", nome_arquivo)
    ]:
        if os.path.exists(local):
            df = pd.read_csv(local)
            date_cols = [c for c in df.columns if c.lower() in ("date", "data")]
            if date_cols:
                col = date_cols[0]
                df["Date"] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
                if col != "Date":
                    df = df.drop(columns=[col])
            return df
    return pd.DataFrame()


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
    print("MODULO 4: Consolidacao do Master Dataset do TCC (100% Empirico)")
    print(f"Recorte Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print("=" * 70)

    df_precos = carregar_tabela("dados_precos_mercado.csv")
    df_consenso = carregar_tabela("dados_rated_consenso.csv")
    df_defillama = carregar_tabela("dados_defillama_curve.csv")
    df_mev = carregar_tabela("dados_mev_relay.csv")

    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df_master = pd.DataFrame({"Date": grid_datas})

    if not df_precos.empty:
        df_master = pd.merge(df_master, df_precos, on="Date", how="left")

    if not df_consenso.empty:
        cols_consenso = [c for c in df_consenso.columns if c not in df_master.columns or c == "Date"]
        df_master = pd.merge(df_master, df_consenso[cols_consenso], on="Date", how="left")

    if not df_defillama.empty:
        cols_defi = [c for c in df_defillama.columns if c not in df_master.columns or c == "Date"]
        df_master = pd.merge(df_master, df_defillama[cols_defi], on="Date", how="left")

    if not df_mev.empty:
        cols_mev = [c for c in df_mev.columns if c not in df_master.columns or c == "Date"]
        df_master = pd.merge(df_master, df_mev[cols_mev], on="Date", how="left")

    # Tratamento
    for col in COLUNAS_DISCRETAS:
        if col in df_master.columns:
            df_master[col] = df_master[col].fillna(0).astype(int)

    for col in COLUNAS_JANELA_MOVEL:
        if col in df_master.columns:
            df_master[col] = df_master[col].interpolate(method="linear", limit_area="inside")

    num_cols = df_master.select_dtypes(include=[np.number]).columns
    cols_continuas = [c for c in num_cols if c not in COLUNAS_DISCRETAS and c not in COLUNAS_JANELA_MOVEL]
    for col in cols_continuas:
        df_master[col] = df_master[col].interpolate(method="linear").ffill().bfill()

    # Precos e Depeg
    df_master["preco_steth_eth"] = df_master["preco_steth_usd"] / df_master["preco_eth_usd"]
    df_master["liquid_staking_basis"] = df_master["preco_steth_eth"] - 1.0
    df_master["depeg_pct"] = df_master["liquid_staking_basis"] * 100.0

    # APR Lido Líquido Nominal
    if "apr_lido_liquido_pct" not in df_master.columns:
        if "apr_lido_consenso_pct" in df_master.columns:
            df_master["apr_lido_liquido_pct"] = df_master["apr_lido_consenso_pct"]
        elif "apr_base_nominal_pct" in df_master.columns:
            df_master["apr_lido_liquido_pct"] = df_master["apr_base_nominal_pct"]

    # SPREAD REAL INDEPENDENTE: Delta APR
    df_master["delta_apr_pct"] = df_master["apr_rede_direto_total_pct"] - df_master["apr_lido_liquido_pct"]

    df_master["taxa_retencao_efetiva_pct"] = np.where(
        df_master["apr_rede_direto_total_pct"] > 0,
        (df_master["delta_apr_pct"] / df_master["apr_rede_direto_total_pct"]) * 100.0,
        0.0
    )

    df_master["custo_oportunidade_diario_pct"] = df_master["delta_apr_pct"] / 365.0
    df_master["custo_oportunidade_acumulado_pct"] = df_master["custo_oportunidade_diario_pct"].cumsum()

    df_master["regime_ethereum"] = df_master["Date"].apply(classificar_regime_historico)

    df_master["evento_terra_luna"] = (df_master["Date"].between("2022-05-08", "2022-05-31")).astype(int)
    df_master["evento_merge"] = (df_master["Date"].between("2022-09-15", "2022-09-22")).astype(int)
    df_master["evento_ftx"] = (df_master["Date"].between("2022-11-06", "2022-11-30")).astype(int)
    df_master["evento_shapella"] = (df_master["Date"].between("2023-04-12", "2023-04-30")).astype(int)

    # Ordenacao Estruturada (Apenas Colunas Estritamente Empiricas)
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
        "custo_oportunidade_diario_pct",
        "custo_oportunidade_acumulado_pct",
        "apr_consenso_bruto_pct",
        "taxa_mev_execucao_apr_pct",
        "total_staked_eth_network",
        "apy_lido_pct",
        "apr_base_nominal_pct",
        "tvl_rede_ethereum_total_usd",
        "tvl_lido_total_usd",
        "tvl_lido_ethereum_usd",
        "dominancia_lido_tvl_defi_pct",
        "tvl_pool_curve_usd",
        "apy_pool_curve_pct",
        "tvl_yield_pool_usd",
        "mev_valor_medio_bloco_eth",
        "mev_total_diario_estimado_eth",
        "evento_terra_luna",
        "evento_merge",
        "evento_ftx",
        "evento_shapella",
        "fonte_preco_eth",
        "fonte_preco_steth",
        "fonte_consenso",
        "qualidade_dado",
        "fonte_mev"
    ]
    cols_finais = [c for c in cols_ordenadas if c in df_master.columns] + [c for c in df_master.columns if c not in cols_ordenadas and "_x" not in c and "_y" not in c]
    df_master = df_master[cols_finais]

    for col in df_master.select_dtypes(include=[np.number]).columns:
        if col in COLUNAS_DISCRETAS:
            df_master[col] = df_master[col].astype(int)
        elif "usd" in col or "tvl" in col or "network" in col:
            df_master[col] = df_master[col].round(2)
        elif "preco_steth_eth" in col or "retorno_log" in col or "volatilidade" in col or "basis" in col or "mev_valor" in col:
            df_master[col] = df_master[col].round(6)
        elif "pct" in col or "apr" in col or "apy" in col or "depeg" in col:
            df_master[col] = df_master[col].round(4)

    # Salvar Master Dataset
    destino = os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv")
    df_master.to_csv(destino, index=False)
    print(f"  -> Salvo em: {destino}")

    print("\n" + "-" * 70)
    print("RESUMO DO MASTER DATASET CONSOLIDADO (100% EMPIRICO):")
    print(f"  -> Dimensao: {df_master.shape[0]} linhas x {df_master.shape[1]} colunas")
    print(f"  -> APR Staking Direto Medio: {df_master['apr_rede_direto_total_pct'].mean():.2f}%")
    print(f"  -> APR Lido Liquido Medio:   {df_master['apr_lido_liquido_pct'].mean():.2f}%")
    print(f"  -> Delta APR Medio (Spread): {df_master['delta_apr_pct'].mean():.4f}%")
    print(f"  -> Taxa de Retencao Media:   {df_master['taxa_retencao_efetiva_pct'].mean():.2f}%")
    print("=" * 70)
    print("MODULO 4 CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()