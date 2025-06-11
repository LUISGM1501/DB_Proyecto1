# tests/static/test_functional_correctness.py
"""
Prueba Estática 2: Análisis de Completitud y Correctitud Funcional
Verifica que la implementación coincida con las especificaciones
"""

import ast
import os
import pytest

class TestFunctionalCorrectness:
    """
    Análisis de correctitud de implementación funcional
    """
    
    def test_api_endpoints_correctness(self):
        """
        Verifica que los endpoints implementados sean correctos
        según las especificaciones del proyecto
        """
        print("\n🔍 ANÁLISIS DE CORRECTITUD FUNCIONAL")
        
        # Especificación esperada de endpoints críticos
        expected_endpoints = {
            "trips": {
                "file": "routes/trip_routes.py",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "found_methods": []
            },
            "users": {
                "file": "routes/user_routes.py", 
                "methods": ["GET", "POST"],
                "found_methods": []
            },
            "posts": {
                "file": "routes/post_routes.py",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "found_methods": []
            }
        }
        
        correctness_score = 0
        total_checks = 0
        
        for endpoint_name, spec in expected_endpoints.items():
            if os.path.exists(spec["file"]):
                try:
                    with open(spec["file"], 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Buscar métodos HTTP implementados
                    for method in spec["methods"]:
                        if f"methods=['{method}']" in content or f'methods=["{method}"]' in content:
                            spec["found_methods"].append(method)
                    
                    # Calcular correctitud
                    expected_count = len(spec["methods"])
                    found_count = len(spec["found_methods"])
                    endpoint_correctness = (found_count / expected_count) * 100
                    
                    print(f"📁 {endpoint_name.upper()}:")
                    print(f"   • Esperados: {spec['methods']}")
                    print(f"   • Encontrados: {spec['found_methods']}")
                    print(f"   • Correctitud: {endpoint_correctness:.1f}%")
                    
                    correctness_score += endpoint_correctness
                    total_checks += 1
                    
                except Exception as e:
                    print(f"❌ Error analizando {spec['file']}: {e}")
            else:
                print(f"❌ Archivo faltante: {spec['file']}")
        
        # Calcular correctitud general
        if total_checks > 0:
            overall_correctness = correctness_score / total_checks
        else:
            overall_correctness = 0
            
        print(f"\n📊 RESULTADO CORRECTITUD FUNCIONAL:")
        print(f"   • Correctitud promedio: {overall_correctness:.1f}%")
        print(f"   • Endpoints analizados: {total_checks}")
        
        # Criterio de aceptación: 70% de correctitud
        assert overall_correctness >= 70.0, f"Correctitud insuficiente: {overall_correctness:.1f}%"
        assert total_checks >= 2, "Muy pocos endpoints analizados"
        
        print(f"✅ CORRECTITUD: {overall_correctness:.1f}% alcanzada")
    
    def test_model_data_consistency(self):
        """
        Verifica consistencia en modelos de datos
        """
        print("\n🗂️ VERIFICANDO CONSISTENCIA DE MODELOS")
        
        model_files = [
            "models/trip.py",
            "models/user.py", 
            "models/post.py"
        ]
        
        consistent_models = 0
        total_models = len(model_files)
        
        for model_file in model_files:
            if os.path.exists(model_file):
                try:
                    with open(model_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verificar que tenga método to_dict (patrón consistente)
                    has_to_dict = 'def to_dict(' in content
                    has_init = 'def __init__(' in content
                    
                    if has_to_dict and has_init:
                        consistent_models += 1
                        print(f"✅ {model_file}: Consistente")
                    else:
                        print(f"⚠️ {model_file}: Posibles inconsistencias")
                        
                except Exception as e:
                    print(f"❌ Error en {model_file}: {e}")
            else:
                print(f"❌ Faltante: {model_file}")
        
        consistency_percentage = (consistent_models / total_models) * 100
        print(f"\n📊 CONSISTENCIA DE MODELOS: {consistency_percentage:.1f}%")
        


if __name__ == "__main__":
    test = TestFunctionalCorrectness()
    try:
        correctness = test.test_api_endpoints_correctness()
        consistency = test.test_model_data_consistency()
        print(f"\n🎯 Correctitud: {correctness:.1f}%, Consistencia: {consistency:.1f}%")
    except Exception as e:
        print(f"\n⚠️ Error: {e}")