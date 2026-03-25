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
- Manipulação de arquivos CSV
- Injeção de dependência (Repository + Service)

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
│       │   ├── memoria_produtos.py
│       │   ├── produtos.py
│       │   └── protocols.py
│       ├── services
│       │   └── produtos.py
│       └── utils
│           ├── arquivos.py
│           ├── console.py
└── pyproject.toml
```

Camadas:

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

3. Execute o projeto
   Na raiz do projeto execute:

```
   cd controle_estoque/src
   python -m app.main
```

## Repositórios (dados)

O sistema usa repositório via injeção de dependência no service, permitindo trocar a implementação sem mudar a regra de negócio.

- Repositório CSV: persiste em `controle_estoque/data/produtos.csv` e não permite `codigo` duplicado.
- Repositório em memória: carrega do CSV na inicialização e opera somente em memória (não persiste ao reiniciar). Se detectar `codigo` duplicado ao carregar, levanta `ValueError` (conflito).

O contrato mínimo do repositório (para o service aceitar qualquer implementação) está em `repositories/protocols.py`.

### Como trocar o repositório

No arquivo `controle_estoque/src/app/main.py`, altere qual classe é instanciada:

- Em memória: `ProdutoInMemoryRepository()`
- CSV: `ProdutoRepository()`

## Melhorias Futuras

- Implementar feedback visual durante processamento
- Criar navegação interativa por teclado
- Implementar ordenação por critérios (nome, preço, quantidade)
- Melhorar tratamento de erros no console (exibir mensagem e continuar)
