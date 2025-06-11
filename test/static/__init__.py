# tests/static/__init__.py
"""
Módulo de Pruebas Estáticas

Este módulo contiene las 4 pruebas estáticas requeridas para el proyecto:

1. test_requirements_review.py - Revisión de completitud de requerimientos
2. test_functional_correctness.py - Análisis de correctitud funcional  
3. test_maintainability.py - Evaluación de mantenibilidad del código
4. test_technical_debt.py - Evaluación de deuda técnica

Uso:
    # Ejecutar todas las pruebas estáticas
    python -m pytest tests/static/ -v
    
    # Ejecutar una prueba específica
    python -m pytest tests/static/test_maintainability.py -v
    
    # Ejecutar en Windows con el script batch
    run_static_tests.bat
"""

__version__ = "1.0.0"
__author__ = "Equipo QA"

# Importar las clases principales para facilitar el uso
from .test_requirements_review import TestRequirementsReview
from .test_functional_correctness import TestFunctionalCorrectness  
from .test_maintainability import TestMaintainability
from .test_technical_debt import TestTechnicalDebt

__all__ = [
    'TestRequirementsReview',
    'TestFunctionalCorrectness', 
    'TestMaintainability',
    'TestTechnicalDebt'
]