#!/usr/bin/python
##coding:utf-8
import connect as cnn


def main_principal():
    opcao = int(input('''
    Escolha uma opção
1 - Inquilino
2 - Enviar Email
'''))
    if opcao == 1:
        cnn.main_cliente()
    elif opcao == 2:





if __name__ == '__main__':
    main_principal()