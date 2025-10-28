from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object without binding to an app.
# Bind later via db.init_app(app) inside your application factory.
db = SQLAlchemy()