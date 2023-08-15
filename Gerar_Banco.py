import sqlite3

banco = sqlite3.connect('C:\\Users\\Cliente\\OneDrive\\Área de Trabalho\\Projeto Software Product - RP Distribuidora\\RPDistribuidora.db')

cursor = banco.cursor()

cursor.execute("CREATE TABLE pedidos (pedido integer, data text, cliente text, produto text, valor real, quantidade integer)")

