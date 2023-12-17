from flask import Flask, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager
from app.models.adminModel import AdminUser

mysql = MySQL()
bootstrap = Bootstrap()
mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser(0, "admin@g.msuiit.edu.ph", "Admin")

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_PORT=MAIL_PORT,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
    )
    bootstrap.init_app(app)
    mysql.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)

    from .controller.admin import admin
    from .controller.subjectsHandled import subjectsHandled
    from .controller.faculty import faculty
    from .controller.subjects import subject
    from .controller.classRecord import classRecord

    app.register_blueprint(admin)
    app.register_blueprint(subjectsHandled)
    app.register_blueprint(faculty)
    app.register_blueprint(subject)
    app.register_blueprint(classRecord)
    

    return app
