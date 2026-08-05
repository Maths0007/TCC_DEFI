# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "pandas",
# ]
# ///
"""
Script 03: Coleta de TVL da Lido, Staking Ratio e Market Share de Liquid Staking (LSD)
Fonte: DefiLlama Protocol API (gratuita, sem API key)
Saídas:
  1. scripts_e_dados/Dados/tvl_lido.csv
  2. scripts_e_dados/Dados/staking_ratio_eth.csv
  3. scripts_e_dados/Dados/market_share_lsd_snapshot.csv
  4. scripts_e_dados/Dados/market_share_lsd.csv
"""
import sys
import time
import pandas as pd
from datetime import datetime, timezone
from utils import (
    fetch_all_protocols,
    fetch_protocol_data,
    save_csv_and_log,
)

TOP_LS_PROTOCOLS = [
    "lido",
    "rocket-pool",
    "coinbase-wrapped-staked-eth",
    "binance-staked-eth",
    "frax-ether",
    "mantle-staked-eth",
    "stakewise",
    "stader",
    "swell",
    "diva-staking",
    "ankr",
]


def main():
    print("=" * 60)
    print("SCRIPT 03 -- Coleta: TVL Lido, Staking Ratio e Market Share LSD")
    print(f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Buscar lista global de protocolos
    print("\n[1/5] Buscando lista de protocolos de Liquid Staking...")
    try:
        all_protocols = fetch_all_protocols()
    except Exception as e:
        print(f"  [ERRO] Falha ao buscar lista de protocolos: {e}")
        sys.exit(1)

    ls_protocols = [
        p for p in all_protocols
        if p.get("category", "").lower() in ("liquid staking", "liquid restaking")
        and "Ethereum" in p.get("chains", [])
    ]
    ls_protocols.sort(key=lambda p: p.get("tvl", 0), reverse=True)
    total_ls_tvl_now = sum(p.get("tvl", 0) for p in ls_protocols)
    print(f"  [OK] {len(ls_protocols)} protocolos encontrados | TVL Total LSD: ${total_ls_tvl_now:,.0f}")

    # 2. Buscar detalhes históricos da Lido
    print("\n[2/5] Buscando dados históricos do protocolo Lido...")
    try:
        lido_data = fetch_protocol_data("lido")
    except Exception as e:
        print(f"  [ERRO] Falha ao buscar dados da Lido: {e}")
        sys.exit(1)

    # Processar e salvar tvl_lido.csv
    tvl_data = lido_data.get("tvl", [])
    chain_tvls = lido_data.get("chainTvls", {})
    eth_tvl = chain_tvls.get("Ethereum", {}).get("tvl", [])

    records_lido = []
    for entry in tvl_data:
        ts = entry.get("date", 0)
        tvl_usd = entry.get("totalLiquidityUSD", 0)
        records_lido.append({
            "data": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d"),
            "tvl_total_usd": tvl_usd,
        })

    df_tvl_lido = pd.DataFrame(records_lido)
    if eth_tvl:
        eth_records = {
            datetime.fromtimestamp(e.get("date", 0), tz=timezone.utc).strftime("%Y-%m-%d"): e.get("totalLiquidityUSD", 0)
            for e in eth_tvl
        }
        df_tvl_lido["tvl_ethereum_usd"] = df_tvl_lido["data"].map(eth_records)

    df_tvl_lido = df_tvl_lido.drop_duplicates(subset=["data"], keep="first").sort_values("data").reset_index(drop=True)

    save_csv_and_log(
        df_tvl_lido,
        "tvl_lido.csv",
        lambda df: print(
            f"  -> TVL mínimo Lido: ${df['tvl_total_usd'].min():,.0f} | "
            f"Máximo: ${df['tvl_total_usd'].max():,.0f} | "
            f"Atual: ${df['tvl_total_usd'].iloc[-1]:,.0f}"
        )
    )

    # 3. Estimar Staking Ratio
    print("\n[3/5] Calculando estimativa do Staking Ratio...")
    lido_tvl_now = lido_data.get("currentChainTvls", {}).get("Ethereum", 0)
    if lido_tvl_now == 0 and len(tvl_data) > 0:
        lido_tvl_now = tvl_data[-1].get("totalLiquidityUSD", 1)

    lido_share = lido_tvl_now / total_ls_tvl_now if total_ls_tvl_now > 0 else 0.7
    LS_SHARE_OF_TOTAL_STAKING = 0.35  # ~35% do staking total é via liquid staking

    staking_records = []
    eth_tvl_source = eth_tvl if eth_tvl else tvl_data
    for entry in eth_tvl_source:
        ts = entry.get("date", 0)
        lido_tvl_usd = entry.get("totalLiquidityUSD", 0)
        dt_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")

        est_total_ls_tvl = lido_tvl_usd / lido_share if lido_share > 0 else 0
        est_total_staking_tvl = est_total_ls_tvl / LS_SHARE_OF_TOTAL_STAKING

        staking_records.append({
            "data": dt_str,
            "lido_tvl_usd": lido_tvl_usd,
            "total_ls_tvl_usd_estimado": est_total_ls_tvl,
            "total_staking_tvl_usd_estimado": est_total_staking_tvl,
        })

    df_staking = pd.DataFrame(staking_records)
    df_staking = df_staking.drop_duplicates(subset=["data"], keep="first").sort_values("data").reset_index(drop=True)

    save_csv_and_log(df_staking, "staking_ratio_eth.csv")

    # 4. Gerar Snapshot de Market Share
    print("\n[4/5] Gerando Snapshot de Market Share dos Top Protocolos...")
    snapshot_records = []
    for p in ls_protocols[:20]:
        tvl = p.get("tvl", 0)
        share = (tvl / total_ls_tvl_now * 100) if total_ls_tvl_now > 0 else 0
        snapshot_records.append({
            "protocolo": p.get("name", ""),
            "slug": p.get("slug", ""),
            "categoria": p.get("category", ""),
            "tvl_usd": tvl,
            "market_share_pct": round(share, 2),
        })

    df_snapshot = pd.DataFrame(snapshot_records)
    save_csv_and_log(df_snapshot, "market_share_lsd_snapshot.csv")

    # 5. Série Histórica de Market Share dos Top Protocolos
    print("\n[5/5] Buscando histórico de TVL dos principais protocolos LSD...")
    all_history = {}
    for slug in TOP_LS_PROTOCOLS:
        print(f"  -> {slug}...", end=" ")
        try:
            p_data = fetch_protocol_data(slug)
            p_eth_tvl = p_data.get("chainTvls", {}).get("Ethereum", {}).get("tvl", [])
            if not p_eth_tvl:
                p_eth_tvl = p_data.get("tvl", [])

            if p_eth_tvl:
                print(f"[OK] {len(p_eth_tvl)} pontos")
                for entry in p_eth_tvl:
                    dt_str = datetime.fromtimestamp(entry.get("date", 0), tz=timezone.utc).strftime("%Y-%m-%d")
                    if dt_str not in all_history:
                        all_history[dt_str] = {}
                    all_history[dt_str][slug] = entry.get("totalLiquidityUSD", 0)
            else:
                print("[AVISO] sem dados")
        except Exception:
            print("[ERRO] falha na requisição")
        time.sleep(0.5)

    dates = sorted(all_history.keys())
    hist_records = []
    for date in dates:
        row = {"data": date}
        for slug in TOP_LS_PROTOCOLS:
            col_name = f"tvl_{slug.replace('-', '_')}"
            row[col_name] = all_history[date].get(slug, None)
        hist_records.append(row)

    df_hist = pd.DataFrame(hist_records).sort_values("data").reset_index(drop=True)
    tvl_cols = [c for c in df_hist.columns if c.startswith("tvl_")]
    df_hist["total_top_tvl"] = df_hist[tvl_cols].sum(axis=1)
    if "tvl_lido" in df_hist.columns:
        df_hist["lido_share_pct"] = (df_hist["tvl_lido"] / df_hist["total_top_tvl"] * 100).round(2)

    save_csv_and_log(
        df_hist,
        "market_share_lsd.csv",
        lambda df: print(
            f"  -> Market Share Lido atual: {df['lido_share_pct'].dropna().iloc[-1]:.1f}%"
            if "lido_share_pct" in df.columns and len(df["lido_share_pct"].dropna()) > 0 else ""
        )
    )

    print("\n[OK] Script 03 concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
