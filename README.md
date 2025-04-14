# Alumind Analyzer

## ✨ Sobre o Projeto

O **AluMind Analyzer** é uma aplicação Flask que recebe feedbacks de usuários, analisa o sentimento utilizando modelos de linguagem (LLMs) e gera relatórios e e-mails automáticos com base nesses feedbacks.

Funcionalidades principais:

- Classificação de sentimento (positivo, negativo, inconclusivo)
- Extração de funcionalidades sugeridas pelos usuários
- Relatórios semanais
- Envio de resumo por e-mail automático

---
## 🛠️ Tecnologias Utilizadas

- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL (Docker)
- Langchain + Gemini API (Google) ou OpenAI
- Pydantic
- smtplib para envio de e-mails

---

## ⚙️ Configurações Iniciais

### Pre-requisitos
- Python 3.11
- Docker desktop
- Postman ou Insomnia (para testar rotas)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/alumind-analyzer.git
cd alumind-analyzer
```

---

### 2. Crie e ative um ambiente virtual 

Se estiver usando **conda**:

```bash
conda create -n alumind-analyzer python=3.11
conda activate alumind-analyzer
```

Se preferir **venv**:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variáveis de ambiente

Troque o arquivo  `.env.example` por `.env` na raiz do projeto e adicione as configurações que forem necessárias:

```env
POSTGRES_USER=alumind
POSTGRES_PASSWORD=alumind123
POSTGRES_DB=alumind_db

DATABASE_URL=postgresql://alumind:alumind123@localhost:5432/alumind_db

GOOGLE_API_KEY=api-key-gemini #inserir uma apikey gemini valida
PROJECT_ID=seu-projeto-google #inserir um projeto do google valido
GEMINI_MODEL=gemini-1.5-flash

OPENAI_API_KEY=api-key-gpt #inserir uma apikey do gpt valida
OPENAI_MODEL=gpt-3.5-turbo

GMAIL_SENDER=email@gmail.com #inserir o email que enviará os resumos
GMAIL_SENDER_PASSWORD=senha-email-app #inserir senha do email

LLM_PROVIDER=OPENAI #a depender da LLM que for usar, mudar entre OPENAI ou GEMINI
```

**Importante:**  
- Use **senha de aplicativo** do Gmail, que pode ser configurada na aba de Segurança > Senhas de App.
- IMPORTANTE: A **senha de aplicativo** só é válida se o email usado tiver autenticação de dois fatores ativada.
- Configure seu acesso às APIs da Gemini/OpenAI.

---

### 5. Subir o Banco de Dados PostgreSQL via Docker

Suba o container:

```bash
docker-compose up -d
```

### 6. Criar as tabelas no Banco

Após o banco estar rodando, execute:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

- Isso cria a estrutura do banco de dados.

---

### 7. Alterar o email do destinatário

Para que o email seja enviado com sucesso, altere o email do destinatário dos resumos semanais, que na atividade é um possível stakeholder:

Acesse o `email_controller.py` e mude o `email-receiver@gmail.com`:
```bash
        recipients = ["email-receiver@gmail.com"] #aqui
        subject = "Resumo Semanal de Feedbacks - AluMind"
        self.email_service.send_email(subject, recipients, email_text)
```

## 🚀 Como Rodar o Projeto

### 1. Iniciar a aplicação Flask

```bash
flask run
```

A aplicação estará disponível em:

```
http://127.0.0.1:5000/
```

---

## 🌟 Rotas Disponíveis

| Rota | Método | Descrição |
|:---|:---|:---|
| `/` | GET | Página inicial |
| `/feedbacks` | POST | Recebe e classifica feedbacks |
| `/report` | GET | Exibe relatório de feedbacks |
| `/report/feedback/<id>` | GET | Exibe detalhes de um feedback específico |
| `/send_mail` | POST | Envia e-mail semanal com resumo dos feedbacks |

---

### Utilize Insomnia ou Postman para testar as rotas /feedbacks e /send_mail 

Exemplo de JSON para `/feedbacks`

```json
{
  "id": "4042f20a-45f4-4647-8050-139ac16f610b",
  "feedback": "Gosto muito de usar o Alumind! Só queria uma forma mais fácil de editar meu perfil."
}
```

---

## Contribuições
Contribuições são bem vindas! Sinta-se a vontade para abrir issues e enviar pull requests.

---
Developed by Jamilla Lobo <♡︎/>
