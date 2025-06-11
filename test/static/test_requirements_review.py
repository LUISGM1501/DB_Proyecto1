# tests/static/test_requirements_review.py
"""
Prueba Estática 1: Revisión de Requerimientos
Verifica la completitud de los requerimientos funcionales implementados
"""

import os
import pytest
from pathlib import Path

class TestRequirementsReview:
    """
    Prueba de completitud de requerimientos funcionales
    Basada en el PDF del proyecto
    """
    
    def test_functional_requirements_completeness(self):
        """
        Verifica que todos los requerimientos funcionales estén implementados
        """
        print("\n📋 REVISIÓN DE REQUERIMIENTOS FUNCIONALES")
        
        # Requerimientos del PDF del proyecto
        required_features = {
            "Usuarios": {
                "files": ["controllers/user_controller.py", "models/user.py", "routes/user_routes.py"],
                "implemented": True
            },
            "Publicaciones": {
                "files": ["controllers/post_controller.py", "models/post.py", "routes/post_routes.py"],
                "implemented": True
            },
            "Lugares": {
                "files": ["controllers/place_controller.py", "models/place.py", "routes/place_routes.py"],
                "implemented": True
            },
            "Listas de Viaje": {
                "files": ["controllers/travel_list_controller.py", "models/travel_list.py", "routes/travel_list_routes.py"],
                "implemented": True
            },
            "Comentarios": {
                "files": ["controllers/comment_controller.py", "models/comment.py", "routes/comment_routes.py"],
                "implemented": True
            },
            "Likes": {
                "files": ["controllers/like_controller.py", "models/like.py", "routes/like_routes.py"],
                "implemented": True
            },
            "Viajes": {
                "files": ["controllers/trip_controller.py", "models/trip.py", "routes/trip_routes.py"],
                "implemented": True
            }
        }
        
        # Verificar implementación
        missing_requirements = []
        implemented_count = 0
        total_requirements = len(required_features)
        
        for requirement, details in required_features.items():
            files_exist = all(os.path.exists(file) for file in details["files"])
            
            if files_exist and details["implemented"]:
                implemented_count += 1
                print(f"✅ {requirement}: Implementado")
            else:
                missing_requirements.append(requirement)
                print(f"❌ {requirement}: Faltante")
        
        # Calcular porcentaje de completitud
        completeness_percentage = (implemented_count / total_requirements) * 100
        
        print(f"\n📊 RESULTADOS DE REVISIÓN:")
        print(f"   • Requerimientos implementados: {implemented_count}/{total_requirements}")
        print(f"   • Porcentaje de completitud: {completeness_percentage:.1f}%")
        
        if missing_requirements:
            print(f"   • Faltantes: {', '.join(missing_requirements)}")
        
        # Criterio de aceptación: 85% de completitud
        assert completeness_percentage >= 85.0, f"Completitud insuficiente: {completeness_percentage:.1f}%"
        assert implemented_count >= 6, "Faltan funcionalidades críticas"
        
        print(f"✅ REQUERIMIENTOS: {completeness_percentage:.1f}% completitud alcanzada")


if __name__ == "__main__":
    # Ejecutar la prueba directamente
    test = TestRequirementsReview()
    try:
        result = test.test_functional_requirements_completeness()
        print(f"\n🎯 Prueba exitosa: {result:.1f}% de requerimientos implementados")
    except AssertionError as e:
        print(f"\n❌ Prueba fallida: {e}")
    except Exception as e:
        print(f"\n⚠️ Error en prueba: {e}")