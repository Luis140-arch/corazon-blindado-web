from models.adminDAO import obtener_todas_evaluaciones_dao

def obtener_metricas_dashboard():
    """Procesa los datos crudos para generar estadísticas del panel"""
    evaluaciones = obtener_todas_evaluaciones_dao()
    total_evaluaciones = len(evaluaciones)
    
    # Contadores por nivel de riesgo
    riesgo_alto = sum(1 for e in evaluaciones if e.get('nivel_riesgo') == 'Alto')
    riesgo_moderado = sum(1 for e in evaluaciones if e.get('nivel_riesgo') == 'Moderado')
    riesgo_leve = sum(1 for e in evaluaciones if e.get('nivel_riesgo') == 'Leve')
    
    return {
        "total": total_evaluaciones,
        "altos": riesgo_alto,
        "moderados": riesgo_moderado,
        "leves": riesgo_leve,
        "lista_recientes": evaluaciones[:20] # Mostramos los 20 más recientes en la tabla
    }