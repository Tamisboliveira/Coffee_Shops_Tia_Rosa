"""
Módulo: clients.py

Descrição:
-----------
Este módulo contém todas as funcionalidades relacionadas à gestão de clientes em um sistema de controle de pedidos.
As operações incluem:
    - Cadastro de novos clientes
    - Visualização da lista de clientes
    - Edição de informações dos clientes
    - Exclusão de clientes
    - Geração de arquivo CSV

Classes:
--------
- Clientes: representa um cliente com código, nome, CPF e data de nascimento

Funções:
--------
- obter_ultimo_codigo_cliente(): gera o próximo código disponível.
- cadastrar_cliente(): realiza o cadastro de um novo cliente.
- exibir_clientes(): exibe a lista atual de clientes.
- editar_clientes(): permite edição dos dados de um cliente existente.
- excluir_cliente(): remove um cliente da lista.
- salvar_clientes_csv(): salva a lista de clientes em arquivo CSV.
- carregar_clientes_csv(): carrega clientes do arquivo CSV, se existir.

"""


import csv
import os

# lista de armazenamento de clientes
lista_clientes = []

# Menu de clientes
opcoes_menu_cliente = [
    ['[1] Cadastrar clientes'],
    ['[2] Exibir clientes'],
    ['[3] Editar clientes'],
    ['[4] Excluir clientes'],
    ['[0] Voltar para o menu principal']
]

# ------ Definição de Classes ------ 

class Cliente():
    def __init__(self,codigo_cliente,nome_cliente,cpf, data_nascimento):
        self.codigo_cliente = codigo_cliente            # Código unico do cliente
        self.nome_cliente = nome_cliente                # Nome do cliente
        self.documento = cpf                            # CPF do cliente
        self.nascimento = data_nascimento               # Data de nascimento
    
    # Exibir informacoes de clientes
    def __str__(self):
        return f'Código: {self.codigo_cliente} | Nome: {self.nome_cliente} | CPF: {self.documento} | Data de Nascimento: {self.nascimento}'
    
# ------ Funçoes ------ 

# Retorna o próximo código disponível para um novo cliente, com base nos registros existentes no arquivo CSV
def obter_ultimo_codigo_cliente():
    ultimo_codigo_cliente = 0
    if os.path.exists('lista_clientes.csv'):
        try:
            with open('lista_clientes.csv', mode='r', newline='', encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo)
                next(leitor, None)  # Pular o cabeçalho
                for linha in leitor:
                    if linha and linha[0].isdigit():
                        ultimo_codigo_cliente = max(ultimo_codigo_cliente, int(linha[0]))
        except FileNotFoundError:
            pass  # O arquivo ainda não existe, retorna 0
        except Exception as e:
            print(f"Erro ao ler códigos de clientes: {e}")
    return ultimo_codigo_cliente + 1           

# Cadastrar Cliente
def cadastrar_cliente():
    codigo_cliente = obter_ultimo_codigo_cliente()
    nome_cliente = input('\n Digite o nome do cliente: ')
    
    # Solicita o CPF, valida se possui 11 dígitos e formata no padrão 000.000.000-00
    documento = input('Digite o CPF do cliente (11 dígitos): ')
    if len(documento) == 11:
        cpf_formatado = '{}.{}.{}-{}'.format(documento[:3],documento[3:6],documento[6:9],documento[9:])
    else:
        cpf_formatado = documento
    
    # Solicita a data de nascimento separadamente (dia, mês, ano) e formata como DD/MM/AAAA
    dia = int(input('Digite o dia de nascimento (2 dígitos): '))
    mes = int(input('Digite o mês de nascimento (2 dígitos): '))
    ano = int(input('Digite o ano de nascimento (4 dígitos): '))
    nascimento = f'{dia}/{mes}/{ano}'
    
    novo_cliente = Cliente(codigo_cliente, nome_cliente,cpf_formatado, nascimento)
    lista_clientes.append(novo_cliente)
    salvar_clientes_csv()
    print(f'\nCliente "{nome_cliente}" cadastrado com sucesso! Código: {novo_cliente.codigo_cliente}\n')
    

# exibir clientes
def exibir_clientes():
    print('\n ------ Lista de Clientes ------\n')
    if not lista_clientes:
        print('\n Não há cliente cadastrado. \n')
    else:
        for cliente in lista_clientes:
            print(cliente)


# Editar clientes
def editar_clientes():
    # Exibe todos os clientes cadastrados para facilitar a escolha do cliente a ser editado
    exibir_clientes()
    # Solicita o código para edição
    cod_editar_cliente = int(input('\n Digite o código do cliente que deseja editar: '))
    cliente_encontrado = False
    # Verifica se o código informado corresponde a algum cliente existente
    # Se encontrado, solicita novos dados e mantém os antigos caso o usuário deixe em branco
    for cliente in lista_clientes:
        if cliente.codigo_cliente == cod_editar_cliente:
            print(f'\nCliente encontrado: {cliente}\n')
            cliente.nome_cliente = input('\nDigite o nome do cliente corrigido: ') or cliente.nome_cliente
            
            # Edita o CPF com formatação
            novo_cpf = input('Digite o novo CPF (11 dígitos): ')
            if len(novo_cpf) == 11:
                cpf_formatado = '{}.{}.{}-{}'.format(novo_cpf[:3],novo_cpf[3:6],novo_cpf[6:9],novo_cpf[9:])
                cliente.documento = cpf_formatado
            else:
                print('CPF inválido. O valor antifo será mantido.\n')
            
            # Editar data de nascimento 
            print('\n Deixe em branco se quiser manter a data de nascimento atual.')
            dia = input('Novo dia de nascimento (2 dígitos): ')
            mes = input('Novo mês de nascimento (2 dígitos): ')
            ano = input('Novo ano de nascimento (4 dígitos): ')
            
            # Usa os valores antigos se os campos forem deixados em branco
            dia_atual, mes_atual, ano_atual = cliente.nascimento.split('/')
            nova_data = f'{dia or dia_atual}/{mes or mes_atual}/{ano or ano_atual}'
            cliente.nascimento = nova_data

            salvar_clientes_csv()
            print('\n Cliente atualizado com sucesso! \n')
            cliente_encontrado = True
            break
    if not cliente_encontrado:
        print('\n Cliente não encontrado.\n')

# Excluir cliente
def excluir_cliente():
    exibir_clientes()
    cod_excluir_cliente = int(input('\n Digite o código do cliente que deseja excluir: '))
    for cliente in lista_clientes:
        if cliente.codigo_cliente == cod_excluir_cliente:
            print(f'Cliente encontrado: {cliente}\n')
            msg_confirmacao = input('Tem certeza que deseja excluir? (s/n): ').lower()
            if msg_confirmacao == 's':
                lista_clientes.remove(cliente)
                salvar_clientes_csv()
                print('\n Cliente excluído com sucesso!\n')
            else:
                print('\n Processo de exclusão cancelado.\n')
            return
    print('\n Produto não encontrado.\n')

# Salvar lista de clientes no arquivo csv
def salvar_clientes_csv():
    with open('lista_clientes.csv',mode='w',newline='',encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        # Cabeçalho
        writer.writerow(['Código','Nome','CPF','Data de Nascimento'])
        # Dados
        for cliente in lista_clientes:
            writer.writerow([cliente.codigo_cliente, cliente.nome_cliente, cliente.documento, cliente.nascimento])
    print('Lista de clientes salva em "lista_clientes.csv".')

# Carregar a lista de clientes do arquivo csv
def carregar_clientes_csv(arquivo ='lista_clientes.csv'):
    if os.path.exists(arquivo) and not lista_clientes: # Verifica se o arquivo existe e se a lista está vazia
        with open(arquivo,mode='r',newline='',encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                try:
                    cliente = Cliente(
                        int(linha['Código']),
                        linha['Nome'],
                        linha['CPF'],
                        linha['Data de Nascimento']
                    )
                    lista_clientes.append(cliente)
                except ValueError as e:
                    print(f"Erro ao carregar linha do CSV de clientes: {linha} - {e}")
