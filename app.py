import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

from controllers.extendidaController import procesar_evaluacion_extendida
from controllers.triajeController import procesar_evaluacion_triaje
from controllers.consultaController import obtener_evaluacion_por_token
from controllers.adminController import obtener_metricas_dashboard

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret_key_default")

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/evaluar', methods=['POST'])
def evaluar():
    resultado = procesar_evaluacion_triaje(request.form)
    return render_template('resultado.html', 
                           token=resultado['token'], 
                           nivel_riesgo=resultado['nivel_riesgo'], 
                           puntaje=resultado['puntaje'], 
                           analisis_ia=resultado['analisis_ia'])

@app.route('/consultar', methods=['POST'])
def consultar():
    token_ingresado = request.form.get('token', '')
    evaluacion = obtener_evaluacion_por_token(token_ingresado)
    
    if not evaluacion:
        return render_template('index.html', error_token="No se encontró ninguna evaluación con ese token.")
        
    return render_template('resultado.html',
                           token=evaluacion.get('token'),
                           nivel_riesgo=evaluacion.get('nivel_riesgo'),
                           puntaje=evaluacion.get('puntaje_phq4'),
                           analisis_ia=evaluacion.get('pautas_ia'))

@app.route('/extendida/<token>')
def vista_extendida(token):
    return render_template('extendida.html', token=token)

@app.route('/evaluar-extendida', methods=['POST'])
def evaluar_extendida():
    resultado = procesar_evaluacion_extendida(request.form)
    return render_template('resultado.html', 
                           token=resultado['token'], 
                           nivel_riesgo="Evaluación Profundizada Completada",
                           puntaje=f"Nivel de Depresión: {resultado['diag_depresion']} | Nivel de Ansiedad: {resultado['diag_ansiedad']}",
                           analisis_ia="Has completado los cuestionarios de profundización. Por favor, acude con tu token de forma presencial o virtual al área de Psicología y Bienestar de la UCV para recibir la orientación correspondiente.",
                           es_extendida=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        # Credenciales del psicólogo
        if usuario == 'psicologia' and password == 'ucv2026':
            session['psicologo_logueado'] = True
            return redirect(url_for('panel_admin'))
        else:
            error = "Credenciales incorrectas."
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('psicologo_logueado', None)
    return redirect(url_for('inicio'))

@app.route('/admin')
def panel_admin():
    # Bloquea el acceso si no hay sesión activa
    if not session.get('psicologo_logueado'):
        return redirect(url_for('login'))
        
    metricas = obtener_metricas_dashboard()
    return render_template('admin.html', metricas=metricas)

# SIEMPRE DEBE IR AL FINAL DEL ARCHIVO
if __name__ == '__main__':
    app.run(debug=True, port=5000)