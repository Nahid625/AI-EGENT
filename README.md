# 🤖 AI-EGENT

> **Deep Research AI Agent** — Powered by LangChain & FastAPI

An intelligent AI agent built with FastAPI and LangChain that handles question-answering, multi-turn chat sessions, user history tracking, image understanding, and deep research capabilities — all backed by a PostgreSQL database.

---

## ✨ Features

| Feature | Status |
|---|---|
| 🧠 AI Q&A (question & answer routes) | ✅ Done |
| 👤 User Authentication (JWT) | 🔧 In Progress |
| 🗂️ Chat Session & History System | 🔧 In Progress |
| 🖼️ Image Understanding & Explanation | 🔧 In Progress |
| 🐘 PostgreSQL Database (via SQLAlchemy + Alembic) | ✅ Configured |
| 🔄 Database Migrations (Alembic) | ✅ Configured |

---

## 🗂️ Project Structure

```
AI-EGENT/
├── main.py               # FastAPI app entry point
├── personal.py           # Personal/dev utilities
├── alembic.ini           # Alembic migration config
├── requirements.txt      # Python dependencies
├── alembic/              # Database migration scripts
├── src/
│   ├── config/
│   │   └── db.py         # Database engine & session setup
│   ├── schemas/
│   │   └── schema.py     # SQLAlchemy models (User, ChatSession, Message)
│   └── routes/
│       ├── ai_router.py  # AI question & answer endpoints
│       └── userRoute.py  # User management endpoints
└── pymodule/             # Custom Python modules
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Nahid625/AI-EGENT.git
cd AI-EGENT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_egent
SECRET_KEY=your_secret_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Start the Server

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`

---

## 📡 API Endpoints

### AI Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ai/ask` | Ask the AI a question |
| `POST` | `/ai/image` | Upload an image for AI explanation |

### User Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/user/register` | Register a new user |
| `POST` | `/user/login` | Login and get JWT token |
| `GET` | `/user/history` | Get user's chat history |
| `GET` | `/user/sessions` | List all chat sessions |

---

## 🗺️ Roadmap

- [x] AI Q&A route implementation
- [x] PostgreSQL integration with SQLAlchemy
- [x] Alembic migration setup
- [ ] **Auth system** — JWT-based user registration & login
- [ ] **Chat history system** — Persist and retrieve per-user Q&A history
- [ ] **Image understanding** — Allow users to upload images and get AI explanations
- [ ] Session management & pagination
- [ ] Rate limiting & API key management
- [ ] Dockerize the application

---

## 🛠️ Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **AI / LLM:** [LangChain](https://www.langchain.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Server:** [Uvicorn](https://www.uvicorn.org/)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 👤 Author

**Nahid** — [@Nahid625](https://github.com/Nahid625)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).