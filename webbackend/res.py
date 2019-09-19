# /distを静的フォルダとして定義する
from flask import Blueprint
app = Blueprint("resource", __name__, static_url_path='/resource', static_folder='./resource')
