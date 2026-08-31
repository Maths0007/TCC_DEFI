# -*- coding: utf-8 -*-
"""
SCRIPT DE PADRONIZACAO E FORMATACAO DO MASTER DATASET DO TCC
Tema: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Frequencia Diaria UTC)

Objetivo:
  - Formatar rigorosamente todas as colunas do dataset_master_tcc_2022_2026.csv.
  - Ordenar colunas por blocos tematicos e academicos.
  - Ajustar tipos e casas decimais:
    * Precos, retornos, volatilidades, basis: 6 decimais
    * APRs, spreads, depeg %, taxas: 4 decimais
    * TVL e reservas: 2 decimais
    * Contagens discretas e flags: inteiros estritos
  - Sincronizar em todos os diretorios do projeto.
"""
import os
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

COLUNAS_DISCRETAS_INT = [
    "slashing_eventos_qtd",
    "evento_terra_luna",
    "evento_merge",
    "evento_ftx",
    "evento_shapella"
]

ORDEM_COLUNAS_FINAL = [
    # 1. Identificacao Temporal e Regime
    "Date",
    "regime_ethereum",

    # 2. Precos de Mercado, Paridade e Depeg
    "preco_eth_usd",
    "preco_steth_usd",
    "preco_steth_eth",
    "liquid_staking_basis",
    "depeg_pct",

    # 3. Retornos e Volatilidade Financeira
    "retorno_log_eth",
    "retorno_log_steth",
    "volatilidade_7d_anual_eth",
    "volatilidade_30d_anual_eth",
    "volatilidade_7d_anual_steth",
    "volatilidade_30d_anual_steth",

    # 4. Rendimentos de Staking, Spread e Custo de Oportunidade (Cerne do TCC)
    "apr_rede_direto_total_pct",
    "apr_lido_liquido_pct",
    "delta_apr_pct",
    "taxa_retencao_efetiva_pct",
    "custo_oportunidade_diario_pct",
    "custo_oportunidade_acumulado_pct",
    "apr_consenso_bruto_pct",
    "taxa_mev_execucao_apr_pct",
    "apy_lido_pct",
    "apr_base_nominal_pct",
    "apy_pool_curve_pct",

    # 5. Camada de Consenso, Seguranca e Slashing
    "efetividade_operadores_lido_pct",
    "slashing_eventos_qtd",
    "slashing_volume_eth",

    # 6. Liquidez em DEX e Total Value Locked (TVL)
    "tvl_lido_total_usd",
    "tvl_lido_ethereum_usd",
    "tvl_pool_curve_usd",
    "reserva_eth_curve",
    "reserva_steth_curve",
    "ratio_reserva_steth_pct",
    "volume_diario_curve_usd",

    # 7. Flags Binarias de Eventos de Estresse / Hard Forks
    "evento_terra_luna",
    "evento_merge",
    "evento_ftx",
    "evento_shapella",

    # 8. Metadados e Fontes
    "fonte_preco_eth",
    "fonte_preco_steth",
    "fonte_consenso",
    "qualidade_dado",
    "reservas_curve_metodo"
]

def formatar_dataset(caminho_csv: str) -> pd.DataFrame:
    df = pd.read_csv(caminho_csv)
    
    # 1. Garantir datas em formato ISO YYYY-MM-DD
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("Date").reset_index(drop=True)

    # 2. Recalculo/reconciliacao de consistencia exata
    df["preco_steth_eth"] = df["preco_steth_usd"] / df["preco_eth_usd"]
    df["liquid_staking_basis"] = df["preco_steth_eth"] - 1.0
    df["depeg_pct"] = df["liquid_staking_basis"] * 100.0

    df["delta_apr_pct"] = df["apr_rede_direto_total_pct"] - df["apr_lido_liquido_pct"]
    df["taxa_retencao_efetiva_pct"] = np.where(
        df["apr_rede_direto_total_pct"] > 0,
        (df["delta_apr_pct"] / df["apr_rede_direto_total_pct"]) * 100.0,
        10.0
    )
    df["custo_oportunidade_diario_pct"] = df["delta_apr_pct"] / 365.0
    df["custo_oportunidade_acumulado_pct"] = df["custo_oportunidade_diario_pct"].cumsum()

    # 3. Tratamento de colunas discretas inteiras
    for col in COLUNAS_DISCRETAS_INT:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # 4. Arredondamento preciso por tipo de variavel
    for col in df.columns:
        if col in COLUNAS_DISCRETAS_INT or col in ["Date", "regime_ethereum", "fonte_preco_eth", "fonte_preco_steth", "fonte_consenso", "qualidade_dado", "reservas_curve_metodo"]:
            continue
        elif "usd" in col or "reserva" in col or "tvl" in col or "volume" in col:
            df[col] = df[col].round(2)
        elif "ratio" in col or "preco_steth_eth" in col or "retorno_log" in col or "volatilidade" in col or "basis" in col:
            df[col] = df[col].round(6)
        elif "pct" in col or "apr" in col or "apy" in col or "depeg" in col or "eth" in col:
            df[col] = df[col].round(4)

    # 5. Reordenar colunas
    cols_existentes = [c for c in ORDEM_COLUNAS_FINAL if c in df.columns]
    outras_cols = [c for c in df.columns if c not in cols_existentes and "snapshot" not in c and "apy_reward" not in c]
    df_formatado = df[cols_existentes + outras_cols]
    
    return df_formatado

def main():
    print("=" * 70)
    print("PADRONIZANDO E FORMATANDO O MASTER DATASET EM TODOS OS DIRETORIOS")
    print("=" * 70)

    caminho_base = os.path.join(BASE_DIR, "files", "dataset_master_tcc_2022_2026.csv")
    if not os.path.exists(caminho_base):
        caminho_base = os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv")

    df = formatar_dataset(caminho_base)

    destinos = [
        os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv"),
        os.path.join(BASE_DIR, "files", "dataset_master_tcc_2022_2026.csv"),
        os.path.join(BASE_DIR, "scripts_e_dados", "Dados", "dataset_master_tcc_2022_2026.csv"),
        os.path.join(BASE_DIR, "files", "scripts_e_dados", "Dados", "dataset_master_tcc_2022_2026.csv")
    ]

    for d in destinos:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        df.to_csv(d, index=False)
        print(f"  [OK] Dataset perfeitamente formatado salvo em: {d}")

    print("\n" + "=" * 70)
    print(f"CONCLUIDO! Dataset padronizado com {len(df)} linhas e {len(df.columns)} colunas.")
    print("=" * 70)

if __name__ == "__main__":
    main()