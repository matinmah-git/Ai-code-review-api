# 🤖 AI Code Review API

An AI-powered code review platform built with **FastAPI** that analyzes source code using Large Language Models (LLMs). The API supports reviewing individual code snippets, uploaded source files, ZIP archives, and public GitHub repositories while providing detailed feedback on code quality, security, performance, maintainability, and best practices.

---

## ✨ Features

* 🔐 JWT Authentication
* 👤 User Registration & Login
* 🤖 AI-Powered Code Review
* 📄 Review Code Snippets
* 📁 Review Uploaded Source Files
* 📦 Review ZIP Archives
* 🌐 Review Public GitHub Repositories
* 📊 Review History
* 💾 Persistent Database Storage
* ⚙️ Service Layer Architecture
* 🛡 Secure Password Hashing
* 🔑 Environment-Based Configuration
* 📝 Structured AI Prompts
* 🚀 RESTful API Design

---

## 🛠 Tech Stack

### Backend

* FastAPI
* Python 3.12+
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* SQLite (Development)
* PostgreSQL (Production Ready)

### Authentication

* JWT
* Passlib (bcrypt)

### AI

* OpenAI SDK
* Compatible with OpenRouter
* Compatible with Local LLMs (Ollama, LM Studio, vLLM)

### Git Integration

* GitPython

---

## 📂 Project Structure

```text
Ai-code-review-api/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── reviews.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── prompts.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── job.py
│   │   ├── review.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── analysis.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── github_service.py
│   │   ├── file_service.py
│   │   ├── review_service.py
│   │   └── auth_service.py
│   │
│   └── main.py
│
├── run.py
├── .env.example
├── requirements.txt
└── README.md

```

---

## 🚀 Supported Review Methods

### 1. Code Snippet

Paste raw source code directly into the API.

```http
POST /reviews/snippet
```

---

### 2. Source File

Upload a single source code file.

```http
POST /reviews/upload
```

---

### 3. ZIP Archive

Upload an entire project as a ZIP archive.

```http
POST /reviews/archive
```

---

### 4. GitHub Repository

Analyze a public GitHub repository.

```http
POST /reviews/github
```

---

## 🤖 AI Review Includes

The AI evaluates code based on:

* Code Quality
* Readability
* Maintainability
* Security Issues
* Performance
* Best Practices
* Potential Bugs
* Suggestions for Improvement
* Refactored Examples (when applicable)

---

## 🔒 Authentication

The API uses JWT Bearer Authentication.

Example:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ai-code-review-api.git

cd ai-code-review-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./app.db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

OPENAI_API_KEY=your_api_key

OPENAI_BASE_URL=https://api.openai.com/v1

OPENAI_MODEL=gpt-5.5
```

Run the server:

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```


---

## 📖 API Documentation

After starting the server:

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

## 🧪 Future Improvements

* Background Review Jobs
* Email Verification
* Password Reset
* Review Sharing
* Team Workspaces
* Webhook Support
* Docker Deployment
* Redis + Celery
* Unit & Integration Tests

---

## 👨‍💻 Author

**Matin Mahpour**

GitHub: https://github.com/matinmah-git
