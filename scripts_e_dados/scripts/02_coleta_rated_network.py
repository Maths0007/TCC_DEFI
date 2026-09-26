"""Nome legado. Consolida referência ETH.STORE, não consulta Rated Network.
APR Lido só é aceito de arquivo documentado. Nunca aplica desconto constante.
"""
import json
import pandas as pd
from comum_tcc import *

def carregar_lido_documentado():
    """Entrada opcional: fontes/apr_lido_validado.csv + .json. Ver README."""
    p = FONTES_DIR/'apr_lido_validado.csv'
    if not p.exists():
        return None
    meta = p.with_suffix('.json')
    if not meta.exists():
        raise ValueError('APR Lido exige metadados de fonte, unidade e método.')
    m = json.loads(meta.read_text())
    if m.get('unidade') != 'percentual_aa' or m.get('tipo') != 'APR' or not m.get('fonte') or not m.get('metodologia') or m.get('sha256') != sha256(p):
        raise ValueError('Metadados do APR Lido incompletos, unidade errada ou hash divergente.')
    df = datas_unicas(pd.read_csv(p),'APR Lido')
    cols = ['Date','apr_lido_liquido_pct','inicio_periodo_lido_utc','fim_periodo_lido_utc']
    if not set(cols).issubset(df):
        raise ValueError(f'APR Lido exige colunas {cols}')
    df = df[cols].copy()
    df['apr_lido_liquido_pct'] = pd.to_numeric(df.apr_lido_liquido_pct, errors='raise')
    for c in cols[2:]:
        df[c] = pd.to_datetime(df[c],utc=True,errors='raise').astype(str)
    inicio = pd.to_datetime(df.inicio_periodo_lido_utc, utc=True)
    fim = pd.to_datetime(df.fim_periodo_lido_utc, utc=True)
    if inicio.isna().any() or fim.isna().any() or (fim <= inicio).any():
        raise ValueError('Períodos Lido ausentes ou inválidos.')
    if not inicio.dt.strftime('%Y-%m-%d').eq(df.Date).all():
        raise ValueError('Date deve ser a data UTC de início do período Lido.')
    df['fonte_apr_lido'] = m['fonte']
    return df

def main():
    df = ler('dados_beaconchain.csv')
    # Alias legado: referência da rede; não retorno garantido de um validador solo.
    df['apr_rede_direto_total_pct'] = df.apr_rede_ethstore_pct
    lido = None if SOMENTE_BEACONCHAIN else carregar_lido_documentado()
    if lido is not None:
        df = juntar(df,lido)
    else:
        df['apr_lido_liquido_pct'] = float('nan')
        for c in ['inicio_periodo_lido_utc','fim_periodo_lido_utc','fonte_apr_lido']:
            df[c] = pd.NA
    df['status_apr_lido'] = df.apr_lido_liquido_pct.notna().map({True:'publicado_com_metadados',False:'ausente_nao_estimado'})
    salvar(df,'dados_rated_consenso.csv',['Beaconcha.in ETH.STORE; nome legado do arquivo conservado'])
if __name__ == '__main__':
    main()
