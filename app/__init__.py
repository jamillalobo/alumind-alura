from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from app.extensions import db
from dotenv import load_dotenv
import os
from app.extensions import db

migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.email_route import email_bp
    from app.routes.feedback_route import feedbacks_bp
    from app.routes.report_route import report_bp
    from app.routes.main_route import main_bp

    app.register_blueprint(feedbacks_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(main_bp)

    return app
