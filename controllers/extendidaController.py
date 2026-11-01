from models.evaluacionDAO import guardar_evaluacion_extendida_dao

def procesar_evaluacion_extendida(datos_form):
    """Suma los puntajes del PHQ-9 y GAD-7 y guarda los detalles"""
    token = datos_form.get('token')
    
    # Puntaje PHQ-9 (Depresión: 9 preguntas de 0 a 3)
    puntaje_phq9 = sum(int(datos_form.get(f'phq9_{i}', 0)) for i in range(1, 10))
    
    # Puntaje GAD-7 (Ansiedad: 7 preguntas de 0 a 3)
    puntaje_gad7 = sum(int(datos_form.get(f'gad7_{i}', 0)) for i in range(1, 8))
    
    # Interpretación Depresión (PHQ-9)
    if puntaje_phq9 <= 4:
        diag_depresion = "Mínima"
    elif puntaje_phq9 <= 9:
        diag_depresion = "Leve"
    elif puntaje_phq9 <= 14:
        diag_depresion = "Moderada"
    elif puntaje_phq9 <= 19:
        diag_depresion = "Moderadamente Severa"
    else:
        diag_depresion = "Severa"
        
    # Interpretación Ansiedad (GAD-7)
    if puntaje_gad7 <= 4:
        diag_ansiedad = "Mínima"
    elif puntaje_gad7 <= 9:
        diag_ansiedad = "Leve"
    elif puntaje_gad7 <= 14:
        diag_ansiedad = "Moderada"
    else:
        diag_ansiedad = "Severa"

    registro_extendido = {
        "token": token,
        "puntaje_phq9": puntaje_phq9,
        "diag_depresion": diag_depresion,
        "puntaje_gad7": puntaje_gad7,
        "diag_ansiedad": diag_ansiedad
    }

    # Guardar en base de datos mediante la capa Modelo
    guardar_evaluacion_extendida_dao(registro_extendido)

    return {
        "token": token,
        "puntaje_phq9": puntaje_phq9,
        "diag_depresion": diag_depresion,
        "puntaje_gad7": puntaje_gad7,
        "diag_ansiedad": diag_ansiedad
    }