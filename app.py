import io
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from database import db, init_db # Importamos la base de datos y su configuracion
from models import Creditos  # Importar el modelo correcto
import os

# Configuracion de la carpeta de las plantillas de HTML
template_dir = os.path.join(os.path.dirname(__file__), 'src', 'templates')

# Inicializamos la app Flask
app = Flask(__name__, template_folder=template_dir)

# Inicializamos la base de datos
init_db(app)

#Rutaa de la aplicacion, es la ruta principal en la cual mostraemos los datos de los clientes
@app.route('/')
def home():
    try:
        # Obtenemos todos los registros que existan en la tabla "Creditos"
        clientes = Creditos.query.all()

        # Convertirmos los registros en una lista de diccionarios
        clientes_dict = [cliente.__dict__ for cliente in clientes]
        
        # Eliminamos metadatos de SQLAlchemy
        for cliente in clientes_dict:
            cliente.pop('_sa_instance_state', None)

        return render_template('index.html', data=clientes_dict)
    
    except Exception as e:
        return f"Error al obtener los clientes: {e}"
    
#Ruta para agregar un nuevo cliente
@app.route('/add', methods=['POST'])
def addCliente():
    try:
        # Crearmos un nuevo objeto Creditos con los datos del formulario
        cliente = Creditos(
            cliente=request.form['nombre'],
            monto=request.form['monto'],
            tasa_interes=request.form['ti'],
            plazo=request.form['plazo'],
            fecha_otorgamiento=request.form['date']
        )
        # Agregamos al nuevo cliente a la base de datos
        db.session.add(cliente)
        db.session.commit()
        # Redirigimos a la página principal
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error al agregar cliente: {e}"

#Ruta para eliminar un cliente
@app.route('/delete/<int:id>')
def deleteCliente(id):
    try:
        # Buscamos al cliente por su ID
        cliente = Creditos.query.get(id)
        if not cliente:
            return "Cliente no encontrado", 404
        
        # Eliminamos al cliente de la base de datos
        db.session.delete(cliente)
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as e:
        return f"Error al eliminar cliente: {e}"
    
#Ruta para editar un cliente
@app.route('/edit/<int:id>', methods=['POST'])
def editCliente(id):
    try:
        # Buscar al cliente por su ID
        cliente = Creditos.query.get(id)
        if not cliente:
            return "Cliente no encontrado", 404

        # Obtenemos los datos del formulario para poder actualizar los datos del cliente
        cliente.cliente = request.form.get('nombre')
        cliente.monto = float(request.form.get('monto'))
        cliente.tasa_interes = float(request.form.get('ti'))
        cliente.plazo = int(request.form.get('plazo'))
        cliente.fecha_otorgamiento = request.form.get('date')

        # Guardamos los cambios en la BD
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"❌ Error al editar cliente: {e}"


#Ruta para probar la conexion a la base de datos
@app.route('/test-db')
def test_db():
    try:
        clientes = Creditos.query.all()
        return f"Conectado a la base de datos. creditos en la tabla: {len(clientes)}"
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"


# Ruta para obtener datos de los creditos
@app.route('/data')
def get_data():
    try:
        # Obtenemos los creditos agrupados por cliente
        data = db.session.query(Creditos.cliente, db.func.sum(Creditos.monto)).group_by(Creditos.cliente).all()
        
        # Convertimos los datos a JSON
        chart_data = {
            "labels": [cliente for cliente, _ in data],
            "values": [monto for _, monto in data]
        }
        
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({"error": str(e)})



# Esta es la parte principal que ejecuta la aplicacion
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creamos las tablas si es que no existen
    app.run(debug=True, port=9000) # Ejecutamos la app en el puerto 9000