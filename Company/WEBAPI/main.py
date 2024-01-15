from flask import Flask, request, render_template
import random
from flask import jsonify
from tool.jsonal import jsonal
from tool.sqltl import sqltl
import json

app = Flask(__name__)

defaultConfig = jsonal('./config/default.json').loadFile()
sqltltx = sqltl()

@app.route("/user/login", methods=["POST"])
def user_login():
    data = request.get_json()
    userName = data.get("userName")
    password = data.get("password")

    if userName == "admin" and password == "123456":
        return jsonify({
            "code": 0,
            "data": {
                "token": "666666"
            }
        })
    else:
        return jsonify({
            "code": 99999999,
            "msg": "用户名或密码错误"
        })

if __name__ == '__main__':
    app.run(host=defaultConfig['host'], port=defaultConfig['post'])