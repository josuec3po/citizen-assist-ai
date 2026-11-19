# Elderly Assist(Citizen Assist AI)

Assistente de terminal em Python, Citizen Assist AI que resolvemos chamar também de Elderly Assist, orienta **pessoas idosas** sobre saúde, transporte,
direitos e benefícios e golpes, usando apenas uma base de conhecimento verificada em fontes oficiais.

## Integrantes
- Josué Franco Braga — RM 569174
- Manoel da Silva Ferreira — RM 572045
- Fernando Lobato Rodrigues — RM 569377

## Público e problema
- **Público:** pessoas idosas (60 anos ou mais) e seus familiares também com idades podendo ser abaixo dos 60.
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
- Menos de 3 pontos: "não encontrei". Nesse caso, o método `sugerir()` faz uma busca
     flexível por palavras soltas (categoria +2, título +1, palavra-chave +1) e apenas
     sugere orientações parecidas. A sugestão não conta como resposta encontrada.

## Privacidade e transparência
- O assistente nunca pede nome, CPF, telefone ou e-mail.
- Pergunta com 8 ou mais dígitos ou com `@` é recusada e **não** é registrada.
- Toda resposta mostra fonte, data de verificação e o aviso de que não é canal oficial.

## Integrações com outras disciplinas
- Nenhuma integração nesta versão, essa disciplina na verdade vai integrar as outras, é a nossa base.

## Fontes consultadas
- Ministério da Saúde (gov.br/saude): Meu SUS Digital, calendário de vacinação do idoso, Farmácia Popular
- Estatuto da Pessoa Idosa (Lei 10.741/2003, planalto.gov.br)
- INSS (gov.br/inss)
- Ministério dos Direitos Humanos (Disque 100)


## Teste com usuários
Testamos com 4 pessoas de fora da equipe, somando 11 atendimentos, entre 12 e 13 de
novembro de 2026. Cada sessão do programa corresponde a uma pessoa, identificada
automaticamente por um código anônimo (P05 a P08). Nenhum nome ou dado pessoal foi registrado.

Indicadores obtidos (opção 3 do menu):
- Resposta encontrada: 82%
- Taxa de acerto (ajudou): 82%
- Tempo médio para encontrar: 10,2 s
- Tentativas por atendimento: 1,0
- Facilidade de uso (1 a 5): 4,2 (4 sessões)

Dúvidas sem solução:
- "transporte"
- "meios de transporte gratis"

Dos 11 atendimentos:
  - 7 foram pela navegação de categorias
  - 4 por pergunta em texto livre, dessas 4 perguntas, 2 não foram encontradas.

Melhoria feita a partir do teste: 
A orientação 5 não tinha "transporte" nem "transporte gratis" nas palavras-chave, e o título diz “gratuito”, não “gratis”. Por isso as duas perguntas deram só 1 ponto. Adicionando "transporte" e "transporte gratis" às palavras-chave da orientação 5 resolve as duas: “meios de transporte gratis” passa a dar 4 pontos (MÉDIA). Essa correção feito por nós é apresentada no vídeo.

## Limitações
- Só responde o que está na base (12 orientações) e não entende sinônimos ou erros de digitação
  que não estejam nas palavras-chave.
- A busca compara palavras exatas: "vacinas" e "vacina" precisam estar ambas na lista.
- O conteúdo é nacional; regras locais (como transporte municipal) variam por cidade.
- As informações mudam com o tempo e precisam ser reverificadas.

## Vídeo técnico

Link: https://youtu.be/PYGpBesCmxo
