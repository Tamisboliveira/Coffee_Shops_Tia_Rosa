import csv
import os

# lista de armazenamento de produtos e clientes
lista_produtos = []
lista_clientes = []

# Mensagem de operação inválida
msg_opcao_inválida = "Operação inválida! Por favor digite um número válido."

# ------ variáveis dos menus de acesso as funcionalidades do sistema ------

# Menu principal
menu = [
    ['[1] Pedido de venda'],
    ['[2] Produtos'],
    ['[3] Clientes'],
    ['[0] Sair'] 
]

# Menu de produtos
opcoes_menu_produto = [
    ['[1] Cadastrar produtos'],
    ['[2] Exibir produtos'],
    ['[3] Editar produtos'],
    ['[4] Excluir produtos'],
    ['[0] Voltar para o menu principal']
]

# Menu de clientes
opcoes_menu_cliente = [
    ['[1] Cadastrar clientes'],
    ['[2] Exibir clientes'],
    ['[3] Editar clientes'],
    ['[4] Excluir clientes'],
    ['[0] Voltar para o menu principal']
]

# Menu Pedidos de vendas
opcoes_menu_venda = [
    ['[1] Novo pedido'],
    ['[2] Exibir pedidos pendentes'],
    ['[3] Exibir cardápio'],
    ['[0] Voltar para o menu principal']
]

# ------ Definição de Classes ------ 

# Produto
class Produtos:
    def __init__(self, codigo_produto, nome_produto, preco_produto, descricao, categoria):
        self.codigo = codigo_produto
        self.nome = nome_produto
        self.preco = preco_produto
        self.descricao = descricao
        self.categoria = categoria
    
    # Exibir informacoes de produtos
    def __str__(self):
        return f'Código: {self.codigo} | Nome: {self.nome} | Preço: R$ {self.preco: .2f} | Descrição: {self.descricao} | Categoria: {self.categoria}'

# Cliente
class Cliente():
    def __init__(self,codigo_cliente,nome_cliente,cpf, data_nascimento):
        self.codigo_cliente = codigo_cliente
        self.nome_cliente = nome_cliente
        self.documento = cpf
        self.nascimento = data_nascimento
    
    # Exibir informacoes de clientes
    def __str__(self):
        return f'Código: {self.codigo_cliente} | Nome: {self.nome_cliente} | CPF: {self.documento} | Data de Nascimento: {self.nascimento}'

# ------ Funçoes ------ 

# Obter o ultimo codigo do produto
def obter_ultimo_codigo_produto():
    ultimo_codigo = 0
    if os.path.exists('lista_produtos.csv'):
        try:
            with open('lista_produtos.csv', mode='r', newline='', encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo)
                next(leitor, None)  # Pular o cabeçalho
                for linha in leitor:
                    if linha and linha[0].isdigit():
                        ultimo_codigo = max(ultimo_codigo, int(linha[0]))
        except FileNotFoundError:
            pass  # O arquivo ainda não existe, retorna 0
        except Exception as e:
            print(f"Erro ao ler códigos de produtos: {e}")
    return ultimo_codigo + 1

# cadastrar produto
def cadastrar_produto():
    codigo = obter_ultimo_codigo_produto()
    nome = input('\nDigite o nome do produto: ')
    preco = float(input('Digite o valor unitário do produto: '))
    descricao = input('Digite a descrição do produto: ')
    categoria = input('Digite a categoria do produto: ')
        
    novo_produto = Produtos(codigo, nome, preco, descricao, categoria)
    lista_produtos.append(novo_produto)
    salvar_produtos_csv()
    print(f'\n Produto "{nome}" cadastrado com sucesso! Código: {novo_produto.codigo}\n')

# exibir produtos
def exibir_produtos():
    print('\n ------ Lista de Produtos ------\n')
    if not lista_produtos:
        print('\n Não há produto cadastrado\n')
    else:
        for produto in lista_produtos:
            print(produto)

# Editar produtos
def editar_produtos():
    # Exibe a lista de produtos cadastrados no sistema
    exibir_produtos()
    # Solicita ao usuário o código do produto que deseja editar
    cod_editar_produto = int(input('\n Digite o código do produto que deseja editar: '))
    produto_encontrado = False
    
    # Verifica a lista de produtos e verifica se o produto foi encontrado
    for produto in lista_produtos:
        if produto.codigo == cod_editar_produto:
            print(f'\n Produto encontrado: {produto}')
            # Caso tenha sido encontrado, pede para o usuário inserir as novas informações ou se não digitar mantém a antiga
            produto.nome = input('\nDigite o novo nome do produto: ') or produto.nome
            try:
                novo_preco = float(input('Digite o novo preço: '))
                if novo_preco:
                    produto.preco = novo_preco
            except ValueError:
                print('Preço inválido. O valor antigo será mantido.\n')
            produto.descricao = input('Digite a nova descrição: ') or produto.descricao
            produto.categoria = input('Digite a nova categoria: ') or produto.categoria
            salvar_produtos_csv()
            print('\n Produto atualizado com sucesso! \n')
            # marca o produto como encontrado, atualizado e encerra o loop
            produto_encontrado = True
            break
        # Se não encontrado, informa ao usuário
        if not produto_encontrado:
            print('\n Produto não encontrado.')

# Excluir produtos
def excluir_produto():
    # Exibe a lista dos produtos
    exibir_produtos()
    # solicita o codigo do produto para exclusão
    cod_excluir_prod = int(input('Digite o código do produto que deseja excluir: '))
    # Procura o código na lista de produtos
    for produto in lista_produtos:
        # se encontrado pergunta ao usuário se realmente deseja excluir
        if produto.codigo == cod_excluir_prod:
            print(f'\nProduto encontrado: {produto} \n')
            msg_confirmacao = input('Tem certeza que deseja excluir? (s/n): ').lower()
            # Se o usuário informar que sim, o produto é removido da lista
            if msg_confirmacao == 's':
                lista_produtos.remove(produto)
                salvar_produtos_csv()
                print('\n Produto excluído com sucesso! \n')
            # Se o usuário clicar em n ou digitar outra coisa, o processo é cancelado
            else:
                print('\n Processo de exclusão cancelado.\n')
            return
    # caso não encontre, informa ao usuário
    print('\n Produto não encontrado. \n')

# Salvar a lista produtos no arquivo csv
def salvar_produtos_csv():
    with open('lista_produtos.csv', mode='w',newline='',encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        # cabecalho
        writer.writerow(['Código','Nome','Preço','Descrição','Categoria'])
        # Dados
        for produto in lista_produtos:
            writer.writerow([produto.codigo, produto.nome, produto.preco, produto.descricao, produto.categoria])
    print('Lista de produtos salva em "lista_produtos.csv".')

# Carregar a lista de produtos do arquivo csv
def carregar_produtos_csv(arquivo ='lista_produtos.csv'):
    if os.path.exists(arquivo) and not lista_produtos: #Verifica se o arquivo existe e se a lista está vazia
        with open(arquivo,mode='r',newline='',encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                try:
                    produto = Produtos(
                        int(linha['Código']),
                        linha['Nome'],
                        float(linha['Preço']),
                        linha['Descrição'],
                        linha['Categoria']
                    )
                    lista_produtos.append(produto)
                except ValueError as e:
                    print(f'Erro ao carregar linha do CSV de produtos: {linha} - {e}')

# obter ultimo codigo do cliente
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
    
    # cadastro CPF e formatação e validação
    documento = input('Digite o CPF do cliente (11 dígitos): ')
    if len(documento) == 11:
        cpf_formatado = '{}.{}.{}-{}'.format(documento[:3],documento[3:6],documento[6:9],documento[9:])
    else:
        cpf_formatado = documento
    
    # cadastra da data de nascimento
    dia = int(input('Digite o dia de nascimento (2 dígitos): '))
    mes = int(input('Digite o mês de nascimento (2 dígitos): '))
    ano = int(input('Digite o ano de nascimento (4 dígitos): '))
    nascimento = f'{dia}/{mes}/{ano}'
    
    novo_cliente = Cliente(codigo_cliente, nome_cliente,cpf_formatado, nascimento)
    lista_clientes.append(novo_cliente)
    salvar_clientes_csv()
    print(f'Cliente "{nome_cliente}" cadastrado com sucesso! Código: {novo_cliente.codigo_cliente}\n')
    

# exibir clientes
def exibir_clientes():
    print('\n ------ Lista de Clientes ------\n')
    if not lista_clientes:
        print('\n Não há cliente cadastrado \n')
    else:
        for cliente in lista_clientes:
            print(cliente)

# Editar clientes
def editar_clientes():
    # exibi a informação dos clientes
    exibir_clientes()
    # Solicita o código para edição
    cod_editar_cliente = int(input('\n Digite o código do cliente que deseja editar: '))
    cliente_encontrado = False
    # procura a informação e se encontrado, solicita ao usuário para editar as informações necessárias
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

# Pedido de venda
def pedido_venda():
    print('Pedido de venda')

# Visualizar Cardapio
def visualizar_cardapio():
    print('Cardápio')

# Status do pedido
def status_pedidos():
    print('Status')

# ----- Menus ------

# Menu produtos
def menu_produto():
    while True:
        print('\n -------- Produtos --------')
        for item in opcoes_menu_produto:
            print(f"{item[0]}")
            
        opcao_selecionada_prod = input('Escolha uma opção: ')
        
        if opcao_selecionada_prod == "1":
            cadastrar_produto()
        elif opcao_selecionada_prod == "2":
            exibir_produtos()
        elif opcao_selecionada_prod == '3':
            editar_produtos()
        elif opcao_selecionada_prod == '4':
            excluir_produto()
        elif opcao_selecionada_prod == "0":
            break
        else:
            print(msg_opcao_inválida)

# Menu clientes
def menu_cliente():
    while True:
        print('\n -------- Clientes --------')
        for item in opcoes_menu_cliente:
            print(f"{item[0]}")
            
        opcao_selecionada_cliente = input('Escolha uma opção: ')
        
        if opcao_selecionada_cliente == "1":
            cadastrar_cliente()
        elif opcao_selecionada_cliente == "2":
            exibir_clientes()
        elif opcao_selecionada_cliente == '3':
            editar_clientes()
        elif opcao_selecionada_cliente == '4':
            excluir_cliente()
        elif opcao_selecionada_cliente == "0":
            break
        else:
            print(msg_opcao_inválida)

# Menu principal
def menu_sistema():
    # carregar os dados dos CSVs ao iniciar o sistema
    carregar_produtos_csv()
    carregar_clientes_csv()
    while True:
        print('\n -------- Menu --------\n')
        for item in menu:
            print(f"{item[0]}")
            
        opcao_menu = input('Escolha uma opção: ')
            
        if opcao_menu == '1':
            pedido_venda()
        elif opcao_menu == '2':
            menu_produto()
        elif opcao_menu == '3':
            menu_cliente()
        elif opcao_menu == '0':
            print('Sistema encerrado com sucesso')
            break
        else:
            print(msg_opcao_inválida)

# Executar menu
menu_sistema()
        

