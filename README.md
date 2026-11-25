# 💳 API de Análise de Crédito

API e interface web desenvolvidas em Python para processamento, geração de dados e análise de perfil de crédito de clientes.

---

## 📋 Sobre o Projeto

O **api-analise-credito** tem como objetivo automatizar a avaliação de risco e concessão de crédito a partir de dados cadastrais e financeiros. O projeto conta com um gerador de massa de dados para testes, uma API principal e uma interface web para visualização e interação.

---

## 📂 Estrutura do Repositório

```text
api-analise-credito/
├── app_web.py           # Interface web para interação com a análise
├── main.py              # Ponto de entrada principal da API
├── gerar_dados.py       # Script para geração de dados fictícios de clientes
├── clientes_teste.xlsx  # Base de dados de exemplo em planilha
├── requirements.txt     # Dependências do projeto
└── .gitignore           # Arquivos ignorados pelo Git
```

---

## 🚀 Tecnologias Utilizadas

* **[Python 3](https://python.org)** — Linguagem principal do projeto
* **Framework Web / API** — *(ex.: FastAPI, Flask ou Streamlit — ajuste conforme seu `requirements.txt`)*
* **Manipulação de Dados** — *(ex.: Pandas, OpenPyXL)*

---

## ⚙️ Pré-requisitos e Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd api-analise-credito
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/macOS:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Como Executar

1. **(Opcional) Gerar novos dados de teste:**
   ```bash
   python gerar_dados.py
   ```

2. **Iniciar a API:**
   ```bash
   uvicorn main:app --reload
   ```
3. **Iniciar a interface web:**
   ```bash
   streamlit run app_web.py
   ```
 

---

## 📌 Exemplos de Uso / Endpoints

> *Adicione aqui as rotas da sua API ou capturas de tela da interface web.*

* **`POST /analisar`** — Recebe os dados do cliente e retorna o score ou status de aprovação.
* **`GET /clientes`** — Lista os registros carregados a partir da base de teste.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request* com melhorias.

---



Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes (ou ajuste conforme a licença escolhida).
