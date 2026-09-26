"""TVL e taxas publicadas no DefiLlama. Sem interpolação ou conversão APY→APR.
O campo chamado apy pelo agregador é preservado como taxa reportada no caso Lido.
O adaptador atual usa APR de Lido; isso não valida a semântica do histórico inteiro.
"""
import pandas as pd
from comum_tcc import *

def diario(records, data_col, fields, nome, unix=False):
    if not records:
        raise ValueError(f'{nome}: resposta vazia')
    df = pd.DataFrame(records)
    timestamp = pd.to_datetime(pd.to_numeric(df[data_col]) if unix else df[data_col],
                               unit='s' if unix else None, utc=True, errors='raise')
    if timestamp.isna().any() or timestamp.duplicated().any():
        raise ValueError(f'{nome}: timestamps ausentes ou duplicados')
    result = pd.DataFrame({'Date':timestamp.dt.strftime('%Y-%m-%d'), '_timestamp':timestamp})
    for orig, dest in fields.items():
        if orig not in df:
            raise ValueError(f'{nome}: campo ausente {orig}')
        result[dest] = pd.to_numeric(df[orig],errors='raise')
    # Se mais de uma coleta no dia, usa a última por timestamp, nunca ordem da resposta.
    result = result.sort_values('_timestamp').drop_duplicates('Date', keep='last')
    result[f'timestamp_{nome}_utc'] = result.pop('_timestamp').astype(str)
    return datas_unicas(result,nome)

def main():
    if not LIDO_POOL_UUID or not CURVE_STETH_POOL_UUID:
        raise ValueError('Configure TCC_LIDO_POOL_UUID e TCC_CURVE_STETH_POOL_UUID com os pools da pesquisa. '
                         'Para usar apenas os ZIPs: python executar_pipeline.py --somente-beaconchain --offline')
    urls = {
        'ethereum_tvl':'https://api.llama.fi/charts/Ethereum',
        'lido_tvl':'https://api.llama.fi/protocol/lido',
        'lido_yields':f'https://yields.llama.fi/chart/{LIDO_POOL_UUID}',
        'curve_yields':f'https://yields.llama.fi/chart/{CURVE_STETH_POOL_UUID}'}
    data = {}
    for key,url in urls.items():
        print(f'Obtendo {key}...', flush=True)
        data[key] = obter_json(url,key)
    lido = data['lido_tvl']
    df = juntar(grid(), diario(data['ethereum_tvl'],'date',{'totalLiquidityUSD':'tvl_rede_ethereum_total_usd'},'ethereum_tvl',True))
    df = juntar(df, diario(lido['tvl'],'date',{'totalLiquidityUSD':'tvl_lido_total_usd'},'lido_tvl',True))
    df = juntar(df, diario(lido['chainTvls']['Ethereum']['tvl'],'date',{'totalLiquidityUSD':'tvl_lido_ethereum_usd'},'lido_ethereum_tvl',True))
    df = juntar(df, diario(data['lido_yields']['data'],'timestamp',{'apy':'taxa_lido_reportada_defillama_pct','tvlUsd':'tvl_yield_pool_usd'},'lido_yields'))
    df = juntar(df, diario(data['curve_yields']['data'],'timestamp',{'apy':'apy_pool_curve_pct','tvlUsd':'tvl_pool_curve_usd'},'curve_yields'))
    df['dominancia_lido_tvl_defi_pct'] = df.tvl_lido_ethereum_usd.div(df.tvl_rede_ethereum_total_usd.where(df.tvl_rede_ethereum_total_usd>0))*100
    for c in ['tvl_rede_ethereum_total_usd','tvl_lido_total_usd','tvl_lido_ethereum_usd','tvl_yield_pool_usd','tvl_pool_curve_usd']:
        if (df[c].dropna()<0).any():
            raise ValueError(f'TVL negativo: {c}')
    df['fonte_taxa_lido_defillama'] = urls['lido_yields']
    df['fonte_tvl_ethereum'] = urls['ethereum_tvl']
    df['fonte_tvl_lido'] = urls['lido_tvl']
    df['fonte_curve'] = urls['curve_yields']
    df['semantica_taxa_lido_defillama'] = 'campo apy do agregador; sem conversao automatica; metodologia historica pendente'
    salvar(df,'dados_defillama_curve.csv',urls)
if __name__ == '__main__':
    main()
