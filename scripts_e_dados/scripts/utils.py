# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "pandas",
# ]
# ///
"""
Módulo de Utilidades para os Scripts de Coleta do TCC (DefiLlama & Data Management)
"""
import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Dados")

COINS_URL = "https://coins.llama.fi"
YIELDS_URL = "https://yields.llama.fi"
PROTOCOLS_URL = "https://api.llama.fi"


def fetch_coins_chart(coin_id: str, start_ts: int = 1546300800, max_span: int = 500) -> list[dict]:
    """
    Busca série histórica completa de preços via DefiLlama Coins API com paginação.
    """
    all_prices = []
    start = start_ts
    now = int(datetime.now(timezone.utc).timestamp())

    while start < now:
        url = f"{COINS_URL}/chart/{coin_id}"
        params = {"period": "1d", "span": max_span, "start": start}
        resp = requests.get(url, params=params, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        coins = data.get("coins", {})
        if not coins:
            break
        key = list(coins.keys())[0]
        prices = coins[key].get("prices", [])
        if not prices:
            break
        all_prices.extend(prices)
        last_ts = prices[-1]["timestamp"]
        start = last_ts + 86400
        print(f"    ... {len(all_prices)} pontos (até {datetime.fromtimestamp(last_ts, tz=timezone.utc).strftime('%Y-%m-%d')})")
        time.sleep(0.5)

    return all_prices


def fetch_yield_pools() -> list[dict]:
    """Busca a lista completa de pools do DefiLlama Yields API."""
    resp = requests.get(f"{YIELDS_URL}/pools", timeout=60)
    resp.raise_for_status()
    return resp.json().get("data", [])


def fetch_yield_pool_history(pool_uuid: str) -> list[dict]:
    """Busca série histórica de APY para um pool específico na DefiLlama Yields API."""
    url = f"{YIELDS_URL}/chart/{pool_uuid}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.json().get("data", [])


def fetch_protocol_data(protocol_slug: str) -> dict:
    """Busca os dados detalhados (incluindo TVL por chain) de um protocolo."""
    resp = requests.get(f"{PROTOCOLS_URL}/protocol/{protocol_slug}", timeout=60)
    resp.raise_for_status()
    return resp.json()


def fetch_all_protocols() -> list[dict]:
    """Busca a lista de todos os protocolos no DefiLlama."""
    resp = requests.get(f"{PROTOCOLS_URL}/protocols", timeout=60)
    resp.raise_for_status()
    return resp.json()


def save_csv_and_log(df: pd.DataFrame, filename: str, metrics_fn=None) -> str:
    """Garante que a pasta Dados existe e salva o DataFrame em CSV."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(output_path, index=False)
    
    print(f"  -> Salvo em: {output_path}")
    if "data" in df.columns and len(df) > 0:
        print(f"  -> Período: {df['data'].iloc[0]} a {df['data'].iloc[-1]}")
    print(f"  -> Total de registros: {len(df)}")
    if metrics_fn:
        metrics_fn(df)
    return output_path
