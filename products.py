"""
Módulo: products.py

Descrição:
-----------
Este módulo contém todas as funcionalidades relacionadas à gestão de produtos em um sistema de controle de pedidos.
As operações incluem:
    - Cadastro de novos produtos
    - Visualização da lista de produtos
    - Edição de informações dos produtos
    - Exclusão de produtos
    - Geração de arquivo CSV

Classes:
--------
- Produtos: representa um produto com código, nome, preço, descrição e categoria

Funções:
--------
- obter_ultimo_codigo_produto(): retorna o próximo código disponível
- cadastrar_produto(): permite cadastrar um novo produto
- exibir_produtos(): exibe todos os produtos cadastrados
- editar_produtos(): permite editar informações de um produto existente
- excluir_produto(): remove um produto da lista
- salvar_produtos_csv(): salva a lista de produtos em CSV
- carregar_produtos_csv(): carrega produtos do arquivo CSV

"""

import csv
import os

# lista de armazenamento de produtos e clientes
lista_produtos = []

# lista com as opções do menu de gerenciamento de produtos
opcoes_menu_produto = [
    ['[1] Cadastrar produtos'],
    ['[2] Exibir produtos'],
    ['[3] Editar produtos'],
    ['[4] Excluir produtos'],
    ['[0] Voltar para o menu principal']
]

# lista com as categorias disponíveis para os produtos
categoria_produtos = [
    ['[1] Bebidas quentes'],
    ['[2] Bebidas geladas'],
    ['[3] Lanches'],
    ['[4] Doces']
]
# ------ Definição de Classes ------ 

# Classe que representa um produto cadastrado
class Produtos:
    def __init__(self, codigo_produto, nome_produto, preco_produto, descricao, categoria):
        self.codigo = codigo_produto        # código unico do produto
        self.nome = nome_produto            # nome do produto
        self.preco = preco_produto          # preço unitário do produto
        self.descricao = descricao          # Descrição detalhada do produto
        self.categoria = categoria          # Categoria a qual o produto pertence
    
    # Exibir informacoes de produtos
    def __str__(self):
        return f'Código: {self.codigo} | Nome: {self.nome} | Preço: R$ {self.preco: .2f} | Descrição: {self.descricao} | Categoria: {self.categoria}'


# ------ Funçoes ------ 

# Retorna o próximo código disponível para um novo produto, com base nos registros existentes no arquivo CSV
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
    print('\nCategorias: ')
    for item in categoria_produtos:
        print(f"{item[0]}")
        
    # Usuário seleciona a categoria através do número, que será convertido em nome descritivo
    selecao_categoria = input('\nSelecione a categoria do produto: ')
    
    if selecao_categoria == '1':
        categoria = 'Bebidas quentes'
    elif selecao_categoria == '2':
        categoria = 'Bebidas geladas'
    elif selecao_categoria == '3':
        categoria = 'Lanches'
    elif selecao_categoria == '4':
        categoria = 'Doces'
    else:
        print('Categoria não encontrada.')
        return
        
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
            
            print('\nCategorias: ')
            for item in categoria_produtos:
                print(f"{item[0]}")
                
            selecao_categoria = input('\nSelecione a categoria do produto: ')
            if selecao_categoria == '':
                pass #usuário mantém a categoria atual
            elif selecao_categoria == '1':
                produto.categoria = 'Bebidas quentes'
            elif selecao_categoria == '2':
                produto.categoria = 'Bebidas geladas'
            elif selecao_categoria == '3':
                produto.categoria = 'Lanches'
            elif selecao_categoria == '4':
                produto.categoria = 'Doces'
            else:
                print('Categoria inválida. Categoria anterior será mantida.')
        
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
                salvar_produtos_csv() # Atualiza o arquivo após remoção
                print('\n Produto excluído com sucesso! \n')
            # Se o usuário clicar em n ou digitar outra coisa, o processo é cancelado
            else:
                print('\n Processo de exclusão cancelado.\n')
            return
    # caso não encontre, informa ao usuário
    print('\n Produto não encontrado. \n')

# Salva a lista de produtos no arquivo CSV para persistência dos dados
def salvar_produtos_csv():
    with open('lista_produtos.csv', mode='w',newline='',encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        # cabecalho
        writer.writerow(['Código','Nome','Preço','Descrição','Categoria'])
        # Dados
        for produto in lista_produtos:
            writer.writerow([int(produto.codigo), produto.nome, produto.preco, produto.descricao, produto.categoria])
    print('Lista de produtos salva em "lista_produtos.csv".')

# Carrega os dados de produtos do arquivo CSV para a lista em memória, evitando duplicidade
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
