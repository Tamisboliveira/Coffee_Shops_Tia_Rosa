# SISTEMA DE GESTÃO DE PEDIDOS PARA A COFFEE SHOPS TIA ROSA 
Este é um sistema simples de gerenciamento de **clientes**, **produtos** e **pedidos de venda**, foi desenvolvido em **Python** com geração de dados via arquivos **CSV**. Ele simula o funcionamento de um sistema de controle básico de vendas com menus interativos em terminal.

---

## 💡 Objetivos do Projeto

Este sistema foi desenvolvido com fins educacionais, com o objetivo de praticar:

- Aplicar os conceitos estudados na disciplina: **Lógica - Algoritmos e programação de computadores.**
- Estruturação de sistemas por módulos
- Manipulação de arquivos CSV
- Criação de menus interativos com laços de repetição e condicionais
- Organização de código com funções reutilizáveis
- Lógica de CRUD (Create, Read, Update, Delete)

## 📌 Observações

- Todos os dados são armazenados em arquivos .csv, facilitando a leitura em editores de planilhas.
- O sistema não utiliza banco de dados, por ser voltado para aprendizado de lógica de programação e estrutura de arquivos.
- O foco é aprendizado prático de Python, seguindo boas práticas como modularização e documentação.

## 📋 Funcionalidades

O sistema permite:

### 📦 Produtos
- Cadastro de novos produtos
- Listagem de produtos cadastrados
- Edição de informações dos produtos
- Exclusão de produtos

### 🧑‍🤝‍🧑 Clientes
- Cadastro de novos clientes
- Listagem de clientes
- Edição de dados cadastrais
- Exclusão de clientes

### 🧾 Pedidos
- Criação de novos pedidos de venda
- Consulta de pedidos pendentes
- Atualização de status dos pedidos (pendente → concluído)

---

## 🗂 Estrutura do Projeto
- clients.py: Funções relacionadas à gestão de clientes
- products.py: Funções relacionadas à gestão de produtos
- orders.py: Funções relacionadas aos pedidos de venda
- main.py: Script principal, ponto de entrada do sistema
- lista_clientes.csv: Base de dados dos clientes
- lista_produtos.csv: Base de dados dos produtos
- lista_pedidos.csv: Base de dados dos pedidos

---

## ▶️ Como Executar

1. **Clone o repositório ou copie os arquivos:**
```bash
git clone https://github.com/Tamisboliveira/Coffee_Shops_Tia_Rosa
```
2. **Execute o script principal:**
```bash
python main.py
```
_Observação: é necessário ter o Python instalado._

## ✍️ Autor
Tamires Bento de Oliveira