from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#  رابط الاتصال بقاعدة البيانات (عدّل القيم حسب جهازك)
DATABASE_URL = "postgresql://username:password@localhost:5432/dbname"

#  إنشاء الاتصال    create create connection
engine = create_engine(DATABASE_URL)

#  إنشاء الجلسة /التعامل مع قاعدة البيانات -session (connect to DB)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#  Base class لكل models *************
Base = declarative_base()