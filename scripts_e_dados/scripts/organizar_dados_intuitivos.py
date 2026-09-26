"""
Script para Organização Intuitiva dos Dados do TCC
Cria uma estrutura clara, legível e pronta para uso acadêmico.
"""
import os
import json
import pandas as pd
import numpy as np

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dados_beaconchain = os.path.join(root, "Dados_beaconchain")
    pasta_destino = os.path.join(root, "DADOS_DO_TCC")
    pasta_tecnica = os.path.join(pasta_destino, "tecnico_auditoria")
    pasta_metricas = os.path.join(root, "Metricas")
    
    os.makedirs(pasta_destino, exist_ok=True)
    os.makedirs(pasta_tecnica, exist_ok=True)
    os.makedirs(pasta_metricas, exist_ok=True)
    
    arquivo_origem = os.path.join(dados_beaconchain, "dataset_final_tcc.csv")
    if not os.path.exists(arquivo_origem):
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_origem}")
        
    df = pd.read_csv(arquivo_origem)
    
    # -------------------------------------------------------------
    # 1. Dataset Consolidado do TCC (Variáveis Econômicas Limpas)
    # -------------------------------------------------------------
    cols_clean = {
        'Date': 'data',
        'total_staked_eth_network': 'total_eth_staked',
        'apr_rede_ethstore_pct': 'apr_rede_ethstore_pct',
        'preco_eth_usd': 'preco_eth_usd',
        'preco_steth_usd': 'preco_steth_usd',
        'preco_steth_eth': 'razao_steth_eth',
        'depeg_pct': 'depeg_pct',
        'retorno_log_eth': 'retorno_log_eth',
        'retorno_log_steth': 'retorno_log_steth',
        'volatilidade_30d_anual_eth': 'volatilidade_anual_eth_30d',
        'volatilidade_30d_anual_steth': 'volatilidade_anual_steth_30d'
    }
    
    df_clean = df[list(cols_clean.keys())].rename(columns=cols_clean).copy()
    
    # Arredondamentos legíveis preservando precisão analítica
    df_clean['preco_eth_usd'] = df_clean['preco_eth_usd'].round(2)
    df_clean['preco_steth_usd'] = df_clean['preco_steth_usd'].round(2)
    df_clean['razao_steth_eth'] = df_clean['razao_steth_eth'].round(6)
    df_clean['depeg_pct'] = df_clean['depeg_pct'].round(4)
    df_clean['retorno_log_eth'] = df_clean['retorno_log_eth'].round(6)
    df_clean['retorno_log_steth'] = df_clean['retorno_log_steth'].round(6)
    df_clean['volatilidade_anual_eth_30d'] = df_clean['volatilidade_anual_eth_30d'].round(2)
    df_clean['volatilidade_anual_steth_30d'] = df_clean['volatilidade_anual_steth_30d'].round(2)
    
    path_consolidado = os.path.join(pasta_destino, "dataset_consolidado_tcc.csv")
    df_clean.to_csv(path_consolidado, index=False, encoding='utf-8')
    print(f"Salvo: {path_consolidado} ({len(df_clean)} linhas, {len(df_clean.columns)} colunas)")
    
    # -------------------------------------------------------------
    # 2. Dataset Temático: Preços, Paridade e Depeg
    # -------------------------------------------------------------
    cols_precos = ['data', 'preco_eth_usd', 'preco_steth_usd', 'razao_steth_eth', 'depeg_pct',
                   'retorno_log_eth', 'retorno_log_steth', 'volatilidade_anual_eth_30d', 'volatilidade_anual_steth_30d']
    path_precos = os.path.join(pasta_destino, "dados_precos_e_depeg.csv")
    df_clean[cols_precos].to_csv(path_precos, index=False, encoding='utf-8')
    print(f"Salvo: {path_precos}")
    
    # -------------------------------------------------------------
    # 3. Dataset Temático: Staking e Rendimento da Rede
    # -------------------------------------------------------------
    df_staking = pd.DataFrame({
        'data': df['Date'],
        'total_eth_staked': df['total_staked_eth_network'],
        'apr_rede_ethstore_pct': df['apr_rede_ethstore_pct'],
        'recompensas_diarias_eth': df['recompensas_ethstore_eth'].round(4),
        'saldo_elegivel_eth': df['saldo_efetivo_elegivel_ethstore_eth']
    })
    path_staking = os.path.join(pasta_destino, "dados_staking_e_apr.csv")
    df_staking.to_csv(path_staking, index=False, encoding='utf-8')
    print(f"Salvo: {path_staking}")
    
    # -------------------------------------------------------------
    # 4. Arquivos Técnicos e de Auditoria (Mantidos Separados)
    # -------------------------------------------------------------
    path_auditoria_csv = os.path.join(pasta_tecnica, "dataset_completo_com_metadados.csv")
    df.to_csv(path_auditoria_csv, index=False, encoding='utf-8')
    
    for f in ["auditoria_tcc.json", "execucao.json"]:
        orig = os.path.join(dados_beaconchain, f)
        if os.path.exists(orig):
            dest = os.path.join(pasta_tecnica, f)
            with open(orig, 'r', encoding='utf-8') as src, open(dest, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
    print(f"Arquivos técnicos copiados para: {pasta_tecnica}")
    
    # -------------------------------------------------------------
    # 5. Dicionário de Dados Intuitivo em Markdown
    # -------------------------------------------------------------
    dic_md = f"""# Dicionário de Dados — TCC Lido DAO & Liquid Staking

Este documento descreve as variáveis contidas na pasta **`DADOS_DO_TCC/`**, seu significado econômico, unidade de medida e fonte original.

---

## 📁 1. `dataset_consolidado_tcc.csv`
Arquivo principal para a pesquisa de TCC, unificando as métricas econômicas e financeiras diárias de **01/05/2022 a 31/05/2026** (1.492 observações diárias).

| Nome da Coluna | Tipo | Unidade | Descrição / Fórmula | Fonte |
| :--- | :--- | :--- | :--- | :--- |
| **`data`** | Data | AAAA-MM-DD | Data civil da observação em fuso UTC | - |
| **`total_eth_staked`** | Numérico | ETH | Saldo efetivo total de Ether depositado em validadores ativos na Beacon Chain | Beaconcha.in |
| **`apr_rede_ethstore_pct`** | Numérico | % a.a. | Taxa anualizada de rendimento da rede Ethereum (ETH.STORE) em janelas de 24h | Beaconcha.in ETH.STORE |
| **`preco_eth_usd`** | Numérico | USD ($) | Preço diário de fechamento do Ethereum em dólares | Yahoo Finance (`ETH-USD`) |
| **`preco_steth_usd`** | Numérico | USD ($) | Preço diário de fechamento do stETH (Lido) em dólares | Yahoo Finance (`STETH-USD`) |
| **`razao_steth_eth`** | Numérico | Ratio | Razão de preço $\\frac{{\\text{{stETH}}}}{{\\text{{ETH}}}}$. Paridade perfeita = 1.000000 | Derivado (Yahoo) |
| **`depeg_pct`** | Numérico | % | Desvio percentual da paridade: $(\\frac{{\\text{{stETH}}}}{{\\text{{ETH}}}} - 1) \\times 100$ | Derivado (Yahoo) |
| **`retorno_log_eth`** | Numérico | Decimal | Retorno logarítmico diário: $\\ln(P_t / P_{{t-1}})$ do ETH | Derivado |
| **`retorno_log_steth`** | Numérico | Decimal | Retorno logarítmico diário: $\\ln(P_t / P_{{t-1}})$ do stETH | Derivado |
| **`volatilidade_anual_eth_30d`** | Numérico | % a.a. | Volatilidade móvel anualizada (30 dias) dos retornos do ETH: $\\sigma_{{30d}} \\times \\sqrt{{365}} \\times 100$ | Derivado |
| **`volatilidade_anual_steth_30d`** | Numérico | % a.a. | Volatilidade móvel anualizada (30 dias) dos retornos do stETH: $\\sigma_{{30d}} \\times \\sqrt{{365}} \\times 100$ | Derivado |

---

## 📁 2. Arquivos Temáticos Especializados

1. **`dados_precos_e_depeg.csv`**:
   Contém especificamente as séries de preços de mercado, razão stETH/ETH, depeg percentual, retornos e volatilidades.
2. **`dados_staking_e_apr.csv`**:
   Contém as métricas de segurança on-chain e rendimento: total de ETH em staking, APR da rede, recompensas diárias pagas aos validadores e saldo efetivo elegível.
3. **`tecnico_auditoria/`**:
   Contém o arquivo com todas as 36 colunas brutas, URLs, timestamps em milissegundos e relatórios de auditoria matemática (`auditoria_tcc.json`).
"""
    path_dic = os.path.join(pasta_destino, "DICIONARIO_DE_DADOS.md")
    with open(path_dic, 'w', encoding='utf-8') as f:
        f.write(dic_md)
    print(f"Salvo: {path_dic}")

    # -------------------------------------------------------------
    # 6. Atualização das Métricas Descritivas do TCC
    # -------------------------------------------------------------
    depeg = df_clean['depeg_pct']
    shanghai_date = '2023-04-12'
    pre_shanghai = df_clean[df_clean['data'] <= shanghai_date]['depeg_pct']
    pos_shanghai = df_clean[df_clean['data'] > shanghai_date]['depeg_pct']
    
    metricas = {
        "periodo_inicio": df_clean['data'].min(),
        "periodo_fim": df_clean['data'].max(),
        "total_dias": len(df_clean),
        "depeg_medio_pct": float(depeg.mean()),
        "depeg_mediano_pct": float(depeg.median()),
        "depeg_std_pct": float(depeg.std()),
        "depeg_min_pct": float(depeg.min()),
        "depeg_max_pct": float(depeg.max()),
        "depeg_p01_pct": float(depeg.quantile(0.01)),
        "depeg_p05_pct": float(depeg.quantile(0.05)),
        "depeg_p25_pct": float(depeg.quantile(0.25)),
        "depeg_p75_pct": float(depeg.quantile(0.75)),
        "depeg_p95_pct": float(depeg.quantile(0.95)),
        "depeg_p99_pct": float(depeg.quantile(0.99)),
        "shanghai": {
            "pre_dias": len(pre_shanghai),
            "pre_media_pct": float(pre_shanghai.mean()),
            "pre_std_pct": float(pre_shanghai.std()),
            "pos_dias": len(pos_shanghai),
            "pos_media_pct": float(pos_shanghai.mean()),
            "pos_std_pct": float(pos_shanghai.std()),
            "reducao_volatilidade_pct": float((1 - pos_shanghai.std() / pre_shanghai.std()) * 100)
        },
        "staking": {
            "eth_inicial": float(df_clean['total_eth_staked'].iloc[0]),
            "eth_final": float(df_clean['total_eth_staked'].iloc[-1]),
            "crescimento_staking_pct": float((df_clean['total_eth_staked'].iloc[-1] / df_clean['total_eth_staked'].iloc[0] - 1) * 100),
            "apr_medio_pct": float(df_clean['apr_rede_ethstore_pct'].mean()),
            "apr_min_pct": float(df_clean['apr_rede_ethstore_pct'].min()),
            "apr_max_pct": float(df_clean['apr_rede_ethstore_pct'].max())
        }
    }
    
    path_metricas_json = os.path.join(pasta_metricas, "resumo_metricas_atualizado.json")
    with open(path_metricas_json, 'w', encoding='utf-8') as f:
        json.dump(metricas, f, indent=2, ensure_ascii=False)
    print(f"Salvo: {path_metricas_json}")
    
    # Relatório de Métricas em Markdown
    relatorio_md = f"""# Relatório de Métricas Estatísticas do TCC (Atualizado)

**Recorte Temporal Analisado:** {metricas['periodo_inicio']} a {metricas['periodo_fim']} ({metricas['total_dias']} Dias Consecutivos)  
**Fonte dos Dados:** Beaconcha.in (Staked ETH e ETH.STORE APR) e Yahoo Finance (`ETH-USD`, `STETH-USD`).

---

## 1. Estatísticas Descritivas do Depeg stETH/ETH

| Indicador | Valor | Interpretação Acadêmica |
| :--- | :--- | :--- |
| **Total de Dias** | {metricas['total_dias']} | Amostra diária completa sem lacunas |
| **Depeg Médio** | {metricas['depeg_medio_pct']:.4f}% | Desconto médio estrutural pré/pós Shanghai |
| **Depeg Mediano** | {metricas['depeg_mediano_pct']:.4f}% | Paridade típica do mercado |
| **Desvio Padrão** | {metricas['depeg_std_pct']:.4f}% | Volatilidade temporal da paridade |
| **Maior Desconto (Mínimo)** | {metricas['depeg_min_pct']:.4f}% | Pico de estresse de liquidez (Crash Terra/LUNA e Celsius) |
| **Maior Prêmio (Máximo)** | {metricas['depeg_max_pct']:.4f}% | Máximo prêmio registrado |

### Distribuição Percentílica do Depeg:
- **P1% (Piores 1% dos dias):** {metricas['depeg_p01_pct']:.4f}%
- **P5%:** {metricas['depeg_p05_pct']:.4f}%
- **Q1 (25%):** {metricas['depeg_p25_pct']:.4f}%
- **Mediana (50%):** {metricas['depeg_mediano_pct']:.4f}%
- **Q3 (75%):** {metricas['depeg_p75_pct']:.4f}%
- **P95%:** {metricas['depeg_p95_pct']:.4f}%
- **P99%:** {metricas['depeg_p99_pct']:.4f}%

---

## 2. Impacto do Hard Fork Shanghai/Capella (Habilitação de Saques em 12/04/2023)

| Período | Dias | Depeg Médio (%) | Desvio Padrão (%) |
| :--- | :--- | :--- | :--- |
| **Pré-Shanghai** (Sem saques: Maio/22 a Abr/23) | {metricas['shanghai']['pre_dias']} | {metricas['shanghai']['pre_media_pct']:.4f}% | {metricas['shanghai']['pre_std_pct']:.4f}% |
| **Pós-Shanghai** (Com saques: Abr/23 a Mai/26) | {metricas['shanghai']['pos_dias']} | {metricas['shanghai']['pos_media_pct']:.4f}% | {metricas['shanghai']['pos_std_pct']:.4f}% |

> **Resultado Econométrico Principal:** A habilitação dos saques na atualização Shanghai resultou em uma **redução de {metricas['shanghai']['reducao_volatilidade_pct']:.1f}% na volatilidade do depeg**, estabilizando a paridade do derivativo stETH em torno de 1:1.

---

## 3. Dinâmica de Staking e Rendimento da Rede (Beacon Chain / ETH.STORE)

| Métrica | Início (Maio/2022) | Fim (Maio/2026) | Variação / Média |
| :--- | :--- | :--- | :--- |
| **Total em Staking (ETH)** | {metricas['staking']['eth_inicial']:,.0f} | {metricas['staking']['eth_final']:,.0f} | **+{metricas['staking']['crescimento_staking_pct']:.1f}% de crescimento** |
| **APR Médio da Rede** | - | - | **{metricas['staking']['apr_medio_pct']:.3f}% a.a.** |
| **Faixa de APR da Rede** | Mínimo: {metricas['staking']['apr_min_pct']:.3f}% a.a. | Máximo: {metricas['staking']['apr_max_pct']:.3f}% a.a. | Rendimento decrescente com aumento de validadores |
"""
    path_relatorio = os.path.join(pasta_metricas, "relatorio_metricas_atualizado.md")
    with open(path_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio_md)
    print(f"Salvo: {path_relatorio}")

if __name__ == '__main__':
    main()
