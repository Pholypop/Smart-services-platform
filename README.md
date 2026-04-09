# 🚀 Smart Services Platform

FastAPI backend API with Swagger UI for testing, structured with models, schemas, routers, and services. Open for collaboration.


---

## 📸 API Testing (Swagger UI)

![Swagger UI](assets/swagger1.png)

## ▶️ How to Run and Test the Project

Follow these steps to run the project locally and test the API.

---

## 1️⃣ Create Virtual Environment

Open terminal inside the project folder:

```bash
python -m venv venv
```

Activate it:

### On Windows:

```bash
venv\Scripts\activate
```

### On macOS / Linux:

```bash
source venv/bin/activate
```

---

## 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] python-jose
```

---

## 3️⃣ Configure Database (IMPORTANT)

Go to:

```bash
database.py
```

Update this line:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/dbname"
```

Example:

```python
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/mydatabase"
```

---

## 4️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

## 5️⃣ Open Swagger UI

Open your browser and go to:

👉 http://127.0.0.1:8000/docs

---

## 6️⃣ Test the API

* Choose any endpoint
* Click **Try it out**
* Enter data
* Click **Execute**
* View the response

---

## 📄 Alternative Docs (ReDoc)

👉 http://127.0.0.1:8000/redoc

---

## ⚠️ Notes

* Python 3.8+ required
* Make sure PostgreSQL is running
* Ensure database exists
* If port is busy:

```bash
uvicorn main:app --reload --port 8001
```

---

## ✅ You're Ready!

Now you can test the API using Swagger UI 🎉
