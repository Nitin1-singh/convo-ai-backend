# FastAPI Project Setup Guide

## 📌 Prerequisites

Make sure you have the following installed:

- **Python 3.11+**
- **Git**
- **pip**
- **virtualenv** (optional but recommended)
- **Docker** (optional)

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/your-repo/your-project.git
cd your-project
```

### 2️⃣ Create a Virtual Environment

#### On **Linux/macOS**:

```sh
python3 -m venv venv
source venv/bin/activate
```

#### On **Windows**:

```sh
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Database

Create a `.env` file in the root directory and add your **DATABASE_URL**:

```
DATABASE_URL=postgresql+asyncpg://your_user:your_password@your_host:your_port/your_db
```

### 5️⃣ Run the Application

Start the FastAPI server using **Uvicorn**:

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**

### 6️⃣ Run with Docker (Optional)

#### Build the Docker Image:

```sh
docker build -t fastapi-app .
```

#### Run the Container:

```sh
docker run -p 8000:8000 fastapi-app
```

```sh
docker run -e DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname" -p 8000:8000 my-fastapi-app
```

## 📌 Troubleshooting

- If **dependencies fail**, ensure you're using the correct Python version (`python --version`).
- If **database issues occur**, verify your `.env` file and database connection.
- For **port conflicts**, use `--port 8080` (or any other free port) when running Uvicorn.

🚀 **You're all set! Happy coding!** 🎯
