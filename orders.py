import csv
import os
import clients
import products

# lista de armazenamento de pedidos
lista_pedidos = []

# Menu Pedidos de vendas
opcoes_menu_venda = [
    ['[1] Novo pedido'],
    ['[2] Pedidos pendentes'],
    ['[3] Alterar status pedido'],
    ['[0] Voltar para o menu principal']
]

# ------ Definição de Classes ------ 

class orders():
    def __init__(self, num_pedido,item, codigo_produto, descricao,quantidade, valor_unitario, valor_total, codigo_cliente, cliente, status_pedido):
        self.num_pedido = num_pedido
        self.item = item
        self.codigo_produto = codigo_produto
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total
        self.codigo_cliente = codigo_cliente
        self.cliente = cliente
        self.status_pedido = status_pedido
        
    # exibir informacoes do pedido
    def __str__(self):
        return f'Nº Pedido: {self.num_pedido} | Cliente: {self.codigo_cliente} - {self.cliente} \n Item: {self.item} | Produto: {self.codigo_produto} - {self.descricao} | Quantidade: {self.quantidade} | Valor unitário R$: {self.valor_unitario:.2f} Valor Total R$: {self.valor_total:.2f}'

# ------ Funçoes ------ 
def salvar_pedidos_csv():
    with open('lista_pedidos.csv', mode='w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        # Cabeçalho do arquivo CSV
        writer.writerow(['num_pedido', 'item', 'codigo_produto', 'descricao', 'quantidade', 'valor_unitario', 'valor_total', 'codigo_cliente', 'cliente', 'status_pedido'])
        # Escrever cada item do pedido na sua própria linha
        for item_pedido in lista_pedidos:
            writer.writerow([
                item_pedido['num_pedido'],
                item_pedido['item'],
                item_pedido['codigo_produto'],
                item_pedido['descricao'],
                item_pedido['quantidade'],
                item_pedido['valor_unitario'],
                item_pedido['valor_total'],
                item_pedido['codigo_cliente'],
                item_pedido['cliente'],
                item_pedido['status_pedido']
            ])
    print('Lista de pedidos salva em "lista_pedidos.csv".')
    
# Obter o ultimo numero do pedido
def obter_ultimo_num_pedido():
    ultimo_num_pedido = 0
    if os.path.exists('lista_pedidos.csv'):
        try:
            with open('lista_pedidos.csv',mode='r',newline='',encoding='utf-8') as arquivo:
                leitor = csv.reader(arquivo) 
                next(leitor, None)
                for linha in leitor:
                    if linha and linha[0].isdigit():
                        ultimo_num_pedido = max(ultimo_num_pedido, int(linha[0]))
        except FileNotFoundError:
            pass 
        except Exception as e:
            print(f"Erro ao ler pedidos: {e}")
    return ultimo_num_pedido + 1

def imprimir_pedido(num_pedido, lista_itens_pedido, cliente):
    print("\n" + "=" * 80)
    print(" "*25 + "Coffee Shops Tia Rosa")
    print("=" * 80)
    print(f"Pedido: {num_pedido:04d}")  # Formata o número do pedido com zeros à esquerda
    print(f"Cliente: {cliente['codigo_cliente']} - {cliente['cliente']}")
    print("-" * 80)
    print(f"{'Item':<5} {'Código + Descrição Produto':<40} {'Qtd.':<8} {'Valor Unit':<12} {'Valor Total':<12}")
    print("-" * 80)

    total_pedido = 0.0
    for item in lista_itens_pedido:
        print(f"{item['item']:<5} {item['codigo_produto']} - {item['descricao']:<36} {item['quantidade']:<8} R$ {item['valor_unitario']:<11.2f} R$ {item['valor_total']:<11.2f}")
        total_pedido += item['valor_total']

    print("-" * 80)
    print(f"{'Total do Pedido:':>68} R$ {total_pedido:<12.2f}")
    print("=" * 80 + "\n")

# cadastrar novo pedido
def novo_pedido():
    num_pedido = obter_ultimo_num_pedido()
    num_item_atual = 1
    
    # Exibir lista de clientes para seleciona-lo
    clients.exibir_clientes()
    cod_cliente_pedido = int(input('\n Digite o código do cliente para o pedido: '))
    cliente_encontrado = next((c for c in clients.lista_clientes if int(c.codigo_cliente) == cod_cliente_pedido), None)
    
    if not cliente_encontrado:
        msg_confirmacao = print('\n Cliente não encontrado. Deseja realizar o cadastro? (s/n): ').lower()
        # se o usuário quiser cadastrar chama a função de cadastro de cliente
        if msg_confirmacao == 's':
            clients.cadastrar_cliente()
        # se não, cancela o processo de pedido e retorna
        else:
            print('\n Pedido cancelado.')
        return
    print(f'\n Pedido Nº {num_pedido} para: {cliente_encontrado.codigo_cliente} - {cliente_encontrado.nome_cliente}\n')
    
    while True:
        # Visualizar a lista de produtos (cardapio)
        products.exibir_produtos()
        print('Insira as informações do pedido: \n')
        
        cod_produto_pedido = int(input('\n Digite o código do produto para o pedido: '))
        prod_encontrado = next((p for p in products.lista_produtos if p.codigo == cod_produto_pedido), None)
        
        if not prod_encontrado:
            print('Produto não encontrado.')
            continue #volta para o inicio do loop para tentar novamente
        else:
            try:
                quantidade = int(input('\n Digite a quantidade desejada: '))
                valor_total_item = float(quantidade * prod_encontrado.preco)
                
                # Criar o item do pedido como um dicionário
                item_pedido = {
                    'num_pedido': num_pedido,
                    'item': num_item_atual,
                    'codigo_produto': prod_encontrado.codigo,
                    'descricao': prod_encontrado.nome,
                    'quantidade': quantidade,
                    'valor_unitario':prod_encontrado.preco,
                    'valor_total': valor_total_item,
                    'codigo_cliente': cliente_encontrado.codigo_cliente,
                    'cliente': cliente_encontrado.nome_cliente,
                    'status_pedido': 'Pendente'
                }
                
                # Adicionar o item à lista de pedidos
                lista_pedidos.append(item_pedido)
                print(f'\n {quantidade} x {prod_encontrado.nome} adicionado ao pedido.')

                continuar = input('\n Deseja adicionar mais itens ao pedido? (s/n): ').lower()
                if continuar != 's':
                    print(f'\n Pedido Nº {num_pedido} finalizado.')
                    salvar_pedidos_csv()
                    
                    # Filtrar os itens do pedido atual para impressão
                    itens_pedido_atual = [item for item in lista_pedidos if item['num_pedido'] == num_pedido]

                    # Buscar as informações completas do cliente na lista de clientes
                    cliente_pedido = next((c for c in clients.lista_clientes if int(c.codigo_cliente) == cod_cliente_pedido), None)
                    cliente_info = {'codigo_cliente': cliente_pedido.codigo_cliente, 'cliente': cliente_pedido.nome_cliente} if cliente_pedido else {'codigo_cliente': 'N/A', 'cliente': 'Cliente não encontrado'}

                    imprimir_pedido(num_pedido, itens_pedido_atual, cliente_info)
                    
                    break # Sai do loop de adicionar itens
                num_item_atual += 1 # incrementa para o próximo item

            except ValueError:
                print('Quantidade inválida. Digite um número inteiro.')

# atualizar status pedidos
def exibir_pedidos_pendentes():
    pedidos_pendentes = [item for item in lista_pedidos if item['status_pedido'].lower() == 'pendente']
    # exibi a informação dos pedidos
    
    if not pedidos_pendentes:
        print('\n Não há pedidos pendentes no momento.\n')
        return
    pedidos_agrupados = {}
    for item in pedidos_pendentes:
        num_pedido = item['num_pedido']
        if num_pedido not in pedidos_agrupados:
            pedidos_agrupados[num_pedido] = []
        pedidos_agrupados[num_pedido].append(item)
    
    print("\n----- Pedidos Pendentes -----\n")
    for num_pedido, itens in pedidos_agrupados.items():
        print(f"Pedido: {num_pedido}")
        for item in itens:
            print(f"  Item {item['item']:<5}  {item['descricao']:<20} Qtd: {item['quantidade']}")
        print("-" * 10 + "\n")

# Editar status de pedidos
def editar_status_pedidos():
    while True:
        exibir_pedidos_pendentes()

        # Verifica se há pedidos pendentes
        pedidos_pendentes_existentes = any(item['status_pedido'].lower() == 'pendente' for item in lista_pedidos)
        if not pedidos_pendentes_existentes:
            print('\n Não há mais pedidos pendentes para alterar o status.')
            break # Sai se não houver pedidos pendentes

        try:
            num_editar_pedido_str = input('\nDigite o número do pedido que deseja marcar como "Concluído" (ou 0 para sair): ')
            if num_editar_pedido_str == '0':
                break
            num_editar_pedido = int(num_editar_pedido_str)
        except ValueError:
            print("Número de pedido inválido. Por favor, digite um número.")
            continue

        # Encontrar ALGUNS itens do pedido para exibir informações gerais (cliente)
        itens_do_pedido = [item for item in lista_pedidos if int(item['num_pedido']) == num_editar_pedido and item['status_pedido'].lower() == 'pendente']

        if not itens_do_pedido:
            print(f"\nPedido Nº {num_editar_pedido} não encontrado ou não está pendente.")
        else:
            # Exibe informações gerais do pedido 
            cliente_info = f"{itens_do_pedido[0]['cliente']} (Código: {itens_do_pedido[0]['codigo_cliente']})"
            print(f"\n--- Pedido Nº {num_editar_pedido} Encontrado ---")
            print(f"Cliente: {cliente_info}")
            print('\nItens do Pedido:')
            for item in itens_do_pedido:
                print(f'- Produto: {item['descricao']:<20} Quantidade: {item['quantidade']}')

            confirmacao = input(f"\nDeseja marcar o Pedido Nº {num_editar_pedido} como 'Concluído'? (s/n): ").lower()
            if confirmacao == 's':
                itens_atualizados_count = 0
                for item in lista_pedidos:
                    if int(item['num_pedido']) == num_editar_pedido and item['status_pedido'].lower() == 'pendente':
                        item['status_pedido'] = 'Concluído'
                        itens_atualizados_count += 1

                if itens_atualizados_count > 0:
                    print(f"\nPedido Nº {num_editar_pedido} marcado como 'Concluído'.")
                    salvar_pedidos_csv()
                else:
                    print("Nenhum item pendente encontrado para este pedido para atualizar.")
            else:
                print("\nAlteração de status cancelada.")

        continuar_alterando = input("\nDeseja alterar o status de outro pedido? (s/n): ").lower()
        if continuar_alterando != 's':
            break
    print("\nSaindo da alteração de status de pedidos.")
    
    
# Carregar a lista de pedidos do arquivo csv
def carregar_pedidos_csv(arquivo='lista_pedidos.csv'):
    if os.path.exists(arquivo) and not lista_pedidos:
        with open(arquivo, mode='r', newline='', encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                try:
                    lista_pedidos.append(linha) # Os dados serão carregados como dicionários
                except Exception as e:
                    print(f"Erro ao carregar pedidos do CSV: {e}")
            