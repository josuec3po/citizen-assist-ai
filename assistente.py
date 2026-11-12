import csv
import json
import os
import time
from datetime import datetime

PONTOS_PARA_ALTA = 6    # 6 pontos ou mais: confiança ALTA
PONTOS_MINIMOS = 3   # de 3 a 5 pontos: confiança MÉDIA; abaixo disso: não encontrei

CAMPOS_CSV = ["participante", "data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos", "sessao",
              "nota_facilidade"]


def pedir_opcao(texto, minimo, maximo):
    """Pede um número até a pessoa digitar um valor válido."""
    while True:
        valor = input(texto).strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return int(valor)
        print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")


def pedir_sim_ou_nao(texto):
    """Pede s ou n até a resposta ser válida. Devolve True para 's'."""
    while True:
        valor = input(texto).strip().lower()
        if valor in ("s", "n"):
            return valor == "s"
        print("Resposta inválida. Digite apenas s ou n.")


class Assistente:
    """Quem conversa com o cidadão: atende, guarda o histórico e calcula indicadores."""

    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv"):
        self.participante = self.proximo_participante()
        self.nome = nome
        self.base = base  # objeto BaseConhecimento (composição)
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.sessao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.historico = []
        self.carregar_historico()

    # ---------- histórico em arquivo ----------
    def carregar_historico(self):
        try:
            with open(self.caminho_historico, encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
            if conteudo.strip():
                dados = json.loads(conteudo)
                if isinstance(dados, list):
                    self.historico = dados
        except FileNotFoundError:
            pass
        except (json.JSONDecodeError, OSError):
            print("Aviso: histórico ilegível. Um novo histórico será iniciado.")

    def salvar_historico(self):
        try:
            os.makedirs(os.path.dirname(self.caminho_historico) or ".", exist_ok=True)
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo):
        """Guarda um atendimento no histórico (e no arquivo JSON)."""
        atendimento = {
            "participante": self.participante,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,                # "pergunta" ou "categoria"
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "sessao": self.sessao,
            "nota_facilidade": None,
        }
        self.historico.append(atendimento)
        self.salvar_historico()

    # ---------- regras ----------
    def contem_dado_sensivel(self, texto):
        """8 ou mais dígitos, ou um @, indica CPF, telefone ou e-mail."""
        digitos = sum(1 for letra in texto if letra.isdigit())
        return digitos >= 8 or "@" in texto

    def nivel_confianca(self, pontos):
        return "ALTA" if pontos >= PONTOS_PARA_ALTA else "MÉDIA"

    # ---------- atendimento por pergunta ----------
    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""
        ultimo_id = None
        encontrou = False

        while True:
            texto = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if texto == "0":
                if tentativas > 0:  # tentou e saiu sem resolver
                    self.registrar("pergunta", ultima_pergunta, ultimo_id,
                                   encontrou, False, tentativas,
                                   round(time.time() - inicio, 1))
                return

            if texto == "":
                print("Você não digitou nada. Escreva sua dúvida ou 0 para voltar.")
                continue

            if self.contem_dado_sensivel(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue  # não conta tentativa e não é registrado

            tentativas += 1
            ultima_pergunta = texto
            resultados = self.base.buscar(texto)

            if not resultados or resultados[0][0] < PONTOS_MINIMOS:
                encontrou = False
                ultimo_id = None
                print("\nNão encontrei uma orientação para essa dúvida.")
                sugestoes = self.base.sugerir(texto)
                if sugestoes:
                    print("\nTalvez uma destas orientações ajude. Tente escrever sobre elas:")
                    for pontos, o in sugestoes:
                        print(f"  - {o.titulo}")
                print("Tente outras palavras ou use a navegação por categorias.")
                categorias = self.base.categorias()
                if categorias:
                    print("Categorias: " + ", ".join(categorias))
                continue

            pontos, melhor = resultados[0]
            encontrou = True
            ultimo_id = melhor.id
            print(f"\nConfiança da resposta: {self.nivel_confianca(pontos)} ({pontos} pontos)")
            melhor.exibir()

            alternativas = [o for p, o in resultados[1:3] if p >= PONTOS_MINIMOS]
            if alternativas:
                print("\nOutras orientações que podem ajudar:")
                for o in alternativas:
                    print(f"  - {o.titulo}")

            ajudou = pedir_sim_ou_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            if ajudou:
                self.registrar("pergunta", texto, melhor.id, True, True,
                               tentativas, round(time.time() - inicio, 1))
                # começa um novo atendimento
                inicio = time.time()
                tentativas = 0
                ultima_pergunta = ""
                ultimo_id = None
                encontrou = False
            else:
                print("Tudo bem. Tente reescrever sua dúvida com outras palavras.")

    # ---------- atendimento por categoria ----------
    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("\nNão há categorias disponíveis no momento.")
            return

        while True:
            print("\nCategorias:")
            for i, nome in enumerate(categorias, start=1):
                print(f"  {i}. {nome}")
            print("  0. Voltar")
            escolha = pedir_opcao("Escolha uma categoria: ", 0, len(categorias))
            if escolha == 0:
                return
            self.mostrar_categoria(categorias[escolha - 1])

    def mostrar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        inicio = time.time()

        while True:
            print(f"\n{categoria}:")
            for i, o in enumerate(orientacoes, start=1):
                print(f"  {i}. {o.titulo}")
            print("  0. Voltar")
            escolha = pedir_opcao("Escolha uma orientação: ", 0, len(orientacoes))
            if escolha == 0:
                return

            orientacao = orientacoes[escolha - 1]
            orientacao.exibir()
            ajudou = pedir_sim_ou_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", "", orientacao.id, True, ajudou, 1,
                           round(time.time() - inicio, 1))
            inicio = time.time()

    # ---------- nota, indicadores e CSV ----------
    def pedir_nota(self):
        # Ao sair, pede nota de facilidade (1 a 5) se houve atendimentos, é claro
        desta_sessao = [a for a in self.historico if a.get("sessao") == self.sessao]
        if not desta_sessao:
            return
        nota = pedir_opcao("\nDe 1 a 5, quão fácil foi usar o assistente? ", 1, 5)
        for atendimento in desta_sessao:
            atendimento["nota_facilidade"] = nota
        self.salvar_historico()

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return

        encontrados = [a for a in self.historico if a.get("encontrou")]
        ajudaram = [a for a in self.historico if a.get("ajudou")]

        pct_encontrada = len(encontrados) / total * 100
        pct_acerto = len(ajudaram) / total * 100

        tempos = [a.get("tempo_segundos", 0) for a in encontrados]
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0

        tentativas_medias = sum(a.get("tentativas", 0) for a in self.historico) / total

        sessoes = {a.get("sessao") for a in self.historico}
        print(f"Sessões de uso (pessoas): {len(sessoes)}")

        # uma nota por sessão (todos os atendimentos da sessão guardam a mesma)
        notas = {}
        for a in self.historico:
            if a.get("nota_facilidade") is not None:
                notas[a.get("sessao")] = a["nota_facilidade"]
        facilidade = sum(notas.values()) / len(notas) if notas else None

        sem_solucao = []
        for a in self.historico:
            pergunta = a.get("pergunta", "")
            if not a.get("ajudou") and pergunta and pergunta not in sem_solucao:
                sem_solucao.append(pergunta)

        print(f"\n===== Indicadores ({total} atendimentos) =====")
        print(f"Resposta encontrada: {pct_encontrada:.0f}%")
        print(f"Taxa de acerto (ajudou): {pct_acerto:.0f}%")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f} s")
        print(f"Tentativas por atendimento: {tentativas_medias:.1f}")
        if facilidade is None:
            print("Facilidade de uso (1 a 5): ainda sem notas")
        else:
            print(f"Facilidade de uso (1 a 5): {facilidade:.1f} ({len(notas)} sessões)")
        if sem_solucao:
            print("Dúvidas sem solução:")
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("Dúvidas sem solução: nenhuma")

    def exportar_csv(self):
        if not self.historico:
            print("\nNão há atendimentos para exportar.")
            return
        try:
            os.makedirs(os.path.dirname(self.caminho_csv) or ".", exist_ok=True)
            # utf-8-sig para o Excel abrir os acentos corretamente
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV)
                escritor.writeheader()
                for a in self.historico:
                    linha = {campo: a.get(campo, "") for campo in CAMPOS_CSV}
                    linha["encontrou"] = "sim" if a.get("encontrou") else "nao"
                    linha["ajudou"] = "sim" if a.get("ajudou") else "nao"
                    escritor.writerow(linha)
            print(f"\nAtendimentos exportados para {self.caminho_csv}")
        except OSError:
            print("Aviso: não foi possível exportar o CSV.")
    def proximo_participante(self):
        """Código anônimo da sessão"""
        sessoes = {a.get("sessao") for a in self.historico}
        return f"P{len(sessoes) + 1:02d}"