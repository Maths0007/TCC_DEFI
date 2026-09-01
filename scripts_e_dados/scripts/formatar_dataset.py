# -*- coding: utf-8 -*-
"""
SCRIPT DE PADRONIZACAO E FORMATACAO DO MASTER DATASET DO TCC (100% EMPIRICO)
"""
import os
import numpy as np
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Dados") if "scripts" not in ROOT_DIR else os.path.join(os.path.dirname(ROOT_DIR), "Dados")

COLUNAS_DISCRETAS_INT = [
    "evento_terra_luna",
    "evento_merge",
    "evento_ftx",
    "evento_shapella"
]

ORDEM_COLUNAS_FINAL = [
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

def formatar_dataset(caminho_csv: str) -> pd.DataFrame:
    df = pd.read_csv(caminho_csv)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("Date").reset_index(drop=True)

    for col in COLUNAS_DISCRETAS_INT:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    for col in df.columns:
        if col in COLUNAS_DISCRETAS_INT or col in ["Date", "regime_ethereum", "fonte_preco_eth", "fonte_preco_steth", "fonte_consenso", "qualidade_dado", "fonte_mev"]:
            continue
        elif "usd" in col or "tvl" in col or "network" in col:
            df[col] = df[col].round(2)
        elif "preco_steth_eth" in col or "retorno_log" in col or "volatilidade" in col or "basis" in col or "mev_valor" in col:
            df[col] = df[col].round(6)
        elif "pct" in col or "apr" in col or "apy" in col or "depeg" in col:
            df[col] = df[col].round(4)

    cols_existentes = [c for c in ORDEM_COLUNAS_FINAL if c in df.columns]
    df_formatado = df[cols_existentes]
    return df_formatado

def main():
    caminho_base = os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv")
    if not os.path.exists(caminho_base):
        caminho_base = os.path.join(ROOT_DIR, "dataset_master_tcc_2022_2026.csv")

    df = formatar_dataset(caminho_base)

    destinos = [
        os.path.join(ROOT_DIR, "dataset_master_tcc_2022_2026.csv"),
        os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv"),
        os.path.join(ROOT_DIR, "scripts_e_dados", "Dados", "dataset_master_tcc_2022_2026.csv")
    ]

    for d in set(destinos):
        os.makedirs(os.path.dirname(d), exist_ok=True)
        df.to_csv(d, index=False)
        print(f"  [OK] Dataset salvo em: {d}")

    print(f"CONCLUIDO! Dataset padronizado com {len(df)} linhas e {len(df.columns)} colunas.")

if __name__ == "__main__":
    main()