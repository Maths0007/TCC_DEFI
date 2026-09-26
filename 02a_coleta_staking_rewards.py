"""Nome preservado por compatibilidade. Importa Beaconcha.in/ETH.STORE dos HTMLs.
Não consulta mais Staking Rewards. Não soma MEV ao ETH.STORE.
"""
import json
import subprocess
import sys
import numpy as np
import pandas as pd
from comum_tcc import *

def main():
    manifest = json.loads((FONTES_DIR / 'manifesto.json').read_text())
    for nome, expected in manifest['sha256'].items():
        if sha256(FONTES_DIR / nome) != expected:
            raise ValueError(f'Fonte alterada: {nome}. Revise antes de atualizar o manifesto.')
    for tipo, script, html, folder, csv, relatorio in [
        ('staking', 'extrair_staking_beaconchain.py', 'fonte_beaconchain.html', 'extracao_staking',
         'eth_staking_beaconchain_2022-04_2026-05.csv', 'validacao_extracao.json'),
        ('apr', 'extrair_apr_ethstore.py', 'fonte_ethstore.html', 'extracao_apr',
         'apr_ethstore_2022-04_2026-05.csv', 'validacao_apr.json')]:
        origem = FONTES_DIR/tipo
        validacao = json.loads((origem/relatorio).read_text(encoding='utf-8'))
        if sha256(origem/html) != validacao['sha256_html'] or sha256(origem/csv) != validacao['sha256_csv']:
            raise ValueError(f'Integridade da fonte {tipo} divergente do relatório original.')
        subprocess.run([sys.executable, str(origem/script), str(origem/html),
                        '--saida', str(DADOS_DIR/folder)], check=True)
        if sha256(DADOS_DIR/folder/csv) != validacao['sha256_csv']:
            raise ValueError(f'Extração {tipo} não reproduz o CSV do ZIP.')
    s = pd.read_csv(DADOS_DIR/'extracao_staking/eth_staking_beaconchain_2022-04_2026-05.csv')
    a = pd.read_csv(DADOS_DIR/'extracao_apr/apr_ethstore_2022-04_2026-05.csv')
    s = s.rename(columns={'data_utc':'Date', 'eth_saldo_efetivo_fonte':'total_staked_eth_network',
                          'timestamp_fonte_ms':'timestamp_staking_fonte_ms'})
    a = a.rename(columns={'data_inicio_periodo_utc':'Date', 'apr_ethstore_percentual_aa':'apr_rede_ethstore_pct',
                          'inicio_periodo_utc':'inicio_periodo_ethstore_utc',
                          'timestamp_fonte_ms':'timestamp_ethstore_fonte_ms',
                          'recompensas_periodo_eth':'recompensas_ethstore_eth',
                          'saldo_efetivo_ethstore_eth':'saldo_efetivo_elegivel_ethstore_eth'})
    df = juntar(juntar(grid(), datas_unicas(s,'staking')), datas_unicas(a,'apr'))
    required = ['total_staked_eth_network','apr_rede_ethstore_pct','recompensas_ethstore_eth','saldo_efetivo_elegivel_ethstore_eth']
    if df[required].isna().any().any():
        raise ValueError('Lacunas nas fontes principais; não serão preenchidas.')
    calc = df.recompensas_ethstore_eth / df.saldo_efetivo_elegivel_ethstore_eth * 36500
    if not np.allclose(calc, df.apr_rede_ethstore_pct, atol=0.000501, rtol=0):
        raise ValueError('APR não confere com a fórmula ETH.STORE.')
    df['fim_periodo_ethstore_utc'] = (pd.to_datetime(df.inicio_periodo_ethstore_utc, utc=True)+pd.Timedelta(days=1)).astype(str)
    df['fonte_staking'] = 'https://beaconcha.in/charts/staked_ether'
    df['fonte_apr_rede'] = 'https://www.beaconcha.in/ethstore'
    df['qualidade_staking_apr'] = 'extraido_html_sem_imputacao; consistencia_interna_verificada'
    df['staking_igual_dia_anterior'] = df.total_staked_eth_network.eq(df.total_staked_eth_network.shift()).astype(int)
    salvar(df, 'dados_beaconchain.csv', manifest)

if __name__ == '__main__':
    main()
