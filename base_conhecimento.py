import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Pesos da pontuação (explicados no README)
PONTOS_PALAVRA_CHAVE = 3
PONTOS_PALAVRA_TITULO = 1
TAMANHO_MINIMO_PALAVRA_TITULO = 4

# Palavras genéricas ignoradas na busca flexível (sugerir)
PALAVRAS_IGNORADAS = {"como", "para", "quero", "saber", "sobre", "preciso", "onde",
                      "fazer", "tenho", "minha", "qual", "quais", "pode", "posso",
                      "gostaria", "queria", "ajuda", "idoso", "idosa", "idosos",
                      "pessoa", "pessoas", "anos", "muito", "estou"}


def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação. Devolve com espaço nas pontas
    para que a busca encontre palavras inteiras (ex.: ' sus ' e não 'susto')."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    """O conjunto de todas as orientações. Lê o JSON e faz a busca."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao (composição)

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao. Nunca trava o programa."""
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
        """Lista de categorias, sem repetir, na ordem em que aparecem."""
        nomes = []
        for o in self.orientacoes:
            if o.categoria not in nomes:
                nomes.append(o.categoria)
        return nomes

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """+3 por palavra-chave que aparece na pergunta;
        +1 por palavra da pergunta (4+ letras) que aparece no título."""
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
        """Devolve lista de tuplas (pontos, orientacao), da maior para a menor."""
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        resultados.sort(key=lambda par: par[0], reverse=True)
        return resultados

    def sugerir(self, pergunta, maximo=3):
        """Busca flexível: palavras soltas da pergunta contra categoria, título e
        palavras-chave. Só serve para sugerir, não para responder."""
        palavras = {p for p in normalizar(pergunta).split()
                    if len(p) >= 4 and p not in PALAVRAS_IGNORADAS}
        sugestoes = []
        for o in self.orientacoes:
            categoria = normalizar(o.categoria).split()
            titulo = normalizar(o.titulo).split()
            chaves = " ".join(normalizar(k) for k in o.palavras_chave).split()
            pontos = 0
            for p in palavras:
                if p in categoria:
                    pontos += 2
                if p in titulo:
                    pontos += 1
                if p in chaves:
                    pontos += 1
            if pontos > 0:
                sugestoes.append((pontos, o))
        sugestoes.sort(key=lambda par: par[0], reverse=True)
        return sugestoes[:maximo]