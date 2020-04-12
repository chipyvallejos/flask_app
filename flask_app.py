# Importo las Bibliotecas necesarias.
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

# Conexion MySQLServer que hice en Docker.
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 6603
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql=MySQL(app)

# Conexion MySQLServer que hice PythonAnyWhere.
# app.config['MYSQL_HOST']='chipyyy.mysql.pythonanywhere-services.com'
# app.config['MYSQL_PORT'] = 3306
# app.config['MYSQL_USER']='chipyyy'
# app.config['MYSQL_PASSWORD']='123456789a'
# app.config['MYSQL_DB'] = 'chipyyy$flaskcontacts'
# mysql=MySQL(app)

# Configuraciones.
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/agregar_contacto', methods = ['POST'])
def agregar_contacto():
   if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
        (fullname, phone, email))
        mysql.connection.commit()
        flash('¡Contacto agregado correctamente!')
        return redirect(url_for('Index'))

@app.route('/editar/<id>')
def obtener_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))  
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/actualizar/<id>', methods = ['POST'])
def actualizar_contacto(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s, 
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('¡Contacto actualizado correctamente!')
        return redirect(url_for('Index'))

@app.route('/eliminar/<string:id>')
def eliminar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('¡Contacto eliminado correctamente!')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run()
    #app.run(debug=True)
