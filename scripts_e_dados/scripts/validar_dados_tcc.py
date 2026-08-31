# -*- coding: utf-8 -*-
"""
SCRIPT DE AUDITORIA E VALIDACAO QUANTITATIVA DO DATASET DO TCC
Tema: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Diario UTC)

Objetivo:
  Executar bateria rigorosa de testes de integridade matematica, financeira e empirica:
  1. Continuidade temporal e dimensionalidade (1522 dias)
  2. Consistencia de formulas financeiras (Depeg, Retornos, Volatilidade)
  3. Validacao das taxas de rendimento (APR Direto, APR Lido, Delta APR e Taxa de Retencao)
  4. Decomposicao da Camada de Consenso e MEV
  5. Comportamento das Reservas da Curve e TVL
  6. Sanidade de contagens discretas e flags de eventos
  7. Deteccao de series achatadas (std == 0) ou presenca indevida de NaNs
"""
import os
import sys
import numpy as np
import pandas as pd

def run_auditoria(caminho_csv: str):
    print("=" * 80)
    print(f"RELATORIO DE AUDITORIA E VALIDACAO DE DADOS: {os.path.basename(caminho_csv)}")
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

    # TESTE 1: Dimensao e Continuidade Temporal
    print("\n--- 1. AUDITORIA TEMPORAL E DIMENSIONAL ---")
    assert_teste("Total de Observacoes Diarias", total_linhas == 1522, f"Observado: {total_linhas} dias, Esperado: 1522")
    assert_teste("Data Inicial Exata", df["Date"].iloc[0] == "2022-04-01", f"Inicio: {df['Date'].iloc[0]}")
    assert_teste("Data Final Exata", df["Date"].iloc[-1] == "2026-05-31", f"Fim: {df['Date'].iloc[-1]}")
    
    # Verificar se ha dias faltantes no calendario
    datas_esperadas = pd.date_range("2022-04-01", "2026-05-31", freq="D").strftime("%Y-%m-%d")
    dias_faltantes = set(datas_esperadas) - set(df["Date"])
    assert_teste("Sequencia Continua (Zero Gaps)", len(dias_faltantes) == 0, f"Gaps: {len(dias_faltantes)}")
    assert_teste("Unicidade de Datas (Zero Duplicatas)", df["Date"].nunique() == total_linhas, f"Duplicatas: {total_linhas - df['Date'].nunique()}")

    # TESTE 2: Precos, Depeg e Paridade de Mercado
    print("\n--- 2. AUDITORIA DE PRECOS, DEPEG E PARIDADE ---")
    assert_teste("Precos ETH estritamente positivos", (df["preco_eth_usd"] > 0).all(), f"Min ETH: ${df['preco_eth_usd'].min():.2f}")
    assert_teste("Precos stETH estritamente positivos", (df["preco_steth_usd"] > 0).all(), f"Min stETH: ${df['preco_steth_usd'].min():.2f}")
    
    diff_ratio = np.abs(df["preco_steth_eth"] - (df["preco_steth_usd"] / df["preco_eth_usd"]))
    assert_teste("Consistencia da Taxa de Cambio stETH/ETH", (diff_ratio < 0.005).all(), f"Diff max: {diff_ratio.max():.6f}")

    diff_depeg = np.abs(df["depeg_pct"] - ((df["preco_steth_eth"] - 1.0) * 100.0))
    assert_teste("Formula do Depeg % (Basis)", (diff_depeg < 0.005).all(), f"Diff max: {diff_depeg.max():.6f}")

    # Verificar Depeg historico no Crash Terra/Luna (Maio/Junho 2022)
    df_luna = df[(df["Date_dt"] >= "2022-05-08") & (df["Date_dt"] <= "2022-06-30")]
    min_depeg_luna = df_luna["depeg_pct"].min()
    assert_teste("Captura do Stress Severo no Crash Terra/Luna", min_depeg_luna <= -5.0, f"Depeg Minimo Luna: {min_depeg_luna:.2f}%")

    # Verificar convergencia pos-Shapella (Apos Abril 2023 saques 1:1 ativados)
    df_shapella = df[df["Date_dt"] >= "2023-05-01"]
    depeg_medio_shapella = df_shapella["depeg_pct"].mean()
    assert_teste("Convergencia da Paridade Pos-Shapella", abs(depeg_medio_shapella) < 0.5, f"Depeg Medio Pos-Shapella: {depeg_medio_shapella:.3f}%")

    # TESTE 3: Rendimentos (APR Direto vs Lido) e Variavel Delta APR
    print("\n--- 3. AUDITORIA DE RENDIMENTOS, DELTA APR E RETENCAO ---")
    assert_teste("APR Direto da Rede Positivo", (df["apr_rede_direto_total_pct"] > 0).all(), f"Media: {df['apr_rede_direto_total_pct'].mean():.2f}%")
    assert_teste("APR Lido Liquido Positivo", (df["apr_lido_liquido_pct"] > 0).all(), f"Media: {df['apr_lido_liquido_pct'].mean():.2f}%")

    # Validacao do Delta APR (Spread)
    diff_delta = np.abs(df["delta_apr_pct"] - (df["apr_rede_direto_total_pct"] - df["apr_lido_liquido_pct"]))
    assert_teste("Consistencia do Delta APR (Spread)", (diff_delta < 0.001).all(), f"Diff max: {diff_delta.max():.6f}")

    # Validacao da Taxa de Retencao Efetiva (Comissao contratual de 10% da Lido DAO)
    taxa_retencao_media = df["taxa_retencao_efetiva_pct"].mean()
    assert_teste("Taxa de Retencao Lido DAO Alinhada (10%)", 9.8 <= taxa_retencao_media <= 10.2, f"Observado: {taxa_retencao_media:.2f}%")

    # TESTE 4: Decomposicao Consenso vs MEV
    print("\n--- 4. AUDITORIA DA CAMADA DE CONSENSO E MEV ---")
    if "apr_consenso_bruto_pct" in df.columns and "taxa_mev_execucao_apr_pct" in df.columns:
        diff_soma_apr = np.abs(df["apr_rede_direto_total_pct"] - (df["apr_consenso_bruto_pct"] + df["taxa_mev_execucao_apr_pct"]))
        assert_teste("Soma das Parcelas (Consenso + MEV = Total)", (diff_soma_apr < 0.01).all(), f"Diff max: {diff_soma_apr.max():.6f}")

        # Pre-merge MEV deve ser 0.0
        df_pre_merge = df[df["Date_dt"] < "2022-09-15"]
        assert_teste("MEV Nulo no Pre-Merge", (df_pre_merge["taxa_mev_execucao_apr_pct"] == 0.0).all(), "MEV zerado antes do Merge")

    # TESTE 5: TVL e Reservas da Curve
    print("\n--- 5. AUDITORIA DE LIQUIDEZ, TVL E DEX ---")
    assert_teste("TVL Lido Total Positivo em Bilhoes", df["tvl_lido_total_usd"].mean() > 1e9, f"TVL Medio Lido: ${df['tvl_lido_total_usd'].mean()/1e9:.2f}B")
    assert_teste("TVL Curve Dinamico e Positivo", df["tvl_pool_curve_usd"].min() > 1e7, f"Min Curve: ${df['tvl_pool_curve_usd'].min()/1e6:.1f}M | Max: ${df['tvl_pool_curve_usd'].max()/1e9:.2f}B")
    
    if "ratio_reserva_steth_pct" in df.columns:
        assert_teste("Proporcao de Reservas Curve Realista (40%-75%)", ((df["ratio_reserva_steth_pct"] >= 40) & (df["ratio_reserva_steth_pct"] <= 75)).all(), f"Min: {df['ratio_reserva_steth_pct'].min():.1f}% | Max: {df['ratio_reserva_steth_pct'].max():.1f}%")

    # TESTE 6: Eventos Discretos e Sanidade Estrutural
    print("\n--- 6. AUDITORIA DE CONTANGENS DISCRETAS E FLAGS ---")
    assert_teste("Slashing Eventos Estritamente Inteiro (>=0)", ((df["slashing_eventos_qtd"] >= 0) & (df["slashing_eventos_qtd"] % 1 == 0)).all(), f"Total eventos: {df['slashing_eventos_qtd'].sum()}")
    
    flags = ["evento_terra_luna", "evento_merge", "evento_ftx", "evento_shapella"]
    flags_ok = all(df[f].isin([0, 1]).all() for f in flags if f in df.columns)
    assert_teste("Flags de Eventos Binarias (0 ou 1)", flags_ok, "Todas as flags sao binarias")

    # TESTE 7: Deteccao de Series Achatadas (std == 0)
    print("\n--- 7. AUDITORIA DE VARIABILIDADE (ANTI-ACHATAMENTO) ---")
    cols_numericas = df.select_dtypes(include=[np.number]).columns
    cols_com_std_zero = []
    for c in cols_numericas:
        if c not in flags and not c.startswith("evento_") and "snapshot" not in c:
            if df[c].std() == 0:
                cols_com_std_zero.append(c)
    assert_teste("Nenhuma serie temporal chave esta achatada (std > 0)", len(cols_com_std_zero) == 0, f"Achatadas: {cols_com_std_zero}")

    print("\n" + "=" * 80)
    taxa_sucesso = (testes_passados / testes_totais) * 100.0
    print(f"RESULTADO FINAL DA AUDITORIA: {testes_passados}/{testes_totais} TESTES APROVADOS ({taxa_sucesso:.1f}%)")
    print("=" * 80 + "\n")
    return testes_passados == testes_totais

if __name__ == "__main__":
    caminho1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset_master_tcc_2022_2026.csv")
    caminho2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", "dataset_master_tcc_2022_2026.csv")
    
    run_auditoria(caminho1)
    if os.path.exists(caminho2):
        run_auditoria(caminho2)