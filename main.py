import json
from orientacao import Orientacao

with open("data/base_conhecimento.json", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

primeiro = dados[0]              # um dicionário
o = Orientacao(**primeiro)       # desempacota o dicionário nos 9 parâmetros
o.exibir()