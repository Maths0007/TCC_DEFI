# -*- coding: utf-8 -*-
"""
MODULO 1: Coleta de Precos Historicos, Retornos, Volatilidade e Depeg (Basis)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Frequencia Diaria UTC)

Fontes: yfinance (ETH-USD e STETH-USD), com contingencia via DefiLlama Coins API
Saidas:
  - dados_precos_mercado.csv (diretorio raiz)
  - scripts_e_dados/Dados/dados_precos_mercado.csv
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DADOS_DIR = os.path.join(BASE_DIR, "Dados")
os.makedirs(DADOS_DIR, exist_ok=True)

DATA_INICIO = "2022-04-01"
DATA_FIM = "2026-05-31"


def download_yfinance_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    import yfinance as yf
    print(f"  -> Baixando serie historica de {ticker} via yfinance ({start} a {end})...")
    end_dt = pd.to_datetime(end) + pd.Timedelta(days=1)
    end_str = end_dt.strftime("%Y-%m-%d")
    
    try:
        df = yf.download(ticker, start=start, end=end_str, progress=False, auto_adjust=False)
    except Exception as e:
        print(f"  [AVISO] Excecao no download de {ticker}: {e}")
        return pd.DataFrame()

    if df.empty:
        print(f"  [AVISO] yfinance nao retornou dados para {ticker}")
        return pd.DataFrame()

    if isinstance(df.columns, pd.MultiIndex):
        if "Close" in df.columns.levels[0]:
            df_close = df["Close"].copy()
            if ticker in df_close.columns:
                df = df_close[[ticker]].rename(columns={ticker: "Close"})
            else:
                df = df_close.iloc[:, 0].to_frame(name="Close")
        else:
            df = df.iloc[:, 0].to_frame(name="Close")
    else:
        if "Close" in df.columns:
            df = df[["Close"]].copy()

    df = df.reset_index()
    date_col = [c for c in df.columns if "Date" in str(c) or "data" in str(c).lower()][0]
    df["Date"] = pd.to_datetime(df[date_col]).dt.tz_localize(None).dt.strftime("%Y-%m-%d")
    df = df[["Date", "Close"]].drop_duplicates(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df


def fetch_defillama_coins_chart(coin_id: str, start_ts: int = 1648771200) -> dict[str, float]:
    url = f"https://coins.llama.fi/chart/{coin_id}"
    params = {"period": "1d", "span": 2000, "start": start_ts}
    try:
        time.sleep(1.5)
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            coins = resp.json().get("coins", {})
            if coins:
                k = list(coins.keys())[0]
                prices = coins[k].get("prices", [])
                out = {}
                for p in prices:
                    dt_str = datetime.fromtimestamp(p["timestamp"], tz=timezone.utc).strftime("%Y-%m-%d")
                    out[dt_str] = float(p["price"])
                return out
    except Exception as e:
        print(f"  [AVISO] Falha no fallback DefiLlama ({coin_id}): {e}")
    return {}


def main():
    print("=" * 70)
    print("MODULO 1: Coleta e Processamento de Precos, Volatilidade e Depeg")
    print(f"Janela Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    print("\n[1/4] Coletando Precos Diarios de ETH-USD...")
    try:
        df_eth = download_yfinance_ticker("ETH-USD", DATA_INICIO, DATA_FIM)
    except Exception as e:
        print(f"  [AVISO] Erro yfinance ETH-USD: {e}. Tentando fallback...")
        df_eth = pd.DataFrame()

    if df_eth.empty:
        eth_dict = fetch_defillama_coins_chart("coingecko:ethereum", 1648771200)
        df_eth = pd.DataFrame(list(eth_dict.items()), columns=["Date", "Close"]).sort_values("Date")

    df_eth = df_eth.rename(columns={"Close": "preco_eth_usd"})
    print(f"  [OK] ETH-USD: {len(df_eth)} registros carregados.")

    print("\n[2/4] Coletando Precos Diarios de STETH-USD...")
    time.sleep(1.5)
    try:
        df_steth = download_yfinance_ticker("STETH-USD", DATA_INICIO, DATA_FIM)
    except Exception as e:
        print(f"  [AVISO] Erro yfinance STETH-USD: {e}. Tentando fallback...")
        df_steth = pd.DataFrame()

    if df_steth.empty:
        steth_dict = fetch_defillama_coins_chart("coingecko:staked-ether", 1648771200)
        df_steth = pd.DataFrame(list(steth_dict.items()), columns=["Date", "Close"]).sort_values("Date")

    df_steth = df_steth.rename(columns={"Close": "preco_steth_usd"})
    print(f"  [OK] STETH-USD: {len(df_steth)} registros carregados.")

    print("\n[3/4] Alinhando series e calculando metricas financeiras...")
    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df = pd.DataFrame({"Date": grid_datas})

    df = pd.merge(df, df_eth, on="Date", how="left")
    df = pd.merge(df, df_steth, on="Date", how="left")

    df["preco_eth_usd"] = df["preco_eth_usd"].interpolate(method="linear").ffill().bfill()
    df["preco_steth_usd"] = df["preco_steth_usd"].interpolate(method="linear").ffill().bfill()

    df["preco_steth_eth"] = df["preco_steth_usd"] / df["preco_eth_usd"]

    df["liquid_staking_basis"] = df["preco_steth_eth"] - 1.0
    df["depeg_pct"] = df["liquid_staking_basis"] * 100.0

    df["retorno_log_eth"] = np.log(df["preco_eth_usd"] / df["preco_eth_usd"].shift(1))
    df["retorno_log_steth"] = np.log(df["preco_steth_usd"] / df["preco_steth_usd"].shift(1))

    sqrt_365 = np.sqrt(365.0)
    df["volatilidade_7d_anual_eth"] = df["retorno_log_eth"].rolling(window=7).std() * sqrt_365
    df["volatilidade_30d_anual_eth"] = df["retorno_log_eth"].rolling(window=30).std() * sqrt_365
    df["volatilidade_7d_anual_steth"] = df["retorno_log_steth"].rolling(window=7).std() * sqrt_365
    df["volatilidade_30d_anual_steth"] = df["retorno_log_steth"].rolling(window=30).std() * sqrt_365

    df["Date_dt"] = pd.to_datetime(df["Date"])
    df = df[(df["Date_dt"] >= pd.to_datetime(DATA_INICIO)) & (df["Date_dt"] <= pd.to_datetime(DATA_FIM))]
    df = df.drop(columns=["Date_dt"]).reset_index(drop=True)

    df["preco_eth_usd"] = df["preco_eth_usd"].round(2)
    df["preco_steth_usd"] = df["preco_steth_usd"].round(2)
    df["preco_steth_eth"] = df["preco_steth_eth"].round(6)
    df["liquid_staking_basis"] = df["liquid_staking_basis"].round(6)
    df["depeg_pct"] = df["depeg_pct"].round(4)
    df["retorno_log_eth"] = df["retorno_log_eth"].round(6)
    df["retorno_log_steth"] = df["retorno_log_steth"].round(6)
    df["volatilidade_7d_anual_eth"] = df["volatilidade_7d_anual_eth"].round(6)
    df["volatilidade_30d_anual_eth"] = df["volatilidade_30d_anual_eth"].round(6)
    df["volatilidade_7d_anual_steth"] = df["volatilidade_7d_anual_steth"].round(6)
    df["volatilidade_30d_anual_steth"] = df["volatilidade_30d_anual_steth"].round(6)

    print("\n[4/4] Salvando dataset de precos e volatilidade...")
    saida_raiz = os.path.join(DADOS_DIR, "dados_precos_mercado.csv")
    saida_dados = os.path.join(DADOS_DIR, "dados_precos_mercado.csv")

    df.to_csv(saida_raiz, index=False)
    df.to_csv(saida_dados, index=False)

    print(f"  -> Salvo com sucesso em: {saida_raiz}")
    print(f"  -> Copia sincronizada em: {saida_dados}")
    print(f"  -> Total de linhas: {len(df)} dias ({df['Date'].iloc[0]} a {df['Date'].iloc[-1]})")
    print(f"  -> Depeg medio: {df['depeg_pct'].mean():.4f}% | Minimo: {df['depeg_pct'].min():.4f}%")
    print(f"  -> Volatilidade 30d media ETH: {df['volatilidade_30d_anual_eth'].mean()*100:.2f}% | stETH: {df['volatilidade_30d_anual_steth'].mean()*100:.2f}%")
    print("=" * 70)
    print("MODULO 1 CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()