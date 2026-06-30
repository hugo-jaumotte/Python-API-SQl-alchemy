# Focus App

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest)
![License](https://img.shields.io/badge/License-MIT-green)

Focus App is a full-stack productivity application based on the Pomodoro technique, built with FastAPI, React, and PostgreSQL.

The project was designed to deepen my understanding of modern backend development, secure authentication systems, database design, automated testing, and cloud deployment. It focuses on implementing features commonly found in production-grade web applications.

Link to Focus App website: https://focus-api-seven.vercel.app/

---

## Highlights

- Secure authentication using JWT stored in HTTP-only cookies
- Email verification during account creation
- Password recovery via email
- Customizable Pomodoro sessions (work and break durations)
- Persistent session history stored in PostgreSQL
- REST API built with FastAPI and SQLAlchemy ORM
- Integration tests using Pytest
- Cloud deployment using Vercel, Render, Neon, and Resend

---

## Features

### Authentication

- User registration
- Email verification
- Login and logout system
- JWT authentication (HS256)
- HTTP-only cookies for token storage
- Password reset via email
- Password hashing using bcrypt
- Protected API routes

### Productivity

- Configurable Pomodoro sessions
- Tracking of work and break intervals
- Session history per user
- Persistent storage in database

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- PyJWT
- bcrypt
- Pytest

### Frontend

- React
- TypeScript
- Vite

### Deployment

| Service   | Platform |
|----------|----------|
| Frontend | Vercel   |
| Backend  | Render   |
| Database | Neon     |
| Emails   | Resend   |

---

## Security

This project implements authentication and security mechanisms inspired by production applications.

- JWT authentication using HS256
- HTTP-only cookies for token storage
- Password hashing with bcrypt
- Email verification before account activation
- Secure password reset workflow
- Protected backend endpoints
- Use of environment variables for sensitive configuration

---

## Running Locally

### Clone the repository

```bash
git clone https://github.com/hugo-jaumotte/Python-API-SQl-alchemy
```

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

./run
```

### Frontend

```bash
cd frontend

npm install

npm run start
```

---

## Testing

Integration tests are implemented using Pytest.

Run tests with:

```bash
cd backend

./run_tests
```

---

## What I Learned

This project helped me gain practical experience in:

- Designing RESTful APIs
- Building authentication systems from scratch
- Working with SQLAlchemy and relational databases
- PostgreSQL database management
- Secure password handling practices
- JWT and cookie-based authentication
- Email-based workflows
- Automated testing with Pytest
- Full-stack application architecture
- Cloud deployment and environment management

---

## Roadmap

Planned improvements:

- Unit testing coverage
- Goal and task management system
- Linking tasks and goals with Pomodoro sessions
- Productivity analytics dashboard
- User account deletion (data removal compliance)
- Pagination for session history
- Security and performance improvements

---

## License

This project is licensed under the MIT License.

---

## Repository

This repository serves as the public-facing portfolio version of the project.
Ongoing development and experimental work are maintained in a private repository.
