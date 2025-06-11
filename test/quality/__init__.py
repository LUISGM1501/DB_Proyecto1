# test/quality/__init__.py
"""
Módulo de Evaluación de Calidad ISO/IEC 25010

Este módulo implementa la evaluación de atributos de calidad según
la norma internacional ISO/IEC 25010:2011 "Systems and software 
Quality Requirements and Evaluation (SQuaRE)".

Atributos de Calidad Evaluados:
1. USABILIDAD (Usability)
   - Aprendizaje (Learnability): Tiempo de respuesta de APIs
   - Reconocimiento (Recognizability): Consistencia de respuestas
   
2. CONFIABILIDAD (Reliability)  
   - Tolerancia a fallos: Tasa de éxito bajo carga
   - Recuperabilidad: Manejo apropiado de errores
   
3. EFICIENCIA DE DESEMPEÑO (Performance Efficiency)
   - Comportamiento temporal: Tiempo de respuesta bajo carga
   - Utilización de recursos: Uso eficiente de memoria

Métricas y Criterios:
- Cada métrica tiene criterios definidos para:
  * ACEPTACIÓN TOTAL (85-100 puntos)
  * ACEPTACIÓN PARCIAL (70-84 puntos) 
  * RECHAZO (<70 puntos)

Uso:
    # Ejecutar evaluación completa
    python -m pytest test/quality/ -v -s
    
    # Ejecutar atributo específico
    python -m pytest test/quality/test_iso25010_attributes.py::TestISO25010QualityAttributes::test_usability_learnability_metric -v -s
"""

__version__ = "1.0.0"
__author__ = "Equipo QA xdxdxdxdxdxd"

# Constantes para criterios de calidad
QUALITY_THRESHOLDS = {
    'EXCELLENT': 85,
    'GOOD': 70, 
    'ACCEPTABLE': 50,
    'POOR': 0
}

QUALITY_ATTRIBUTES = [
    'Usabilidad',
    'Confiabilidad', 
    'Eficiencia de Desempeño'
]