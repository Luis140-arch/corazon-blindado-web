from models.evaluacionDAO import buscar_evaluacion_por_token_dao

def obtener_evaluacion_por_token(token_ingresado):
    """Lógica para consultar la evaluación desde la Capa Modelo"""
    if not token_ingresado:
        return None
    return buscar_evaluacion_por_token_dao(token_ingresado.strip().upper())