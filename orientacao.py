class Orientacao:
    # Inicializar classe
    def __init__(self, id, categoria, titulo, palavras_chave,
                 resposta, documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        # Orientação na tela, com fonte, data e aviso.
        print(f"\n>> {self.titulo}  [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for doc in self.documentos:
            print(f"  - {doc}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.")