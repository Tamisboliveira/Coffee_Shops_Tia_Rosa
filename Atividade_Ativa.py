#Criando informações para o menu de acesso ao sistema
menu = [
    ['[1] Pedido de venda'],
    ['[2] Cadastro produtos'],
    ['[3] Cadastro clientes'],
    ['[4] Cardápio'],
    ['[5] Status pedidos'],
    ['[0] Sair'] 
]

cabecalho = '\n -------- Menu --------'

# ------ Criando Classes ------ 
#Produto
class Produtos():
    def __init__(self, codigo_produto, nome_produto, preco, descricao, categoria):
        self.codigo = codigo_produto
        self.nome = nome_produto
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria

#Cliente
class Cliente():
    def __init__(self,codigo_cliente,nome_cliente,cpf, data_nascimento):
        self.codigo = codigo_cliente
        self.nome = nome_cliente
        self.documento = cpf
        self.nascimento = data_nascimento

# ------ Criando funçoes ------ 

#Pedido de venda
def pedido_venda():
    print('Pedido de venda')

#Cadastro de Produtos
def cadastro_produto():
    print('Produto')

#Cadastro de Cliente
def cadastro_cliente():
    print('Cliente')

#Visualizar Cardapio
def visualizar_cardapio():
    print('Cardápio')

#Status do pedido
def status_pedidos():
    print('Status')

#Função seleção do menu
def menu_sistema():
    while True:
        print(cabecalho)
        for item in menu:
            print(f"{item[0]}")
            
        opcao_menu = input('Escolha uma opção: ')
            
        if opcao_menu == '1':
            pedido_venda()
        elif opcao_menu == '2':
            cadastro_produto()
        elif opcao_menu == '3':
            cadastro_cliente()
        elif opcao_menu == '4':
            visualizar_cardapio()
        elif opcao_menu == '5':
            status_pedidos()
        elif opcao_menu == '0':
            print('Sistema encerrado com sucesso')
            break
        else:
            print('Opção inválida!')

#Executar menu
menu_sistema()
        

