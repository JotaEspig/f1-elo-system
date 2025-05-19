# F1 Elo System

Este projeto implementa um sistema de avaliação Elo para pilotos e construtores de Fórmula 1, utilizando dados históricos da categoria. O objetivo é calcular e acompanhar a evolução do "rating" de desempenho de cada piloto e equipe ao longo das temporadas, com base nos resultados das corridas.

## Funcionalidades
- Leitura de dados históricos de F1 (pilotos, construtores, corridas, resultados, etc.)
- Cálculo do Elo para pilotos e construtores após cada corrida
- Reset do Elo de equipes a cada início de temporada
- Comparação de desempenho entre companheiros de equipe e entre equipes diferentes
- Exibição dos rankings de Elo ao final de cada temporada

## Estrutura do Projeto
- `main.py`: Script principal, executa a simulação e exibe os resultados
- `elo.py`: Funções de cálculo do Elo
- `classes.py`: Definição das classes de domínio (Driver, Constructor, Race, RaceResult)
- `consts.py`: Constantes do sistema Elo
- `utils.py`: Funções utilitárias para leitura dos arquivos CSV
- `f1data/`: Pasta com os arquivos CSV de dados históricos da F1

## Como rodar
1. **Pré-requisitos:**
   - Python 3.10 ou superior
   - (Opcional) Crie um ambiente virtual:
     ```zsh
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. **Instale dependências** (se houver):
   - Este projeto não depende de bibliotecas externas além da biblioteca padrão do Python.
3. **Execute o simulador:**
   ```zsh
   python main.py
   ```

## Como usar
- O script irá processar os dados e, ao final de cada temporada, exibir os rankings de Elo dos pilotos e construtores.
- Você pode escolher visualizar o ranking de pilotos ou construtores ao final de cada ano.

## Dados
Os arquivos CSV em `f1data/` devem seguir o formato dos datasets públicos de F1 (ex: [Kaggle Formula 1 World Championship](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)).

## Licença
Este projeto é apenas para fins educacionais e de pesquisa.
