import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Pesos da pontuação (explicados no README)
PONTOS_PALAVRA_CHAVE = 3
PONTOS_PALAVRA_TITULO = 1
TAMANHO_MINIMO_PALAVRA_TITULO = 4


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    # Lê o JSON e faz a busca. -> conjunto das orientações"""

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao (composição)

    def carregar(self):
       # Lê o JSON e cria os objetos Orientacao. 
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print("Aviso: arquivo da base de conhecimento não encontrado.")
            return
        except (json.JSONDecodeError, OSError):
            print("Aviso: arquivo da base de conhecimento ausente ou corrompido.")
            return

        if not isinstance(dados, list):
            print("Aviso: o JSON da base deve ser uma lista de orientações.")
            return

        self.orientacoes = []
        for registro in dados:
            try:
                self.orientacoes.append(Orientacao(**registro))
            except TypeError:
                print("Aviso: um registro com campos incorretos foi ignorado.")

    def categorias(self):
        # Lista de categorias, sem repetir, na ordem em que aparecem
        nomes = []
        for o in self.orientacoes:
            if o.categoria not in nomes:
                nomes.append(o.categoria)
        return nomes

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        # +3 por palavra-chave que aparece na pergunta, 
        # +1 por palavra da pergunta (4+ letras) que aparece no título.
        pergunta_norm = normalizar(pergunta)
        pontos = 0

        for palavra in orientacao.palavras_chave:
            if normalizar(palavra) in pergunta_norm:
                pontos += PONTOS_PALAVRA_CHAVE

        titulo_norm = normalizar(orientacao.titulo)
        for palavra in pergunta_norm.split():
            if (len(palavra) >= TAMANHO_MINIMO_PALAVRA_TITULO
                    and (" " + palavra + " ") in titulo_norm):
                pontos += PONTOS_PALAVRA_TITULO

        return pontos

    def buscar(self, pergunta):
        # tuplas (pontos, orientacao) ordem maior -> menor"""
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        resultados.sort(key=lambda par: par[0], reverse=True)
        return resultados