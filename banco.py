import psycopg2
from datetime import datetime
import pytz

# 🔌 CONEXÃO COM POSTGRESQL (Render)
def conectar():
    conn = psycopg2.connect(
        "postgresql://alexandre_da_silva_de_maria_user:rqzaUqjnAvANzkrSTAbwU8manvA6nG7K@dpg-d81lkd1j2pic73c3go6g-a.ohio-postgres.render.com/alexandre_da_silva_de_maria"
    )
    return conn

def hora_brasilia():
    tz = pytz.timezone("America/Sao_Paulo")
    return datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')

# 🏗️ CRIAR TABELAS
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slot (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            valor DOUBLE PRECISION NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# 👤 CADASTRAR USUÁRIO
def cadastrar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)",
            (usuario, senha)
        )
        conn.commit()
        return True

    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False

    finally:
        conn.close()


# 🔐 LOGIN
def login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE usuario = %s AND senha = %s",
        (usuario, senha)
    )

    resultado = cursor.fetchone()
    conn.close()
    return resultado


# 💰 DEPÓSITO
def adicionar_deposito(usuario_id, valor):
    conn = conectar()
    cursor = conn.cursor()

    data_hora = hora_brasilia()

    cursor.execute(
        "INSERT INTO slot (usuario_id, tipo, valor, data_hora) VALUES (%s, %s, %s, %s)",
        (usuario_id, 'deposito', float(valor), data_hora)
    )

    conn.commit()
    conn.close()


# 💸 SAQUE
def adicionar_saque(usuario_id, valor):
    conn = conectar()
    cursor = conn.cursor()

    data_hora = hora_brasilia()

    cursor.execute(
        "INSERT INTO slot (usuario_id, tipo, valor, data_hora) VALUES (%s, %s, %s, %s)",
        (usuario_id, 'saque', float(valor), data_hora)
    )

    conn.commit()
    conn.close()


# 📊 LISTAR DEPÓSITOS
def listar_deposito(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM slot WHERE usuario_id = %s AND tipo = %s",
        (usuario_id, 'deposito')
    )

    dados = cursor.fetchall()
    conn.close()
    return dados


# 📊 LISTAR SAQUES
def listar_saque(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM slot WHERE usuario_id = %s AND tipo = %s",
        (usuario_id, 'saque')
    )

    dados = cursor.fetchall()
    conn.close()
    return dados


# 💵 SOMA DEPÓSITOS
def soma_deposito(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(valor) FROM slot WHERE usuario_id = %s AND tipo = %s",
        (usuario_id, 'deposito')
    )

    total = cursor.fetchone()[0]
    conn.close()

    return total or 0


# 💵 SOMA SAQUES
def soma_saque(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(valor) FROM slot WHERE usuario_id = %s AND tipo = %s",
        (usuario_id, 'saque')
    )

    total = cursor.fetchone()[0]
    conn.close()

    return total or 0


# 🗑️ FUNÇÃO PARA APAGAR REGISTRO
def apagar_registro(registro_id, usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM slot
        WHERE id = %s AND usuario_id = %s
        """,
        (registro_id, usuario_id)
    )

    conn.commit()
    conn.close()