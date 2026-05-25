import sqlite3
from datetime import datetime

def conectar():
    conn = sqlite3.connect("slot.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS slot (id INTEGER PRIMARY KEY AUTOINCREMENT,  usuario_id INTEGER NOT NULL, tipo TEXT NOT NULL, valor REAL NOT NULL, data_hora TEXT NOT NULL, FOREIGN KEY (usuario_id) REFERENCES usuarios(id))""")
    conn.commit()
    conn.close()

def cadastrar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
    conn.commit()
    conn.close()

def login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT id FROM usuarios WHERE usuario = ? AND senha = ?""", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def adicionar_deposito(usuario_id, valor):
    conn = conectar()
    cursor = conn.cursor()
    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute("INSERT INTO slot (usuario_id, tipo, valor, data_hora) VALUES ( ?, ?, ?, ?)", (usuario_id, 'deposito',valor, data_hora))
    conn.commit()
    conn.close()

def adicionar_saque(usuario_id, valor):
    conn = conectar()
    cursor = conn.cursor()
    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute("INSERT INTO slot (usuario_id, tipo, valor, data_hora) VALUES (?, ?, ?, ?)", (usuario_id, 'saque',valor, data_hora))
    conn.commit()
    conn.close()

def listar_deposito(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM slot WHERE usuario_id = ? AND tipo = ?",(usuario_id, 'deposito'))
    valor = cursor.fetchall()
    conn.close()
    return valor

def listar_saque(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM slot WHERE usuario_id = ? AND tipo = ?",(usuario_id, 'saque'))
    valor = cursor.fetchall()
    conn.close()
    return valor

def soma_deposito(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM (valor) FROM slot WHERE usuario_id = ? AND tipo = ?", (usuario_id, 'deposito'))
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0

def soma_saque(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM (valor) FROM slot WHERE usuario_id = ? AND tipo = ?", (usuario_id, 'saque'))
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0

def limpar_banco(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM slot WHERE usuario_id = ?",(usuario_id,))
    conn.commit()
    conn.close()
    