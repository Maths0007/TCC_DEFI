# -*- coding: utf-8 -*-
"""
MODULO 1: Coleta de Precos Historicos, Retornos, Volatilidade e Depeg (Basis)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)

Fontes:
  - yfinance (ETH-USD e STETH-USD)
  - Contingencia automatica via DefiLlama Coins API

Metricas Calculadas:
  1. Preco de Fechamento ETH (USD) e stETH (USD)
  2. Taxa de Cambio Direta: preco_steth_eth = preco_steth_usd / preco_eth_usd
  3. Liquid Staking Basis: basis = preco_steth_eth - 1.0000
  4. Descolamento Percentual (Depeg %): depeg_pct = basis * 100
  5. Retornos Logaritmicos Diarios: r_t = ln(P_t / P_{t-1})
  6. Volatilidade Realizada de 7 dias e 30 dias anualizada (sigma * sqrt(365) * 100)

Saidas:
  - dados_precos_mercado.csv (diretorio raiz)
  - scripts_e_dados/Dados/dados_precos_mercado.csv
  - files/dados_precos_mercado.csv
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
DADOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Dados")
FILES_DIR = os.path.join(ROOT_DIR, "files")
os.makedirs(DADOS_DIR, exist_ok=True)
os.makedirs(FILES_DIR, exist_ok=True)

# RECORTE TEMPORAL ATUALIZADO
DATA_INICIO = "2022-05-05"
DATA_FIM = "2026-05-31"


def download_yfinance_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Baixa cotacoes diarias do Yahoo Finance via yfinance.
    Normaliza a coluna de data para 'Date' (YYYY-MM-DD em UTC).
    """
    import yfinance as yf
    print(f"  -> Baixando serie historica de {ticker} via yfinance ({start} a {end})...")
    
    # yfinance requer end exclusivo no dia seguinte para capturar a data final completa
    end_dt = pd.to_datetime(end) + pd.Timedelta(days=1)
    end_str = end_dt.strftime("%Y-%m-%d")
    
    try:
        df_raw = yf.download(ticker, start=start, end=end_str, progress=False, auto_adjust=False)
    except Exception as e:
        print(f"  [AVISO] Excecao no download de {ticker}: {e}")
        return pd.DataFrame()

    if df_raw.empty:
        print(f"  [AVISO] yfinance nao retornou dados para {ticker}")
        return pd.DataFrame()

    # Extrair series de fechamento tratando MultiIndex de colunas
    if isinstance(df_raw.columns, pd.MultiIndex):
        close_series = df_raw["Close"].iloc[:, 0] if isinstance(df_raw["Close"], pd.DataFrame) else df_raw["Close"]
    else:
        col = "Close" if "Close" in df_raw.columns else ("Adj Close" if "Adj Close" in df_raw.columns else df_raw.columns[0])
        close_series = df_raw[col]

    df = pd.DataFrame({"Close": close_series.values}, index=df_raw.index)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df["Date"] = df.index.strftime("%Y-%m-%d")
    df = df.reset_index(drop=True)
    df = df.dropna(subset=["Close"]).drop_duplicates(subset=["Date"]).sort_values("Date")
    return df


def fallback_defillama_coins(token_symbol: str, dates: list[str]) -> dict:
    """
    Contingencia via DefiLlama Coins API caso haja lacunas no yfinance.
    """
    print(f"  [CONTINGENCIA] Consultando DefiLlama Coins API para {token_symbol}...")
    coin_id = "coingecko:ethereum" if token_symbol == "ETH" else "coingecko:staked-ether"
    precos = {}
    
    for dt_str in dates:
        dt = pd.to_datetime(dt_str)
        ts = int(dt.replace(tzinfo=timezone.utc).timestamp())
        url = f"https://coins.llama.fi/prices/historical/{ts}/{coin_id}"
        try:
            time.sleep(0.15)
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json().get("coins", {}).get(coin_id, {})
                p = data.get("price")
                if p is not None:
                    precos[dt_str] = float(p)
        except Exception:
            continue
            
    return precos


def processar_precos_mercado(df_eth: pd.DataFrame, df_steth: pd.DataFrame) -> pd.DataFrame:
    """
    Combina as series temporais de ETH e stETH, alinha o grid continuo de datas,
    calcula paridade, basis, depeg %, retornos logaritmicos e volatilidades 7d/30d.
    """
    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df_master = pd.DataFrame({"Date": grid_datas})

    # Mesclar ETH
    df_eth_sub = df_eth[["Date", "Close"]].rename(columns={"Close": "preco_eth_usd"})
    df_eth_sub["fonte_preco_eth"] = "yfinance_ETH-USD"
    df_master = pd.merge(df_master, df_eth_sub, on="Date", how="left")

    # Mesclar stETH
    df_steth_sub = df_steth[["Date", "Close"]].rename(columns={"Close": "preco_steth_usd"})
    df_steth_sub["fonte_preco_steth"] = "yfinance_STETH-USD"
    df_master = pd.merge(df_master, df_steth_sub, on="Date", how="left")

    # Checar se ha lacunas necessitando contingencia
    eth_nans = df_master[df_master["preco_eth_usd"].isna()]["Date"].tolist()
    if eth_nans:
        print(f"  [AVISO] {len(eth_nans)} datas sem preco de ETH no yfinance. Acionando contingencia...")
        precos_fb = fallback_defillama_coins("ETH", eth_nans)
        for d, p in precos_fb.items():
            idx = df_master[df_master["Date"] == d].index
            df_master.loc[idx, "preco_eth_usd"] = p
            df_master.loc[idx, "fonte_preco_eth"] = "defillama_coins_ETH"

    steth_nans = df_master[df_master["preco_steth_usd"].isna()]["Date"].tolist()
    if steth_nans:
        print(f"  [AVISO] {len(steth_nans)} datas sem preco de stETH no yfinance. Acionando contingencia...")
        precos_fb = fallback_defillama_coins("stETH", steth_nans)
        for d, p in precos_fb.items():
            idx = df_master[df_master["Date"] == d].index
            df_master.loc[idx, "preco_steth_usd"] = p
            df_master.loc[idx, "fonte_preco_steth"] = "defillama_coins_stETH"

    # Interpolacao suave linear para eventuais lacunas remanescentes
    df_master["preco_eth_usd"] = df_master["preco_eth_usd"].interpolate(method="linear").ffill().bfill()
    df_master["preco_steth_usd"] = df_master["preco_steth_usd"].interpolate(method="linear").ffill().bfill()

    # 1. Taxa de Cambio Direta (Preco Relativo no Mercado Secundario)
    df_master["preco_steth_eth"] = df_master["preco_steth_usd"] / df_master["preco_eth_usd"]

    # 2. Liquid Staking Basis e Depeg %
    # Basis = Preco_stETH/Preco_ETH - 1.0000
    df_master["liquid_staking_basis"] = df_master["preco_steth_eth"] - 1.0
    df_master["depeg_pct"] = df_master["liquid_staking_basis"] * 100.0

    # 3. Retornos Logaritmicos Diarios: r_t = ln(P_t / P_{t-1})
    df_master["retorno_log_eth"] = np.log(df_master["preco_eth_usd"] / df_master["preco_eth_usd"].shift(1))
    df_master["retorno_log_steth"] = np.log(df_master["preco_steth_usd"] / df_master["preco_steth_usd"].shift(1))

    # 4. Volatilidade Realizada de 7 dias e 30 dias anualizada (sqrt(365))
    fator_anualizacao = np.sqrt(365.0) * 100.0
    
    # min_periods exige historico suficiente na janela (nao fabrica dado na borda inicial)
    df_master["volatilidade_7d_anual_eth"] = df_master["retorno_log_eth"].rolling(window=7, min_periods=7).std() * fator_anualizacao
    df_master["volatilidade_30d_anual_eth"] = df_master["retorno_log_eth"].rolling(window=30, min_periods=30).std() * fator_anualizacao
    
    df_master["volatilidade_7d_anual_steth"] = df_master["retorno_log_steth"].rolling(window=7, min_periods=7).std() * fator_anualizacao
    df_master["volatilidade_30d_anual_steth"] = df_master["retorno_log_steth"].rolling(window=30, min_periods=30).std() * fator_anualizacao

    # Formatar arredondamentos para saida rigorosa
    df_master["preco_eth_usd"] = df_master["preco_eth_usd"].round(2)
    df_master["preco_steth_usd"] = df_master["preco_steth_usd"].round(2)
    df_master["preco_steth_eth"] = df_master["preco_steth_eth"].round(6)
    df_master["liquid_staking_basis"] = df_master["liquid_staking_basis"].round(6)
    df_master["depeg_pct"] = df_master["depeg_pct"].round(4)
    df_master["retorno_log_eth"] = df_master["retorno_log_eth"].round(6)
    df_master["retorno_log_steth"] = df_master["retorno_log_steth"].round(6)
    df_master["volatilidade_7d_anual_eth"] = df_master["volatilidade_7d_anual_eth"].round(4)
    df_master["volatilidade_30d_anual_eth"] = df_master["volatilidade_30d_anual_eth"].round(4)
    df_master["volatilidade_7d_anual_steth"] = df_master["volatilidade_7d_anual_steth"].round(4)
    df_master["volatilidade_30d_anual_steth"] = df_master["volatilidade_30d_anual_steth"].round(4)

    return df_master


def main():
    print("=" * 70)
    print("MODULO 1: Coleta e Processamento de Precos, Volatilidade e Depeg")
    print(f"Recorte Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    # 1. Download ETH-USD
    print("\n[1/4] Coletando Precos Diarios de ETH-USD...")
    df_eth = download_yfinance_ticker("ETH-USD", DATA_INICIO, DATA_FIM)
    print(f"  [OK] ETH-USD: {len(df_eth)} registros carregados.")

    # 2. Download STETH-USD
    print("\n[2/4] Coletando Precos Diarios de STETH-USD...")
    df_steth = download_yfinance_ticker("STETH-USD", DATA_INICIO, DATA_FIM)
    print(f"  [OK] STETH-USD: {len(df_steth)} registros carregados.")

    if df_eth.empty or df_steth.empty:
        print("[ERRO FATAL] Falha na coleta de precos do yfinance.")
        sys.exit(1)

    # 3. Processamento Quantitativo e Alinhamento
    print("\n[3/4] Alinhando series temporais e calculando metricas financeiras...")
    df_mercado = processar_precos_mercado(df_eth, df_steth)

    # Validacoes de Integridade
    assert len(df_mercado) == 1488, f"Esperado 1488 dias entre {DATA_INICIO} e {DATA_FIM}, obtido {len(df_mercado)}"
    assert df_mercado["depeg_pct"].std() > 0.05, "[ERRO] Depeg com variabilidade nula detectado!"
    assert (df_mercado["preco_eth_usd"] > 0).all(), "[ERRO] Precos nulos ou negativos em ETH!"
    assert (df_mercado["preco_steth_usd"] > 0).all(), "[ERRO] Precos nulos ou negativos em stETH!"

    # 4. Salvamento em todas as pastas
    print("\n[4/4] Salvando dataset_precos_mercado.csv...")
    destinos = [
        os.path.join(ROOT_DIR, "dados_precos_mercado.csv"),
        os.path.join(DADOS_DIR, "dados_precos_mercado.csv"),
        os.path.join(FILES_DIR, "dados_precos_mercado.csv"),
        os.path.join(FILES_DIR, "scripts_e_dados", "Dados", "dados_precos_mercado.csv")
    ]

    for d in destinos:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        df_mercado.to_csv(d, index=False)
        print(f"  -> Salvo em: {d}")

    # Estatisticas Descritivas Finais
    print("\n" + "-" * 70)
    print("RESUMO ESTATISTICO DA SERIE DE PRECOS E DEPEG (2022-05-05 a 2026-05-31):")
    print(f"  -> Total de Observacoes: {len(df_mercado)} dias")
    print(f"  -> Preco Medio ETH:   ${df_mercado['preco_eth_usd'].mean():.2f} (Min: ${df_mercado['preco_eth_usd'].min():.2f}, Max: ${df_mercado['preco_eth_usd'].max():.2f})")
    print(f"  -> Preco Medio stETH: ${df_mercado['preco_steth_usd'].mean():.2f} (Min: ${df_mercado['preco_steth_usd'].min():.2f}, Max: ${df_mercado['preco_steth_usd'].max():.2f})")
    print(f"  -> Taxa stETH/ETH Media: {df_mercado['preco_steth_eth'].mean():.6f}")
    print(f"  -> Depeg Medio: {df_mercado['depeg_pct'].mean():.4f}% | Depeg Minimo: {df_mercado['depeg_pct'].min():.4f}% (Crash Terra/Luna)")
    print(f"  -> Volatilidade 30d Anualizada Media: ETH {df_mercado['volatilidade_30d_anual_eth'].mean():.2f}% | stETH {df_mercado['volatilidade_30d_anual_steth'].mean():.2f}%")
    print("=" * 70)
    print("MODULO 1 CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()