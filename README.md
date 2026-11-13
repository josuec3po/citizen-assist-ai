# Elderly Assist(Citizen Assist AI)

Assistente de terminal em Python, Citizen Assist AI que resolvemos chamar também de Elderly Assist, orienta **pessoas idosas** sobre saúde, transporte,
direitos e benefícios e golpes, usando apenas uma base de conhecimento verificada em fontes oficiais.

## Integrantes
- Josué Franco Braga — RM 569174
- Manoel da Silva Ferreira — RM 572045
- Fernando Lobato Rodrigues — RM 569377

## Público e problema
- **Público:** pessoas idosas (50 anos ou mais) e seus familiares.
- **Problema:** a informação sobre Cartão SUS, vacinas, benefícios do INSS, transporte e golpes
  existe, mas está espalhada, em linguagem técnica e misturada com páginas falsas.

## ODS relacionados
**ODS 3, Saúde e Bem-Estar (meta 3.8):** o assistente orienta pessoas idosas sobre
Cartão SUS, vacinas e remédios gratuitos pelo Farmácia Popular, o que facilita o
acesso a serviços de saúde, medicamentos e vacinas.

**ODS 10, Redução das Desigualdades (meta 10.2):** reúne em linguagem simples direitos
e benefícios (aposentadoria, BPC, transporte gratuito, atendimento prioritário) que
muitas pessoas idosas, sobretudo as com pouco acesso digital, têm dificuldade de
encontrar, promovendo inclusão independentemente da idade.

**ODS 16, Paz, Justiça e Instituições Eficazes (metas 16.10 e 16.1):** dá acesso
público a informação confiável, sempre com fonte oficial e data de verificação, e
orienta sobre como denunciar violência contra a pessoa idosa e como evitar golpes.

## Como executar
Requisitos: Python 3 (somente biblioteca padrão, sem instalar nada).

```
cd citizen-assist-ai
python main.py
```
Execute sempre dentro da pasta do projeto, porque os caminhos de `data/` são relativos.

## Estrutura
```
citizen-assist-ai/
├── README.md
├── main.py               # menu principal
├── orientacao.py         # classe Orientacao
├── base_conhecimento.py  # classe BaseConhecimento + normalizar()
├── assistente.py         # classe Assistente
└── data/
    ├── base_conhecimento.json   # 12 orientações, 4 categorias
    ├── historico.json           # atendimentos (criado/atualizado pelo programa)
    └── atendimentos.csv         # exportação dos atendimentos
```

## Regra de pontuação
Pergunta e títulos/palavras-chave são normalizados (minúsculas, sem acento, sem pontuação).
- Palavra-chave da orientação que aparece na pergunta: **+3 pontos**
- Palavra da pergunta (4 letras ou mais) que aparece no título: **+1 ponto**
- Melhor orientação com **6 pontos ou mais**: confiança **ALTA**
- Melhor orientação com **3 a 5 pontos**: confiança **MÉDIA**
- Menos de 3 pontos: "não encontrei", com sugestão de outras palavras e das categorias
- O assistente mostra a melhor orientação e até duas alternativas com 3 pontos ou mais.

## Privacidade e transparência
- O assistente nunca pede nome, CPF, telefone ou e-mail.
- Pergunta com 8 ou mais dígitos ou com `@` é recusada e **não** é registrada.
- Toda resposta mostra fonte, data de verificação e o aviso de que não é canal oficial.

## Integrações com outras disciplinas

## Fontes consultadas
- Ministério da Saúde (gov.br/saude): Meu SUS Digital, calendário de vacinação do idoso, Farmácia Popular
- Estatuto da Pessoa Idosa (Lei 10.741/2003, planalto.gov.br)
- INSS (gov.br/inss)
- Ministério dos Direitos Humanos (Disque 100)


## Teste com usuários
- Pessoas de fora da equipe: 3
- Atendimentos totais: 3
- Indicadores obtidos: -
- Dúvidas sem solução: -
- Melhoria feita a partir do teste: 
  - 9/11 - Uma pessoa digitou só "transporte" e o assistente não encontrou (1 ponto, abaixo do
    mínimo de 3). Adicionamos a palavra-chave "transporte" às orientações 5 e 6; agora a mesma
    pergunta dá 4 pontos e a orientação é mostrada.
- Não registrar nomes nem dados das pessoas testadas.

## Limitações
- Só responde o que está na base (12 orientações) e não entende sinônimos ou erros de digitação
  que não estejam nas palavras-chave.
- A busca compara palavras exatas: "vacinas" e "vacina" precisam estar ambas na lista.
- O conteúdo é nacional; regras locais (como transporte municipal) variam por cidade.
- As informações mudam com o tempo e precisam ser reverificadas.

## Vídeo técnico
