"""
Script Orquestrador Principal (Atualizado):
Executa a nova pipeline do TCC, delegando para executar_pipeline.py.
Compatibilidade retroativa com execuções legadas de coletar_todos.py.
"""
import sys
import subprocess
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    script_exec = root / 'executar_pipeline.py'
    cmd = [sys.executable, str(script_exec)]
    
    # Se nenhum argumento for passado, usa a execução padrão verificada (somente-beaconchain + offline)
    args = sys.argv[1:]
    if not args:
        cmd += ['--somente-beaconchain', '--offline']
    else:
        cmd += args
        
    print(f"Iniciando pipeline atualizada do TCC via {script_exec.name}...")
    rc = subprocess.run(cmd).returncode
    sys.exit(rc)

if __name__ == '__main__':
    main()
