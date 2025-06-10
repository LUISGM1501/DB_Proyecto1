#!/usr/bin/env python3
"""
Script de diagnóstico para entender por qué fallan las pruebas de integración
"""

import pytest
from flask_jwt_extended import create_access_token
from app import app

def test_debug_trip_routes():
    """Diagnóstico detallado de las rutas de trips"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            # Test 1: Verificar que la aplicación responda
            print("\n=== TEST 1: Verificar home ===")
            response = client.get('/')
            print(f"Home status: {response.status_code}")
            print(f"Home response: {response.get_data(as_text=True)}")
            
            # Test 2: Verificar ruta trips sin auth
            print("\n=== TEST 2: Trips sin autenticación ===")
            response = client.get('/trips')
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_data(as_text=True)}")
            
            # Test 3: Crear token JWT
            print("\n=== TEST 3: Crear token JWT ===")
            try:
                access_token = create_access_token(identity=1)
                print(f"Token creado exitosamente: {access_token[:50]}...")
            except Exception as e:
                print(f"Error creando token: {e}")
                return
            
            # Test 4: Probar con token válido
            print("\n=== TEST 4: Trips con autenticación ===")
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.get('/trips', headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_data(as_text=True)}")
            
            # Test 5: Probar POST con token válido
            print("\n=== TEST 5: POST trips con autenticación ===")
            trip_data = {
                'title': 'Test Trip',
                'start_date': '2024-12-01',
                'end_date': '2024-12-15'
            }
            response = client.post('/trips', headers=headers, json=trip_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_data(as_text=True)}")
            
            # Test 6: Verificar configuración JWT
            print("\n=== TEST 6: Configuración JWT ===")
            print(f"JWT_SECRET_KEY configurado: {bool(app.config.get('JWT_SECRET_KEY'))}")
            print(f"JWT_ACCESS_TOKEN_EXPIRES: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}")

if __name__ == "__main__":
    test_debug_trip_routes()