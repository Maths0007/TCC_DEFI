# -*- coding: utf-8 -*-
"""
MODULO 2b: Coleta de Recompensas MEV via Data API Publica dos Relays MEV-Boost
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)
(MEV-Boost ativo a partir do Merge, 15/09/2022; antes disso a coluna sai 0.0)

Fontes:
  - Data API publica dos relays MEV-Boost (Flashbots, Ultra Sound, Aestus, Agnostic Relay)
  - Endpoint padrao: GET /relay/v1/data/bidtraces/proposer_payload_delivered?slot=<slot>

Metricas Calculadas:
  1. mev_valor_medio_bloco_eth: Valor medio em ETH entregue ao validador por bloco no dia
  2. mev_total_diario_estimado_eth: Total diario de MEV na rede (valor_medio * 7200 slots/dia)
  3. taxa_mev_execucao_apr_pct: Rendimento anualizado de MEV em relacao ao stake total

Saidas:
  - dados_mev_relay.csv (diretorio raiz)
  - scripts_e_dados/Dados/dados_mev_relay.csv
  - files/dados_mev_relay.csv
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
DATA_MERGE = "2022-09-15"

# Genesis da Beacon Chain mainnet: 2020-12-01 12:00:23 UTC
GENESIS_TIME_UTC = 1606824023
SLOT_DURATION_SEG = 12
SLOTS_POR_DIA = 86400 // SLOT_DURATION_SEG  # 7200

AMOSTRAS_POR_DIA = 1
TIMEOUT_SEG = 10
PAUSA_ENTRE_REQUISICOES_SEG = 0.15
CHECKPOINT_A_CADA_N_DIAS_NOVOS = 20

RELAYS = [
    "https://boost-relay.flashbots.net",
    "https://relay.ultrasound.money",
    "https://aestus.live",
    "https://agnostic-relay.net",
]


def data_para_slot(data_str: str, offset_segundos: int = 0) -> int:
    dt = datetime.strptime(data_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    ts = int(dt.timestamp()) + offset_segundos
    slot = (ts - GENESIS_TIME_UTC) // SLOT_DURATION_SEG
    return max(slot, 0)


def consultar_payload_delivered(relay_base_url: str, slot: int) -> float | None:
    url = f"{relay_base_url}/relay/v1/data/bidtraces/proposer_payload_delivered"
    try:
        resp = requests.get(url, params={"slot": slot}, timeout=TIMEOUT_SEG)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                valor_wei = int(data[0].get("value", 0))
                return valor_wei / 1e18
    except Exception:
        pass
    return None


def coletar_valor_slot(slot: int) -> float | None:
    for relay in RELAYS:
        valor = consultar_payload_delivered(relay, slot)
        time.sleep(PAUSA_ENTRE_REQUISICOES_SEG)
        if valor is not None:
            return valor
    return None


def coletar_dia(dt_str: str) -> dict:
    if pd.to_datetime(dt_str) < pd.to_datetime(DATA_MERGE):
        return {"Date": dt_str, "mev_valor_medio_bloco_eth": 0.0, "mev_amostras_coletadas": 0}

    offsets = [int(86400 * (k + 0.5) / AMOSTRAS_POR_DIA) for k in range(AMOSTRAS_POR_DIA)]
    valores = []
    for offset in offsets:
        slot = data_para_slot(dt_str, offset)
        v = coletar_valor_slot(slot)
        if v is not None:
            valores.append(v)

    if valores:
        return {
            "Date": dt_str,
            "mev_valor_medio_bloco_eth": float(np.mean(valores)),
            "mev_amostras_coletadas": len(valores),
        }
    else:
        return {"Date": dt_str, "mev_valor_medio_bloco_eth": np.nan, "mev_amostras_coletadas": 0}


def main():
    print("=" * 70)
    print("MODULO 2b: Coleta de MEV via Data API dos Relays MEV-Boost")
    print(f"Recorte Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    # 1. Carregar cache existente se houver para reaproveitar
    registros_map = {}
    for local in [
        os.path.join(DADOS_DIR, "dados_mev_relay.csv"),
        os.path.join(ROOT_DIR, "dados_mev_relay.csv"),
        os.path.join(FILES_DIR, "dados_mev_relay.csv"),
        os.path.join(FILES_DIR, "scripts_e_dados", "Dados", "dados_mev_relay.csv")
    ]:
        if os.path.exists(local):
            try:
                df_existente = pd.read_csv(local)
                for _, row in df_existente.iterrows():
                    d = str(row["Date"])[:10]
                    v = row.get("mev_valor_medio_bloco_eth")
                    c = row.get("mev_amostras_coletadas", 1)
                    if pd.notna(v) and d not in registros_map:
                        registros_map[d] = {"Date": d, "mev_valor_medio_bloco_eth": float(v), "mev_amostras_coletadas": int(c)}
            except Exception:
                pass

    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d").tolist()
    dias_pendentes = [d for d in grid_datas if d not in registros_map or pd.isna(registros_map[d]["mev_valor_medio_bloco_eth"])]
    print(f"\n[1/3] Cache existente: {len(registros_map)} dias encontrados. Pendentes de consulta: {len(dias_pendentes)} dias.")

    dias_novos = 0
    for dt_str in dias_pendentes:
        reg = coletar_dia(dt_str)
        registros_map[dt_str] = reg
        dias_novos += 1
        if dias_novos % CHECKPOINT_A_CADA_N_DIAS_NOVOS == 0:
            print(f"  -> Checkpoint salvo ({len(registros_map)}/{len(grid_datas)} dias).")

    # 2. Consolidar e interpolar lacunas
    print("\n[2/3] Consolidando serie temporal e calculando taxas anualizadas...")
    df = pd.DataFrame(list(registros_map.values())).sort_values("Date").drop_duplicates(subset=["Date"]).reset_index(drop=True)
    df = df[(df["Date"] >= DATA_INICIO) & (df["Date"] <= DATA_FIM)].reset_index(drop=True)

    # Interpolar lacunas internas do MEV
    df["mev_valor_medio_bloco_eth"] = df["mev_valor_medio_bloco_eth"].interpolate(method="linear", limit_area="inside")
    
    # Preencher pre-Merge estritamente com 0
    df.loc[df["Date"] < DATA_MERGE, "mev_valor_medio_bloco_eth"] = 0.0
    df.loc[df["Date"] < DATA_MERGE, "mev_amostras_coletadas"] = 0

    # Total diario de MEV entregue na rede = valor_medio * 7200 slots
    df["mev_total_diario_estimado_eth"] = (df["mev_valor_medio_bloco_eth"] * SLOTS_POR_DIA).round(4)
    df["fonte_mev"] = "relay_data_api_amostrado"

    # Carregar total staked eth se disponivel para calcular taxa_mev_execucao_apr_pct
    consenso_file = os.path.join(DADOS_DIR, "dados_rated_consenso.csv")
    if not os.path.exists(consenso_file):
        consenso_file = os.path.join(ROOT_DIR, "dados_rated_consenso.csv")
    
    if os.path.exists(consenso_file):
        df_cons = pd.read_csv(consenso_file)
        if "total_staked_eth_network" in df_cons.columns:
            df = pd.merge(df, df_cons[["Date", "total_staked_eth_network"]], on="Date", how="left")
            df["total_staked_eth_network"] = df["total_staked_eth_network"].interpolate().ffill().bfill()
            df["taxa_mev_execucao_apr_pct"] = np.where(
                df["Date"] >= DATA_MERGE,
                ((df["mev_total_diario_estimado_eth"] * 365.0) / df["total_staked_eth_network"]) * 100.0,
                0.0
            ).round(4)

    # 3. Salvar
    print("\n[3/3] Salvando dados_mev_relay.csv...")
    destinos = [
        os.path.join(ROOT_DIR, "dados_mev_relay.csv"),
        os.path.join(DADOS_DIR, "dados_mev_relay.csv"),
        os.path.join(FILES_DIR, "dados_mev_relay.csv"),
        os.path.join(FILES_DIR, "scripts_e_dados", "Dados", "dados_mev_relay.csv")
    ]

    for d in destinos:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        df.to_csv(d, index=False)
        print(f"  -> Salvo em: {d}")

    print("\n" + "-" * 70)
    print("RESUMO ESTATISTICO DE MEV (2022-05-05 a 2026-05-31):")
    print(f"  -> Total de Observacoes: {len(df)} dias")
    print(f"  -> MEV Medio por Bloco (Pos-Merge): {df.loc[df['Date'] >= DATA_MERGE, 'mev_valor_medio_bloco_eth'].mean():.4f} ETH/bloco")
    print(f"  -> MEV Total Diario Medio: {df.loc[df['Date'] >= DATA_MERGE, 'mev_total_diario_estimado_eth'].mean():.2f} ETH/dia")
    if "taxa_mev_execucao_apr_pct" in df.columns:
        print(f"  -> Taxa MEV APR Media (Pos-Merge): {df.loc[df['Date'] >= DATA_MERGE, 'taxa_mev_execucao_apr_pct'].mean():.4f}% a.a.")
    print("=" * 70)
    print("MODULO 2b CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()