from models.conexion import supabase

def guardar_evaluacion_dao(data_evaluacion):
    """Guarda un registro de triaje anónimo en Supabase (INSERT)"""
    if not supabase:
        print("⚠️ Supabase no inicializado.")
        return None
    try:
        response = supabase.table("evaluaciones").insert(data_evaluacion).execute()
        print("✅ Guardado exitoso mediante DAO:", response.data)
        return response.data
    except Exception as e:
        print(f"❌ Error DAO Guardar: {e}")
        return None

def buscar_evaluacion_por_token_dao(token):
    """Busca un registro por su token único en Supabase (SELECT)"""
    if not supabase:
        return None
    try:
        response = supabase.table("evaluaciones").select("*").eq("token", token).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Error DAO Buscar Token: {e}")
        return None
def guardar_evaluacion_extendida_dao(data_extendida):
    """Guarda o actualiza el detalle del PHQ-9 y GAD-7 en Supabase"""
    if not supabase:
        print("⚠️ Supabase no inicializado.")
        return None
    try:
        # Insertamos el registro de la evaluación extendida vinculada al token
        response = supabase.table("evaluaciones_extendidas").insert(data_extendida).execute()
        print("✅ Evaluación extendida guardada:", response.data)
        return response.data
    except Exception as e:
        print(f"❌ Error DAO Guardar Extendida: {e}")
        return None