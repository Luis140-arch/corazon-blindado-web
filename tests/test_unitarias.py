import pytest
import re

# Ejemplo de funciones a importar desde tu backend (ajusta las rutas si es necesario)
def calcular_phq4(respuestas):
    if len(respuestas) != 4 or any(r not in (0, 1, 2, 3) for r in respuestas):
        raise ValueError("Respuestas PHQ-4 inválidas")
    return sum(respuestas)

def clasificar_phq9(puntaje):
    if puntaje < 0 or puntaje > 27:
        raise ValueError("Puntaje PHQ-9 fuera de rango")
    if puntaje <= 4: return "Mínimo"
    if puntaje <= 9: return "Leve"
    if puntaje <= 14: return "Moderado"
    if puntaje <= 19: return "Moderadamente severo"
    return "Severo"

def test_phq4_extremos():
    assert calcular_phq4([0, 0, 0, 0]) == 0
    assert calcular_phq4([3, 3, 3, 3]) == 12

def test_phq4_invalido():
    with pytest.raises(ValueError):
        calcular_phq4([0, 4, -1, 2])

def test_clasificar_phq9_bordes():
    assert clasificar_phq9(10) == "Moderado"
    assert clasificar_phq9(20) == "Severo"