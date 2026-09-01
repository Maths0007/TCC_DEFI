# -*- coding: utf-8 -*-
"""
ORQUESTRADOR MESTRE DO PIPELINE DE DADOS DO TCC
Tema: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-05-05 a 2026-05-31 (Diario UTC)

Executa em sequencia os 5 modulos de engenharia de dados e auditoria:
  1. 01_coleta_precos.py          -> Precos ETH/stETH, Depeg % e Volatilidade
  2. 02_coleta_rated_network.py    -> Formula Oficial Beacon Chain: APR = 16.632,32 / sqrt(S) + MEV
  3. 03_coleta_defillama_curve.py  -> TVL Lido, Yields e Historico Real da Pool Curve stETH/ETH
  4. 04_consolidar_dataset.py      -> Master Dataset Consolidado (1488 dias x 47 colunas)
  5. 05_gerar_graficos_tcc.py      -> Renderizacao das Figuras Academicas em 300 DPI
  6. validar_dados_tcc.py          -> Auditoria Quantitativa Automatica (22 testes)
"""
import os
import sys
import time
import subprocess
from datetime import datetime, timezone

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXEC = sys.executable

SCRIPTS = [
    ("Modulo 1: Precos, Volatilidade e Depeg", "01_coleta_precos.py"),
    ("Modulo 2: Camada de Consenso e Staking Direto (16632/sqrt(S))", "02_coleta_rated_network.py"),
    ("Modulo 3: TVL, Yields e Pool Curve stETH/ETH", "03_coleta_defillama_curve.py"),
    ("Modulo 4: Consolidacao do Master Dataset (Delta APR)", "04_consolidar_dataset.py"),
    ("Modulo 5: Figuras Academicas em 300 DPI", "05_gerar_graficos_tcc.py"),
    ("Auditoria Quantitativa e Validacao", "validar_dados_tcc.py")
]

def main():
    print("=" * 80)
    print("PIPELINE DE ENGENHARIA DE DADOS PARA O TCC - LIQUID STAKING (LIDO DAO)")
    print("Tema: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO")
    print("      como alternativa de investimento em ativos digitais")
    print("Recorte Temporal: 2022-05-05 a 2026-05-31 (Frequencia Diaria UTC)")
    print(f"Inicio da Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 80)

    tempo_inicio_total = time.time()
    sucessos = 0

    for i, (nome, arquivo) in enumerate(SCRIPTS, 1):
        caminho_script = os.path.join(ROOT_DIR, arquivo)
        if not os.path.exists(caminho_script):
            print(f"\n[ERRO] Script {arquivo} nao encontrado em {ROOT_DIR}!")
            continue

        print(f"\n[{i}/{len(SCRIPTS)}] EXECUTANDO: {nome} ({arquivo})...")
        t0 = time.time()
        
        proc = subprocess.run([PYTHON_EXEC, caminho_script], cwd=ROOT_DIR)
        t_exec = time.time() - t0

        if proc.returncode == 0:
            sucessos += 1
            print(f"  -> Concluido com sucesso em {t_exec:.2f}s")
        else:
            print(f"  -> [FALHA] {arquivo} encerrou com codigo de erro {proc.returncode} apos {t_exec:.2f}s")

    tempo_total = time.time() - tempo_inicio_total
    print("\n" + "=" * 80)
    print("RESUMO DA EXECUCAO DO PIPELINE COMPLETO:")
    print(f"  -> Modulos Executados com Sucesso: {sucessos}/{len(SCRIPTS)}")
    print(f"  -> Tempo Total de Execucao: {tempo_total:.2f} segundos")
    print("\nARQUIVOS PRINCIPAIS DISPONIVEIS:")
    print("  [1] dataset_master_tcc_2022_2026.csv (Master Dataset - 1488 linhas x 47 colunas)")
    print("  [2] dados_precos_mercado.csv (Precos ETH/stETH, Depeg %, Volatilidades)")
    print("  [3] dados_rated_consenso.csv (Curva de Emissao e Staking Direto)")
    print("  [4] dados_defillama_curve.csv (TVL Lido e Reservas da Pool Curve)")
    print("  [5] grafico_01_paridade_depeg_2022_2026.png (Evolucao da Paridade 300 DPI)")
    print("  [6] grafico_02_comparativo_apr_retornos.png (Curva de Retornos e Spread 300 DPI)")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()