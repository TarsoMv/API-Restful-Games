import os
from dotenv import load_dotenv
from flask import Flask 
from flask_jwt_extended import JWTManager
from views.views import views_bp
from auth.auth import login_bp
from user.user import user_bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(views_bp)
app.register_blueprint(login_bp)
app.register_blueprint(user_bp)

app.config["JWT_SECRET_KEY"] = os.environ["secretkey"]
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)