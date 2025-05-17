"""
Módulo: main.py

Descrição:
-----------
Este módulo é o ponto de entrada do sistema de controle de pedidos.
Gerencia a navegação entre os menus principais e executa as funcionalidades 
relacionadas a clientes, produtos e pedidos.

Funcionalidades:
----------------
- Menu principal do sistema
- Acesso aos submenus:
    - Pedido de venda
    - Produtos
    - Clientes
- Execução das operações de cadastro, edição, exclusão e visualização
- Carregamento automático dos dados salvos em arquivos CSV ao iniciar o sistema

Funções:
--------
- menu_produto(): exibe e gerencia as opções do menu de produtos.
- menu_cliente(): exibe e gerencia as opções do menu de clientes.
- menu_orders(): exibe e gerencia as opções do menu de pedidos.
- menu_sistema(): exibe o menu principal e direciona o fluxo de navegação do sistema.

Execução:
---------
O sistema inicia automaticamente ao rodar o script, por meio da chamada da função menu_sistema().
"""

import clients
import products
import orders

# Mensagem de operação inválida
msg_opcao_invalida = "Operação inválida! Por favor digite um número válido."

# Menu principal com acesso às funcionalidades do sistema

# Menu principal
menu = [
    ['[1] Pedido de venda'],
    ['[2] Produtos'],
    ['[3] Clientes'],
    ['[0] Sair'] 
]

# ----- Menus ------

# Menu produtos
def menu_produto():
    while True:
        print('\n -------- Produtos --------\n')
        for item in products.opcoes_menu_produto:
            print(f"{item[0]}")
            
        opcao_selecionada_prod = input('\nEscolha uma opção: ')
        
        if opcao_selecionada_prod == "1":
            products.cadastrar_produto()
        elif opcao_selecionada_prod == "2":
            products.exibir_produtos()
        elif opcao_selecionada_prod == '3':
            products.editar_produtos()
        elif opcao_selecionada_prod == '4':
            products.excluir_produto()
        elif opcao_selecionada_prod == "0":
            print('Voltando ao menu principal...\n')
            break
        else:
            print(msg_opcao_invalida)

# Menu clientes
def menu_cliente():
    while True:
        print('\n -------- Clientes --------\n')
        for item in clients.opcoes_menu_cliente:
            print(f"{item[0]}")
            
        opcao_selecionada_cliente = input('\nEscolha uma opção: ')
        
        if opcao_selecionada_cliente == "1":
            clients.cadastrar_cliente()
        elif opcao_selecionada_cliente == "2":
            clients.exibir_clientes()
        elif opcao_selecionada_cliente == '3':
            clients.editar_clientes()
        elif opcao_selecionada_cliente == '4':
            clients.excluir_cliente()
        elif opcao_selecionada_cliente == "0":
            print('Voltando ao menu principal...\n')
            break
        else:
            print(msg_opcao_invalida)

# Menu pedidos
def menu_orders():
    while True:
        print('\n -------- Pedidos --------\n')
        for item in orders.opcoes_menu_venda:
            print(f"{item[0]}")
            
        opcao_selecionada_orders = input('\nEscolha uma opção: ')
        
        if opcao_selecionada_orders == "1":
            orders.novo_pedido()
        elif opcao_selecionada_orders == "2":
            orders.exibir_pedidos_pendentes()
        elif opcao_selecionada_orders== '3':
            orders.editar_status_pedidos()
        elif opcao_selecionada_orders == "0":
            print('Voltando ao menu principal...\n')
            break
        else:
            print(msg_opcao_invalida)

# Menu principal
def menu_sistema():
    # carregar os dados dos CSVs ao iniciar o sistema
    products.carregar_produtos_csv()
    clients.carregar_clientes_csv()
    orders.carregar_pedidos_csv()
    while True:
        print('\n -------- Menu --------\n')
        for item in menu:
            print(f"{item[0]}")
            
        opcao_menu = input('Escolha uma opção: ')
            
        if opcao_menu == '1':
            menu_orders()
        elif opcao_menu == '2':
            menu_produto()
        elif opcao_menu == '3':
            menu_cliente()
        elif opcao_menu == '0':
            print('Sistema encerrado com sucesso')
            break
        else:
            print(msg_opcao_invalida)

# Executar menu
menu_sistema()
        

