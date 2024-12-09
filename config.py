import os

class Config:
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI = 'mysql://root:senha@localhost/quickmed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
