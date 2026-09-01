# -*- coding: utf-8 -*-
"""
MODULO 4: Consolidacao do Master Dataset do TCC (2022-2026)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)

Objetivo:
  - Merge (Full Outer Join) de todas as tabelas intermediarias pela chave temporal (Date YYYY-MM-DD).
  - Tratamento Rigoroso de Dados:
    * Variaveis continuas: interpolacao linear suave + ffill/bfill.
    * Janelas moveis (retornos e volatilidade): interpolacao apenas interna (limit_area="inside").
    * Contagens discretas e eventos (slashing, flags): fillna(0) estrito.
  - Calculo da variavel principal de spread de retornos:
    Delta_APR_t = APR_Rede_Direto_t - APR_Lido_Liquido_t
  - Engenharia de atributos financeiros, custos de oportunidade e classificacao de regimes tecnologicos.

Saidas:
  - dataset_master_tcc_2022_2026.csv (diretorio raiz)
  - scripts_e_dados/Dados/dataset_master_tcc_2022_2026.csv
  - files/dataset_master_tcc_2022_2026.csv
"""
import os
import sys
import numpy as np
import pandas as pd
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

COLUNAS_DISCRETAS = [
    "slashing_eventos_qtd",
    "slashing_volume_eth",
    "evento_terra_luna",
    "evento_merge",
    "evento_ftx",
    "evento_shapella",
    "mev_amostras_coletadas"
]

COLUNAS_JANELA_MOVEL = [
    "retorno_log_eth",
    "retorno_log_steth",
    "volatilidade_7d_anual_eth",
    "volatilidade_30d_anual_eth",
    "volatilidade_7d_anual_steth",
    "volatilidade_30d_anual_steth",
    "mev_valor_medio_bloco_eth",
    "mev_total_diario_estimado_eth"
]


def carregar_tabela(nome_arquivo: str) -> pd.DataFrame:
    for local in [
        os.path.join(ROOT_DIR, nome_arquivo),
        os.path.join(DADOS_DIR, nome_arquivo),
        os.path.join(FILES_DIR, nome_arquivo),
        os.path.join(FILES_DIR, "scripts_e_dados", "Dados", nome_arquivo)
    ]:
        if os.path.exists(local):
            df = pd.read_csv(local)
            date_cols = [c for c in df.columns if c.lower() in ("date", "data")]
            if date_cols:
                col = date_cols[0]
                df["Date"] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
                if col != "Date":
                    df = df.drop(columns=[col])
            return df
    print(f"  [AVISO] Arquivo {nome_arquivo} nao encontrado!")
    return pd.DataFrame()


def classificar_regime_historico(dt_str: str) -> str:
    dt = pd.to_datetime(dt_str)
    if dt < pd.to_datetime("2022-09-15"):
        return "Pre-Merge"
    elif dt < pd.to_datetime("2023-04-12"):
        return "Post-Merge_Pre-Shapella"
    else:
        return "Post-Shapella"


def main():
    print("=" * 70)
    print("MODULO 4: Consolidacao do Master Dataset do TCC (2022-2026)")
    print(f"Recorte Temporal: {DATA_INICIO} a {DATA_FIM} (Diario UTC)")
    print(f"Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)

    # 1. Carregar tabelas parciais
    print("\n[1/4] Carregando datasets intermediarios...")
    df_precos = carregar_tabela("dados_precos_mercado.csv")
    df_consenso = carregar_tabela("dados_rated_consenso.csv")
    df_defillama = carregar_tabela("dados_defillama_curve.csv")
    df_mev = carregar_tabela("dados_mev_relay.csv")

    print(f"  -> Precos e Volatilidade: {len(df_precos)} linhas")
    print(f"  -> Camada de Consenso:   {len(df_consenso)} linhas")
    print(f"  -> DefiLlama & Curve:     {len(df_defillama)} linhas")
    print(f"  -> MEV via Relays:        {len(df_mev)} linhas" if not df_mev.empty else "  -> MEV via Relays:        opcional")

    # 2. Outer Join no grid continuo
    print("\n[2/4] Realizando Full Outer Join temporal no grid continuo...")
    grid_datas = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="D").strftime("%Y-%m-%d")
    df_master = pd.DataFrame({"Date": grid_datas})

    if not df_precos.empty:
        df_master = pd.merge(df_master, df_precos, on="Date", how="left")
    if not df_consenso.empty:
        df_master = pd.merge(df_master, df_consenso, on="Date", how="left")
    if not df_defillama.empty:
        df_master = pd.merge(df_master, df_defillama, on="Date", how="left")
    if not df_mev.empty:
        df_master = pd.merge(df_master, df_mev, on="Date", how="left")

    # 3. Tratamento Diferenciado de Dados
    print("\n[3/4] Aplicando tratamento quantitativo rigoroso...")

    # A. Preenchimento estrito com 0 em colunas discretas
    for col in COLUNAS_DISCRETAS:
        if col in df_master.columns:
            df_master[col] = df_master[col].fillna(0)
            if "qtd" in col or "evento" in col or "amostras" in col:
                df_master[col] = df_master[col].astype(int)

    # B. Interpolacao apenas interna em janelas moveis
    for col in COLUNAS_JANELA_MOVEL:
        if col in df_master.columns:
            df_master[col] = df_master[col].interpolate(method="linear", limit_area="inside")

    # C. Interpolacao suave linear nas demais colunas continuas
    num_cols = df_master.select_dtypes(include=[np.number]).columns
    cols_continuas = [c for c in num_cols if c not in COLUNAS_DISCRETAS and c not in COLUNAS_JANELA_MOVEL]
    for col in cols_continuas:
        df_master[col] = df_master[col].interpolate(method="linear").ffill().bfill()

    # D. Reconciliação dos Preços, Paridade e Depeg
    df_master["preco_steth_eth"] = df_master["preco_steth_usd"] / df_master["preco_eth_usd"]
    df_master["liquid_staking_basis"] = df_master["preco_steth_eth"] - 1.0
    df_master["depeg_pct"] = df_master["liquid_staking_basis"] * 100.0

    # E. CALCULO DA VARIAVEL PRINCIPAL DO TCC:
    # Delta_APR_t = APR_Rede_Direto_t - APR_Lido_Liquido_t
    if "apr_lido_liquido_pct" not in df_master.columns and "apr_lido_consenso_pct" in df_master.columns:
        df_master["apr_lido_liquido_pct"] = df_master["apr_lido_consenso_pct"]

    df_master["delta_apr_pct"] = df_master["apr_rede_direto_total_pct"] - df_master["apr_lido_liquido_pct"]

    # Taxa de Retencao Efetiva da Lido DAO (% cobrada sobre o staking)
    df_master["taxa_retencao_efetiva_pct"] = np.where(
        df_master["apr_rede_direto_total_pct"] > 0,
        (df_master["delta_apr_pct"] / df_master["apr_rede_direto_total_pct"]) * 100.0,
        10.0
    )

    # Custo de Oportunidade Diario e Acumulado
    df_master["custo_oportunidade_diario_pct"] = df_master["delta_apr_pct"] / 365.0
    df_master["custo_oportunidade_acumulado_pct"] = df_master["custo_oportunidade_diario_pct"].cumsum()

    # Classificacao de Regimes Tecnologicos
    df_master["regime_ethereum"] = df_master["Date"].apply(classificar_regime_historico)

    # Flags Binarias de Eventos de Estresse
    df_master["evento_terra_luna"] = (df_master["Date"].between("2022-05-08", "2022-05-31")).astype(int)
    df_master["evento_merge"] = (df_master["Date"].between("2022-09-15", "2022-09-22")).astype(int)
    df_master["evento_ftx"] = (df_master["Date"].between("2022-11-06", "2022-11-30")).astype(int)
    df_master["evento_shapella"] = (df_master["Date"].between("2023-04-12", "2023-04-30")).astype(int)

    # Recorte estrito
    df_master["Date_dt"] = pd.to_datetime(df_master["Date"])
    df_master = df_master[(df_master["Date_dt"] >= pd.to_datetime(DATA_INICIO)) & (df_master["Date_dt"] <= pd.to_datetime(DATA_FIM))]
    df_master = df_master.drop(columns=["Date_dt"]).sort_values("Date").reset_index(drop=True)

    # Validacoes de Integridade
    assert len(df_master) == 1488, f"Esperado 1488 dias entre {DATA_INICIO} e {DATA_FIM}, obtido {len(df_master)}"
    assert (df_master["slashing_eventos_qtd"] % 1 == 0).all(), "[ERRO] Valores fracionarios em contagem de slashing!"
    assert df_master["depeg_pct"].std() > 0.05, "[ERRO] Depeg com variabilidade nula!"
    assert df_master["tvl_pool_curve_usd"].std() > 1e6, "[ERRO] TVL da pool Curve com variabilidade nula!"

    # Ordenacao Estrategica de Colunas
    cols_ordenadas = [
        "Date",
        "regime_ethereum",
        "preco_eth_usd",
        "preco_steth_usd",
        "preco_steth_eth",
        "liquid_staking_basis",
        "depeg_pct",
        "retorno_log_eth",
        "retorno_log_steth",
        "volatilidade_7d_anual_eth",
        "volatilidade_30d_anual_eth",
        "volatilidade_7d_anual_steth",
        "volatilidade_30d_anual_steth",
        "apr_rede_direto_total_pct",
        "apr_lido_liquido_pct",
        "delta_apr_pct",
        "taxa_retencao_efetiva_pct",
        "custo_oportunidade_diario_pct",
        "custo_oportunidade_acumulado_pct",
        "apr_consenso_bruto_pct",
        "taxa_mev_execucao_apr_pct",
        "total_staked_eth_network",
        "apy_lido_pct",
        "apr_base_nominal_pct",
        "apy_pool_curve_pct",
        "efetividade_operadores_lido_pct",
        "slashing_eventos_qtd",
        "slashing_volume_eth",
        "tvl_lido_total_usd",
        "tvl_lido_ethereum_usd",
        "tvl_pool_curve_usd",
        "reserva_eth_curve",
        "reserva_steth_curve",
        "ratio_reserva_steth_pct",
        "volume_diario_curve_usd",
        "evento_terra_luna",
        "evento_merge",
        "evento_ftx",
        "evento_shapella",
        "fonte_preco_eth",
        "fonte_preco_steth",
        "fonte_consenso",
        "qualidade_dado",
        "reservas_curve_metodo"
    ]
    cols_finais = [c for c in cols_ordenadas if c in df_master.columns] + [c for c in df_master.columns if c not in cols_ordenadas]
    df_master = df_master[cols_finais]

    # Arredondamentos Finais
    for col in df_master.select_dtypes(include=[np.number]).columns:
        if col in COLUNAS_DISCRETAS:
            if "qtd" in col or "evento" in col or "amostras" in col:
                df_master[col] = df_master[col].astype(int)
            else:
                df_master[col] = df_master[col].round(4)
        elif "usd" in col or "reserva" in col or "tvl" in col or "volume" in col or "network" in col:
            df_master[col] = df_master[col].round(2)
        elif "ratio" in col or "preco_steth_eth" in col or "retorno_log" in col or "volatilidade" in col or "basis" in col:
            df_master[col] = df_master[col].round(6)
        elif "pct" in col or "apr" in col or "apy" in col or "depeg" in col:
            df_master[col] = df_master[col].round(4)

    # 4. Salvar Master Dataset
    print("\n[4/4] Salvando dataset_master_tcc_2022_2026.csv...")
    destinos = [os.path.join(DADOS_DIR, "dataset_master_tcc_2022_2026.csv")]")]

    for d in destinos:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        df_master.to_csv(d, index=False)
        print(f"  -> Salvo em: {d}")

    print("\n" + "-" * 70)
    print("RESUMO DO MASTER DATASET CONSOLIDADO (2022-05-05 a 2026-05-31):")
    print(f"  -> Dimensao: {df_master.shape[0]} linhas x {df_master.shape[1]} colunas")
    print(f"  -> Periodo Estrito: {df_master['Date'].iloc[0]} a {df_master['Date'].iloc[-1]}")
    print(f"  -> Delta APR Medio (Comissao Lido): {df_master['delta_apr_pct'].mean():.4f}%")
    print(f"  -> Taxa de Retencao Media: {df_master['taxa_retencao_efetiva_pct'].mean():.2f}%")
    print(f"  -> Depeg Medio: {df_master['depeg_pct'].mean():.4f}% | Depeg Minimo: {df_master['depeg_pct'].min():.4f}%")
    print(f"  -> Custo de Oportunidade Acumulado Total: {df_master['custo_oportunidade_acumulado_pct'].iloc[-1]:.2f}%")
    print("=" * 70)
    print("MODULO 4 CONCLUIDO COM SUCESSO!\n")


if __name__ == "__main__":
    main()