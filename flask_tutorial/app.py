import os
from re import S
import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

class BaseConfig(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(BaseConfig)

db = SQLAlchemy(app)


# 定义模型类
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"Note<{self.body}>"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    phone = db.Column(db.String(20), unique=True)
    articles = db.relationship("Article")

    def __repr__(self) -> str:
        return f"Author<{self.name}>"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))

    def __repr__(self) -> str:
        return f"Article<{self.title}>"


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    books = db.relationship("Book", back_populates="writer")

    def __repr__(self) -> str:
        return f"Writer<{self.name}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50), index=True)
    writer_id=db.Column(db.Integer, db.ForeignKey("writer.id"))
    writer = db.relationship("Writer", back_populates="books")

    def __repr__(self) -> str:
        return f"Book<{self.title}>"


# flask shell 自动加载return模块
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note, Author=Author, Article=Article, Writer=Writer, Book=Book)


# 在终端通过命令 flask initdb 执行
@app.cli.command()
def initdb():
    db.create_all()
    click.echo("Initialized database.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7900)
