from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey

DATABASE_URL = "postgresql://postgres:Deblina@localhost/mydb"

engine = create_engine(DATABASE_URL) #stores connection to postgres

SessionLocal = sessionmaker(bind = engine) 

class Base(DeclarativeBase):
    pass

class Registration(Base):
    __tablename__ = "Registration"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(40), nullable = False)
    username: Mapped[str] = mapped_column(String(30), unique = True, nullable = False)
    password: Mapped[str] = mapped_column(String(225), nullable = False)

class Login_logs(Base):
    __tablename__ = "Login_logs"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Registration.id"), nullable = False)
    login_time: Mapped[datetime] = mapped_column(DateTime, default = lambda: datetime.now(timezone.utc))

Base.metadata.create_all(engine)
