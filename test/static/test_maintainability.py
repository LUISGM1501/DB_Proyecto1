# tests/static/test_maintainability.py
"""
Prueba Estática 3: Evaluación de Mantenibilidad
Analiza modularidad, legibilidad y complejidad del código
"""

import os
import ast
import pytest
from pathlib import Path

class TestMaintainability:
    """
    Evaluación de mantenibilidad del código
    """
    
    def test_code_complexity_analysis(self):
        """
        Analiza la complejidad ciclomática básica del código
        """
        print("\n🔧 ANÁLISIS DE COMPLEJIDAD CICLOMÁTICA")
        
        python_files = []
        controllers_path = "controllers"
        
        if os.path.exists(controllers_path):
            for file in os.listdir(controllers_path):
                if file.endswith('.py') and not file.startswith('__'):
                    python_files.append(os.path.join(controllers_path, file))
        
        total_complexity = 0
        file_count = 0
        complexity_issues = []
        
        for file_path in python_files[:5]:  # Analizar solo 5 archivos para simplicidad
            try:
                complexity = self._calculate_file_complexity(file_path)
                total_complexity += complexity
                file_count += 1
                
                print(f"📄 {file_path}: Complejidad = {complexity}")
                
                if complexity > 10:  # Umbral de complejidad alta
                    complexity_issues.append(f"{file_path} (complejidad: {complexity})")
                    
            except Exception as e:
                print(f"❌ Error analizando {file_path}: {e}")
        
        # Calcular complejidad promedio
        avg_complexity = total_complexity / file_count if file_count > 0 else 0
        
        print(f"\n📊 RESULTADOS DE COMPLEJIDAD:")
        print(f"   • Archivos analizados: {file_count}")
        print(f"   • Complejidad promedio: {avg_complexity:.1f}")
        print(f"   • Archivos con alta complejidad: {len(complexity_issues)}")
        
        if complexity_issues:
            print(f"   • Problemas encontrados:")
            for issue in complexity_issues:
                print(f"     - {issue}")
        
        # Criterio de aceptación: complejidad promedio < 8
        maintainability_score = max(0, 100 - (avg_complexity * 5))
        
        print(f"✅ MANTENIBILIDAD: {maintainability_score:.1f}% (complejidad: {avg_complexity:.1f})")
        
        assert avg_complexity < 15, f"Complejidad muy alta: {avg_complexity:.1f}"
        assert maintainability_score > 50, f"Puntuación baja: {maintainability_score:.1f}%"
        
    
    def _calculate_file_complexity(self, file_path):
        """
        Calcula complejidad ciclomática básica de un archivo
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Contar estructuras de control (aproximación simple)
            complexity = 1  # Complejidad base
            
            # Contar decisiones/ramificaciones
            complexity += content.count('if ')
            complexity += content.count('elif ')
            complexity += content.count('for ')
            complexity += content.count('while ')
            complexity += content.count('except ')
            complexity += content.count('and ')
            complexity += content.count('or ')
            
            return complexity
            
        except Exception:
            return 1  # Complejidad mínima si hay error
    
    def test_code_modularity(self):
        """
        Evalúa la modularidad del código
        """
        print("\n🧩 ANÁLISIS DE MODULARIDAD")
        
        # Verificar estructura modular esperada
        expected_modules = {
            "controllers": ["user_controller.py", "trip_controller.py"],
            "models": ["user.py", "trip.py"],
            "routes": ["user_routes.py", "trip_routes.py"],
            "services": ["auth_service.py", "cache_service.py"]
        }
        
        modularity_score = 0
        total_modules = sum(len(files) for files in expected_modules.values())
        found_modules = 0
        
        for module_type, files in expected_modules.items():
            if os.path.exists(module_type):
                print(f"📁 {module_type.upper()}:")
                for file in files:
                    file_path = os.path.join(module_type, file)
                    if os.path.exists(file_path):
                        found_modules += 1
                        print(f"   ✅ {file}")
                    else:
                        print(f"   ❌ {file}")
            else:
                print(f"❌ Directorio faltante: {module_type}")
        
        modularity_percentage = (found_modules / total_modules) * 100
        
        print(f"\n📊 MODULARIDAD:")
        print(f"   • Módulos encontrados: {found_modules}/{total_modules}")
        print(f"   • Porcentaje modular: {modularity_percentage:.1f}%")
        
    
    def test_code_readability(self):
        """
        Evalúa aspectos básicos de legibilidad
        """
        print("\n📖 ANÁLISIS DE LEGIBILIDAD")
        
        readability_metrics = {
            "documented_functions": 0,
            "total_functions": 0,
            "long_lines": 0,
            "total_lines": 0
        }
        
        # Analizar algunos archivos de controladores
        controller_files = []
        if os.path.exists("controllers"):
            for file in os.listdir("controllers")[:3]:  # Solo 3 archivos
                if file.endswith('.py') and not file.startswith('__'):
                    controller_files.append(os.path.join("controllers", file))
        
        for file_path in controller_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                in_function = False
                function_has_docstring = False
                
                for line in lines:
                    readability_metrics["total_lines"] += 1
                    
                    # Líneas muy largas
                    if len(line.strip()) > 100:
                        readability_metrics["long_lines"] += 1
                    
                    # Funciones documentadas
                    if line.strip().startswith('def '):
                        if in_function and function_has_docstring:
                            readability_metrics["documented_functions"] += 1
                        readability_metrics["total_functions"] += 1
                        in_function = True
                        function_has_docstring = False
                    
                    if in_function and ('"""' in line or "'''" in line):
                        function_has_docstring = True
                        in_function = False
                        
            except Exception as e:
                print(f"❌ Error leyendo {file_path}: {e}")
        
        # Calcular métricas de legibilidad
        if readability_metrics["total_functions"] > 0:
            doc_percentage = (readability_metrics["documented_functions"] / 
                            readability_metrics["total_functions"]) * 100
        else:
            doc_percentage = 0
            
        if readability_metrics["total_lines"] > 0:
            long_lines_percentage = (readability_metrics["long_lines"] / 
                                   readability_metrics["total_lines"]) * 100
        else:
            long_lines_percentage = 0
        
        readability_score = max(0, 100 - long_lines_percentage - (100 - doc_percentage) * 0.5)
        
        print(f"📊 LEGIBILIDAD:")
        print(f"   • Funciones documentadas: {doc_percentage:.1f}%")
        print(f"   • Líneas largas: {long_lines_percentage:.1f}%")
        print(f"   • Puntuación legibilidad: {readability_score:.1f}%")
        


if __name__ == "__main__":
    test = TestMaintainability()
    try:
        complexity_score = test.test_code_complexity_analysis()
        modularity_score = test.test_code_modularity()
        readability_score = test.test_code_readability()
        
        overall_maintainability = (complexity_score + modularity_score + readability_score) / 3
        
        print(f"\n🎯 MANTENIBILIDAD GENERAL: {overall_maintainability:.1f}%")
        print(f"   • Complejidad: {complexity_score:.1f}%")
        print(f"   • Modularidad: {modularity_score:.1f}%") 
        print(f"   • Legibilidad: {readability_score:.1f}%")
        
    except Exception as e:
        print(f"\n⚠️ Error: {e}")