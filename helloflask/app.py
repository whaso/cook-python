import os
import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(BaseConfig)

db = SQLAlchemy(app)


# 定义模型类, 外键定义在多的一侧
# ========= 一对多 ==========
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


class Singer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    songs = db.relationship("Song", backref="singer")

    def __repr__(self) -> str:
        return f"Singer<{self.name}>"


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    singer_id = db.Column(db.Integer, db.ForeignKey("singer.id"))
    create_time = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"Song<{self.name}>"
    

# ========= 多对一 =========
class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    city = db.relationship("City")


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)


class OrderTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime)
    

# flask shell 自动加载return模块
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, **get_models_dict())


# 在终端通过命令 flask initdb 执行
@app.cli.command()
def initdb():
    db.create_all()
    click.echo("Initialized database.")


class torm(db.Model):
    # __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


def get_models_dict():
    import sys
    import inspect
    # 用 hasattr query 判断是模型类, 暂时没想到别的办法
    clsmembers = inspect.getmembers(sys.modules[__name__], lambda a: hasattr(a, "query"))

    # 转换成字典k:v
    models = {k: v for k, v in clsmembers}
    return models

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7900)
