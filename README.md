# 🧠 AutoMind - Plataforma de Vendas Veiculares com IA

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![IA](https://img.shields.io/badge/AI-Scikit--Learn-orange)

> **Projeto de TCC:** Sistema web para compra e venda de veículos que utiliza Inteligência Artificial (Machine Learning) para auxiliar vendedores na precificação justa de seus automóveis.

---

## 🎯 O Problema
Vendedores particulares muitas vezes têm dificuldade em definir o preço de venda de seus veículos. Preços muito altos afugentam compradores; preços muito baixos geram prejuízo.

## 💡 A Solução (AutoMind)
Uma plataforma completa de marketplace (estilo Webmotors) integrada a um módulo de **Inteligência Artificial Preditiva**.
O sistema analisa o ano de fabricação e a quilometragem do veículo e, utilizando um modelo de **Regressão Linear**, sugere o valor ideal de mercado em tempo real.

---

## 🚀 Funcionalidades Principais

### 1. Módulo de Inteligência Artificial
* **Sugestão de Preço:** Algoritmo treinado com base histórica de mercado.
* **Aprendizado Contínuo:** O modelo pode ser re-treinado conforme novos anúncios são inseridos na plataforma.

### 2. Gestão de Anúncios (CRUD)
* **Cadastro Completo:** Upload de fotos, marca, modelo, ano, KM e categoria.
* **Painel do Vendedor:** Permite editar e excluir seus próprios anúncios.
* **Catálogo Público:** Busca e filtragem de veículos por categoria (Carros, Motos, Caminhões).

### 3. Segurança e Acesso
* **Sistema de Login:** Autenticação criptografada (Hash de senha).
* **Controle de Permissão:** Diferenciação entre perfis de `Cliente` (apenas visualiza/contata) e `Vendedor` (cria anúncios).

### 4. Experiência do Usuário (UX)
* **Dark Mode:** Tema escuro automático com persistência de preferência.
* **Contato Direto:** Botão de WhatsApp integrado na página do anúncio.
* **Design Responsivo:** Adaptável para Celulares e Desktop.

---

## 🛠 Tecnologias Utilizadas

* **Back-end:** Python 3, Flask (Framework Web).
* **Banco de Dados:** SQLite com SQLAlchemy (ORM).
* **Inteligência Artificial:** Scikit-Learn (Biblioteca de Ciência de Dados), Pandas, Numpy.
* **Front-end:** HTML5, CSS3 Moderno (Grid/Flexbox), JavaScript (Fetch API).

---

## 📸 Capturas de Tela

*(Espaço reservado para colocar prints do sistema rodando)*

---

## ⚙️ Como Rodar o Projeto

### Pré-requisitos
* Python instalado (versão 3.8 ou superior).
* Git instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/automind-tcc.git](https://github.com/SEU-USUARIO/automind-tcc.git)
    cd automind-tcc
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

5.  **Acesse no navegador:**
    Abra `http://127.0.0.1:5000`

---

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos.

---
**Desenvolvido por Jefferson Alan Schmidt Ludwig**