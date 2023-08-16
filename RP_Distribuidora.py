import sqlite3
import PySimpleGUI as sg
from datetime import datetime

banco = sqlite3.connect(r'D:\Projects\help_rodo\Projeto-Software-Product-RPDistribuidora\RPDistribuidora.db')
cursor = banco.cursor()


def tratar_dados(pdd, dados):
    data = datetime.now().strftime('%d/%m/%Y')
    pedido = pdd
    cliente = dados['-Cliente-']
    contador_linhas = 0
    produto = []
    valor = []
    qtd = []

    for i in dados:
        if 'Produto' in i:
            produto.append(dados[i])
            contador_linhas += 1
        elif 'Valor' in i:
            valor.append(dados[i])
        elif 'Qtd' in i:
            qtd.append(dados[i])

    ic = 0
    while ic < contador_linhas:
        valores = [(pedido, data, cliente, produto[ic], valor[ic], qtd[ic])]
        cursor.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?,?)", valores)
        ic += 1


class sistema():
    def janela_inicio():
        sg.theme('DarkTeal10')
        layout = [[sg.Text('Bem vindo a RP Distribuidora LTDA')],
                  [sg.Text('Selecione o que deseja fazer:')],
                  [sg.Button('Novo Pedido')],
                  [sg.Button('Sair')]]

        janela_inicio = sg.Window('RP Distribuidora', layout)
        event, value = janela_inicio.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            elif event == 'Novo Pedido':
                janela_inicio.close()
                sistema.adicionar_pedido()
                break
        janela_inicio.close()

    def adicionar_pedido():
        try:
            cursor.execute('SELECT MAX(pedido) FROM pedidos')
            pedido = ((cursor.fetchall())[0][0]) + 1
        except:
            pedido = 1

        def new_layout(i):
            return [[sg.Text(f'Produto {i}:', size=(9, 1)), sg.InputText(size=(25, i), k=(f'-Produto {i}-')), sg.Text('Valor:'), sg.InputText(size=(10, 1), k=(f'-Valor {i}-')), sg.Text('Quantidade:'), sg.InputText(size=(5, 1), k=(f'-Qtd {i}-'))]]

        linha_pedido = [[sg.Text('Produto 1:', size=(9, 1)), sg.InputText(size=(25, 0), k=('-Produto 1-')), sg.Text('Valor:'), sg.InputText(size=(10, 1), k=(f'-Valor 1-')), sg.Text('Quantidade:'), sg.InputText(size=(5, 1), k=('-Qtd 1-'))]]

        layout = [[sg.Text('Adicionar novo pedido')],
                  [sg.Text('Cliente:', size=(10, 1)), sg.InputText(size=(25, 0), k='-Cliente-'), sg.Button("Novo Produto")],
                  [sg.Column(linha_pedido, key='-Column-')],
                  [sg.Button('Sair'), sg.Button('Ok')]]

        janela_novo_pedido = sg.Window('Novo Pedido', layout, resizable=True)
        qtd_pedido = 2
        while True:
            event, value = janela_novo_pedido.read()
            if event in (sg.WIN_CLOSED, 'Sair'):
                janela_novo_pedido.close()
                break
            elif event == 'Novo Produto':
                if qtd_pedido <= 20:
                    janela_novo_pedido.extend_layout(janela_novo_pedido['-Column-'], new_layout(qtd_pedido))
                    qtd_pedido += 1
                else:
                    sg.Popup('Limite de produto atingidos')
                    janela_novo_pedido['Novo Produto'].update(visible=False)
            elif event == 'Ok':
                janela_novo_pedido.close()
                tratar_dados(pedido, value)
                break
        sistema.janela_inicio()


sistema.janela_inicio()
banco.commit()
banco.close()
