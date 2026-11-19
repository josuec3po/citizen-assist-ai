from base_conhecimento import BaseConhecimento

base = BaseConhecimento("data/base_conhecimento.json")
base.carregar()

while True:
    pergunta = input("\nPergunta (0 para sair): ")
    if pergunta == "0":
        break
    resultados = base.buscar(pergunta)
    if not resultados:
        print("  Nenhuma orientação pontuou.")
    for pontos, o in resultados:
        print(f"  {pontos} pontos -> [{o.id}] {o.titulo}")