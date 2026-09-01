# -*- coding: utf-8 -*-
"""
MODULO 3: TVL, Yields e Liquidez DEX da Pool Curve (DefiLlama)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)

Fontes (100% Diretas e Empiricas):
  1. DefiLlama Charts Ethereum: https://api.llama.fi/charts/Ethereum
     -> Serie historica diaria do TVL TOTAL do Ecossistema Ethereum.
  2. DefiLlama Protocol API: https://api.llama.fi/protocol/lido
     -> Serie historica diaria de TVL Total e TVL Ethereum da Lido DAO.
  3. DefiLlama Yields API (Pool Lido stETH): https://yields.llama.fi/chart/747c1d2a-c668-4682-b9f9-296708a3dd90
     -> Historico diario de APY e TVL reportados pelo oraculo da Lido.
  4. DefiLlama Yields API (Pool Curve stETH/ETH): https://yields.llama.fi/chart/57d30b9c-fc66-4ac2-b666-69ad5f410cce
     -> Serie historica REAL e direta de TVL e APY da pool Curve stETH/ETH (sem modelagem sintetica de reservas).

Metricas Calculadas:
  1. tvl_rede_ethereum_total_usd: Valor Total Bloqueado na rede Ethereum
  2. tvl_lido_total_usd e tvl_lido_ethereum_usd: TVL da Lido DAO
  3. dominancia_lido_tvl_defi_pct: Participacao do Lido no TVL Total do Ethereum (%)
  4. apy_lido_pct e apr_base_nominal_pct: Rendimentos reais reportados e conversao para APR nominal
  5. tvl_pool_curve_usd e apy_pool_curve_pct: TVL real da pool Curve stETH/ETH no mercado secundario

Saidas:
  - scripts_e_dados/Dados/dados_defillama_curve.csv
  - dados_defillama_curve.csv
"""
import os
import sys
import time
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Dados") if "scripts" not in ROOT_DIR else os.path.join(os.path.dirname(ROOT_DIR), "Dados")
os.makedirs(DADOS_DIR, exist_ok=True)

DATA_INICIO = "2022-05-05"
DATA_FIM = "2026-05-31"

LIDO_POOL_UUID = "747c1d2a-c668-4682-b9f9-296708a3dd90"
CURVE_STETH_POOL_UUID = "57d30b9c-fc66-4ac2-b666-69ad5f410cce"


def fetch_ethereum_global_tvl() -> pd.DataFrame:
    """Coleta a serie historica do TVL TOTAL da rede Ethereum via DefiLlama Charts API."""
    print("  -> Buscando historico de TVL TOTAL da Rede Ethereum via DefiLlama Charts...")
    url = "https://api.llama.fi/charts/Ethereum"
    try:
        time.sleep(0.3)
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            df["Date"] = pd.to_datetime(pd.to_numeric(df["date"]), unit="s").dt.strftime("%Y-%m-%d")
            df = df.rename(columns={"totalLiquidityUSD": "tvl_rede_ethereum_total_usd"})
            print(f"  [OK] TVL Total Ethereum: {len(df)} registros obtidos.")
            return df[["Date", "tvl_rede_ethereum_total_usd"]].drop_duplicates(subset=["Date"])
    except Exception as e:
        print(f"  [AVISO] Falha ao coletar TVL Total Ethereum: {e}")
    return pd.DataFrame()


def fetch_lido_tvl_protocol() -> pd.DataFrame:
    """Coleta o historico completo de TVL da Lido via DefiLlama Protocol API."""
    print("  -> Buscando historico de TVL da Lido via DefiLlama Protocol API...")
    url = "https://api.llama.fi/protocol/lido"
    try:
        time.sleep(0.3)
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            tvl_total_list = data.get("tvl", [])
            chain_tvls = data.get("chainTvls", {})
            eth_tvl_list = chain_tvls.get("Ethereum", {}).get("tvl", [])

            df_total = pd.DataFrame(tvl_total_list)
            df_total["Date"] = pd.to_datetime(df_total["date"], unit="s").dt.strftime("%Y-%m-%d")
            df_total = df_total.rename(columns={"totalLiquidityUSD": "tvl_lido_total_usd"})

            df_eth = pd.DataFrame(eth_tvl_list)
            df_eth["Date"] = pd.to_datetime(df_eth["date"], unit="s").dt.strftime("%Y-%m-%d")
            df_eth = df_eth.rename(columns={"totalLiquidityUSD": "tvl_lido_ethereum_usd"})

            df_merged = pd.merge(df_total[["Date", "tvl_lido_total_usd"]],
                                 df_eth[["Date", "tvl_lido_ethereum_usd"]],
                                 on="Date", how="outer")
            print(f"  [OK] TVL Lido: {len(df_merged)} registros obtidos.")
            return df_merged
    except Exception as e:
        print(f"  [AVISO] Falha ao coletar TVL Lido: {e}")
    return pd.DataFrame()


def fetch_lido_yields_history() -> pd.DataFrame:
    """Coleta o historico de APY/Yields do pool Lido stETH via DefiLlama Yields API."""
    print(f"  -> Buscando historico de APY/Yields do Lido (Pool: {LIDO_POOL_UUID})...")
    url = f"https://yields.llama.fi/chart/{LIDO_POOL_UUID}"
    try:
        time.sleep(0.3)
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            chart = r.json().get("data", [])
            records = []
            for pt in chart:
                records.append({
                    "Date": str(pt.get("timestamp", ""))[:10],
                    "apy_lido_pct": pt.get("apy"),
                    "tvl_yield_pool_usd": pt.get("tvlUsd"),
                })
            df = pd.DataFrame(records).dropna(subset=["Date"]).drop_duplicates(subset=["Date"])
            print(f"  [OK] Yields Lido: {len(df)} registros obtidos.")
            return df
    except Exception as e:
        print(f"  [AVISO] Falha ao coletar yields do Lido: {e}")
    return pd.DataFrame()


def fetch_curve_steth_pool_history() -> pd.DataFrame:
    """Coleta a serie historica REAL e direta de TVL e APY da pool Curve stETH/ETH via DefiLlama."""
    print(f"  -> Buscando serie historica REAL do TVL da pool Curve stETH/ETH (Pool: {CURVE_STETH_POOL_UUID})...")
    url = f"https://yields.llama.fi/chart/{CURVE_STETH_POOL_UUID}"
    try:
        time.sleep(0.3)
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            chart = r.json().get("data", [])
            records = []
            for pt in chart:
                records.append({
                    "Date": str(pt.get("timestamp", ""))[:10],
                    "tvl_pool_curve_usd": pt.get("tvlUsd"),
                    "apy_pool_curve_pct": pt.get("apy"),
                })
            df = pd.DataFrame(records).dropna(subset=["Date"]).drop_duplicates(subset=["Date"])
            print(f"  [OK] Curve stETH TVL Historico: {len(df)} registros reais obtidos.")
            return df
    except Exception as e:
        print(f"  [AVISO] Falha ao coletar historico Curve: {e}")
    return pd.DataFrame()


def processar_metricas_defillama_curve(df_eth_tvl: pd.DataFrame, df_tvl: pd.DataFrame,
                                       df_yields: pd.DataFrame, df_curve: pd.DataFrame) -> pd.DataFrame:
    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df_master = pd.DataFrame({"Date": grid_datas})

    if not df_eth_tvl.empty:
        df_master = pd.merge(df_master, df_eth_tvl, on="Date", how="left")
    if not df_tvl.empty:
        df_master = pd.merge(df_master, df_tvl, on="Date", how="left")
    if not df_yields.empty:
        df_master = pd.merge(df_master, df_yields, on="Date", how="left")
    if not df_curve.empty:
        df_master = pd.merge(df_master, df_curve, on="Date", how="left")

    cols_interp = ["tvl_rede_ethereum_total_usd", "tvl_lido_total_usd", "tvl_lido_ethereum_usd", "apy_lido_pct", "tvl_yield_pool_usd", "tvl_pool_curve_usd", "apy_pool_curve_pct"]
    for c in cols_interp:
        if c in df_master.columns:
            df_master[c] = df_master[c].interpolate(method="linear").ffill().bfill()

    # Dominancia da Lido no TVL Total do Ecossistema Ethereum (%)
    df_master["dominancia_lido_tvl_defi_pct"] = (df_master["tvl_lido_ethereum_usd"] / df_master["tvl_rede_ethereum_total_usd"]) * 100.0

    # Conversao APY Composto -> APR Nominal Diario (n=365):
    df_master["apr_base_nominal_pct"] = 365.0 * (
        np.power(1.0 + df_master["apy_lido_pct"] / 100.0, 1.0 / 365.0) - 1.0
    ) * 100.0

    # Arredondamentos rigorosos
    df_master["tvl_rede_ethereum_total_usd"] = df_master["tvl_rede_ethereum_total_usd"].round(2)
    df_master["tvl_lido_total_usd"] = df_master["tvl_lido_total_usd"].round(2)
    df_master["tvl_lido_ethereum_usd"] = df_master["tvl_lido_ethereum_usd"].round(2)
    df_master["dominancia_lido_tvl_defi_pct"] = df_master["dominancia_lido_tvl_defi_pct"].round(4)
    df_master["tvl_yield_pool_usd"] = df_master["tvl_yield_pool_usd"].round(2)
    df_master["tvl_pool_curve_usd"] = df_master["tvl_pool_curve_usd"].round(2)
    df_master["apy_lido_pct"] = df_master["apy_lido_pct"].round(4)
    df_master["apr_base_nominal_pct"] = df_master["apr_base_nominal_pct"].round(4)
    df_master["apy_pool_curve_pct"] = df_master["apy_pool_curve_pct"].round(4)

    return df_master


def main():
    print("=" * 70)
    print("MODULO 3: TVL, Yields e Liquidez DEX da Pool Curve (DefiLlama)")
    print(f"Recorte Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print("=" * 70)

    print("\n[1/4] Coletando TVL Global do Ecossistema Ethereum...")
    df_eth_tvl = fetch_ethereum_global_tvl()

    print("\n[2/4] Coletando TVL Historico do Lido...")
    df_tvl = fetch_lido_tvl_protocol()

    print("\n[3/4] Coletando Historico de Rendimentos e Pool Curve...")
    df_yields = fetch_lido_yields_history()
    df_curve = fetch_curve_steth_pool_history()

    print("\n[4/4] Processando consolidacao e dominancia de TVL...")
    df_final = processar_metricas_defillama_curve(df_eth_tvl, df_tvl, df_yields, df_curve)

    # Validacoes
    assert len(df_final) == 1488, f"Esperado 1488 dias, obtido {len(df_final)}"
    assert df_final["tvl_rede_ethereum_total_usd"].mean() > 1e10, "[ERRO] TVL Total do Ethereum inconsistente!"

    # Salvar
    destino = os.path.join(DADOS_DIR, "dados_defillama_curve.csv")
    df_final.to_csv(destino, index=False)
    print(f"  -> Salvo em: {destino}")

    print("\n" + "-" * 70)
    print("RESUMO ESTATISTICO DE TVL E LIQUIDEZ (2022-05-05 a 2026-05-31):")
    print(f"  -> Total de Observacoes: {len(df_final)} dias")
    print(f"  -> TVL Total Rede Ethereum Medio: ${df_final['tvl_rede_ethereum_total_usd'].mean():,.2f}")
    print(f"  -> TVL Lido Ethereum Medio:       ${df_final['tvl_lido_ethereum_usd'].mean():,.2f}")
    print(f"  -> Dominancia Media Lido no TVL:  {df_final['dominancia_lido_tvl_defi_pct'].mean():.2f}%")
    print(f"  -> TVL Medio Curve stETH Real:    ${df_final['tvl_pool_curve_usd'].mean():,.2f}")
    print("=" * 70)
    print("MODULO 3 CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()