# -*- coding: utf-8 -*-
"""
SCRIPT DE AUDITORIA E VALIDACAO QUANTITATIVA DO DATASET DO TCC (100% EMPIRICO)
"""
import os
import sys
import numpy as np
import pandas as pd

def run_auditoria(caminho_csv: str):
    print("=" * 80)
    print(f"RELATORIO DE AUDITORIA E VALIDACAO DE DADOS (100% EMPIRICO): {os.path.basename(caminho_csv)}")
    print(f"Caminho: {caminho_csv}")
    print("=" * 80)

    if not os.path.exists(caminho_csv):
        print(f"[FALHA CRITICA] Arquivo nao encontrado: {caminho_csv}")
        return False

    df = pd.read_csv(caminho_csv)
    df["Date_dt"] = pd.to_datetime(df["Date"])
    total_linhas = len(df)

    testes_passados = 0
    testes_totais = 0

    def assert_teste(nome: str, condicao: bool, detalhe: str = ""):
        nonlocal testes_passados, testes_totais
        testes_totais += 1
        if condicao:
            testes_passados += 1
            print(f"  [PASSOU] {nome} {('(' + detalhe + ')') if detalhe else ''}")
        else:
            print(f"  [FALHOU] {nome} -> {detalhe}")

    # TESTE 1: Temporalidade
    print("\n--- 1. AUDITORIA TEMPORAL E DIMENSIONAL ---")
    assert_teste("Total de Observacoes Diarias", total_linhas == 1488, f"Observado: {total_linhas} dias, Esperado: 1488")
    assert_teste("Data Inicial Exata", df["Date"].iloc[0] == "2022-05-05", f"Inicio: {df['Date'].iloc[0]}")
    assert_teste("Data Final Exata", df["Date"].iloc[-1] == "2026-05-31", f"Fim: {df['Date'].iloc[-1]}")
    
    datas_esperadas = pd.date_range("2022-05-05", "2026-05-31", freq="D").strftime("%Y-%m-%d")
    dias_faltantes = set(datas_esperadas) - set(df["Date"])
    assert_teste("Sequencia Continua (Zero Gaps)", len(dias_faltantes) == 0, f"Gaps: {len(dias_faltantes)}")
    assert_teste("Unicidade de Datas (Zero Duplicatas)", df["Date"].nunique() == total_linhas, f"Duplicatas: {total_linhas - df['Date'].nunique()}")

    # TESTE 2: Precos e Depeg
    print("\n--- 2. AUDITORIA DE PRECOS, DEPEG E PARIDADE ---")
    assert_teste("Precos ETH estritamente positivos", (df["preco_eth_usd"] > 0).all(), f"Min ETH: ${df['preco_eth_usd'].min():.2f}")
    assert_teste("Precos stETH estritamente positivos", (df["preco_steth_usd"] > 0).all(), f"Min stETH: ${df['preco_steth_usd'].min():.2f}")
    
    diff_ratio = np.abs(df["preco_steth_eth"] - (df["preco_steth_usd"] / df["preco_eth_usd"]))
    assert_teste("Consistencia da Taxa de Cambio stETH/ETH", (diff_ratio < 0.005).all(), f"Diff max: {diff_ratio.max():.6f}")

    diff_depeg = np.abs(df["depeg_pct"] - ((df["preco_steth_eth"] - 1.0) * 100.0))
    assert_teste("Formula do Depeg % (Basis)", (diff_depeg < 0.005).all(), f"Diff max: {diff_depeg.max():.6f}")

    df_luna = df[(df["Date_dt"] >= "2022-05-08") & (df["Date_dt"] <= "2022-06-30")]
    min_depeg_luna = df_luna["depeg_pct"].min()
    assert_teste("Captura do Stress Severo no Crash Terra/Luna", min_depeg_luna <= -5.0, f"Depeg Minimo Luna: {min_depeg_luna:.2f}%")

    df_shapella = df[df["Date_dt"] >= "2023-05-01"]
    depeg_medio_shapella = df_shapella["depeg_pct"].mean()
    assert_teste("Convergencia da Paridade Pos-Shapella", abs(depeg_medio_shapella) < 0.5, f"Depeg Medio Pos-Shapella: {depeg_medio_shapella:.3f}%")

    # TESTE 3: Rendimentos Independentes
    print("\n--- 3. AUDITORIA DE RENDIMENTOS E DELTA APR ---")
    assert_teste("APR Direto da Rede Positivo", (df["apr_rede_direto_total_pct"] > 0).all(), f"Media: {df['apr_rede_direto_total_pct'].mean():.2f}%")
    assert_teste("APR Lido Liquido Positivo", (df["apr_lido_liquido_pct"] > 0).all(), f"Media: {df['apr_lido_liquido_pct'].mean():.2f}%")

    diff_delta = np.abs(df["delta_apr_pct"] - (df["apr_rede_direto_total_pct"] - df["apr_lido_liquido_pct"]))
    assert_teste("Consistencia do Delta APR (Spread)", (diff_delta < 0.001).all(), f"Diff max: {diff_delta.max():.6f}")

    taxa_retencao_media = df["taxa_retencao_efetiva_pct"].mean()
    assert_teste("Taxa de Retencao Lido DAO Empirica (~8.7% a 10.5%)", 7.0 <= taxa_retencao_media <= 13.0, f"Observado: {taxa_retencao_media:.2f}%")

    # TESTE 4: Decomposicao Consenso vs MEV
    print("\n--- 4. AUDITORIA DA CAMADA DE CONSENSO E MEV ---")
    if "apr_consenso_bruto_pct" in df.columns and "taxa_mev_execucao_apr_pct" in df.columns:
        diff_soma_apr = np.abs(df["apr_rede_direto_total_pct"] - (df["apr_consenso_bruto_pct"] + df["taxa_mev_execucao_apr_pct"]))
        assert_teste("Soma das Parcelas (Consenso + MEV = Total)", (diff_soma_apr < 0.01).all(), f"Diff max: {diff_soma_apr.max():.6f}")

        df_pre_merge = df[df["Date_dt"] < "2022-09-15"]
        assert_teste("MEV Nulo no Pre-Merge", (df_pre_merge["taxa_mev_execucao_apr_pct"] == 0.0).all(), "MEV zerado antes do Merge")

    # TESTE 5: TVL e Liquidez Real da Curve
    print("\n--- 5. AUDITORIA DE LIQUIDEZ E TVL ---")
    assert_teste("TVL Total Ethereum Positivo", df["tvl_rede_ethereum_total_usd"].mean() > 1e10, f"TVL Total Eth: ${df['tvl_rede_ethereum_total_usd'].mean()/1e9:.2f}B")
    assert_teste("TVL Lido Total Positivo em Bilhoes", df["tvl_lido_total_usd"].mean() > 1e9, f"TVL Lido: ${df['tvl_lido_total_usd'].mean()/1e9:.2f}B")
    assert_teste("TVL Curve Dinamico e Positivo", df["tvl_pool_curve_usd"].min() > 1e7, f"Min Curve: ${df['tvl_pool_curve_usd'].min()/1e6:.1f}M | Max: ${df['tvl_pool_curve_usd'].max()/1e9:.2f}B")

    # TESTE 6: Flags Binarias
    print("\n--- 6. AUDITORIA DE FLAGS DE EVENTOS ---")
    flags = ["evento_terra_luna", "evento_merge", "evento_ftx", "evento_shapella"]
    flags_ok = all(df[f].isin([0, 1]).all() for f in flags if f in df.columns)
    assert_teste("Flags de Eventos Binarias (0 ou 1)", flags_ok, "Todas as flags sao binarias")

    # TESTE 7: Variabilidade Anti-Achatamento
    print("\n--- 7. AUDITORIA DE VARIABILIDADE ---")
    cols_numericas = df.select_dtypes(include=[np.number]).columns
    cols_ignorar = flags + ["mev_amostras_coletadas"]
    cols_com_std_zero = [c for c in cols_numericas if c not in cols_ignorar and not c.startswith("evento_") and df[c].std() == 0]
    assert_teste("Nenhuma serie temporal chave esta achatada (std > 0)", len(cols_com_std_zero) == 0, f"Achatadas: {cols_com_std_zero}")

    print("\n" + "=" * 80)
    taxa_sucesso = (testes_passados / testes_totais) * 100.0
    print(f"RESULTADO FINAL DA AUDITORIA: {testes_passados}/{testes_totais} TESTES APROVADOS ({taxa_sucesso:.1f}%)")
    print("=" * 80 + "\n")
    return testes_passados == testes_totais

if __name__ == "__main__":
    caminho_dir = os.path.dirname(os.path.abspath(__file__))
    caminho1 = os.path.join(caminho_dir, "..", "Dados", "dataset_master_tcc_2022_2026.csv")
    if not os.path.exists(caminho1):
        caminho1 = os.path.join(caminho_dir, "dataset_master_tcc_2022_2026.csv")
    run_auditoria(caminho1)