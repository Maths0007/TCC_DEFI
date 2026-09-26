"""Auditoria de integridade; lacunas declaradas não equivalem a observações."""
import argparse
from comum_tcc import *

CORE=['total_staked_eth_network','apr_rede_ethstore_pct','recompensas_ethstore_eth','saldo_efetivo_elegivel_ethstore_eth']
def verificar(df, fonte):
    erros=[]
    if df.Date.tolist()!=grid().Date.tolist(): erros.append('Calendário incompleto ou divergente')
    if df[CORE].isna().any().any(): erros.append('Lacunas nas séries Beaconcha.in')
    if not np.isfinite(df[CORE].to_numpy(dtype=float)).all(): erros.append('Valores não finitos nas séries principais')
    if (df[['total_staked_eth_network','saldo_efetivo_elegivel_ethstore_eth']]<=0).any().any(): erros.append('Saldo não positivo')
    calc=df.recompensas_ethstore_eth/df.saldo_efetivo_elegivel_ethstore_eth*36500
    if not np.allclose(calc,df.apr_rede_ethstore_pct,atol=.000501,rtol=0): erros.append('Fórmula ETH.STORE divergente')
    if not np.allclose(df.apr_rede_direto_total_pct,df.apr_rede_ethstore_pct,rtol=0,atol=0): erros.append('APR da rede alterado')
    if df.Date.tolist()!=fonte.Date.tolist() or not np.allclose(df[CORE],fonte[CORE],rtol=1e-14,atol=1e-12): erros.append('Valores diferem da extração')
    alinhada=df.apr_lido_liquido_pct.notna()
    for parte in ('inicio','fim'):
        a=pd.to_datetime(df[f'{parte}_periodo_ethstore_utc'],utc=True)
        b=pd.to_datetime(df[f'{parte}_periodo_lido_utc'],utc=True)
        alinhada &= a.notna() & b.notna() & a.eq(b)
    esperado=(df.apr_rede_ethstore_pct-df.apr_lido_liquido_pct).where(alinhada)
    if not np.allclose(df.delta_apr_pp,esperado,equal_nan=True) or not df.comparacao_apr_alinhada.eq(alinhada.astype(int)).all(): erros.append('Comparação APR inválida')
    proibidas={'taxa_retencao_efetiva_pct','apr_mev_pct','custo_oportunidade_acumulado'}
    if proibidas.intersection(df): erros.append('Colunas legadas sem metodologia válida')
    return erros

def verificar_completude(df):
    """Exige as séries do escopo registrado no dataset, sem preencher lacunas."""
    if 'escopo_dataset' not in df or df.escopo_dataset.isna().any():
        return ['Escopo do dataset ausente'], []
    escopos = df.escopo_dataset.unique().tolist()
    if len(escopos) != 1 or escopos[0] not in ('staking_apr_rede', 'mercado_staking_defi'):
        return ['Escopo do dataset inválido ou misturado'], []
    obrigatorias = list(CORE)
    if escopos[0] == 'mercado_staking_defi':
        obrigatorias += ['apr_lido_liquido_pct', 'delta_apr_pp',
                         'preco_eth_usd', 'preco_steth_usd',
                         'tvl_rede_ethereum_total_usd', 'tvl_lido_total_usd',
                         'tvl_lido_ethereum_usd', 'taxa_lido_reportada_defillama_pct',
                         'tvl_yield_pool_usd', 'apy_pool_curve_pct', 'tvl_pool_curve_usd']
    erros = []
    for coluna in obrigatorias:
        if coluna not in df:
            erros.append(f'Completude exigida: coluna ausente {coluna}')
        else:
            valores = pd.to_numeric(df[coluna], errors='coerce').to_numpy(dtype=float)
            invalidos = int((~np.isfinite(valores)).sum())
            if invalidos:
                erros.append(f'Completude exigida: {coluna} ({invalidos} ausentes ou inválidos)')
    return erros, obrigatorias

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--exigir-completo',action='store_true'); args=parser.parse_args()
    erros=[]; cobertura={}; obrigatorias=[]; erros_completude=[]; erros_integridade=[]
    try:
        df=ler('dataset_final_tcc.csv'); fonte=ler('dados_beaconchain.csv')
        erros_integridade=verificar(df,fonte)
        erros.extend(erros_integridade)
        cobertura={c:{'observados':int(df[c].notna().sum()),'ausentes':int(df[c].isna().sum())} for c in df}
        if args.exigir_completo:
            erros_completude, obrigatorias = verificar_completude(df)
            erros.extend(erros_completude)
    except Exception as exc:
        erros_integridade.append(str(exc)); erros.append(str(exc))
    salvar_json(DADOS_DIR/'auditoria_tcc.json',{
        'aprovado':not erros,
        'aprovado_integridade':not erros_integridade,
        'completude_exigida':args.exigir_completo,
        'aprovado_completude':(not erros_completude and not erros_integridade) if args.exigir_completo else None,
        'colunas_completude_exigidas':obrigatorias,
        'erros':erros,'cobertura':cobertura,
        'limite':'Consistência interna e fidelidade à extração; não auditoria independente da blockchain. Ausentes permanecem ausentes.'})
    print('Auditoria: '+('APROVADA (ver cobertura)' if not erros else '; '.join(erros)))
    return 1 if erros else 0
if __name__ == '__main__': raise SystemExit(main())
