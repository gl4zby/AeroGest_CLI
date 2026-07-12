from datetime import datetime
from html import escape
from pathlib import Path

import database


def linha_html(valores):
    celulas = ""

    for valor in valores:
        celulas += f"<td>{escape(str(valor))}</td>"

    return f"<tr>{celulas}</tr>"


def gerar_relatorio():
    aeronaves = database.listar_aeronaves()
    movimentos = database.listar_movimentos()
    estatisticas = database.obter_estatisticas()

    linhas_aeronaves = ""
    for aeronave in aeronaves:
        linhas_aeronaves += linha_html(aeronave)

    linhas_movimentos = ""
    for movimento in movimentos:
        linhas_movimentos += linha_html(movimento)

    if not linhas_aeronaves:
        linhas_aeronaves = '<tr><td colspan="5">Sem aeronaves.</td></tr>'

    if not linhas_movimentos:
        linhas_movimentos = '<tr><td colspan="5">Sem movimentos.</td></tr>'

    agora = datetime.now()
    pasta = Path("relatorios")
    pasta.mkdir(exist_ok=True)

    caminho = pasta / f"relatorio_{agora:%Y%m%d_%H%M%S}.html"

    conteudo = f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>Relatório AeroGest</title>
    <style>
        body {{ font-family: Arial; margin: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 25px; }}
        th, td {{ border: 1px solid black; padding: 7px; }}
        th {{ background: #dddddd; }}
    </style>
</head>
<body>
    <h1>Relatório AeroGest</h1>
    <p>Gerado em {agora:%d/%m/%Y às %H:%M}</p>

    <h2>Estatísticas</h2>
    <p>Total de aeronaves: {estatisticas["total_aeronaves"]}</p>
    <p>Aeronaves em manutenção: {estatisticas["em_manutencao"]}</p>
    <p>Chegadas: {estatisticas["chegadas"]}</p>
    <p>Partidas: {estatisticas["partidas"]}</p>

    <h2>Aeronaves</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Matrícula</th>
            <th>Modelo</th>
            <th>Capacidade</th>
            <th>Estado</th>
        </tr>
        {linhas_aeronaves}
    </table>

    <h2>Movimentos</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Matrícula</th>
            <th>Tipo</th>
            <th>Origem/Destino</th>
            <th>Data/Hora</th>
        </tr>
        {linhas_movimentos}
    </table>
</body>
</html>
"""

    caminho.write_text(conteudo, encoding="utf-8")
    return caminho
