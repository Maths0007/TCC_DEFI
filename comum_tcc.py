"""Configuração e operações compartilhadas da pipeline do TCC."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
if ROOT_DIR.name == 'scripts' and ROOT_DIR.parent.name == 'scripts_e_dados':
    ROOT_DIR = ROOT_DIR.parent.parent
elif ROOT_DIR.name == 'scripts_e_dados':
    ROOT_DIR = ROOT_DIR.parent
DATA_INICIO = os.environ.get('TCC_DATA_INICIO', '2022-05-01')
DATA_FIM = os.environ.get('TCC_DATA_FIM', '2026-05-31')
if not ('2022-04-01' <= DATA_INICIO <= DATA_FIM <= '2026-05-31'):
    raise ValueError('Período deve estar entre 2022-04-01 e 2026-05-31.')
OFFLINE = os.environ.get('TCC_OFFLINE', '0') == '1'
SOMENTE_BEACONCHAIN = os.environ.get('TCC_SOMENTE_BEACONCHAIN', '0') == '1'
def caminho(chave, padrao):
    p = Path(os.environ.get(chave, str(padrao))).expanduser()
    return p if p.is_absolute() else ROOT_DIR / p
FONTES_DIR = caminho('TCC_FONTES_DIR', ROOT_DIR/'fontes')
DADOS_DIR = caminho('TCC_DADOS_DIR', ROOT_DIR/'scripts_e_dados'/('Dados_beaconchain' if SOMENTE_BEACONCHAIN else 'Dados'))
CACHE_DIR = caminho('TCC_CACHE_DIR', ROOT_DIR/'cache')
GRAFICOS_DIR = DADOS_DIR/'graficos'
# Os IDs dos pools não estavam nos arquivos recebidos. Informe os pools da pesquisa.
LIDO_POOL_UUID = os.environ.get('TCC_LIDO_POOL_UUID', '')
CURVE_STETH_POOL_UUID = os.environ.get('TCC_CURVE_STETH_POOL_UUID', '')

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def salvar_json(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def grid():
    return pd.DataFrame({'Date':pd.date_range(DATA_INICIO, DATA_FIM).strftime('%Y-%m-%d')})

def datas_unicas(df, nome):
    df = df.copy()
    if 'Date' not in df: raise ValueError(f'{nome}: coluna Date ausente')
    datas = pd.to_datetime(df.Date, format='%Y-%m-%d', errors='raise')
    if datas.isna().any() or datas.duplicated().any():
        raise ValueError(f'{nome}: datas ausentes ou duplicadas')
    df['Date'] = datas.dt.strftime('%Y-%m-%d')
    return df.sort_values('Date').reset_index(drop=True)

def juntar(base, novo):
    base = datas_unicas(base, 'base'); novo = datas_unicas(novo, 'entrada')
    comuns = (set(base) & set(novo)) - {'Date'}
    if comuns: raise ValueError(f'Colunas sobrepostas: {sorted(comuns)}')
    return base.merge(novo, on='Date', how='left', validate='one_to_one')

def salvar(df, nome, fontes):
    df = datas_unicas(df, nome)
    DADOS_DIR.mkdir(parents=True, exist_ok=True)
    path = DADOS_DIR/nome
    df.to_csv(path, index=False, encoding='utf-8')
    salvar_json(path.with_suffix('.metadados.json'), {'arquivo':nome, 'sha256':sha256(path),
        'fontes':fontes, 'linhas':len(df), 'inicio':DATA_INICIO, 'fim':DATA_FIM,
        'gerado_em_utc':datetime.now(timezone.utc).isoformat()})

def ler(nome):
    path = DADOS_DIR/nome
    meta = json.loads(path.with_suffix('.metadados.json').read_text(encoding='utf-8'))
    if meta['sha256'] != sha256(path): raise ValueError(f'Arquivo alterado: {nome}')
    return datas_unicas(pd.read_csv(path), nome)

def obter_json(url, chave):
    path = CACHE_DIR/(chave+'.json'); meta = path.with_suffix('.meta.json')
    if path.exists():
        m = json.loads(meta.read_text(encoding='utf-8'))
        if m.get('sha256') != sha256(path) or m.get('url') != url:
            raise ValueError(f'Cache inválido ou de outra URL: {path}')
        return json.loads(path.read_text(encoding='utf-8'))
    if OFFLINE: raise FileNotFoundError(f'Cache ausente no modo offline: {path}')
    import requests
    response = requests.get(url, timeout=60); response.raise_for_status()
    data = response.json()
    salvar_json(path, data)
    salvar_json(meta, {'url':url, 'sha256':sha256(path), 'coletado_em_utc':datetime.now(timezone.utc).isoformat()})
    return data
