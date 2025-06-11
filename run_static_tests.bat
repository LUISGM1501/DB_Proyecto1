@echo off
REM run_static_tests.bat
REM Script para ejecutar todas las pruebas estáticas en Windows

echo ========================================
echo 🔍 EJECUTANDO PRUEBAS ESTÁTICAS
echo ========================================

echo.
echo Creando directorio test/static si no existe...
if not exist "test\static" mkdir "test\static"

echo.
echo 📋 PRUEBA 1: Revisión de Requerimientos
echo ----------------------------------------
python -m pytest test/static/test_requirements_review.py -v

echo.
echo 🔍 PRUEBA 2: Análisis de Correctitud Funcional  
echo ----------------------------------------
python -m pytest test/static/test_functional_correctness.py -v

echo.
echo 🔧 PRUEBA 3: Evaluación de Mantenibilidad
echo ----------------------------------------
python -m pytest test/static/test_maintainability.py -v

echo.
echo 💳 PRUEBA 4: Evaluación de Deuda Técnica
echo ----------------------------------------
python -m pytest test/static/test_technical_debt.py -v

echo.
echo ========================================
echo ✅ PRUEBAS ESTÁTICAS COMPLETADAS
echo ========================================
echo.
echo Para ejecutar todas las pruebas del proyecto:
echo pytest test/ --cov=. --cov-report=html -v
echo.
pause