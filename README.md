# Palindrome Checker App

A full-stack application that lets users submit words and checks if they are palindromes.  
The app provides a REST API and a simple UI for interacting with stored messages.

---

## 🌍 Live Demo

**Frontend**: [https://qlikpalindrom.z16.web.core.windows.net/](https://qlikpalindrom.z16.web.core.windows.net/)  
**API Docs**: [https://qlik-backend.orangesky-3031b73d.northeurope.azurecontainerapps.io/docs](https://qlik-backend.orangesky-3031b73d.northeurope.azurecontainerapps.io/docs)

---

## 🧰 Requirements

- Docker + Docker Compose
- Make (optional, but recommended)
- Python 3.11.6 + Pipenv
- Node.js
- PyEnv (optional, but recommended)

---

## 📁 Repository Structure

```
.
├── backend/         # FastAPI backend service
├── frontend/        # React frontend service
├── local_env/       # Local Docker Compose setup
├── prod_env/        # Production infrastructure (Terraform on Azure)
├── Makefile         # Top-level common tasks
├── README.md        # Project documentation
├── env.make.sample  # Sample environment configuration
```

Each subproject includes its own `Makefile` for convenience.

---

## ▶️ Run the App Locally

The local environment uses Docker Compose to start both backend and frontend.

```bash
cd local_env
make compose-up
```

- Frontend: http://localhost:3000  
- Backend: http://localhost:8000

To stop:

```bash
make compose-down
```

---

## ☁️ Provision Production Environment

Infrastructure is defined using Terraform and provisioned on Azure.

```bash
cd prod_env
make terraform-init    # One-time initialization
make terraform-plan    # Preview infrastructure changes
make terraform-apply   # Apply infrastructure changes
```

Remote Terraform state is stored in Azure Blob Storage.

---

## 🔧 Development Tasks

Common tasks per subproject:

### `backend/`

```bash
make pipenv-install      # Install dependencies
make pipenv-run          # Run the app locally
make pipenv-test         # Run backend tests
make azure-deploy        # Deploy to Azure
```

### `frontend/`

```bash
make npm-start           # Start frontend in dev mode
make npm-build           # Build production bundle
make azure-deploy        # Deploy to Azure Static Web Apps
```

### `local_env/`

```bash
make compose-up          # Start local Docker environment
make compose-down        # Tear down local stack
```

### `prod_env/`

```bash
make terraform-init      # Initialize Terraform
make terraform-plan      # Show planned changes
make terraform-apply     # Apply infrastructure changes
```

Run `make` in any directory to see available commands.

---

## 🔄 System Overview

This sequence diagram outlines how the system components interact:

```mermaid
sequenceDiagram
  participant User
  participant Frontend
  participant Backend
  participant Store

  User->>Frontend: Submit message
  Frontend->>Backend: POST /messages
  Backend->>Store: Save message
  Store-->>Backend: Message ID
  Backend-->>Frontend: 201 Created

  User->>Frontend: View all messages
  Frontend->>Backend: GET /messages
  Backend->>Store: Retrieve messages
  Backend-->>Frontend: List of messages

  User->>Frontend: View message details
  Frontend->>Backend: GET /messages/{id}
  Backend->>Store: Fetch message
  Backend->>Backend: Check palindrome
  Backend-->>Frontend: Message + result

  User->>Frontend: Delete message
  Frontend->>Backend: DELETE /messages/{id}
  Backend->>Store: Delete message
  Backend-->>Frontend: 204 No Content
```

---

## 📚 REST API Reference

Available once backend is running:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

> Live docs is available at: [https://qlik-backend.orangesky-3031b73d.northeurope.azurecontainerapps.io/docs](https://qlik-backend.orangesky-3031b73d.northeurope.azurecontainerapps.io/docs)

### Endpoints

| Method | Path               | Description                         |
|--------|--------------------|-------------------------------------|
| POST   | `/messages`        | Submit a new message                |
| GET    | `/messages`        | List all submitted messages         |
| GET    | `/messages/{id}`   | Retrieve message + palindrome check |
| DELETE | `/messages/{id}`   | Delete a specific message           |

---

## ⚖️ License

This project is released under the MIT License.  
See the `LICENSE` file for full details.

---

## 👤 Author

Created by [David Runemalm](https://www.davidrunemalm.com)  
As part of a technical assignment for Qlik.
