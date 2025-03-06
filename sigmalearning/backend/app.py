from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config, mail
from models import db
from auth import auth_bp
from routes import routes_bp
from flask_migrate import Migrate
import os

app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

# Flask-Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Use your SMTP server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")  # Set in .env
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")  # Set in .env

# Initialize database and JWT
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
mail.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(routes_bp, url_prefix="/api")

if __name__ == '__main__':
    with app.app_context():
        # WARNING: drop_all() will delete all tables and data. Use only in development.
        db.drop_all()
        db.create_all()
        # Create the superuser if it doesn't exist
        from models import User
        if not User.query.filter_by(username="SuperAdmin").first():
            superuser = User(username="SuperAdmin", email="superadmin@sigma.com")
            superuser.set_password("SuperSecurePassword")
            superuser.is_admin = True
            db.session.add(superuser)
            db.session.commit()
            print("Superuser created successfully!")
    app.run(debug=True)


