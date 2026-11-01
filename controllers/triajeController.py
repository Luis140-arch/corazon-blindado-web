import os
import random
import string
import google.generativeai as genai
from models.evaluacionDAO import guardar_evaluacion_dao

def generar_token(longitud=8):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def analizar_con_gemini(texto_libre):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Te recomendamos realizar pausas activas durante tu jornada de estudio y acudir a orientación psicológica si percibes un alto nivel de estrés."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        Eres un orientador preventivo de salud mental para estudiantes universitarios.
        Analiza la siguiente situación expresada por un estudiante:
        "{texto_libre}"
        
        INSTRUCCIONES:
        1. Escribe de 2 a 3 pautas de autocuidado preventivo, breves y empáticas.
        2. Mantén un tono amigable, tranquilizador y constructivo.
        3. NO emitas diagnósticos clínicos ni menciones medicamentos.
        4. Responde directamente en texto plano con viñetas o párrafos breves.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error con Gemini API: {e}")
        return "Mantén hábitos saludables, organiza tus tiempos de estudio y contacta a Bienestar UCV si necesitas hablar con un profesional."

def procesar_evaluacion_triaje(datos_form):
    """Calcula el riesgo, analiza con IA y coordina el guardado con la Capa Modelo"""
    edad = datos_form.get('edad')
    sexo = datos_form.get('sexo')
    texto_libre = datos_form.get('pregunta_libre', '')
    tiempo_llenado = int(datos_form.get('tiempo_segundos', 0))
    
    p1 = int(datos_form.get('p1', 0))
    p2 = int(datos_form.get('p2', 0))
    p3 = int(datos_form.get('p3', 0))
    p4 = int(datos_form.get('p4', 0))
    puntaje = p1 + p2 + p3 + p4
    
    if puntaje <= 4:
        nivel_riesgo = "Leve"
    elif puntaje <= 8:
        nivel_riesgo = "Moderado"
    else:
        nivel_riesgo = "Alto"
        
    pautas_ia = analizar_con_gemini(texto_libre)
    token = generar_token()
    
    registro = {
        "token": token,
        "rango_edad": edad,
        "sexo": sexo,
        "tiempo_llenado": tiempo_llenado,
        "puntaje_phq4": puntaje,
        "nivel_riesgo": nivel_riesgo,
        "texto_libre": texto_libre,
        "pautas_ia": pautas_ia
    }
    
    # Delegar persistencia al DAO (Capa Modelo)
    guardar_evaluacion_dao(registro)
    
    return {
        "token": token,
        "nivel_riesgo": nivel_riesgo,
        "puntaje": puntaje,
        "analisis_ia": pautas_ia
    }