"""Fechamentos Yahoo, sem mesclar snapshots de meia-noite de outra fonte.
Retornos abaixo são retornos de preço; não incluem o rebase do stETH.
"""
import json
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from comum_tcc import *

def download_yfinance_ticker(ticker, start, end):
    chave = f'yahoo_{ticker}_{start}_{end}'
    path = CACHE_DIR / (chave + '.csv')
    meta = path.with_suffix('.meta.json')
    if path.exists():
        if not meta.exists() or json.loads(meta.read_text())['sha256'] != sha256(path):
            raise ValueError('Cache de preços alterado ou sem metadados.')
        return datas_unicas(pd.read_csv(path), ticker)
    if OFFLINE:
        raise FileNotFoundError(f'Cache de preços ausente: {path}')
    try:
        import yfinance as yf
    except ImportError as e:
        raise RuntimeError('Instale requirements.txt para coletar preços online.') from e
    raw = yf.download(ticker, start=start, end=(pd.Timestamp(end)+pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
                      auto_adjust=False, repair=False, rounding=False, keepna=True, progress=False, timeout=25)
    if raw is None or raw.empty:
        raise ValueError(f'Yahoo não retornou preços de {ticker}. Não há fallback ou dados inventados.')
    close = raw['Close']
    if isinstance(close, pd.DataFrame):
        close = close[ticker]
    df = pd.DataFrame({'Date':pd.to_datetime(raw.index, utc=True).strftime('%Y-%m-%d'), 'Close':close.to_numpy()})
    df = datas_unicas(df, ticker)
    if (df.Close.dropna() <= 0).any():
        raise ValueError('Preço não positivo.')
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    raw.to_csv(CACHE_DIR/(chave+'.resposta.csv'))
    df.to_csv(path, index=False)
    salvar_json(meta, {'ticker':ticker,'provedor':'Yahoo Finance via yfinance', 'yfinance_version':yf.__version__,
        'inicio':start,'fim_inclusivo':end,'sha256':sha256(path), 'auto_adjust':False,'repair':False,
        'coletado_em_utc':datetime.now(timezone.utc).isoformat(),
        'observacao':'Date preserva o rótulo diário do provedor; não é alinhamento intradiário com ETH.STORE.'})
    return df

def processar_precos_mercado(eth, steth):
    start = (pd.Timestamp(DATA_INICIO)-pd.Timedelta(days=31)).strftime('%Y-%m-%d')
    df = pd.DataFrame({'Date':pd.date_range(start, DATA_FIM).strftime('%Y-%m-%d')})
    for token, data in [('eth',eth),('steth',steth)]:
        data = datas_unicas(data,token).rename(columns={'Close':f'preco_{token}_usd'})
        df = juntar(df, data[['Date',f'preco_{token}_usd']])
        price = df[f'preco_{token}_usd']
        if (price.dropna() <= 0).any():
            raise ValueError(f'Preço inválido: {token}')
        df[f'fonte_preco_{token}'] = pd.Series('Yahoo Finance via yfinance', index=df.index).where(price.notna())
        df[f'retorno_log_{token}'] = np.log(price / price.shift())
        for window in [7,30]:
            df[f'volatilidade_{window}d_anual_{token}'] = df[f'retorno_log_{token}'].rolling(window,min_periods=window).std(ddof=1)*np.sqrt(365)*100
    df['preco_steth_eth'] = df.preco_steth_usd / df.preco_eth_usd
    df['liquid_staking_basis'] = df.preco_steth_eth-1
    df['depeg_pct'] = df.liquid_staking_basis*100
    return df[df.Date.between(DATA_INICIO,DATA_FIM)].reset_index(drop=True)

def main():
    start = (pd.Timestamp(DATA_INICIO)-pd.Timedelta(days=31)).strftime('%Y-%m-%d')
    eth = download_yfinance_ticker('ETH-USD',start,DATA_FIM)
    steth = download_yfinance_ticker('STETH-USD',start,DATA_FIM)
    salvar(processar_precos_mercado(eth,steth),'dados_precos_mercado.csv', ['Yahoo Finance: ETH-USD e STETH-USD; 31 dias de aquecimento'])
if __name__ == '__main__':
    main()
