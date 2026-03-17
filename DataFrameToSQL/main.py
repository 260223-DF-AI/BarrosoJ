import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, dotenv_values

load_dotenv("./env")
CONNECTION_STR: dict = dotenv_values()["CONNECTION"]

engine = create_engine(CONNECTION_STR)

df = pd.read_sql("SELECT * FROM artists", engine)
print(df)
df = pd.concat([df.iloc[[0]], df.iloc[[0]]])

df.to_sql(
    name="processed",
    con=engine,
    index=False,
    if_exists="replace"
)

print("Wrote to DB")


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass

class Multiple(Base):
    __tablename__ = "multiple"
    id: Mapped[int] = mapped_column(primary_key=True)
    artists: Mapped[list["Artist"]] = relationship()

class Artist(Base):
    __tablename__ = 'alt_artists'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hire_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    multiple: Mapped["Multiple"] = relationship(back_populates="artists")


halsey = Artist(first_name="Ash", last_name="Frig", email="h@a.l")

Base.metadata.create_all(engine)