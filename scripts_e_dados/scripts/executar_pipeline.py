"""Orquestração com falha explícita e registro de execução."""
import argparse
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime,timezone
import json

def main():
    p=argparse.ArgumentParser()
    for opt in ['offline','somente-beaconchain','sem-graficos','exigir-completo']: p.add_argument('--'+opt,action='store_true')
    args=p.parse_args(); root=Path(__file__).resolve().parent
    root_proj = root.parent.parent if root.name == 'scripts' and root.parent.name == 'scripts_e_dados' else (root.parent if root.name == 'scripts_e_dados' else root)
    env=os.environ.copy()
    env['TCC_OFFLINE']='1' if args.offline else '0'
    env['TCC_SOMENTE_BEACONCHAIN']='1' if args.somente_beaconchain else '0'
    out=Path(env.get('TCC_DADOS_DIR',str(root_proj/'scripts_e_dados'/('Dados_beaconchain' if args.somente_beaconchain else 'Dados'))))
    out.mkdir(parents=True,exist_ok=True); env['TCC_DADOS_DIR']=str(out.resolve())
    if not args.somente_beaconchain and (not env.get('TCC_LIDO_POOL_UUID') or not env.get('TCC_CURVE_STETH_POOL_UUID')):
        p.error('Modo completo exige TCC_LIDO_POOL_UUID e TCC_CURVE_STETH_POOL_UUID. '
                'Para os dados dos ZIPs, use --somente-beaconchain --offline.')
    etapas=['02a_coleta_staking_rewards.py']
    if not args.somente_beaconchain: etapas+=['01_coleta_precos.py','03_coleta_defillama_curve.py']
    etapas+=['02_coleta_rated_network.py','04_consolidar_dataset.py','formatar_dataset.py','validar_dados_tcc.py']
    if not args.sem_graficos: etapas+=['05_gerar_graficos_tcc.py']
    registro={'inicio_utc':datetime.now(timezone.utc).isoformat(),'argumentos':vars(args),'etapas':[],'status':'em_andamento'}
    for etapa in etapas:
        cmd=[sys.executable,str(root/etapa)]
        if etapa=='validar_dados_tcc.py' and args.exigir_completo: cmd+=['--exigir-completo']
        print(f'Executando {etapa}',flush=True)
        rc=subprocess.run(cmd,env=env,cwd=root).returncode
        registro['etapas'].append({'script':etapa,'codigo_saida':rc})
        registro['status']='falhou' if rc else 'em_andamento'
        (out/'execucao.json').write_text(json.dumps(registro,indent=2),encoding='utf-8')
        if rc: return rc
    registro['status']='concluido'; registro['fim_utc']=datetime.now(timezone.utc).isoformat()
    (out/'execucao.json').write_text(json.dumps(registro,indent=2),encoding='utf-8')
    print(f'Concluído. Consulte cobertura em {out / "auditoria_tcc.json"}'); return 0
if __name__=='__main__': raise SystemExit(main())
