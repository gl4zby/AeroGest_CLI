from datetime import datetime

import database
from relatorio import gerar_relatorio


ESTADOS_AERONAVE = [
    "Disponível",
    "Em voo",
    "Manutenção",
]

TIPOS_MOVIMENTO = [
    "Chegada",
    "Partida",
]


def pausar():
    input("\nPressiona ENTER para continuar...")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()

        if texto:
            return texto

        print("O campo não pode ficar vazio.")


def ler_inteiro_positivo(mensagem):
    while True:
        texto = input(mensagem).strip()

        try:
            numero = int(texto)

            if numero > 0:
                return numero

            print("O número deve ser superior a zero.")
        except ValueError:
            print("Introduz um número inteiro válido.")


def escolher_da_lista(lista, titulo):
    print(f"\n{titulo}")

    for indice, valor in enumerate(lista, start=1):
        print(f"{indice}. {valor}")

    while True:
        escolha = input("Escolha: ").strip()

        try:
            indice = int(escolha)

            if 1 <= indice <= len(lista):
                return lista[indice - 1]

            print("Escolha uma opção válida.")
        except ValueError:
            print("Introduz o número da opção.")


def ler_data_hora():
    while True:
        texto = input("Data e hora (AAAA-MM-DD HH:MM): ").strip()

        try:
            data = datetime.strptime(texto, "%Y-%m-%d %H:%M")
            return data.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Formato inválido. Exemplo: 2026-07-15 14:30")


def mostrar_aeronaves(aeronaves):
    if not aeronaves:
        print("\nNão existem aeronaves registadas.")
        return

    print("\n" + "-" * 82)
    print(
        f"{'ID':<5}"
        f"{'Matrícula':<15}"
        f"{'Modelo':<30}"
        f"{'Capacidade':<12}"
        f"{'Estado':<20}"
    )
    print("-" * 82)

    for aeronave in aeronaves:
        aeronave_id, matricula, modelo, capacidade, estado = aeronave

        print(
            f"{aeronave_id:<5}"
            f"{matricula:<15}"
            f"{modelo:<30}"
            f"{capacidade:<12}"
            f"{estado:<20}"
        )

    print("-" * 82)


def mostrar_movimentos(movimentos):
    if not movimentos:
        print("\nNão existem movimentos registados.")
        return

    print("\n" + "-" * 90)
    print(
        f"{'ID':<5}"
        f"{'Matrícula':<15}"
        f"{'Tipo':<12}"
        f"{'Origem/Destino':<30}"
        f"{'Data/Hora':<20}"
    )
    print("-" * 90)

    for movimento in movimentos:
        movimento_id, matricula, tipo, origem_destino, data_hora = movimento

        print(
            f"{movimento_id:<5}"
            f"{matricula:<15}"
            f"{tipo:<12}"
            f"{origem_destino:<30}"
            f"{data_hora:<20}"
        )

    print("-" * 90)


def adicionar_aeronave():
    print("\n=== ADICIONAR AERONAVE ===")

    matricula = ler_texto("Matrícula: ").upper()
    modelo = ler_texto("Modelo: ")
    capacidade = ler_inteiro_positivo("Capacidade: ")
    estado = escolher_da_lista(
        ESTADOS_AERONAVE,
        "Estado da aeronave",
    )

    database.adicionar_aeronave(
        matricula,
        modelo,
        capacidade,
        estado,
    )

    print("\nAeronave adicionada com sucesso.")


def listar_aeronaves():
    print("\n=== LISTAR AERONAVES ===")
    mostrar_aeronaves(database.listar_aeronaves())


def alterar_estado_aeronave():
    print("\n=== ALTERAR ESTADO DA AERONAVE ===")

    aeronaves = database.listar_aeronaves()
    mostrar_aeronaves(aeronaves)

    if not aeronaves:
        return

    aeronave_id = ler_inteiro_positivo("ID da aeronave: ")
    novo_estado = escolher_da_lista(
        ESTADOS_AERONAVE,
        "Novo estado",
    )

    alterados = database.alterar_estado_aeronave(
        aeronave_id,
        novo_estado,
    )

    if alterados == 0:
        print("\nNão foi encontrada uma aeronave com esse ID.")
    else:
        print("\nEstado alterado com sucesso.")


def registar_movimento():
    print("\n=== REGISTAR CHEGADA OU PARTIDA ===")

    aeronaves = database.listar_aeronaves()
    mostrar_aeronaves(aeronaves)

    if not aeronaves:
        print("\nPrimeiro tens de adicionar uma aeronave.")
        return

    aeronave_id = ler_inteiro_positivo("ID da aeronave: ")

    if not database.aeronave_existe(aeronave_id):
        print("\nNão existe uma aeronave com esse ID.")
        return

    tipo = escolher_da_lista(
        TIPOS_MOVIMENTO,
        "Tipo de movimento",
    )

    origem_destino = ler_texto("Origem ou destino: ")
    data_hora = ler_data_hora()

    database.adicionar_movimento(
        aeronave_id,
        tipo,
        origem_destino,
        data_hora,
    )

    print("\nMovimento registado com sucesso.")


def listar_movimentos():
    print("\n=== LISTAR MOVIMENTOS ===")
    mostrar_movimentos(database.listar_movimentos())


def filtrar_movimentos():
    print("\n=== FILTRAR MOVIMENTOS ===")

    tipo = escolher_da_lista(
        TIPOS_MOVIMENTO,
        "Escolhe o tipo",
    )

    mostrar_movimentos(database.listar_movimentos(tipo))


def mostrar_estatisticas():
    print("\n=== ESTATÍSTICAS ===")

    dados = database.obter_estatisticas()

    print(f"Total de aeronaves: {dados['total_aeronaves']}")
    print(f"Aeronaves em manutenção: {dados['em_manutencao']}")
    print(f"Chegadas registadas: {dados['chegadas']}")
    print(f"Partidas registadas: {dados['partidas']}")


def criar_relatorio():
    print("\n=== GERAR RELATÓRIO ===")

    caminho = gerar_relatorio()

    print("Relatório criado com sucesso.")
    print(f"Local: {caminho.resolve()}")


def mostrar_menu():
    print(
        """
========================================
              AEROGEST
      Gestão simples de aeródromo
========================================

1. Adicionar aeronave
2. Listar aeronaves
3. Alterar estado da aeronave
4. Registar chegada ou partida
5. Listar movimentos
6. Filtrar movimentos
7. Mostrar estatísticas
8. Gerar relatório HTML

0. Sair
"""
    )


def executar():
    database.inicializar_base_dados()

    while True:
        mostrar_menu()
        opcao = input("Escolhe uma opção: ").strip()

        try:
            if opcao == "1":
                adicionar_aeronave()
            elif opcao == "2":
                listar_aeronaves()
            elif opcao == "3":
                alterar_estado_aeronave()
            elif opcao == "4":
                registar_movimento()
            elif opcao == "5":
                listar_movimentos()
            elif opcao == "6":
                filtrar_movimentos()
            elif opcao == "7":
                mostrar_estatisticas()
            elif opcao == "8":
                criar_relatorio()
            elif opcao == "0":
                print("\nPrograma terminado.")
                break
            else:
                print("\nOpção inválida.")
        except Exception as erro:
            print(f"\nOcorreu um erro: {erro}")

        if opcao != "0":
            pausar()


if __name__ == "__main__":
    executar()
