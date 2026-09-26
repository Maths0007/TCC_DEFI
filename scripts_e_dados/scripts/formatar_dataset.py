"""Ordena colunas sem arredondar, preencher ou remover informação."""
from comum_tcc import *

def main():
    nome='dataset_final_tcc.csv'
    df=ler(nome)
    meta=json.loads((DADOS_DIR/Path(nome).with_suffix('.metadados.json')).read_text())
    primeiras=['Date','total_staked_eth_network','apr_rede_ethstore_pct','preco_eth_usd','preco_steth_usd','preco_steth_eth','depeg_pct','retorno_log_eth','retorno_log_steth','volatilidade_30d_anual_eth','volatilidade_30d_anual_steth','apr_lido_liquido_pct','delta_apr_pp']
    ordem=[c for c in primeiras if c in df]+[c for c in df if c not in primeiras]
    salvar(df[ordem],nome,meta['fontes'])
if __name__ == '__main__': main()
