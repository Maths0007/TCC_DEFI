# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "pandas",
# ]
# ///
"""
Script 01: Coleta de dados de preço ETH/USD e Depeg stETH/ETH
Fonte: DefiLlama Coins API (gratuita, sem API key)
Saídas:
  1. scripts_e_dados/Dados/preco_eth_usd.csv
  2. scripts_e_dados/Dados/depeg_steth_eth.csv
"""
import sys
import time
import pandas as pd
from datetime import datetime, timezone
from utils import fetch_coins_chart, save_csv_and_log

STETH_ID = "coingecko:staked-ether"
ETH_ID = "coingecko:ethereum"


def main():
    print("=" * 60)
    print("SCRIPT 01 -- Coleta: Preços ETH/USD e Depeg stETH/ETH")
    print(f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Buscar preços historicos de ETH/USD (desde o lançamento do Ethereum em 2015)
    print("\n[1/4] Buscando preços históricos ETH/USD...")
    eth_prices = fetch_coins_chart(ETH_ID, start_ts=1438387200)
    if not eth_prices:
        print("  [ERRO] Nenhum dado retornado para ETH")
        sys.exit(1)
    print(f"  [OK] {len(eth_prices)} pontos totais para ETH")

    # 2. Processar e salvar preco_eth_usd.csv
    print("\n[2/4] Processando e salvando preco_eth_usd.csv...")
    eth_records = []
    eth_by_date = {}
    for entry in eth_prices:
        ts = entry.get("timestamp", 0)
        price = entry.get("price", 0)
        dt_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        eth_by_date[dt_str] = price
        eth_records.append({
            "data": dt_str,
            "preco_eth_usd": round(price, 2),
        })

    df_eth = pd.DataFrame(eth_records)
    df_eth = df_eth.drop_duplicates(subset=["data"], keep="first").sort_values("data").reset_index(drop=True)

    save_csv_and_log(
        df_eth,
        "preco_eth_usd.csv",
        lambda df: print(
            f"  -> Preço mínimo: ${df['preco_eth_usd'].min():,.2f} | "
            f"Máximo: ${df['preco_eth_usd'].max():,.2f} | "
            f"Atual: ${df['preco_eth_usd'].iloc[-1]:,.2f}"
        )
    )

    # 3. Buscar preços históricos stETH/USD
    print("\n[3/4] Buscando preços históricos stETH/USD...")
    time.sleep(1)
    steth_prices = fetch_coins_chart(STETH_ID, start_ts=1609459200)  # Desde 2021-01-01
    if not steth_prices:
        print("  [ERRO] Nenhum dado retornado para stETH")
        sys.exit(1)
    print(f"  [OK] {len(steth_prices)} pontos totais para stETH")

    # 4. Calcular ratio stETH/ETH e depeg_pct, salvar depeg_steth_eth.csv
    print("\n[4/4] Processando e salvando depeg_steth_eth.csv...")
    steth_by_date = {}
    for entry in steth_prices:
        dt_str = datetime.fromtimestamp(entry["timestamp"], tz=timezone.utc).strftime("%Y-%m-%d")
        steth_by_date[dt_str] = entry["price"]

    common_dates = sorted(set(steth_by_date.keys()) & set(eth_by_date.keys()))
    depeg_records = []
    for dt in common_dates:
        steth_usd = steth_by_date[dt]
        eth_usd = eth_by_date[dt]
        if eth_usd > 0 and steth_usd > 0:
            ratio = steth_usd / eth_usd
            depeg_records.append({
                "data": dt,
                "preco_steth_eth": round(ratio, 6),
                "preco_steth_usd": round(steth_usd, 2),
                "preco_eth_usd": round(eth_usd, 2),
                "depeg_pct": round((ratio - 1.0) * 100, 4),
            })

    df_depeg = pd.DataFrame(depeg_records)
    df_depeg = df_depeg.sort_values("data").reset_index(drop=True)

    save_csv_and_log(
        df_depeg,
        "depeg_steth_eth.csv",
        lambda df: print(
            f"  -> Depeg mínimo (pior desconto): {df['depeg_pct'].min():.4f}%\n"
            f"  -> Depeg máximo (maior prêmio):  {df['depeg_pct'].max():.4f}%\n"
            f"  -> Depeg médio:                  {df['depeg_pct'].mean():.4f}%"
        )
    )

    print("\n[OK] Script 01 concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
