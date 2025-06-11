# test/functional/__init__.py
"""
Módulo de Pruebas Funcionales

Este módulo contiene las pruebas funcionales que validan los flujos de negocio
end-to-end del sistema. Las pruebas funcionales se enfocan en verificar que
los componentes trabajen juntos correctamente para cumplir los requerimientos
de negocio.

Diferencias con otros tipos de pruebas:
- Unitarias: Prueban componentes aislados
- Integración: Prueban la comunicación entre componentes  
- Funcionales: Prueban flujos de negocio completos
- Sistema: Prueban el sistema completo
- Aceptación: Prueban criterios de aceptación del usuario

Pruebas incluidas:
- test_functional_trips.py: Flujo completo de gestión de viajes

Uso:
    # Ejecutar todas las pruebas funcionales
    python -m pytest test/functional/ -v
    
    # Ejecutar la prueba específica
    python -m pytest test/functional/test_functional_trips.py -v
"""

__version__ = "1.0.0"
__author__ = "Equipo QA xdxdxdxdxddxd"