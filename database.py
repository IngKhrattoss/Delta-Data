from flask_sqlalchemy import SQLAlchemy
import os

# Definimos la base de datos
db = SQLAlchemy()

def init_db(app):
     # Obtenemos la ruta base del proyecto
    base_dir = os.path.abspath(os.path.dirname(__file__))  
    db_path = os.path.join(base_dir, "ExamenCreditos.db")  # Creamos la BD en el proyecto
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    print(f"La ruta de la base de datos es: {app.config['SQLALCHEMY_DATABASE_URI']}")  # Este print nos ayuda a verificar la ruta de nuestra BD
