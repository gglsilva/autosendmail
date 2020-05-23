# connect.py
import sqlite3
import main

class Connect(object):

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # imprimindo nome do banco
            print("Banco:", db_name)
            # lendo a versão do SQLite
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            # imprimindo a versão do SQLite
            print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Erro ao abrir banco.")
            return False


    def commit_db(self):
        if self.conn:
            self.conn.commit()


    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class ClientesDb(object):
    tb_name = 'clientes'

    def __init__(self):
        self.db = Connect('inquilinos.db')
#       self.db = Connect('clientes.db')


    def criar_schema(self, schema_name='clientes_schema.sql'):
        print("Criando tabela %s ..." % self.tb_name)

        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error:
            print("Aviso: A tabela %s já existe." % self.tb_name)
            return False

        print("Tabela %s criada com sucesso." % self.tb_name)

    def inserir_com_parametros(self):
        # solicitando os dados ao usuário
        self.nome = input('Nome: ')
        self.email = input('Email: ')

        try:
            self.db.cursor.execute("""
            INSERT INTO clientes (nome, email)
            VALUES (?,?)
            """, (self.nome, self.email))
            # gravando no bd
            self.db.commit_db()
            print("Dados inseridos com sucesso.")
        except sqlite3.IntegrityError:
            print("Aviso: O email deve ser único.")
            return False


    def ler_todos_clientes(self):
        sql = 'SELECT * FROM clientes ORDER BY nome'
        r = self.db.cursor.execute(sql)
        return r.fetchall()


    def imprimir_todos_clientes(self):
        lista = self.ler_todos_clientes()
        for c in lista:
            print(c)


    def localizar_cliente_por_nome(self, nome):
        n = self.db.cursor.execute(
            'SELECT * FROM clientes WHERE nome = ?', (nome,))
        return n.fetchone()


    def localizar_cliente(self, id):
        r = self.db.cursor.execute(
            'SELECT * FROM clientes WHERE id = ?', (id,))
        return r.fetchone()


    def atualizar(self, id):
        try:
            c = self.localizar_cliente(id)
            if c:
                # solicitando os dados ao usuário
                # se for no python2.x digite entre aspas simples
                self.novo_email = input('email: ')
                self.db.cursor.execute("""
                UPDATE clientes
                SET email = ?
                WHERE id = ?
                """, (self.novo_email, id,))
                # gravando no bd
                self.db.commit_db()
                print("Dados atualizados com sucesso.")
            else:
                print('Não existe cliente com o id informado.')
        except e:
            raise e


    def deletar(self, id):
        try:
            c = self.localizar_cliente(id)
            # verificando se existe cliente com o ID passado, caso exista
            if c:
                self.db.cursor.execute("""
                DELETE FROM clientes WHERE id = ?
                """, (id,))
                # gravando no bd
                self.db.commit_db()
                print("Registro %d excluído com sucesso." % id)
            else:
                print('Não existe cliente com o código informado.')
        except e:
            raise e


    def close_connection(self):
        self.db.close_db()



def main_cliente():
    cliente = ClientesDb()
    op = int(input('''
        Menu de Inquilinos
1 - Adicionar 
2 - Atualizar
3 - Pesquisar
4 - Deletar
5 - Voltar
'''))
    if op == 1:
        cliente.inserir_com_parametros()
    elif op == 2:
        nome = input(str('Digite o Nome do Cliente:'))
        id = cliente.localizar_cliente_por_nome(nome)
        cliente.atualizar(id[0])
    elif op == 3:
        nome = input(str('Digite o Nome do Cliente:'))
        id = cliente.localizar_cliente_por_nome(nome)
        cliente.localizar_cliente(id[0])
    elif op == 4:
        nome = input(str('Digite o Nome do Cliente:'))
        id = cliente.localizar_cliente_por_nome(nome)
        cliente.deletar(id[0])
    elif op == 5:
        main.main_principal()
    else:
        print('Opção invalida, Digite uma opção valida')
        main_cliente()

'''
if __name__ == '__main__':
    cliente = ClientesDb()
    #cliente.criar_schema()
    #cliente.inserir_com_parametros()
    cliente.imprimir_todos_clientes()
    #cliente.atualizar(3)
    cliente.deletar(3)
    cliente.imprimir_todos_clientes()
    cliente.close_connection()
    '''