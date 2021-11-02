import os

from flask_sayhello import app


dev_db = f"mysql+pymysql://root:123456@127.0.0.1:3306/sayhello?charset=utf8mb4"

SECRET_KEY = os.getenv("SECRET_KEY", "bogwang.cn")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", dev_db)