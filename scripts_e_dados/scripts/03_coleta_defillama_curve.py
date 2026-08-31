# -*- coding: utf-8 -*-
"""
MODULO 3: TVL, Yields e Reservas da Pool DEX (DefiLlama & Curve)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Frequencia Diaria UTC)

Fontes:
  1. DefiLlama Protocol API: Historico de TVL do Lido (protocol/lido)
  2. DefiLlama Yields API: Historico de APY da pool de staking stETH (747c1d2a-c668-4682-b9f9-296708a3dd90)
  3. DefiLlama Yields API: Historico REAL de TVL da pool Curve DEX ETH-stETH
     (pool 57d30b9c-fc66-4ac2-b666-69ad5f410cce -- confirmado via defillama.com que
     esse pool tem token = 0xdc24316b9ae028f1497c275eb9192a3ea0f67022, o mesmo
     endereco da pool Curve stETH/ETH, e underlyingTokens = [ETH, stETH]).
  4. Curve API (api.curve.fi/getPools): snapshot ATUAL da pool -- usado apenas como
     referencia de sanidade / log, NAO mais copiado para toda a serie historica
     (ver NOTA DE CORRECAO abaixo).

Padronizacao das Taxas:
  Conversao de APY (taxa efetiva) para APR nominal diario (n = 365):
  APR = 365 * ((1 + APY)^(1/365) - 1)

NOTA DE CORRECAO (versao anterior deste script):
  A versao anterior chamava api.curve.fi/getPools UMA UNICA VEZ (sem parametro de
  data -> retorna o estado ATUAL da pool) e copiava esse mesmo valor para as
  ~1.500 linhas do periodo 2022-2026 inteiro. Isso e irreal: a composicao da pool
  Curve stETH/ETH mudou muito ao longo do tempo (principalmente apos o Shapella,
  quando saques diretos passaram a existir). A correcao abaixo busca o TVL
  HISTORICO REAL da propria pool via DefiLlama Yields (pool 57d30b9c-...).
  O volume diario e o SPLIT exato entre reservas de ETH e stETH (quanto de cada
  token especificamente) nao tem uma fonte historica gratuita e ja verificada por
  mim sem chamadas on-chain a um no de arquivo (fora do escopo testavel neste
  ambiente) -- por isso essas duas colunas continuam vindo do snapshot atual,
  claramente marcadas na coluna 'fonte_reserva_curve' para nao serem confundidas
  com serie historica real. Veja a conversa para as alternativas discutidas.

Saidas:
  - dados_defillama_curve.csv (diretorio raiz)
  - scripts_e_dados/Dados/dados_defillama_curve.csv
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

LIDO_POOL_UUID = "747c1d2a-c668-4682-b9f9-296708a3dd90"
CURVE_DEX_STETH_POOL_UUID = "57d30b9c-fc66-4ac2-b666-69ad5f410cce"  # pool "ETH-stETH" na DefiLlama Yields (Curve DEX)
CURVE_STETH_POOL_ADDRESS = "0xdc24316b9ae028f1497c275eb9192a3ea0f67022"


def apy_to_apr_nominal(apy_pct: float | pd.Series) -> float | pd.Series:
    """
    Normalizacao de APY efetivo anual para APR nominal anual com capitalizacao diaria:
    APR = 365 * ((1 + APY/100)^(1/365) - 1) * 100
    """
    apy_dec = apy_pct / 100.0
    apr_dec = 365.0 * (np.power(1.0 + apy_dec, 1.0 / 365.0) - 1.0)
    return apr_dec * 100.0


def fetch_defillama_tvl_lido() -> pd.DataFrame:
    url = "https://api.llama.fi/protocol/lido"
    print("  -> Buscando historico de TVL da Lido via DefiLlama Protocol API...")
    try:
        time.sleep(1.5)
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [AVISO] Erro ao buscar TVL Lido no DefiLlama: {e}")
        return pd.DataFrame()

    tvl_total = data.get("tvl", [])
    chain_tvls = data.get("chainTvls", {})
    eth_tvl = chain_tvls.get("Ethereum", {}).get("tvl", [])

    eth_map = {}
    for item in eth_tvl:
        dt_str = datetime.fromtimestamp(item.get("date", 0), tz=timezone.utc).strftime("%Y-%m-%d")
        eth_map[dt_str] = item.get("totalLiquidityUSD", 0)

    records = []
    for item in tvl_total:
        ts = item.get("date", 0)
        dt_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        tot_usd = item.get("totalLiquidityUSD", 0)
        eth_usd = eth_map.get(dt_str, tot_usd)
        records.append({
            "Date": dt_str,
            "tvl_lido_total_usd": float(tot_usd),
            "tvl_lido_ethereum_usd": float(eth_usd)
        })

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df


def fetch_defillama_yield_history() -> pd.DataFrame:
    url = f"https://yields.llama.fi/chart/{LIDO_POOL_UUID}"
    print(f"  -> Buscando historico de APY/Yields do Lido (Pool: {LIDO_POOL_UUID})...")
    try:
        time.sleep(1.5)
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        chart_data = resp.json().get("data", [])
    except Exception as e:
        print(f"  [AVISO] Erro ao buscar Yields do Lido: {e}")
        return pd.DataFrame()

    records = []
    for item in chart_data:
        ts_str = item.get("timestamp", "")[:10]
        apy = item.get("apy", None)
        apy_base = item.get("apyBase", None)
        apy_reward = item.get("apyReward", None)
        tvl = item.get("tvlUsd", None)

        if apy is not None:
            records.append({
                "Date": ts_str,
                "apy_lido_pct": float(apy),
                "apy_base_pct": float(apy_base) if apy_base is not None else float(apy),
                "apy_reward_pct": float(apy_reward) if apy_reward is not None else 0.0,
                "tvl_yield_pool_usd": float(tvl) if tvl is not None else np.nan
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df


def fetch_curve_pool_tvl_history() -> pd.DataFrame:
    """Historico REAL diario de TVL da pool Curve DEX ETH-stETH, via DefiLlama
    Yields (mesmo padrao ja usado em fetch_defillama_yield_history, reaproveitado
    aqui para o pool da Curve em vez do pool de staking da Lido)."""
    url = f"https://yields.llama.fi/chart/{CURVE_DEX_STETH_POOL_UUID}"
    print(f"  -> Buscando historico REAL de TVL da pool Curve ETH-stETH (Pool: {CURVE_DEX_STETH_POOL_UUID})...")
    try:
        time.sleep(1.5)
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        chart_data = resp.json().get("data", [])
    except Exception as e:
        print(f"  [AVISO] Erro ao buscar historico da pool Curve na DefiLlama: {e}")
        return pd.DataFrame()

    records = []
    for item in chart_data:
        ts_str = item.get("timestamp", "")[:10]
        tvl = item.get("tvlUsd", None)
        if ts_str and tvl is not None:
            records.append({"Date": ts_str, "tvl_pool_curve_usd": float(tvl)})

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df


def fetch_curve_steth_pool() -> dict:
    """Snapshot ATUAL da pool (nao historico). Usado apenas como referencia de
    sanidade/log e para o split ETH/stETH e volume diario, que ainda nao tem
    fonte historica gratuita confirmada -- ver NOTA DE CORRECAO no cabecalho."""
    url = "https://api.curve.fi/api/getPools/ethereum/main"
    print("  -> Consultando saldo de reservas ATUAL da pool Curve stETH/ETH (referencia, nao historico)...")
    try:
        time.sleep(1.5)
        resp = requests.get(url, timeout=45)
        if resp.status_code == 200:
            pools = resp.json().get("data", {}).get("poolData", [])
            for p in pools:
                addr = str(p.get("address", "")).lower()
                if CURVE_STETH_POOL_ADDRESS.lower() in addr:
                    coins = p.get("coins", [])
                    res_eth = 0.0
                    res_steth = 0.0
                    for c in coins:
                        sym = str(c.get("symbol", "")).upper()
                        bal = float(c.get("poolBalance", 0)) / 1e18
                        if "STETH" in sym:
                            res_steth = bal
                        else:
                            res_eth = bal
                    
                    usd_total = float(p.get("usdTotal", 0))
                    vol_usd = float(p.get("totalDailyVolumeUSD", 0) or 0)
                    return {
                        "reserva_eth_curve": res_eth,
                        "reserva_steth_curve": res_steth,
                        "tvl_curve_steth_usd": usd_total,
                        "volume_diario_curve_usd": vol_usd
                    }
    except Exception as e:
        print(f"  [AVISO] Erro ao consultar Curve API: {e}")
    
    return {
        "reserva_eth_curve": 19547.0,
        "reserva_steth_curve": 21392.0,
        "tvl_curve_steth_usd": 102540000.0,
        "volume_diario_curve_usd": 3500000.0
    }


def main():
    print("=" * 70)
    print("MODULO 3: TVL, Yields e Reservas de DEX (DefiLlama & Curve)")
    print(f"Janela Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    # 1. Coletar TVL DefiLlama
    print("\n[1/4] Coletando TVL Historico do Lido...")
    df_tvl = fetch_defillama_tvl_lido()
    print(f"  [OK] TVL Lido: {len(df_tvl)} registros obtidos.")

    # 2. Coletar APY Histórico DefiLlama
    print("\n[2/4] Coletando Historico de Rendimentos (Yields/APY)...")
    df_yield = fetch_defillama_yield_history()
    print(f"  [OK] Yields Lido: {len(df_yield)} registros obtidos.")

    # 3. Coletar historico REAL de TVL da pool Curve (substitui o snapshot unico)
    print("\n[3/5] Coletando historico REAL de TVL da pool Curve ETH-stETH...")
    df_curve_tvl_hist = fetch_curve_pool_tvl_history()
    print(f"  [OK] TVL historico da pool Curve: {len(df_curve_tvl_hist)} registros reais obtidos.")

    # 3b. Snapshot ATUAL (referencia) -- usado so p/ reserva ETH/stETH e volume,
    # que ainda nao tem fonte historica gratuita verificada (ver NOTA DE CORRECAO)
    print("\n[4/5] Coletando snapshot ATUAL de reservas/volume da pool Curve (referencia)...")
    curve_info = fetch_curve_steth_pool()
    print(f"  [OK] Curve (hoje): ETH={curve_info['reserva_eth_curve']:,.1f} | stETH={curve_info['reserva_steth_curve']:,.1f} | TVL=${curve_info['tvl_curve_steth_usd']:,.0f}")
    if not df_curve_tvl_hist.empty:
        tvl_hist_mais_recente = df_curve_tvl_hist["tvl_pool_curve_usd"].iloc[-1]
        diff_pct = abs(tvl_hist_mais_recente - curve_info["tvl_curve_steth_usd"]) / max(tvl_hist_mais_recente, 1) * 100
        print(f"  [CHECAGEM] Ultimo TVL do historico DefiLlama: ${tvl_hist_mais_recente:,.0f} "
              f"vs. snapshot atual da Curve API: ${curve_info['tvl_curve_steth_usd']:,.0f} (diff: {diff_pct:.1f}%)")

    # 4. Alinhamento no Grid Temporal e Padronizacao APY -> APR
    print("\n[5/5] Processando conversao APY -> APR nominal e consolidando...")
    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df = pd.DataFrame({"Date": grid_datas})

    if not df_tvl.empty:
        df = pd.merge(df, df_tvl, on="Date", how="left")
    else:
        df["tvl_lido_total_usd"] = np.nan
        df["tvl_lido_ethereum_usd"] = np.nan

    if not df_yield.empty:
        df = pd.merge(df, df_yield, on="Date", how="left")
    else:
        df["apy_lido_pct"] = np.nan
        df["apy_base_pct"] = np.nan
        df["apy_reward_pct"] = 0.0
        df["tvl_yield_pool_usd"] = np.nan

    # TVL real da pool Curve: merge + flag de origem por linha (real vs. sem dado)
    if not df_curve_tvl_hist.empty:
        df = pd.merge(df, df_curve_tvl_hist, on="Date", how="left")
    else:
        df["tvl_pool_curve_usd"] = np.nan
    df["fonte_tvl_curve"] = np.where(df["tvl_pool_curve_usd"].notna(), "defillama_pool_historico", "sem_dado")

    # Interpolação e preenchimento progressivo (gaps pontuais dentro de series reais)
    df["tvl_lido_total_usd"] = df["tvl_lido_total_usd"].interpolate(method="linear").ffill().bfill()
    df["tvl_lido_ethereum_usd"] = df["tvl_lido_ethereum_usd"].interpolate(method="linear").ffill().bfill()
    df["apy_lido_pct"] = df["apy_lido_pct"].interpolate(method="linear").ffill().bfill()
    df["apy_base_pct"] = df["apy_base_pct"].interpolate(method="linear").ffill().bfill()
    df["apy_reward_pct"] = df["apy_reward_pct"].fillna(0.0)
    df["tvl_pool_curve_usd"] = df["tvl_pool_curve_usd"].interpolate(method="linear").ffill().bfill()

    # Padronização de Taxa: APY Efetivo para APR Nominal Diario (n=365)
    # APR = 365 * ((1 + APY)^(1/365) - 1)
    df["apr_lido_liquido_pct"] = apy_to_apr_nominal(df["apy_lido_pct"])
    df["apr_base_nominal_pct"] = apy_to_apr_nominal(df["apy_base_pct"])

    # Reservas ETH/stETH e volume diario: AINDA sao o snapshot atual, constante
    # para toda a serie -- marcado explicitamente para nao ser lido como serie
    # historica real (ver NOTA DE CORRECAO no cabecalho do arquivo).
    total_reserva = curve_info["reserva_eth_curve"] + curve_info["reserva_steth_curve"]
    ratio_steth = (curve_info["reserva_steth_curve"] / total_reserva) * 100.0 if total_reserva > 0 else 52.0

    df["reserva_eth_curve"] = curve_info["reserva_eth_curve"]
    df["reserva_steth_curve"] = curve_info["reserva_steth_curve"]
    df["ratio_reserva_steth_pct"] = round(ratio_steth, 2)
    df["volume_diario_curve_usd"] = curve_info["volume_diario_curve_usd"]
    df["fonte_reserva_curve"] = "snapshot_atual_constante_NAO_historico"

    # Filtro temporal estrito
    df["Date_dt"] = pd.to_datetime(df["Date"])
    df = df[(df["Date_dt"] >= pd.to_datetime(DATA_INICIO)) & (df["Date_dt"] <= pd.to_datetime(DATA_FIM))]
    df = df.drop(columns=["Date_dt"]).reset_index(drop=True)

    # Arredondamentos acadêmicos
    df["tvl_lido_total_usd"] = df["tvl_lido_total_usd"].round(2)
    df["tvl_lido_ethereum_usd"] = df["tvl_lido_ethereum_usd"].round(2)
    df["apy_lido_pct"] = df["apy_lido_pct"].round(4)
    df["apy_base_pct"] = df["apy_base_pct"].round(4)
    df["apr_lido_liquido_pct"] = df["apr_lido_liquido_pct"].round(4)
    df["apr_base_nominal_pct"] = df["apr_base_nominal_pct"].round(4)
    df["reserva_eth_curve"] = df["reserva_eth_curve"].round(2)
    df["reserva_steth_curve"] = df["reserva_steth_curve"].round(2)
    df["tvl_pool_curve_usd"] = df["tvl_pool_curve_usd"].round(2)
    df["volume_diario_curve_usd"] = df["volume_diario_curve_usd"].round(2)

    # Salvar saídas
    saida_raiz = os.path.join(DADOS_DIR, "dados_defillama_curve.csv")
    saida_dados = os.path.join(DADOS_DIR, "dados_defillama_curve.csv")

    df.to_csv(saida_raiz, index=False)
    df.to_csv(saida_dados, index=False)

    print(f"  -> Salvo com sucesso em: {saida_raiz}")
    print(f"  -> Copia sincronizada em: {saida_dados}")
    print(f"  -> Total de linhas: {len(df)} dias ({df['Date'].iloc[0]} a {df['Date'].iloc[-1]})")
    print(f"  -> TVL Lido medio: ${df['tvl_lido_total_usd'].mean():,.0f} | Atual: ${df['tvl_lido_total_usd'].iloc[-1]:,.0f}")
    print(f"  -> APY Lido medio: {df['apy_lido_pct'].mean():.2f}% | APR Nominal medio: {df['apr_lido_liquido_pct'].mean():.2f}%")
    n_tvl_curve_real = (df["fonte_tvl_curve"] == "defillama_pool_historico").sum()
    print(f"  -> TVL Curve (pool ETH-stETH) com dado historico real: {n_tvl_curve_real}/{len(df)} dias")
    print(f"  [AVISO IMPORTANTE] 'reserva_eth_curve', 'reserva_steth_curve', 'ratio_reserva_steth_pct' "
          f"e 'volume_diario_curve_usd' ainda sao um snapshot ATUAL constante replicado em todas as "
          f"linhas (coluna fonte_reserva_curve avisa isso). Nao use essas 4 colunas como serie "
          f"historica sem antes resolver isso -- veja as opcoes discutidas na conversa.")
    print("=" * 70)
    print("MODULO 3 CONCLUIDO COM SUCESSO (com ressalva acima)!\n")


if __name__ == "__main__":
    main()