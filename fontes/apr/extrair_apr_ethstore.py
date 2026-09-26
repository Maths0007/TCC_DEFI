"""Extrai dados ETH.STORE de HTML fornecido, sem executar JavaScript.
Uso: python extrair_apr_ethstore.py fonte_ethstore.html --saida resultados_apr
"""
import argparse
import csv
import hashlib
import json
import math
import re
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

class Fonte(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ativo = False
        self.linhas = []
    def handle_starttag(self, tag, attrs):
        if tag == 'td' and 'line-content' in dict(attrs).get('class', '').split():
            self.ativo = True
            self.linhas.append('')
    def handle_endtag(self, tag):
        if tag == 'td':
            self.ativo = False
    def handle_data(self, texto):
        if self.ativo:
            self.linhas[-1] += texto

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('--saida', type=Path, default=Path('resultados_apr'))
    args = parser.parse_args()
    bruto = args.html.read_bytes()
    texto = bruto.decode('utf-8-sig')
    fonte = Fonte()
    fonte.feed(texto)
    texto = '\n'.join(fonte.linhas) if fonte.linhas else texto
    series = {}
    for m in re.finditer(r"name:\s*'([^']+)'\s*,\s*(?:visible:\s*false,\s*)?data:\s*", texto):
        nome = m[1]
        if nome not in ['ETH.STORE®', 'Total Staking Rewards', 'Total Effective Balance']:
            continue
        dados, _ = json.JSONDecoder().raw_decode(texto[m.end():])
        if nome in series:
            raise ValueError(f'Série duplicada: {nome}')
        for t, v in dados:
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError(f'Valor inválido em {nome}')
        if len(dict(dados)) != len(dados):
            raise ValueError(f'Timestamp duplicado em {nome}')
        series[nome] = dict(dados)
    if len(series) != 3:
        raise ValueError('Uma ou mais séries estão ausentes.')
    inicio, fim = date(2022, 4, 1), date(2026, 5, 31)
    registros, erros, dias = [], [], []
    for t, taxa in sorted(series['ETH.STORE®'].items()):
        momento = datetime.fromtimestamp(t / 1000, timezone.utc)
        dia = momento.date()
        if not inicio <= dia <= fim:
            continue
        recompensa = series['Total Staking Rewards'][t]
        saldo = series['Total Effective Balance'][t]
        if saldo <= 0:
            raise ValueError('Saldo efetivo não positivo.')
        recalculada = recompensa / saldo * 365 * 100
        erros.append(abs(taxa - recalculada))
        dias.append(dia)
        registros.append([str(dia), taxa, momento.isoformat(), t, recompensa, saldo])
    if len(set(dias)) != len(dias):
        raise ValueError('Datas duplicadas no período.')
    esperadas = [inicio + timedelta(days=i) for i in range((fim-inicio).days+1)]
    faltantes = [str(d) for d in esperadas if d not in set(dias)]
    args.saida.mkdir(parents=True, exist_ok=True)
    destino = args.saida / 'apr_ethstore_2022-04_2026-05.csv'
    with destino.open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['data_inicio_periodo_utc', 'apr_ethstore_percentual_aa', 'inicio_periodo_utc', 'timestamp_fonte_ms', 'recompensas_periodo_eth', 'saldo_efetivo_ethstore_eth'])
        escritor.writerows(registros)
    relatorio = {
        'fonte': 'https://www.beaconcha.in/ethstore',
        'entrada': args.html.name,
        'sha256_html': hashlib.sha256(bruto).hexdigest(),
        'sha256_csv': hashlib.sha256(destino.read_bytes()).hexdigest(),
        'inicio': str(inicio), 'fim': str(fim),
        'dias_esperados': len(esperadas), 'registros': len(registros),
        'datas_ausentes': faltantes, 'datas_duplicadas': [],
        'formula_percentual': 'recompensas_periodo_eth / saldo_efetivo_ethstore_eth * 365 * 100',
        'erro_maximo_formula_pontos_percentuais': max(erros) if erros else None,
        'divergencias_acima_de_0_000501_pp': sum(e > 0.000501 for e in erros),
        'precisao_publicada': 'Três casas decimais em pontos percentuais; zeros finais podem ser omitidos.',
        'periodo_de_rendimento': '24 horas iniciadas às 12:00:23 UTC; a data do CSV é a data de início.',
        'tratamento': 'Extração, filtro por data de início e ordenação. Valores publicados mantidos sem interpolação ou preenchimento.',
        'limitacao': 'Conferência de fidelidade ao HTML recebido e consistência interna da fórmula; não é auditoria on-chain independente.',
        'processado_em_utc': datetime.now(timezone.utc).isoformat()
    }
    (args.saida / 'validacao_apr.json').write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
