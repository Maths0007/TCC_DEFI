"""Testes de integridade e alinhamento; não usam internet nem alteram os dados."""
import importlib.util
import unittest
from pathlib import Path
import pandas as pd
import comum_tcc as c

def modulo(nome):
    spec = importlib.util.spec_from_file_location('m_'+nome, c.ROOT_DIR/(nome+'.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class Testes(unittest.TestCase):
    def test_fontes_e_hashes(self):
        manifesto = c.json.loads((c.FONTES_DIR/'manifesto.json').read_text())
        for nome, digest in manifesto['sha256'].items():
            self.assertEqual(c.sha256(c.FONTES_DIR/nome), digest)

    def test_duplicatas_rejeitadas(self):
        with self.assertRaises(ValueError):
            c.datas_unicas(pd.DataFrame({'Date':['2022-04-01']*2}), 'teste')

    def test_apr_periodos_diferentes_nao_comparados(self):
        m = modulo('04_consolidar_dataset')
        df = pd.DataFrame({'apr_rede_ethstore_pct':[5.,5.], 'apr_lido_liquido_pct':[4.,4.],
            'inicio_periodo_ethstore_utc':['2022-04-01T12:00:23Z']*2,
            'fim_periodo_ethstore_utc':['2022-04-02T12:00:23Z']*2,
            'inicio_periodo_lido_utc':['2022-04-01T12:00:23Z','2022-04-01T00:00:00Z'],
            'fim_periodo_lido_utc':['2022-04-02T12:00:23Z','2022-04-02T00:00:00Z']})
        result = m.comparar_apr(df)
        self.assertEqual(result.delta_apr_pp.iloc[0],1.)
        self.assertTrue(pd.isna(result.delta_apr_pp.iloc[1]))

    def test_precos_nao_preenchem_lacunas(self):
        m = modulo('01_coleta_precos')
        entrada = pd.DataFrame({'Date':['2022-04-01','2022-04-03'],'Close':[100.,110.]})
        result = m.processar_precos_mercado(entrada,entrada)
        self.assertTrue(pd.isna(result.loc[result.Date.eq('2022-04-02'),'preco_eth_usd']).all())
        self.assertTrue(pd.isna(result.loc[result.Date.eq('2022-04-03'),'retorno_log_eth']).all())

    def test_defillama_ultima_observacao_por_timestamp(self):
        m = modulo('03_coleta_defillama_curve')
        df = m.diario([{'t':'2022-04-01T23:00:00Z','v':2},
                       {'t':'2022-04-01T01:00:00Z','v':1}], 't', {'v':'valor'}, 'teste')
        self.assertEqual(df.valor.iloc[0],2)

    def test_completude_beaconchain_sem_lido_ou_precos(self):
        m = modulo('validar_dados_tcc')
        df = pd.DataFrame({c:[1.] for c in m.CORE})
        df['escopo_dataset'] = 'staking_apr_rede'
        erros, cols = m.verificar_completude(df)
        self.assertEqual(erros, [])
        self.assertNotIn('apr_lido_liquido_pct', cols)
        for valor in [float('nan'), float('inf')]:
            df.loc[0, 'apr_rede_ethstore_pct'] = valor
            self.assertTrue(m.verificar_completude(df)[0])

    def test_completude_mercado_continua_rigorosa(self):
        m = modulo('validar_dados_tcc')
        df = pd.DataFrame({c:[1.] for c in m.CORE})
        df['escopo_dataset'] = 'mercado_staking_defi'
        erros, cols = m.verificar_completude(df)
        self.assertTrue(erros)
        self.assertIn('delta_apr_pp', cols)
        for col in cols: df[col] = 1.
        self.assertEqual(m.verificar_completude(df)[0], [])
        df.loc[0, 'tvl_pool_curve_usd'] = float('nan')
        self.assertTrue(m.verificar_completude(df)[0])

    def test_completude_rejeita_escopo_invalido(self):
        m = modulo('validar_dados_tcc')
        for df in [pd.DataFrame(), pd.DataFrame({'escopo_dataset':['desconhecido']}),
                   pd.DataFrame({'escopo_dataset':['staking_apr_rede','mercado_staking_defi']})]:
            self.assertTrue(m.verificar_completude(df)[0])

if __name__ == '__main__': unittest.main()
