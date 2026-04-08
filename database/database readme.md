## 🗄️ Database Configuration (PostgreSQL)

This project uses PostgreSQL as the database.
You need to update the database connection settings manually based on your local setup.

---

### 1️⃣ Install PostgreSQL

Make sure PostgreSQL is installed and running on your machine.

---

### 2️⃣ Create a Database

Create a database (you can choose any name), for example:

```sql
CREATE DATABASE mydatabase;
```

---

### 3️⃣ Update Database Configuration

Go to the file:

```bash
database.py
```

Find the database connection configuration:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/dbname"
```

---

### 4️⃣ Modify the Values

Replace the values with your own PostgreSQL credentials:

* `username` → your PostgreSQL username
* `password` → your PostgreSQL password
* `localhost` → your host (usually localhost)
* `5432` → your port (default is 5432)
* `dbname` → your database name

Example:

```python
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/mydatabase"
```

---

### 5️⃣ Run the Project

After updating the database configuration, run:

```bash
uvicorn main:app --reload
```

---

## ⚠️ Important Notes

* Make sure PostgreSQL service is running
* Ensure the database exists before running the app
* If connection fails, double-check your credentials

---

## ✅ Done!

Your project should now be connected to your local PostgreSQL database 🎉
