# Sistema de Controle de Estoque

Projeto desenvolvido como Produção Individual Textual (PTI) do curso de Práticas de Programação no SENAC.

O sistema tem como objetivo gerenciar produtos em estoque, permitindo cadastro e listagem de quantidades através de interface console.

## Objetivo do Projeto

Desenvolver um sistema para controle de estoque que permita:

- Cadastro de produtos
- Controle de quantidade
- Visualização de estoque

O projeto aplica conceitos de:

- Programação orientada a objetos
- Estrutura de dados
- Manipulação de arquivos csv

## Tecnologias Utilizadas

- Python

## Estrutura do Projeto

O projeto segue uma separação por camadas:

```
controle_estoque
├── data
│   └── produtos.csv
├── src
│   └── app
│       ├── config.py
│       ├── main.py
│       ├── models
│       │   └── produto.py
│       ├── repositories
│       │   └── produtos.py
│       ├── services
│       │   └── produtos.py
│       └── utils
│           ├── arquivos.py
│           ├── console.py
│           └── csv.py
└── pyproject.toml
```

O projeto segue uma separação por camadas:

- Models: Representação das entidades
- Repositories: Manipulação de dados
- Services: Regras de negócio
- Utils: Funções auxiliares
- App: Ponto de entrada da aplicação

## Como Executar o Projeto

1. Clone o repositório:

```
   git clone https://github.com/Byorks/PTI-2S-SENAC-PP.git
```

2. Acesse a pasta do projeto:

```
   cd PTI-2S-SENAC-PP
```

1. Execute o projeto
   Na raiz do projeto execute:

```
   python -m src.app.main
```

## 📈 Melhorias Futuras

- Implementar feedback visual durante processamento
- Criar navegação interativa por teclado
- Implementar ordenação por critérios (nome, preço, quantidade)
- Validar duplicidade de código de produto
