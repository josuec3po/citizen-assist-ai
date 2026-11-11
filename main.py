from base_conhecimento import BaseConhecimento
from assistente import Assistente, pedir_opcao


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    print("=" * 50)
    print(f" {assistente.nome}: orientação para pessoas idosas")
    print("=" * 50)
    print("Este assistente NÃO é um canal oficial e não pede nome, CPF,")
    print("telefone ou e-mail. Não digite dados pessoais.")

    if not base.orientacoes:
        print("\nAtenção: a base de conhecimento está vazia ou não foi carregada.")

    try:
        while True:
            print("\n--- Menu principal ---")
            print("1. Fazer uma pergunta")
            print("2. Navegar por categorias")
            print("3. Ver indicadores")
            print("4. Exportar atendimentos (CSV)")
            print("0. Sair")
            opcao = pedir_opcao("Escolha uma opção: ", 0, 4)

            if opcao == 1:
                assistente.perguntar()
            elif opcao == 2:
                assistente.navegar()
            elif opcao == 3:
                assistente.indicadores()
            elif opcao == 4:
                assistente.exportar_csv()
            else:
                assistente.pedir_nota()
                assistente.exportar_csv()
                print("\nObrigado por usar o assistente. Até logo!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\nAtendimento encerrado.")


if __name__ == "__main__":
    main()