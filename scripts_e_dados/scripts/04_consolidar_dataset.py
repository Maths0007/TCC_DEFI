"""Consolidação sem preenchimento de lacunas ou comissão inferida."""
from comum_tcc import *

def comparar_apr(df):
    df = df.copy()
    alinhada = df.apr_lido_liquido_pct.notna() & df.apr_rede_ethstore_pct.notna()
    for parte in ('inicio','fim'):
        rede = pd.to_datetime(df[f'{parte}_periodo_ethstore_utc'],utc=True,errors='raise')
        lido = pd.to_datetime(df[f'{parte}_periodo_lido_utc'],utc=True,errors='raise')
        alinhada &= rede.notna() & lido.notna() & rede.eq(lido)
    df['comparacao_apr_alinhada'] = alinhada.astype(int)
    df['delta_apr_pp'] = (df.apr_rede_ethstore_pct-df.apr_lido_liquido_pct).where(alinhada)
    return df

def main():
    df = juntar(grid(),ler('dados_rated_consenso.csv'))
    fontes = ['dados_rated_consenso.csv']
    if not SOMENTE_BEACONCHAIN:
        for nome in ['dados_precos_mercado.csv','dados_defillama_curve.csv']:
            df = juntar(df,ler(nome)); fontes.append(nome)
    elif (DADOS_DIR/'dados_precos_mercado.csv').exists():
        df = juntar(df,ler('dados_precos_mercado.csv')); fontes.append('dados_precos_mercado.csv')
    df = comparar_apr(df)
    df['escopo_dataset'] = 'staking_apr_rede' if SOMENTE_BEACONCHAIN else 'mercado_staking_defi'
    df['status_comparacao_apr'] = df.comparacao_apr_alinhada.map({1:'periodos_alinhados',0:'indisponivel_sem_dados_comparaveis'})
    salvar(df,'dataset_final_tcc.csv',fontes)
if __name__ == '__main__': main()
