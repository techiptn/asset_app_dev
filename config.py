"""Flask App configuration."""
from os import environ, path
from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask config variables."""

    # General Config
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")
    # STATIC_FOLDER = 'static'
    # TEMPLATES_FOLDER = 'templates'

    # Database
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS Secrets
    # AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    # AWS_KEY_ID = environ.get('AWS_KEY_ID')


'''
from werkzeug.security import generate_password_hash
passw = 'testpassword123'
encrypwkey=generate_password_hash(passw,
                    method='pbkdf2:sha256',
                    salt_length=8)
'''

adminpass = environ.get("ADMIN_PASS")

userpass = environ.get("USER_PASS")

# userID of admin should be 'admin' Don't change admin ID
users_db = { 'admin': adminpass
            ,'user': userpass
}
