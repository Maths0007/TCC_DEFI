# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "pandas",
#     "numpy",
#     "scipy",
#     "matplotlib",
#     "seaborn",
# ]
# ///
"""
Script Orquestrador Principal: Executa a pipeline completa de coleta de dados, 
cálculo de métricas estatísticas e geração de gráficos acadêmicos do TCC.
"""
import time
from datetime import datetime
import importlib

coleta_precos = importlib.import_module("01_coleta_precos")
coleta_apr = importlib.import_module("02_coleta_apr")
coleta_tvl_lsd = importlib.import_module("03_coleta_tvl_lsd")
gerar_metricas = importlib.import_module("04_gerar_metricas")
gerar_graficos = importlib.import_module("05_gerar_graficos")


def main():
    inicio = time.time()
    print("#" * 75)
    print("PIPELINE COMPLETA DE DADOS, MÉTRICAS E GRÁFICOS - TCC DEFI")
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#" * 75)
    print()

    # 1. Executar Coleta de Preços e Depeg
    print("ETAPA 1/5: Coleta de Preços ETH/USD e Depeg stETH/ETH")
    coleta_precos.main()
    print("\n" + "-" * 75 + "\n")

    # 2. Executar Coleta de APR
    print("ETAPA 2/5: Coleta de Taxas APR/APY (Lido vs. Staking Direto)")
    coleta_apr.main()
    print("\n" + "-" * 75 + "\n")

    # 3. Executar Coleta de TVL e Market Share
    print("ETAPA 3/5: Coleta de TVL, Staking Ratio e Market Share LSD/LRT")
    coleta_tvl_lsd.main()
    print("\n" + "-" * 75 + "\n")

    # 4. Executar Cálculo de Métricas Estatísticas e Econométricas
    print("ETAPA 4/5: Cálculo de Métricas Estatísticas, Econométricas e Governança")
    gerar_metricas.main()
    print("\n" + "-" * 75 + "\n")

    # 5. Executar Geração de Gráficos Acadêmicos (300 DPI)
    print("ETAPA 5/5: Geração de 8 Gráficos Acadêmicos de Alta Resolução (300 DPI)")
    gerar_graficos.main()
    print("\n" + "-" * 75 + "\n")

    duracao = time.time() - inicio
    print("#" * 75)
    print(f"PIPELINE EXECUTADA E CONCLUÍDA COM SUCESSO EM {duracao:.1f} SEGUNDOS!")
    print("  - 8 Arquivos CSV brutos salvos em: scripts_e_dados/Dados/")
    print("  - 6 Arquivos de métricas e relatório salvos em: scripts_e_dados/Metricas/")
    print("  - 8 Gráficos acadêmicos (300 DPI) salvos em: scripts_e_dados/Graficos/")
    print("#" * 75)


if __name__ == "__main__":
    main()
