from models.conexion import supabase

def obtener_todas_evaluaciones_dao():
    """Obtiene el historial completo de triajes para el dashboard"""
    if not supabase:
        return []
    try:
        # Traemos todos los registros ordenados por el más reciente
        response = supabase.table("evaluaciones").select("*").order("id", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error DAO Admin: {e}")
        return []