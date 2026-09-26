"""Extrai a série Staked ETH de um HTML salvo do Beaconcha.in.
Não executa JavaScript, não faz requisições e não preenche dados ausentes.
Uso: python extrair_staking_beaconchain.py arquivo.html --saida resultados
"""
import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

class FonteSalva(HTMLParser):
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
    parser.add_argument('--saida', type=Path, default=Path('resultados'))
    args = parser.parse_args()
    bruto = args.html.read_bytes()
    texto = bruto.decode('utf-8-sig')
    fonte = FonteSalva()
    fonte.feed(texto)
    texto = '\n'.join(fonte.linhas) if fonte.linhas else texto
    correspondencias = list(re.finditer(r'series:\s*(\[\{"name":"Staked ETH")', texto))
    if len(correspondencias) != 1:
        raise ValueError('Série Staked ETH ausente ou ambígua no HTML.')
    series, _ = json.JSONDecoder().raw_decode(texto[correspondencias[0].start(1):])
    serie = [s for s in series if s.get('name') == 'Staked ETH']
    if len(serie) != 1:
        raise ValueError('Número inesperado de séries Staked ETH.')
    pontos = serie[0]['data']
    inicio, fim = date(2022, 4, 1), date(2026, 5, 31)
    registros = []
    for timestamp, valor in pontos:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not math.isfinite(valor) or valor <= 0:
            raise ValueError('Valor numérico inválido na série.')
        momento = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        if inicio <= momento.date() <= fim:
            registros.append((momento.date(), valor, timestamp))
    registros.sort()
    contagens = Counter(r[0] for r in registros)
    duplicadas = [str(d) for d, n in contagens.items() if n > 1]
    if duplicadas:
        raise ValueError(f'Datas duplicadas: {duplicadas}')
    esperadas = [inicio + timedelta(days=i) for i in range((fim-inicio).days+1)]
    faltantes = [str(d) for d in esperadas if d not in contagens]
    repetidos = [str(registros[i][0]) for i in range(1, len(registros))
                 if registros[i][0] - registros[i-1][0] == timedelta(days=1)
                 and registros[i][1] == registros[i-1][1]]
    args.saida.mkdir(parents=True, exist_ok=True)
    nome = 'eth_staking_beaconchain_2022-04_2026-05.csv'
    destino = args.saida / nome
    with destino.open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['data_utc', 'eth_saldo_efetivo_fonte', 'timestamp_fonte_ms'])
        escritor.writerows((str(d), v, t) for d, v, t in registros)
    relatorio = {
        'fonte_declarada': 'https://beaconcha.in/charts/staked_ether',
        'entrada': args.html.name,
        'sha256_html': hashlib.sha256(bruto).hexdigest(),
        'sha256_csv': hashlib.sha256(destino.read_bytes()).hexdigest(),
        'serie': 'Staked ETH',
        'definicao_literal_fonte': 'History of daily staked ETH, which is the sum of all Effective Balances.',
        'inicio': str(inicio), 'fim': str(fim),
        'dias_esperados': len(esperadas), 'registros_extraidos': len(registros),
        'datas_ausentes': faltantes, 'datas_duplicadas': duplicadas,
        'datas_com_valor_igual_ao_dia_anterior': repetidos,
        'pontos_na_serie_original': len(pontos),
        'processado_em_utc': datetime.now(timezone.utc).isoformat(),
        'tratamento': 'Filtro de período, ordenação e conversão do timestamp para data UTC. Valores mantidos sem arredondamento, interpolação ou preenchimento.',
        'limites': 'Valida a fidelidade da extração ao HTML fornecido pelo usuário. Não audita a blockchain nem a metodologia histórica do provedor. Timestamp à meia-noite pode representar rótulo diário, não horário de observação.'
    }
    (args.saida / 'validacao_extracao.json').write_text(json.dumps(relatorio, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: relatorio[k] for k in ['dias_esperados','registros_extraidos','datas_ausentes','datas_duplicadas','sha256_csv']}, indent=2))

if __name__ == '__main__':
    main()
