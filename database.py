import mysql.connector
from mysql.connector import IntegrityError

import db_config


def ligar_servidor():
    return mysql.connector.connect(
        host=db_config.HOST,
        user=db_config.USER,
        password=db_config.PASSWORD,
        port=db_config.PORT,
    )


def ligar_base_dados():
    return mysql.connector.connect(
        host=db_config.HOST,
        user=db_config.USER,
        password=db_config.PASSWORD,
        port=db_config.PORT,
        database=db_config.DATABASE,
    )


def inicializar_base_dados():
    """Cria a base de dados e as tabelas na primeira execução."""
    ligacao = ligar_servidor()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS " + db_config.DATABASE + " "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
    finally:
        cursor.close()
        ligacao.close()

    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS aeronaves (
                id INT AUTO_INCREMENT PRIMARY KEY,
                matricula VARCHAR(20) NOT NULL UNIQUE,
                modelo VARCHAR(80) NOT NULL,
                capacidade INT NOT NULL,
                estado VARCHAR(30) NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                aeronave_id INT NOT NULL,
                tipo VARCHAR(20) NOT NULL,
                origem_destino VARCHAR(100) NOT NULL,
                data_hora DATETIME NOT NULL,
                FOREIGN KEY (aeronave_id)
                    REFERENCES aeronaves(id)
            )
            """
        )

        ligacao.commit()
    finally:
        cursor.close()
        ligacao.close()


def adicionar_aeronave(matricula, modelo, capacidade, estado):
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO aeronaves (matricula, modelo, capacidade, estado)
            VALUES (%s, %s, %s, %s)
            """,
            (matricula, modelo, capacidade, estado),
        )
        ligacao.commit()
    except IntegrityError as erro:
        raise ValueError("Já existe uma aeronave com essa matrícula.") from erro
    finally:
        cursor.close()
        ligacao.close()


def listar_aeronaves():
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            """
            SELECT id, matricula, modelo, capacidade, estado
            FROM aeronaves
            ORDER BY matricula
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        ligacao.close()


def alterar_estado_aeronave(aeronave_id, novo_estado):
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            """
            UPDATE aeronaves
            SET estado = %s
            WHERE id = %s
            """,
            (novo_estado, aeronave_id),
        )
        ligacao.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        ligacao.close()


def aeronave_existe(aeronave_id):
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            "SELECT id FROM aeronaves WHERE id = %s",
            (aeronave_id,),
        )
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        ligacao.close()


def adicionar_movimento(
    aeronave_id,
    tipo,
    origem_destino,
    data_hora,
):
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO movimentos
                (aeronave_id, tipo, origem_destino, data_hora)
            VALUES (%s, %s, %s, %s)
            """,
            (aeronave_id, tipo, origem_destino, data_hora),
        )
        ligacao.commit()
    finally:
        cursor.close()
        ligacao.close()


def listar_movimentos(tipo=None):
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    consulta_base = """
        SELECT
            m.id,
            a.matricula,
            m.tipo,
            m.origem_destino,
            DATE_FORMAT(m.data_hora, '%Y-%m-%d %H:%i')
        FROM movimentos AS m
        INNER JOIN aeronaves AS a
            ON a.id = m.aeronave_id
    """

    try:
        if tipo:
            cursor.execute(
                consulta_base
                + """
                WHERE m.tipo = %s
                ORDER BY m.data_hora
                """,
                (tipo,),
            )
        else:
            cursor.execute(
                consulta_base
                + """
                ORDER BY m.data_hora
                """
            )

        return cursor.fetchall()
    finally:
        cursor.close()
        ligacao.close()


def obter_estatisticas():
    ligacao = ligar_base_dados()
    cursor = ligacao.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM aeronaves")
        total_aeronaves = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM aeronaves WHERE estado = %s",
            ("Manutenção",),
        )
        em_manutencao = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM movimentos WHERE tipo = %s",
            ("Chegada",),
        )
        chegadas = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM movimentos WHERE tipo = %s",
            ("Partida",),
        )
        partidas = cursor.fetchone()[0]

        return {
            "total_aeronaves": total_aeronaves,
            "em_manutencao": em_manutencao,
            "chegadas": chegadas,
            "partidas": partidas,
        }
    finally:
        cursor.close()
        ligacao.close()
