"""Gráficos preservam lacunas e sinais; APR não é retorno acumulado."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from comum_tcc import *

def main():
    df=ler('dataset_final_tcc.csv'); x=pd.to_datetime(df.Date)
    GRAFICOS_DIR.mkdir(parents=True,exist_ok=True)
    for nome in ['staking_apr_rede.png','delta_apr.png','mercado_steth.png']:
        (GRAFICOS_DIR/nome).unlink(missing_ok=True)
    fig,ax=plt.subplots(2,1,figsize=(12,8),sharex=True)
    ax[0].plot(x,df.total_staked_eth_network/1e6,color='#245f87')
    ax[0].set_ylabel('Saldo efetivo (milhões de ETH)'); ax[0].set_title('Ethereum: staking e APR diário publicado')
    ax[1].plot(x,df.apr_rede_ethstore_pct,label='Rede — ETH.STORE',color='#245f87',lw=1)
    if df.apr_lido_liquido_pct.notna().any(): ax[1].plot(x,df.apr_lido_liquido_pct,label='Lido — fonte documentada',lw=1)
    ax[1].set_ylabel('APR (% ao ano)'); ax[1].legend()
    for a in ax: a.grid(alpha=.2)
    fig.text(.06,.02,'Fonte: Beaconcha.in. APR: períodos de 24h rotulados pela data de início (12:00:23 UTC). Sem imputação.',fontsize=9)
    fig.tight_layout(rect=(0,.05,1,1)); fig.savefig(GRAFICOS_DIR/'staking_apr_rede.png',dpi=200); plt.close(fig)
    if df.delta_apr_pp.notna().any():
        fig,ax=plt.subplots(figsize=(12,4)); ax.plot(x,df.delta_apr_pp); ax.axhline(0,color='gray',lw=.8)
        ax.set(title='Diferença APR rede − Lido, apenas períodos alinhados',ylabel='Pontos percentuais (não comissão)')
        fig.tight_layout(); fig.savefig(GRAFICOS_DIR/'delta_apr.png',dpi=200); plt.close(fig)
    if 'depeg_pct' in df and df.depeg_pct.notna().any():
        fig,ax=plt.subplots(2,1,figsize=(12,7),sharex=True)
        ax[0].plot(x,df.preco_eth_usd,label='ETH'); ax[0].plot(x,df.preco_steth_usd,label='stETH')
        ax[0].set_ylabel('Preço (USD)'); ax[0].legend()
        ax[1].plot(x,df.depeg_pct); ax[1].axhline(0,color='gray',lw=.8)
        ax[1].set_ylabel('Desvio stETH/ETH (%)')
        for a in ax: a.grid(alpha=.2)
        fig.suptitle('Fechamentos publicados pelo Yahoo Finance — lacunas preservadas')
        fig.tight_layout(); fig.savefig(GRAFICOS_DIR/'mercado_steth.png',dpi=200); plt.close(fig)
if __name__ == '__main__': main()
