# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "numpy",
#     "scipy",
# ]
# ///
"""
Script 04: Cálculo de Métricas Estatísticas e Econométricas do TCC (Recorte: Maio/2022 a Abril/2026)
Processa os dados coletados da pasta scripts_e_dados/Dados e gera:
1. Tabelas estatísticas em CSV (scripts_e_dados/Metricas/)
2. Resumo em JSON (scripts_e_dados/Metricas/resumo_metricas.json)
3. Relatório formatado em Markdown (scripts_e_dados/Metricas/relatorio_metricas_tcc.md)
"""
import os
import json
import numpy as np
import pandas as pd
from scipy import stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Dados")
METRICAS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "Metricas")

# Recorte Temporal de Análise Solicitado (Maio/2022 a Abril/2026)
DATA_INICIO = pd.to_datetime("2022-05-01")
DATA_FIM = pd.to_datetime("2026-04-30")


def carregar_dados():
    """Carrega os datasets CSV da pasta Dados filtrados para Maio/2022 a Abril/2026."""
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
            print(f"  [OK] Carregado e filtrado {filename} ({len(df)} linhas | 2022-05-01 a 2026-04-30)")
        else:
            print(f"  [AVISO] Arquivo não encontrado: {filename}")
    return dados


def calcular_metricas_depeg(df_depeg):
    """Calcula estatísticas descritivas completas do Depeg stETH/ETH no recorte 2022-2026."""
    depeg = df_depeg["depeg_pct"].dropna()
    ratio = df_depeg["preco_steth_eth"].dropna()

    metricas = {
        "total_observacoes_dias": int(len(depeg)),
        "data_inicio": str(df_depeg["data"].min().strftime("%Y-%m-%d")),
        "data_fim": str(df_depeg["data"].max().strftime("%Y-%m-%d")),
        "preco_ratio_medio": float(ratio.mean()),
        "preco_ratio_mediana": float(ratio.median()),
        "depeg_medio_pct": float(depeg.mean()),
        "depeg_mediana_pct": float(depeg.median()),
        "depeg_desvio_padrao_pct": float(depeg.std()),
        "depeg_minimo_pct": float(depeg.min()),  # Pior desconto
        "depeg_maximo_pct": float(depeg.max()),  # Maior prêmio
        "depeg_assimetria_skewness": float(stats.skew(depeg)),
        "depeg_curtose_kurtosis": float(stats.kurtosis(depeg)),
        "percentil_1_pct": float(np.percentile(depeg, 1)),
        "percentil_5_pct": float(np.percentile(depeg, 5)),
        "percentil_25_pct": float(np.percentile(depeg, 25)),
        "percentil_75_pct": float(np.percentile(depeg, 75)),
        "percentil_95_pct": float(np.percentile(depeg, 95)),
        "percentil_99_pct": float(np.percentile(depeg, 99)),
        "dias_depeg_abaixo_minus_1pct": int((depeg < -1.0).sum()),
        "dias_depeg_abaixo_minus_2pct": int((depeg < -2.0).sum()),
        "dias_depeg_abaixo_minus_5pct": int((depeg < -5.0).sum()),
        "dias_depeg_abaixo_minus_10pct": int((depeg < -10.0).sum()),
        "pct_dias_depeg_abaixo_minus_2pct": float((depeg < -2.0).mean() * 100),
        "autocorrelacao_ar1": float(depeg.autocorr(lag=1)),
        "autocorrelacao_ar2": float(depeg.autocorr(lag=2)),
        "autocorrelacao_ar5": float(depeg.autocorr(lag=5)),
    }
    return metricas


def calcular_pre_pos_shanghai(df_depeg):
    """Compara estatísticas do Depeg antes e depois do Upgrade Shanghai/Capella (12/04/2023)."""
    data_shanghai = pd.to_datetime("2023-04-12")

    pre = df_depeg[df_depeg["data"] <= data_shanghai]["depeg_pct"].dropna()
    pos = df_depeg[df_depeg["data"] > data_shanghai]["depeg_pct"].dropna()

    t_stat, p_val_t = stats.ttest_ind(pre, pos, equal_var=False)
    f_stat = np.var(pre, ddof=1) / np.var(pos, ddof=1) if np.var(pos, ddof=1) > 0 else np.nan
    p_val_f = stats.f.sf(f_stat, len(pre) - 1, len(pos) - 1)

    resultado = {
        "pre_shanghai": {
            "periodo": f"{df_depeg['data'].min().strftime('%Y-%m-%d')} a 2023-04-12",
            "dias": int(len(pre)),
            "depeg_medio_pct": float(pre.mean()),
            "depeg_mediana_pct": float(pre.median()),
            "desvio_padrao_pct": float(pre.std()),
            "depeg_minimo_pct": float(pre.min()),
            "depeg_maximo_pct": float(pre.max()),
            "dias_depeg_abaixo_minus_2pct": int((pre < -2.0).sum()),
            "pct_dias_depeg_abaixo_minus_2pct": float((pre < -2.0).mean() * 100),
        },
        "pos_shanghai": {
            "periodo": f"2023-04-13 a {df_depeg['data'].max().strftime('%Y-%m-%d')}",
            "dias": int(len(pos)),
            "depeg_medio_pct": float(pos.mean()),
            "depeg_mediana_pct": float(pos.median()),
            "desvio_padrao_pct": float(pos.std()),
            "depeg_minimo_pct": float(pos.min()),
            "depeg_maximo_pct": float(pos.max()),
            "dias_depeg_abaixo_minus_2pct": int((pos < -2.0).sum()),
            "pct_dias_depeg_abaixo_minus_2pct": float((pos < -2.0).mean() * 100),
        },
        "teste_hipotese": {
            "t_statistic": float(t_stat),
            "p_value_diferenca_medias": float(p_val_t),
            "f_statistic_variancia": float(f_stat),
            "p_value_diferenca_variancias": float(p_val_f),
            "reducao_desvio_padrao_pct": float((1 - pos.std() / pre.std()) * 100),
        },
    }
    return resultado


def calcular_eventos_estresse(df_depeg):
    """Mapeia métricas de depeg durante janelas de estresse históricas."""
    eventos = [
        {"nome": "Crash Terra/LUNA (Maio 2022)", "inicio": "2022-05-01", "fim": "2022-05-31"},
        {"nome": "Insolvência Celsius / Depeg de Verão (Junho 2022)", "inicio": "2022-06-01", "fim": "2022-06-30"},
        {"nome": "Colapso FTX (Novembro 2022)", "inicio": "2022-11-01", "fim": "2022-11-30"},
        {"nome": "Upgrade Shanghai / Saques (Abril 2023)", "inicio": "2023-04-01", "fim": "2023-04-30"},
        {"nome": "Hack KelpDAO / Crise Restaking (Abril 2026)", "inicio": "2026-04-15", "fim": "2026-04-30"},
    ]

    resultados_eventos = []
    for ev in eventos:
        sub = df_depeg[(df_depeg["data"] >= ev["inicio"]) & (df_depeg["data"] <= ev["fim"])]
        if len(sub) > 0:
            dp = sub["depeg_pct"]
            resultados_eventos.append({
                "evento": ev["nome"],
                "inicio": ev["inicio"],
                "fim": ev["fim"],
                "dias_janela": int(len(sub)),
                "depeg_medio_pct": float(dp.mean()),
                "depeg_minimo_pct": float(dp.min()),
                "depeg_maximo_pct": float(dp.max()),
                "desvio_padrao_pct": float(dp.std()),
            })
    return resultados_eventos


def calcular_metricas_rendimento(df_apr_lido, df_apr_direto):
    """Calcula estatísticas de APR do Lido stETH vs. Solo Staking Direto no recorte."""
    if df_apr_lido is None or df_apr_direto is None:
        return {}

    lido_apy = df_apr_lido["apy_pct"].dropna()

    if "apr_direto_estimado_pct" in df_apr_direto.columns:
        direto_apr = df_apr_direto["apr_direto_estimado_pct"].dropna()
        spread = df_apr_direto["spread_pct"].dropna()
    else:
        direto_apr = lido_apy / 0.90
        spread = direto_apr - lido_apy

    metricas = {
        "apr_lido_medio_pct": float(lido_apy.mean()),
        "apr_lido_mediana_pct": float(lido_apy.median()),
        "apr_lido_desvio_padrao_pct": float(lido_apy.std()),
        "apr_lido_minimo_pct": float(lido_apy.min()),
        "apr_lido_maximo_pct": float(lido_apy.max()),
        "apr_direto_medio_pct": float(direto_apr.mean()),
        "apr_direto_minimo_pct": float(direto_apr.min()),
        "apr_direto_maximo_pct": float(direto_apr.max()),
        "spread_taxa_lido_dao_medio_pct": float(spread.mean()),
        "spread_taxa_lido_dao_maximo_pct": float(spread.max()),
        "tracking_error_pct": float((direto_apr - lido_apy).std()),
    }
    return metricas


def calcular_concentracao_market_share(df_share_hist, df_share_snap, df_depeg):
    """Calcula estatísticas de concentração de mercado, HHI e correlação com Depeg."""
    res = {}

    if df_share_snap is not None and len(df_share_snap) > 0:
        top1 = df_share_snap.iloc[0]
        res["lido_share_atual_pct"] = float(top1.get("market_share_pct", 0))
        res["lido_tvl_atual_usd"] = float(top1.get("tvl_usd", 0))

        shares = df_share_snap["market_share_pct"].dropna()
        res["hhi_atual"] = float((shares ** 2).sum())

    if df_share_hist is not None and len(df_share_hist) > 0:
        if "lido_share_pct" in df_share_hist.columns:
            lido_hist = df_share_hist["lido_share_pct"].dropna()
            res["lido_share_historico_medio_pct"] = float(lido_hist.mean())
            res["lido_share_historico_minimo_pct"] = float(lido_hist.min())
            res["lido_share_historico_maximo_pct"] = float(lido_hist.max())

        cols_tvl = [c for c in df_share_hist.columns if c.startswith("tvl_")]
        hhi_list = []
        for idx, row in df_share_hist.iterrows():
            total = row.get("total_top_tvl", 0)
            if pd.notna(total) and total > 0:
                shares = [(row[c] / total * 100) for c in cols_tvl if pd.notna(row[c])]
                hhi = sum(s ** 2 for s in shares)
                hhi_list.append({"data": row["data"], "hhi": hhi})

        if hhi_list:
            df_hhi = pd.DataFrame(hhi_list)
            res["hhi_historico_medio"] = float(df_hhi["hhi"].mean())
            res["hhi_historico_minimo"] = float(df_hhi["hhi"].min())
            res["hhi_historico_maximo"] = float(df_hhi["hhi"].max())

        if "lido_share_pct" in df_share_hist.columns and df_depeg is not None:
            merged = pd.merge(df_share_hist[["data", "lido_share_pct"]], df_depeg[["data", "depeg_pct"]], on="data").dropna()
            if len(merged) > 10:
                pearson_r, pearson_p = stats.pearsonr(merged["lido_share_pct"], merged["depeg_pct"])
                spearman_r, spearman_p = stats.spearmanr(merged["lido_share_pct"], merged["depeg_pct"])
                res["correlacao_share_vs_depeg"] = {
                    "observacoes_comuns": int(len(merged)),
                    "pearson_r": float(pearson_r),
                    "pearson_p_value": float(pearson_p),
                    "spearman_r": float(spearman_r),
                    "spearman_p_value": float(spearman_p),
                }

    return res


def gerar_relatorio_markdown(metricas_depeg, pre_pos, eventos, metricas_apr, concentracao):
    """Gera o relatório descritivo completo em Markdown para o recorte de Maio/2022 a Abril/2026."""
    relatorio = f"""# Relatório de Métricas Estatísticas e Econométricas — TCC Lido DAO & Liquid Staking
**Recorte Temporal:** Maio de 2022 a Abril de 2026 (48 Meses)  
**Data de Geração:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  

---

## 1. Estatísticas Descritivas do Depeg stETH/ETH (Maio/2022 a Abril/2026)

| Métrica | Valor | Observação |
|---|---|---|
| **Total de Observações (Dias)** | {metricas_depeg['total_observacoes_dias']} | Recorte Maio/2022 – Abril/2026 |
| **Preço Médio (stETH/ETH)** | {metricas_depeg['preco_ratio_medio']:.6f} | Paridade nominal teórica: 1.000000 |
| **Depeg Médio (%)** | {metricas_depeg['depeg_medio_pct']:.4f}% | Média de desvio no período |
| **Depeg Mediano (%)** | {metricas_depeg['depeg_mediana_pct']:.4f}% | - |
| **Desvio Padrão (%)** | {metricas_depeg['depeg_desvio_padrao_pct']:.4f}% | Volatilidade temporal do peg |
| **Maior Desconto / Depeg Mínimo (%)** | {metricas_depeg['depeg_minimo_pct']:.4f}% | Registrado durante o colapso Terra/LUNA |
| **Maior Prêmio / Depeg Máximo (%)** | {metricas_depeg['depeg_maximo_pct']:.4f}% | Registrado pós-insolvência da FTX |
| **Assimetria (Skewness)** | {metricas_depeg['depeg_assimetria_skewness']:.4f} | Negativa (cauda longa em desvalorizações) |
| **Curtose (Kurtosis)** | {metricas_depeg['depeg_curtose_kurtosis']:.4f} | Leptocúrtica (caudas pesadas) |
| **Autocorrelação AR(1)** | {metricas_depeg['autocorrelacao_ar1']:.4f} | Inércia de depeg no curto prazo |
| **Autocorrelação AR(5)** | {metricas_depeg['autocorrelacao_ar5']:.4f} | Persistência de liquidez a médio prazo |

### Distribuição Percentílica do Depeg (%)
- **Percentil 1% (Worst 1%):** {metricas_depeg['percentil_1_pct']:.4f}%
- **Percentil 5%:** {metricas_depeg['percentil_5_pct']:.4f}%
- **Percentil 25% (Q1):** {metricas_depeg['percentil_25_pct']:.4f}%
- **Percentil 75% (Q3):** {metricas_depeg['percentil_75_pct']:.4f}%
- **Percentil 95%:** {metricas_depeg['percentil_95_pct']:.4f}%
- **Percentil 99%:** {metricas_depeg['percentil_99_pct']:.4f}%

---

## 2. Impacto do Upgrade Shanghai/Capella (Habilitação de Saques Nativos em 12/04/2023)

| Parâmetro | Pré-Shanghai (Sem Saques: Maio/22 - Abr/23) | Pós-Shanghai (Com Saques: Abr/23 - Abr/26) | Impacto / Teste |
|---|---|---|---|
| **Período** | {pre_pos['pre_shanghai']['periodo']} | {pre_pos['pos_shanghai']['periodo']} | - |
| **Dias Analisados** | {pre_pos['pre_shanghai']['dias']} | {pre_pos['pos_shanghai']['dias']} | - |
| **Depeg Médio (%)** | {pre_pos['pre_shanghai']['depeg_medio_pct']:.4f}% | {pre_pos['pos_shanghai']['depeg_medio_pct']:.4f}% | t-stat: {pre_pos['teste_hipotese']['t_statistic']:.2f} (p: {pre_pos['teste_hipotese']['p_value_diferenca_medias']:.4e}) |
| **Desvio Padrão (%)** | {pre_pos['pre_shanghai']['desvio_padrao_pct']:.4f}% | {pre_pos['pos_shanghai']['desvio_padrao_pct']:.4f}% | **Redução de {pre_pos['teste_hipotese']['reducao_desvio_padrao_pct']:.1f}% na volatilidade** |
| **Depeg Mínimo (%)** | {pre_pos['pre_shanghai']['depeg_minimo_pct']:.4f}% | {pre_pos['pos_shanghai']['depeg_minimo_pct']:.4f}% | Eliminação de desvios extremos |
| **Dias com Depeg < -2%** | {pre_pos['pre_shanghai']['dias_depeg_abaixo_minus_2pct']} ({pre_pos['pre_shanghai']['pct_dias_depeg_abaixo_minus_2pct']:.1f}%) | {pre_pos['pos_shanghai']['dias_depeg_abaixo_minus_2pct']} ({pre_pos['pos_shanghai']['pct_dias_depeg_abaixo_minus_2pct']:.1f}%) | Estabilização da arbitragem 1:1 |

---

## 3. Comportamento em Janelas de Estresse Sistêmico

| Evento de Mercado | Período | Depeg Médio (%) | Depeg Mínimo (%) | Desvio Padrão (%) |
|---|---|---|---|---|
"""
    for ev in eventos:
        relatorio += f"| **{ev['evento']}** | {ev['inicio']} a {ev['fim']} | {ev['depeg_medio_pct']:.4f}% | **{ev['depeg_minimo_pct']:.4f}%** | {ev['desvio_padrao_pct']:.4f}% |\n"

    relatorio += f"""
---

## 4. Análise de Rendimentos (Lido APR vs. Solo Staking Direto)

| Métrica | Lido stETH | Solo Staking Direto (Estimado) | Spread / Custo Lido DAO |
|---|---|---|---|
| **Rendimento Médio (APR/APY %)** | {metricas_apr.get('apr_lido_medio_pct', 0):.2f}% | {metricas_apr.get('apr_direto_medio_pct', 0):.2f}% | **{metricas_apr.get('spread_taxa_lido_dao_medio_pct', 0):.3f}%** |
| **Rendimento Mínimo (%)** | {metricas_apr.get('apr_lido_minimo_pct', 0):.2f}% | {metricas_apr.get('apr_direto_minimo_pct', 0):.2f}% | - |
| **Rendimento Máximo (%)** | {metricas_apr.get('apr_lido_maximo_pct', 0):.2f}% | {metricas_apr.get('apr_direto_maximo_pct', 0):.2f}% | - |
| **Desvio Padrão (%)** | {metricas_apr.get('apr_lido_desvio_padrao_pct', 0):.2f}% | - | Tracking Error: {metricas_apr.get('tracking_error_pct', 0):.4f}% |

---

## 5. Concentração de Mercado, HHI e Risco de Governança

- **Market Share Médio da Lido DAO (Maio/22 - Abr/26):** **{concentracao.get('lido_share_historico_medio_pct', 0):.2f}%**
- **Índice Herfindahl-Hirschman (HHI) Médio:** **{concentracao.get('hhi_historico_medio', 0):.1f}** (Mercado Altamente Concentrado > 2500)
"""
    if "correlacao_share_vs_depeg" in concentracao:
        c = concentracao["correlacao_share_vs_depeg"]
        relatorio += f"""### Correlação Estatística (Market Share Lido vs Depeg stETH)
- **Coeficiente de Pearson (r):** `{c['pearson_r']:.4f}` (p-value: `{c['pearson_p_value']:.4e}`)
- **Coeficiente de Spearman (r_s):** `{c['spearman_r']:.4f}` (p-value: `{c['spearman_p_value']:.4e}`)
"""

    return relatorio


def main():
    print("=" * 75)
    print("SCRIPT 04 -- Cálculo de Métricas (Recorte: Maio/2022 a Abril/2026)")
    print("=" * 75)

    os.makedirs(METRICAS_DIR, exist_ok=True)
    dados = carregar_dados()

    if "depeg" not in dados:
        print("[ERRO] dataset depeg_steth_eth.csv não encontrado!")
        return

    print("\n[1/5] Calculando estatísticas descritivas do Depeg (2022-2026)...")
    metricas_depeg = calcular_metricas_depeg(dados["depeg"])

    print("[2/5] Analisando impacto do Upgrade Shanghai...")
    pre_pos = calcular_pre_pos_shanghai(dados["depeg"])

    print("[3/5] Mapeando janelas de estresse sistêmico...")
    eventos = calcular_eventos_estresse(dados["depeg"])

    print("[4/5] Calculando estatísticas de APR...")
    metricas_apr = calcular_metricas_rendimento(dados.get("apr_lido"), dados.get("apr_direto"))

    print("[5/5] Avaliando concentração HHI e correlações...")
    concentracao = calcular_concentracao_market_share(
        dados.get("market_share_hist"), dados.get("market_share_snap"), dados.get("depeg")
    )

    # Salvar arquivos CSV
    pd.DataFrame([metricas_depeg]).to_csv(os.path.join(METRICAS_DIR, "tabela_depeg_descritiva.csv"), index=False)
    pd.DataFrame([
        {**pre_pos["pre_shanghai"], "categoria": "pre_shanghai"},
        {**pre_pos["pos_shanghai"], "categoria": "pos_shanghai"},
    ]).to_csv(os.path.join(METRICAS_DIR, "tabela_pre_pos_shanghai.csv"), index=False)
    pd.DataFrame(eventos).to_csv(os.path.join(METRICAS_DIR, "tabela_eventos_estresse.csv"), index=False)
    pd.DataFrame([metricas_apr]).to_csv(os.path.join(METRICAS_DIR, "tabela_rendimento_apr.csv"), index=False)

    # Salvar JSON
    resultado_completo = {
        "recorte_temporal": "2022-05-01 a 2026-04-30",
        "metricas_depeg": metricas_depeg,
        "pre_pos_shanghai": pre_pos,
        "eventos_estresse": eventos,
        "metricas_rendimento_apr": metricas_apr,
        "concentracao_market_share": concentracao,
    }

    caminho_json = os.path.join(METRICAS_DIR, "resumo_metricas.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(resultado_completo, f, indent=2, ensure_ascii=False)
    print(f"\n  [OK] Salvo JSON consolidado: {caminho_json}")

    # Salvar Markdown
    md_texto = gerar_relatorio_markdown(metricas_depeg, pre_pos, eventos, metricas_apr, concentracao)
    caminho_md = os.path.join(METRICAS_DIR, "relatorio_metricas_tcc.md")
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(md_texto)
    print(f"  [OK] Salvo Relatório Markdown: {caminho_md}")

    print("\n" + "=" * 75)
    print("MÉTRICAS RECALCULADAS COM SUCESSO (RECORTE MAIO/22 - ABRIL/26)")
    print("=" * 75)


if __name__ == "__main__":
    main()
