# -*- coding: utf-8 -*-
"""
ORQUESTRADOR MESTRE: Pipeline de Coleta, Filtragem, Consolidacao e Visualizacao (2022-2026)
Tema TCC: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO como alternativa de investimento em ativos digitais
Recorte Temporal: 2022-04-01 a 2026-05-31 (Frequencia Diaria UTC)

Executa em sequencia os modulos:
  1. 01_coleta_precos.py          -> dados_precos_mercado.csv
  2. 02_coleta_rated_network.py    -> dados_rated_consenso.csv
  3. 03_coleta_defillama_curve.py  -> dados_defillama_curve.csv
  4. 04_consolidar_dataset.py      -> dataset_master_tcc_2022_2026.csv
  5. 05_gerar_graficos_tcc.py      -> grafico_01_paridade_depeg_2022_2026.png
                                      grafico_02_comparativo_apr_retornos.png
"""
import os
import sys
import time
import subprocess
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ETAPAS = [
    ("01_coleta_precos.py", "Modulo 1: Precos Historicos, Volatilidade e Depeg"),
    ("02_coleta_rated_network.py", "Modulo 2: Camada de Consenso, Recompensas e Slashing"),
    ("03_coleta_defillama_curve.py", "Modulo 3: TVL, Yields e Reservas DEX (DefiLlama & Curve)"),
    ("04_consolidar_dataset.py", "Modulo 4: Consolidacao do Master Dataset (2022-2026)"),
    ("05_gerar_graficos_tcc.py", "Modulo 5: Renderizacao de Figuras Academicas em 300 DPI"),
]


def executar_modulo(script_nome: str, descricao: str) -> bool:
    print("\n" + "#" * 75)
    print(f"EXECUTANDO: {descricao} ({script_nome})")
    print("#" * 75)
    inicio = time.time()

    script_path = os.path.join(ROOT_DIR, script_nome)
    cmd = [sys.executable, script_path]

    try:
        subprocess.run(cmd, cwd=ROOT_DIR, check=True)
        duracao = time.time() - inicio
        print(f"\n[SUCESSO] {script_nome} concluido em {duracao:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        duracao = time.time() - inicio
        print(f"\n[FALHA] Erro na execucao de {script_nome} (Codigo {e.returncode}) apos {duracao:.2f}s")
        return False
    except Exception as e:
        duracao = time.time() - inicio
        print(f"\n[FALHA] Excecao em {script_nome}: {e} apos {duracao:.2f}s")
        return False


def main():
    print("=" * 75)
    print("PIPELINE DE ENGENHARIA DE DADOS PARA O TCC - LIQUID STAKING (LIDO DAO)")
    print("Tema: Financas Descentralizadas: A avaliacao do liquid staking via Lido DAO")
    print("      como alternativa de investimento em ativos digitais")
    print(f"Recorte Temporal Obrigatorio: 2022-04-01 a 2026-05-31 (Diario UTC)")
    print(f"Inicio da Execucao: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 75)

    tempo_inicio = time.time()
    concluidos = 0

    for script, desc in ETAPAS:
        ok = executar_modulo(script, desc)
        if ok:
            concluidos += 1
        else:
            print(f"\n[INTERRUPCAO] Falha critica no modulo {script}. Abortando pipeline.")
            sys.exit(1)

    tempo_total = time.time() - tempo_inicio

    print("\n" + "=" * 75)
    print("RESUMO DA EXECUCAO DO PIPELINE COMPLETO:")
    print(f"  -> Modulos executados com sucesso: {concluidos}/{len(ETAPAS)}")
    print(f"  -> Tempo total de execucao: {tempo_total:.2f} segundos")
    print("\nDATASETS E GRAFICOS GERADOS:")
    print("  [1] dados_precos_mercado.csv (Precos ETH/stETH, retornos log, volatilidade 7d/30d)")
    print("  [2] dados_rated_consenso.csv (APR consenso nativo, MEV, efetividade e slashings)")
    print("  [3] dados_defillama_curve.csv (TVL Lido, APY->APR nominal e reservas DEX Curve)")
    print("  [4] dataset_master_tcc_2022_2026.csv (Master Dataset com Delta APR consolidado)")
    print("  [5] grafico_01_paridade_depeg_2022_2026.png (Evolucao da Paridade stETH/ETH 300 DPI)")
    print("  [6] grafico_02_comparativo_apr_retornos.png (Curva de Retornos e Spread 300 DPI)")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()