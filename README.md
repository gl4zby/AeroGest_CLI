# AeroGest CLI

Aplicação de linha de comandos em Python para gestão simples de um aeródromo, com MySQL e geração de relatórios HTML.

## Funcionalidades

- Adicionar e listar aeronaves.
- Alterar o estado de uma aeronave.
- Registar e listar chegadas e partidas.
- Filtrar movimentos por tipo.
- Mostrar estatísticas.
- Gerar um relatório HTML.

## Tecnologias

- Python
- MySQL
- mysql-connector-python
- HTML

## Requisitos

- Python instalado.
- MySQL instalado e em execução.

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r dependencias.tx
Copy-Item db_config.exemplo.py db_config.py
```

Antes de executar, configura os dados da tua instalação MySQL em `db_config.py`.

## Execução

```powershell
python main.py
```

## Ficheiros principais

- `main.py`: menu e interação com o utilizador.
- `database.py`: ligação ao MySQL e operações da base de dados.
- `relatorio.py`: geração do relatório HTML.

Não publicar `db_config.py`, porque pode conter credenciais locais.
