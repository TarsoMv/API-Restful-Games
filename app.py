from flask import Flask 
from flask_jwt_extended import JWTManager
from views.views import views_bp
from auth.auth import login_bp

app = Flask(__name__)
app.register_blueprint(views_bp)
app.register_blueprint(login_bp)

app.config["JWT_SECRET_KEY"] = "chave_secreta"
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)