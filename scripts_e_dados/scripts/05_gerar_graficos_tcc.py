# -*- coding: utf-8 -*-
"""
MODULO 5: Geracao de Figuras Academicas em Alta Resolucao (300 DPI)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)

Graficos Produzidos:
  1. grafico_01_paridade_depeg_2022_2026.png:
     - Evolucao da Paridade stETH/ETH e Depeg % com marcacoes nos marcos historicos:
       * Crash Terra/Luna (Maio de 2022)
       * The Merge (Setembro de 2022)
       * Hard Fork Shapella (Abril de 2023)
  2. grafico_02_comparativo_apr_retornos.png:
     - Curva Comparativa de Retornos: APR do Staking Direto (via formula 16632.32/sqrt(S) + MEV)
       vs. APR Liquido do stETH (Lido DAO) com area de spread (Delta APR).

Saidas:
  - scripts_e_dados/Graficos/grafico_01_paridade_depeg_2022_2026.png
  - scripts_e_dados/Graficos/grafico_02_comparativo_apr_retornos.png
  - Copias na raiz e na pasta files/
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

matplotlib.use("Agg")

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "semibold",
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.titlesize": 14,
    "figure.titleweight": "bold",
    "axes.edgecolor": "#b0bec5",
    "axes.linewidth": 1.0,
    "grid.color": "#e0e0e0",
    "grid.linestyle": "--",
    "grid.alpha": 0.75,
})

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Dados")
GRAFICOS_DIR = os.path.join(ROOT_DIR, "scripts_e_dados", "Graficos")
FILES_DIR = os.path.join(ROOT_DIR, "files")
os.makedirs(GRAFICOS_DIR, exist_ok=True)
os.makedirs(FILES_DIR, exist_ok=True)

# RECORTE TEMPORAL ATUALIZADO
DATA_INICIO = "2022-05-05"
DATA_FIM = "2026-05-31"


def carregar_dataset_master() -> pd.DataFrame:
    for local in [
        os.path.join(ROOT_DIR, "dataset_master_tcc_2022_2026.csv"),
        os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv"),
        os.path.join(FILES_DIR, "dataset_master_tcc_2022_2026.csv")
    ]:
        if os.path.exists(local):
            df = pd.read_csv(local)
            df["Date_dt"] = pd.to_datetime(df["Date"])
            df = df[(df["Date_dt"] >= pd.to_datetime(DATA_INICIO)) & (df["Date_dt"] <= pd.to_datetime(DATA_FIM))]
            df = df.sort_values("Date_dt").reset_index(drop=True)
            return df

    print(f"  [ERRO] Dataset master nao encontrado. Execute 04_consolidar_dataset.py primeiro!")
    sys.exit(1)


def salvar_grafico(fig, nome_arquivo: str):
    destinos = [os.path.join(DADOS_DIR, "destinos = [
        os.path.join(GRAFICOS_DIR, nome_arquivo),
        os.path.join(ROOT_DIR, nome_arquivo),
        os.path.join(FILES_DIR, nome_arquivo),
        os.path.join(FILES_DIR, "scripts_e_dados", "Graficos", nome_arquivo)
    ]")]

    for d in destinos:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        fig.savefig(d, dpi=300, bbox_inches="tight")
        print(f"  [OK] 300 DPI salvo em: {d}")

    plt.close(fig)


def gerar_grafico_01_paridade_depeg(df: pd.DataFrame):
    print("\n[1/2] Renderizando Grafico 1: Evolucao da Paridade stETH/ETH e Depeg %...")

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.2], "hspace": 0.08}
    )

    # Subplot 1: Razao de Precos stETH / ETH
    ax1.plot(df["Date_dt"], df["preco_steth_eth"], color="#0284c7", linewidth=1.6, label="Taxa de Cambio stETH/ETH", zorder=3)
    ax1.axhline(1.0, color="#dc2626", linestyle="--", linewidth=1.3, label="Paridade Teorica (1.0000 ETH)", zorder=2)
    ax1.fill_between(df["Date_dt"], df["preco_steth_eth"], 1.0, where=(df["preco_steth_eth"] < 1.0),
                     color="#ef4444", alpha=0.15, label="Desconto de Liquidez (Depeg)", zorder=1)

    # Subplot 2: Depeg % (Liquid Staking Basis)
    ax2.plot(df["Date_dt"], df["depeg_pct"], color="#b91c1c", linewidth=1.3, label="Depeg % (Basis)", zorder=3)
    ax2.axhline(0.0, color="#64748b", linestyle="-", linewidth=1.0, alpha=0.8, zorder=2)
    ax2.axhline(-2.0, color="#f59e0b", linestyle=":", linewidth=1.1, label="Limite Critico (-2.0%)", zorder=2)
    ax2.axhline(-5.0, color="#dc2626", linestyle=":", linewidth=1.1, label="Stress Severo (-5.0%)", zorder=2)
    ax2.fill_between(df["Date_dt"], df["depeg_pct"], 0.0, where=(df["depeg_pct"] < 0.0),
                     color="#f87171", alpha=0.2, zorder=1)

    # Eventos Historicos Estruturais
    eventos = [
        {
            "data": pd.to_datetime("2022-05-12"),
            "nome": "Crash Terra/Luna\n(Mai/2022)",
            "cor": "#dc2626",
            "y1": 0.935,
        },
        {
            "data": pd.to_datetime("2022-09-15"),
            "nome": "The Merge\n(Set/2022)",
            "cor": "#059669",
            "y1": 0.985,
        },
        {
            "data": pd.to_datetime("2023-04-12"),
            "nome": "Upgrade Shapella\n(Abr/2023)",
            "cor": "#2563eb",
            "y1": 0.998,
        },
    ]

    for ev in eventos:
        dt = ev["data"]
        if df["Date_dt"].min() <= dt <= df["Date_dt"].max():
            ax1.axvline(dt, color=ev["cor"], linestyle="-.", linewidth=1.3, alpha=0.85, zorder=4)
            ax2.axvline(dt, color=ev["cor"], linestyle="-.", linewidth=1.3, alpha=0.85, zorder=4)

            ax1.annotate(
                ev["nome"],
                xy=(dt, ev["y1"]),
                xytext=(0, 26),
                textcoords="offset points",
                ha="center",
                fontsize=8.5,
                fontweight="bold",
                color=ev["cor"],
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec=ev["cor"], lw=1.2, alpha=0.9),
                arrowprops=dict(arrowstyle="->", color=ev["cor"], lw=1.2)
            )

    # Limites dinamicos
    min_ratio = df["preco_steth_eth"].min()
    max_ratio = df["preco_steth_eth"].max()
    ax1.set_ylim(min(min_ratio * 0.985, 0.925), max(max_ratio * 1.015, 1.015))

    min_depeg = df["depeg_pct"].min()
    max_depeg = df["depeg_pct"].max()
    ax2.set_ylim(min(min_depeg * 1.15, -7.5), max(max_depeg * 1.2, 1.5))

    ax1.set_title("Evolucao da Paridade de Mercado stETH/ETH e Depeg Historico (2022-2026)", pad=14, fontsize=13)
    ax1.set_ylabel("Preco Relativo (stETH / ETH)")
    ax1.legend(loc="lower right", framealpha=0.92, facecolor="#ffffff")

    ax2.set_ylabel("Depeg / Basis (%)")
    ax2.set_xlabel("Data (UTC)")
    ax2.legend(loc="lower right", framealpha=0.92, facecolor="#ffffff")

    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    fig.autofmt_xdate(rotation=35, ha="right")

    salvar_grafico(fig, "grafico_01_paridade_depeg_2022_2026.png")


def gerar_grafico_02_comparativo_apr(df: pd.DataFrame):
    print("\n[2/2] Renderizando Grafico 2: Curva Comparativa de Retornos (APR Direto vs. Liquido stETH)...")

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.1], "hspace": 0.08}
    )

    # Subplot 1: Curvas de APR
    ax1.plot(df["Date_dt"], df["apr_rede_direto_total_pct"], color="#059669", linewidth=1.8,
             label=r"APR Staking Direto da Rede ($\frac{16.632,32}{\sqrt{S}} + \mathrm{MEV}$)", zorder=3)
    ax1.plot(df["Date_dt"], df["apr_lido_liquido_pct"], color="#0284c7", linewidth=1.8,
             label="APR Liquido stETH (Lido DAO)", zorder=3)

    # Area sombreada de spread
    ax1.fill_between(
        df["Date_dt"],
        df["apr_lido_liquido_pct"],
        df["apr_rede_direto_total_pct"],
        where=(df["apr_rede_direto_total_pct"] >= df["apr_lido_liquido_pct"]),
        color="#fbbf24", alpha=0.35, label="Comissao Lido DAO (Spread / Delta APR)", zorder=2
    )

    # Subplot 2: Delta APR
    ax2.plot(df["Date_dt"], df["delta_apr_pct"], color="#d97706", linewidth=1.4,
             label=r"$\Delta\mathrm{APR}_t = \mathrm{APR}_{\mathrm{Direto}} - \mathrm{APR}_{\mathrm{Lido}}$", zorder=3)
    media_delta = df["delta_apr_pct"].mean()
    ax2.axhline(media_delta, color="#b45309", linestyle="--", linewidth=1.2,
                label=f"Media Historica ({media_delta:.2f}%)", zorder=2)

    # Marcadores de Eventos
    eventos = [
        (pd.to_datetime("2022-09-15"), "The Merge", "#059669"),
        (pd.to_datetime("2023-04-12"), "Shapella", "#2563eb"),
    ]
    for dt, label_txt, cor in eventos:
        if df["Date_dt"].min() <= dt <= df["Date_dt"].max():
            ax1.axvline(dt, color=cor, linestyle=":", linewidth=1.2, alpha=0.8)
            ax2.axvline(dt, color=cor, linestyle=":", linewidth=1.2, alpha=0.8)
            ax1.text(
                dt, ax1.get_ylim()[1] * 0.90 if ax1.get_ylim()[1] > 0 else 5.0, f" {label_txt}",
                fontsize=8.5, fontweight="bold", color=cor, rotation=90, va="top"
            )

    # Limites dinamicos
    min_apr = min(df["apr_lido_liquido_pct"].min(), df["apr_rede_direto_total_pct"].min())
    max_apr = max(df["apr_lido_liquido_pct"].max(), df["apr_rede_direto_total_pct"].max())
    ax1.set_ylim(bottom=max(1.0, min_apr * 0.85), top=max_apr * 1.15)

    max_delta = df["delta_apr_pct"].max()
    ax2.set_ylim(bottom=0.0, top=max(max_delta * 1.25, 0.7))

    ax1.set_title("Curva Comparativa de Retornos: Staking Direto vs. Liquid Staking Lido DAO (2022-2026)", pad=14, fontsize=13)
    ax1.set_ylabel("Rendimento Anualizado Nominal (APR %)")
    ax1.legend(loc="upper right", framealpha=0.92, facecolor="#ffffff")

    ax2.set_ylabel(r"$\Delta\mathrm{APR}$ (%)")
    ax2.set_xlabel("Data (UTC)")
    ax2.legend(loc="upper right", framealpha=0.92, facecolor="#ffffff")

    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    fig.autofmt_xdate(rotation=35, ha="right")

    salvar_grafico(fig, "grafico_02_comparativo_apr_retornos.png")


def main():
    print("=" * 70)
    print("MODULO 5: Geracao de Figuras Academicas em Alta Resolucao (300 DPI)")
    print(f"Recorte Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    df_master = carregar_dataset_master()
    print(f"Dataset carregado com {len(df_master)} observacoes diarias ({df_master['Date'].iloc[0]} a {df_master['Date'].iloc[-1]}).")

    gerar_grafico_01_paridade_depeg(df_master)
    gerar_grafico_02_comparativo_apr(df_master)

    print("\n" + "=" * 70)
    print("MODULO 5 CONCLUIDO COM SUCESSO! FIGURAS 300 DPI GERADAS.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()