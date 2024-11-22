from flask import Flask
from flask_cors import CORS
from app.api.word_api import word_api
from app.api.character_api import character_api

app = Flask(__name__)
CORS(app)

# 注册路由
app.register_blueprint(word_api)
app.register_blueprint(character_api)

if __name__ == "__main__":
    app.run(debug=True)

