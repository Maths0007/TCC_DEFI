# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "numpy",
#     "matplotlib",
#     "seaborn",
#     "scipy",
# ]
# ///
"""
Script 05: Geração de Gráficos Acadêmicos para o TCC (Recorte: Maio/2022 a Abril/2026, 300 DPI)
Processa os dados de scripts_e_dados/Dados e salva todas as figuras na pasta scripts_e_dados/Graficos/
"""
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

matplotlib.use("Agg")
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 14,
    "axes.edgecolor": "#cccccc",
    "axes.linewidth": 0.8,
    "grid.color": "#e6e6e6",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Dados")
GRAFICOS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Graficos")

# Recorte Temporal de Análise Solicitado (Maio/2022 a Abril/2026)
DATA_INICIO = pd.to_datetime("2022-05-01")
DATA_FIM = pd.to_datetime("2026-04-30")


def carregar_dados():
    """Carrega datasets da pasta Dados filtrados para Maio/2022 a Abril/2026."""
    dados = {}
    arquivos = {
        "depeg": "depeg_steth_eth.csv",
        "preco_eth": "preco_eth_usd.csv",
        "apr_lido": "apr_lido_historico.csv",
        "apr_direto": "apr_staking_direto_eth.csv",
        "tvl_lido": "tvl_lido.csv",
        "staking_ratio": "staking_ratio_eth.csv",
        "market_share_hist": "market_share_lsd.csv",
        "market_share_snap": "market_share_lsd_snapshot.csv",
    }
    for chave, filename in arquivos.items():
        caminho = os.path.join(DADOS_DIR, filename)
        if os.path.exists(caminho):
            df = pd.read_csv(caminho)
            if "data" in df.columns:
                df["data"] = pd.to_datetime(df["data"])
                df = df[(df["data"] >= DATA_INICIO) & (df["data"] <= DATA_FIM)].reset_index(drop=True)
            dados[chave] = df
    return dados


def salvar_figura(fig, filename):
    """Salva figura em PNG de 300 DPI."""
    os.makedirs(GRAFICOS_DIR, exist_ok=True)
    caminho = os.path.join(GRAFICOS_DIR, filename)
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Gráfico salvo: {caminho}")


def fig01_depeg_historico(df_depeg):
    """Figura 1: Evolução Histórica da Paridade stETH/ETH e Depeg % (Maio/2022 - Abril/2026)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1.2]})

    ax1.plot(df_depeg["data"], df_depeg["preco_steth_eth"], color="#1f77b4", linewidth=1.2, label="Razão stETH/ETH")
    ax1.axhline(1.0, color="#d62728", linestyle="--", linewidth=1.2, label="Paridade 1:1 (ETH)")

    eventos = [
        (pd.to_datetime("2022-05-12"), 0.93, "Crash Terra/LUNA", "#d62728"),
        (pd.to_datetime("2022-11-09"), 0.98, "Falência FTX", "#ff7f0e"),
        (pd.to_datetime("2023-04-12"), 1.00, "Shanghai Upgrade", "#2ca02c"),
        (pd.to_datetime("2026-04-18"), 0.99, "Hack KelpDAO", "#9467bd"),
    ]
    for dt, y_pos, texto, cor in eventos:
        if df_depeg["data"].min() <= dt <= df_depeg["data"].max():
            ax1.axvline(dt, color=cor, linestyle=":", alpha=0.7, linewidth=1.2)
            ax1.annotate(texto, xy=(dt, y_pos), xytext=(dt + pd.Timedelta(days=20), y_pos - 0.03),
                         arrowprops=dict(arrowstyle="->", color=cor, lw=0.9), fontsize=8, color=cor, fontweight="bold",
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=cor, alpha=0.8))

    ax1.set_ylabel("Preço stETH em ETH")
    ax1.set_title("Figura 1: Série Histórica da Paridade stETH/ETH e Eventos de Estresse (Maio/2022 – Abril/2026)", fontweight="bold", pad=12)
    ax1.legend(loc="lower right", frameon=True)
    ax1.set_ylim(0.85, 1.08)

    ax2.plot(df_depeg["data"], df_depeg["depeg_pct"], color="#9467bd", linewidth=1.0, label="Depeg (%)")
    ax2.axhline(0, color="black", linestyle="-", linewidth=0.8)
    ax2.axhline(-2.0, color="#ff7f0e", linestyle=":", linewidth=1.0, label="Limiar de Alerta (-2%)")
    ax2.axhline(-5.0, color="#d62728", linestyle="--", linewidth=1.0, label="Depeg Severo (-5%)")
    ax2.fill_between(df_depeg["data"], df_depeg["depeg_pct"], 0, where=(df_depeg["depeg_pct"] < 0), color="#d62728", alpha=0.2)
    ax2.fill_between(df_depeg["data"], df_depeg["depeg_pct"], 0, where=(df_depeg["depeg_pct"] >= 0), color="#2ca02c", alpha=0.2)

    ax2.set_ylabel("Depeg (%)")
    ax2.set_xlabel("Data")
    ax2.legend(loc="lower right", frameon=True)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=4))

    plt.tight_layout()
    salvar_figura(fig, "fig01_depeg_historico_steth.png")


def fig02_depeg_pre_pos_shanghai(df_depeg):
    """Figura 2: Análise Comparativa Pré vs Pós-Shanghai Upgrade (12/04/2023)."""
    data_shanghai = pd.to_datetime("2023-04-12")
    df_depeg["periodo"] = np.where(df_depeg["data"] <= data_shanghai, "Pré-Shanghai\n(Sem Saques)", "Pós-Shanghai\n(Com Saques)")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [2, 1]})

    pre = df_depeg[df_depeg["data"] <= data_shanghai]
    pos = df_depeg[df_depeg["data"] > data_shanghai]

    ax1.plot(pre["data"], pre["depeg_pct"], color="#d62728", linewidth=1.0, label="Pré-Shanghai (Volatilidade Alta)")
    ax1.plot(pos["data"], pos["depeg_pct"], color="#2ca02c", linewidth=1.0, label="Pós-Shanghai (Estabilizado)")
    ax1.axvline(data_shanghai, color="black", linestyle="--", linewidth=1.5, label="Shanghai (12/04/2023)")
    ax1.axhline(0, color="gray", linestyle=":", linewidth=0.8)

    ax1.set_ylabel("Depeg (%)")
    ax1.set_xlabel("Data")
    ax1.set_title("A. Evolução Temporal do Depeg (%) Pré e Pós-Shanghai", fontweight="bold")
    ax1.legend(loc="lower right", frameon=True)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))

    sns.boxplot(x="periodo", y="depeg_pct", data=df_depeg, ax=ax2, hue="periodo", palette=["#ff9999", "#99ff99"], width=0.4, fliersize=2, legend=False)
    ax2.axhline(0, color="gray", linestyle=":", linewidth=0.8)
    ax2.set_ylabel("Depeg (%)")
    ax2.set_xlabel("")
    ax2.set_title("B. Distribuição de Volatilidade", fontweight="bold")

    fig.suptitle("Figura 2: Impacto da Habilitação de Saques Nativos (Shanghai/Capella) sobre a Estabilidade do Peg", fontweight="bold", y=1.02)
    plt.tight_layout()
    salvar_figura(fig, "fig02_depeg_pre_pos_shanghai.png")


def fig03_histograma_distribuicao(df_depeg):
    """Figura 3: Histograma e Densidade KDE da Distribuição do Depeg (%) no Recorte."""
    fig, ax = plt.subplots(figsize=(9, 5))
    depeg = df_depeg["depeg_pct"].dropna()

    sns.histplot(depeg, kde=True, ax=ax, color="#1f77b4", bins=60, stat="density", alpha=0.4, edgecolor="white")

    media = depeg.mean()
    mediana = depeg.median()
    p1 = np.percentile(depeg, 1)

    ax.axvline(media, color="#d62728", linestyle="--", linewidth=1.2, label=f"Média: {media:.2f}%")
    ax.axvline(mediana, color="#2ca02c", linestyle="-", linewidth=1.2, label=f"Mediana: {mediana:.2f}%")
    ax.axvline(p1, color="#ff7f0e", linestyle=":", linewidth=1.2, label=f"Percentil 1% (Worst): {p1:.2f}%")

    ax.set_xlabel("Depeg (%)")
    ax.set_ylabel("Densidade de Frequência")
    ax.set_title("Figura 3: Distribuição Empírica do Depeg stETH/ETH (Maio/2022 – Abril/2026)", fontweight="bold", pad=12)
    ax.set_xlim(-15, 5)
    ax.legend(loc="upper left", frameon=True)

    ax.annotate("Cauda longa de liquidação em momentos de estresse\n(Crash Terra/LUNA depeg < -10%)",
                xy=(-10, 0.05), xytext=(-14, 0.15),
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1),
                fontsize=8, color="#d62728", bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff0f0", edgecolor="#d62728"))

    plt.tight_layout()
    salvar_figura(fig, "fig03_histograma_distribuicao_depeg.png")


def fig04_rendimento_apr(df_apr_lido, df_apr_direto):
    """Figura 4: Comparativo de Rendimentos (Lido APR vs. Solo Staking APR Direto)."""
    fig, ax = plt.subplots(figsize=(10, 5))

    if df_apr_direto is not None and "apr_direto_estimado_pct" in df_apr_direto.columns:
        merged = pd.merge(df_apr_lido[["data", "apy_pct"]], df_apr_direto[["data", "apr_direto_estimado_pct"]], on="data").dropna()
        ax.plot(merged["data"], merged["apr_direto_estimado_pct"], color="#1f77b4", linewidth=1.5, label="Solo Staking Direto (Bruto Estimado)")
        ax.plot(merged["data"], merged["apy_pct"], color="#2ca02c", linewidth=1.5, label="Lido stETH (Líquido pós-taxa de 10%)")
        ax.fill_between(merged["data"], merged["apy_pct"], merged["apr_direto_estimado_pct"], color="#ff7f0e", alpha=0.3, label="Spread da Comissão Lido DAO (10%)")
    else:
        ax.plot(df_apr_lido["data"], df_apr_lido["apy_pct"], color="#2ca02c", linewidth=1.5, label="Lido stETH APY (%)")

    ax.set_ylabel("Taxa Anual de Rendimento (%)")
    ax.set_xlabel("Data")
    ax.set_title("Figura 4: Rendimento de Staking — Lido stETH vs. Solo Staking Direto (Maio/2022 – Abril/2026)", fontweight="bold", pad=12)
    ax.legend(loc="upper right", frameon=True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))

    plt.tight_layout()
    salvar_figura(fig, "fig04_rendimento_apr_lido_vs_solo.png")


def fig05_tvl_vs_preco_eth(df_tvl, df_preco_eth):
    """Figura 5: Evolução do TVL da Lido (USD) vs. Preço do Ethereum (USD)."""
    fig, ax1 = plt.subplots(figsize=(11, 5.5))

    merged = pd.merge(df_tvl[["data", "tvl_total_usd"]], df_preco_eth[["data", "preco_eth_usd"]], on="data").dropna()
    merged["tvl_bilhoes"] = merged["tvl_total_usd"] / 1e9

    color_tvl = "#1f77b4"
    ax1.plot(merged["data"], merged["tvl_bilhoes"], color=color_tvl, linewidth=1.5, label="TVL Lido (Bilhões USD)")
    ax1.fill_between(merged["data"], merged["tvl_bilhoes"], color=color_tvl, alpha=0.15)
    ax1.set_ylabel("TVL Lido (Bilhões de USD)", color=color_tvl, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=color_tvl)

    ax2 = ax1.twinx()
    color_eth = "#ff7f0e"
    ax2.plot(merged["data"], merged["preco_eth_usd"], color=color_eth, linewidth=1.2, linestyle="--", label="Preço ETH/USD")
    ax2.set_ylabel("Preço do Ethereum (USD)", color=color_eth, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_eth)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    ax1.set_title("Figura 5: Relação entre o Capital Trava no Protocolo Lido (TVL) e a Cotação do ETH (Maio/2022 – Abril/2026)", fontweight="bold", pad=12)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

    plt.tight_layout()
    salvar_figura(fig, "fig05_evolucao_tvl_lido_vs_preco_eth.png")


def fig06_market_share_stacked(df_share_hist):
    """Figura 6: Gráfico de Área Empilhada do Market Share de Liquid Staking (%) no Recorte."""
    fig, ax = plt.subplots(figsize=(11, 6))

    cols_tvl = [c for c in df_share_hist.columns if c.startswith("tvl_")]
    df_clean = df_share_hist.dropna(subset=["total_top_tvl"]).copy()
    df_clean = df_clean[df_clean["total_top_tvl"] > 0]

    nomes_map = {
        "tvl_lido": "Lido DAO",
        "tvl_binance_staked_eth": "Binance (bETH)",
        "tvl_coinbase_wrapped_staked_eth": "Coinbase (cbETH)",
        "tvl_rocket_pool": "Rocket Pool (rETH)",
        "tvl_frax_ether": "Frax Ether (frxETH)",
        "tvl_stakewise": "StakeWise",
        "tvl_stader": "Stader (ETHx)",
        "tvl_swell": "Swell (swETH)",
        "tvl_ankr": "Ankr",
    }

    ultimos = df_clean[cols_tvl].iloc[-1].fillna(0)
    cols_ordenadas = ultimos.sort_values(ascending=False).index.tolist()

    y_data = []
    labels = []
    for c in cols_ordenadas:
        s = (df_clean[c].fillna(0) / df_clean["total_top_tvl"] * 100).values
        y_data.append(s)
        labels.append(nomes_map.get(c, c.replace("tvl_", "").title()))

    colors = sns.color_palette("tab10", len(labels))

    ax.stackplot(df_clean["data"], y_data, labels=labels, colors=colors, alpha=0.85)
    ax.axhline(33.33, color="black", linestyle="--", linewidth=1.5, label="Teto Crítico de Consenso (33,3%)")

    ax.set_ylabel("Participação de Mercado - Market Share (%)")
    ax.set_xlabel("Data")
    ax.set_title("Figura 6: Evolução do Market Share dos Protocolos de Liquid Staking no Ethereum (Maio/2022 – Abril/2026)", fontweight="bold", pad=12)
    ax.set_ylim(0, 100)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))

    plt.tight_layout()
    salvar_figura(fig, "fig06_market_share_historico_lsd.png")


def fig07_scatter_market_share_vs_depeg(df_share_hist, df_depeg):
    """Figura 7: Diagrama de Dispersão entre Dominância da Lido (%) e Depeg stETH (%)."""
    merged = pd.merge(df_share_hist[["data", "lido_share_pct"]], df_depeg[["data", "depeg_pct"]], on="data").dropna()

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    sns.regplot(x="lido_share_pct", y="depeg_pct", data=merged, ax=ax,
                color="#1f77b4", scatter_kws={"alpha": 0.3, "s": 15},
                line_kws={"color": "#d62728", "linewidth": 2, "label": "Linha de Regressão OLS"})

    ax.axhline(0, color="gray", linestyle=":", linewidth=0.8)
    ax.axvline(33.33, color="black", linestyle="--", linewidth=1.0, label="Teto de Descentralização (33.3%)")

    ax.set_xlabel("Market Share da Lido DAO (%)")
    ax.set_ylabel("Depeg stETH (%)")
    ax.set_title("Figura 7: Regressão: Concentração da Lido DAO vs. Magnitude do Depeg (Maio/2022 – Abril/2026)", fontweight="bold", pad=12)
    ax.legend(loc="lower left", frameon=True)

    plt.tight_layout()
    salvar_figura(fig, "fig07_dispersao_market_share_vs_depeg.png")


def fig08_indice_hhi(df_share_hist):
    """Figura 8: Evolução do Índice Herfindahl-Hirschman (HHI) de Concentração de Mercado."""
    cols_tvl = [c for c in df_share_hist.columns if c.startswith("tvl_")]
    df_clean = df_share_hist.dropna(subset=["total_top_tvl"]).copy()
    df_clean = df_clean[df_clean["total_top_tvl"] > 0]

    hhi_values = []
    for idx, row in df_clean.iterrows():
        total = row["total_top_tvl"]
        shares = [(row[c] / total * 100) for c in cols_tvl if pd.notna(row[c])]
        hhi = sum(s ** 2 for s in shares)
        hhi_values.append(hhi)

    df_clean["hhi"] = hhi_values

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_clean["data"], df_clean["hhi"], color="#d62728", linewidth=1.5, label="Índice HHI (Liquid Staking)")

    ax.axhline(2500, color="#ff7f0e", linestyle="--", linewidth=1.2, label="Mercado Altamente Concentrado (HHI > 2500)")
    ax.axhline(1500, color="#2ca02c", linestyle=":", linewidth=1.2, label="Mercado Moderadamente Concentrado (1500-2500)")

    ax.fill_between(df_clean["data"], df_clean["hhi"], 2500, where=(df_clean["hhi"] >= 2500), color="#d62728", alpha=0.15)

    ax.set_ylabel("Índice Herfindahl-Hirschman (HHI)")
    ax.set_xlabel("Data")
    ax.set_title("Figura 8: Evolução da Concentração de Mercado no Ecossistema Liquid Staking (HHI: 2022–2026)", fontweight="bold", pad=12)
    ax.set_ylim(0, 10000)
    ax.legend(loc="upper right", frameon=True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))

    plt.tight_layout()
    salvar_figura(fig, "fig08_indice_hhi_concentracao.png")


def main():
    print("=" * 75)
    print("SCRIPT 05 -- Geração de Gráficos Acadêmicos (Recorte: Maio/2022 a Abril/2026)")
    print("=" * 75)

    dados = carregar_dados()

    if "depeg" in dados:
        print("\n[1/8] Gerando Figura 1: Série Histórica de Depeg...")
        fig01_depeg_historico(dados["depeg"].copy())

        print("[2/8] Gerando Figura 2: Depeg Pré vs Pós-Shanghai Upgrade...")
        fig02_depeg_pre_pos_shanghai(dados["depeg"].copy())

        print("[3/8] Gerando Figura 3: Histograma e Densidade do Depeg...")
        fig03_histograma_distribuicao(dados["depeg"].copy())

    if "apr_lido" in dados:
        print("[4/8] Gerando Figura 4: Rendimento APR Lido vs Solo Staking...")
        fig04_rendimento_apr(dados["apr_lido"].copy(), dados.get("apr_direto"))

    if "tvl_lido" in dados and "preco_eth" in dados:
        print("[5/8] Gerando Figura 5: TVL Lido vs Preço do Ethereum...")
        fig05_tvl_vs_preco_eth(dados["tvl_lido"].copy(), dados["preco_eth"].copy())

    if "market_share_hist" in dados:
        print("[6/8] Gerando Figura 6: Market Share de Liquid Staking (Área Empilhada)...")
        fig06_market_share_stacked(dados["market_share_hist"].copy())

        if "depeg" in dados:
            print("[7/8] Gerando Figura 7: Regressão Dispersão Market Share vs Depeg...")
            fig07_scatter_market_share_vs_depeg(dados["market_share_hist"].copy(), dados["depeg"].copy())

        print("[8/8] Gerando Figura 8: Evolução do Índice HHI de Concentração...")
        fig08_indice_hhi(dados["market_share_hist"].copy())

    print("\n" + "=" * 75)
    print("TODOS OS 8 GRÁFICOS REGERADOS COM SUCESSO (RECORTE MAIO/22 - ABRIL/26)")
    print("=" * 75)


if __name__ == "__main__":
    main()
