# Smart-services-platform
FastAPI backend API with Swagger UI for testing, structured with models, schemas, routers, and services. Open for collaboration.
▶️ How to Run and Test the Project

Follow these steps to run the project locally and test the API using Swagger UI.


1️⃣ Create Virtual Environment (Recommended) & install libraries
 Open the Powershell inside the project folder and then type the following commands:
 👉 python -m venv venv

 📌 Then install the following libraries:
   -> pip install uvicorn
   ->  pip install sqlalchemy fastapi uvicorn
   -> pip install psycopg2-binary
   ->  pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose
 📌 Activate it:

         .On Windows:
         -> venv\Scripts\activate

2️⃣ Run the Server 
  -> uvicorn main:app

3️⃣ Open Swagger UI

 After running the server, open your browser and go to:

 http://127.0.0.1:8000/docs

4️⃣Test the API
  .Choose any endpoint
  .Click "Try it out"
  .Enter the required data
  .Click "Execute"
  .View the response

5️⃣🧪 Alternative Docs (ReDoc)

    You can also check:

    http://127.0.0.1:8000/redoc

⚠️ Notes
  Make sure Python is installed (3.8+)
  Ensure all dependencies are installed correctly
  If the port is busy, change it using:
  uvicorn main:app --reload --port 8001


🚀 You're Ready!

 Now you can explore and test all API endpoints بسهولة باستخدام Swagger UI 🎉

    
