# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "pandas",
# ]
# ///
"""
Script 02: Coleta de APR histórica do Lido (stETH) e Staking Direto do Ethereum
Fonte: DefiLlama Yields API (gratuita, sem API key)
Saídas:
  1. scripts_e_dados/Dados/apr_lido_historico.csv
  2. scripts_e_dados/Dados/apr_staking_direto_eth.csv
"""
import os
import sys
import pandas as pd
from datetime import datetime
from utils import (
    OUTPUT_DIR,
    fetch_yield_pools,
    fetch_yield_pool_history,
    save_csv_and_log,
)

LIDO_FEE = 0.10  # 10% de comissão da Lido (5% operadores + 5% tesouraria DAO)


def find_lido_pool(pools: list[dict]) -> str | None:
    """Encontra o UUID do pool Lido stETH no DefiLlama Yields."""
    candidates = []
    for pool in pools:
        project = pool.get("project", "").lower()
        symbol = pool.get("symbol", "").upper()
        chain = pool.get("chain", "").lower()
        if "lido" in project and chain == "ethereum" and "STETH" in symbol:
            candidates.append(pool)

    if not candidates:
        for pool in pools:
            project = pool.get("project", "").lower()
            chain = pool.get("chain", "").lower()
            if "lido" in project and chain == "ethereum":
                candidates.append(pool)

    if candidates:
        candidates.sort(key=lambda p: p.get("tvlUsd", 0), reverse=True)
        best = candidates[0]
        print(f"  [OK] Pool Lido encontrado: {best.get('symbol')} | "
              f"TVL: ${best.get('tvlUsd', 0):,.0f} | "
              f"APY atual: {best.get('apy', 0):.2f}%")
        return best["pool"]

    return None


def main():
    print("=" * 60)
    print("SCRIPT 02 -- Coleta: APR Lido (stETH) e Staking Direto")
    print(f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Buscar lista de pools e identificar Lido stETH
    print("\n[1/3] Buscando pools na DefiLlama Yields API...")
    try:
        pools = fetch_yield_pools()
        pool_uuid = find_lido_pool(pools)
        if not pool_uuid:
            print("  [ERRO] Pool Lido stETH não encontrado!")
            sys.exit(1)
    except Exception as e:
        print(f"  [ERRO] Erro ao buscar pools: {e}")
        sys.exit(1)

    # 2. Buscar histórico do pool Lido
    print(f"\n[2/3] Buscando histórico de APY da Lido (pool: {pool_uuid})...")
    try:
        history = fetch_yield_pool_history(pool_uuid)
        print(f"  [OK] {len(history)} pontos de dados obtidos")
    except Exception as e:
        print(f"  [ERRO] Falha ao buscar histórico do pool: {e}")
        sys.exit(1)

    # Construir DataFrame Lido APR
    records = []
    for entry in history:
        records.append({
            "data": entry.get("timestamp", "")[:10],
            "apy_pct": entry.get("apy", None),
            "tvl_usd": entry.get("tvlUsd", None),
            "il7d": entry.get("il7d", None),
            "apy_base": entry.get("apyBase", None),
            "apy_reward": entry.get("apyReward", None),
        })

    df_lido = pd.DataFrame(records)

    # Integrar dados suplementares do Dune Analytics se disponível
    dune_csv = os.path.join(OUTPUT_DIR, "apr_lido_dune.csv")
    if os.path.exists(dune_csv):
        print(f"  -> Integrando dados históricos do Dune Analytics: {dune_csv}")
        try:
            df_dune = pd.read_csv(dune_csv)
            if "data" in df_dune.columns and "apy_pct" in df_dune.columns:
                df_lido = pd.concat([df_dune, df_lido], ignore_index=True)
                print(f"  [OK] Dados do Dune integrados com sucesso")
        except Exception as e:
            print(f"  [AVISO] Não foi possível ler {dune_csv}: {e}")

    df_lido = df_lido.drop_duplicates(subset=["data"], keep="first").sort_values("data").reset_index(drop=True)
    df_lido = df_lido.dropna(subset=["apy_pct"])

    save_csv_and_log(
        df_lido,
        "apr_lido_historico.csv",
        lambda df: print(
            f"  -> APY mínimo: {df['apy_pct'].min():.2f}% | "
            f"Máximo: {df['apy_pct'].max():.2f}% | "
            f"Médio: {df['apy_pct'].mean():.2f}%"
        )
    )

    # 3. Derivar APR de Staking Direto
    print("\n[3/3] Derivando APR de Staking Direto (comissão Lido de 10%)...")
    df_direto = pd.DataFrame()
    df_direto["data"] = df_lido["data"].values
    df_direto["apr_lido_pct"] = df_lido["apy_pct"].values
    df_direto["apr_direto_estimado_pct"] = df_direto["apr_lido_pct"] / (1 - LIDO_FEE)
    df_direto["spread_pct"] = df_direto["apr_direto_estimado_pct"] - df_direto["apr_lido_pct"]
    df_direto["fonte"] = "derivado_lido"

    save_csv_and_log(
        df_direto,
        "apr_staking_direto_eth.csv",
        lambda df: print(
            f"  -> APR Direto mínimo: {df['apr_direto_estimado_pct'].min():.2f}% | "
            f"Máximo: {df['apr_direto_estimado_pct'].max():.2f}% | "
            f"Médio: {df['apr_direto_estimado_pct'].mean():.2f}%\n"
            f"  -> Spread médio (custo Lido): {df['spread_pct'].mean():.3f}%"
        )
    )

    print("\n[OK] Script 02 concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
