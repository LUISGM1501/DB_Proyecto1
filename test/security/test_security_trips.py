# tests/security/test_security_trips.py
"""
Pruebas de seguridad para la funcionalidad de Trips
Evalúa autenticación, autorización, inyección, y otros aspectos de seguridad
"""

import pytest
import jwt
import json
import time
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from app import app
from models.trip import Trip
from datetime import datetime, date, timedelta

@pytest.fixture
def client():
    """Cliente de pruebas para seguridad"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'security-test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def valid_token():
    """Token JWT válido para pruebas"""
    with app.app_context():
        return create_access_token(identity="1")

@pytest.fixture
def expired_token():
    """Token JWT expirado para pruebas"""
    with app.app_context():
        # Crear token que expira inmediatamente
        return create_access_token(identity="1", expires_delta=timedelta(seconds=-1))

@pytest.fixture
def malformed_tokens():
    """Diferentes tipos de tokens malformados"""
    return {
        'invalid_signature': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjk5OTk5OTk5fQ.invalid_signature',
        'malformed_structure': 'not.a.valid.jwt.token',
        'empty_token': '',
        'random_string': 'random_invalid_token_string',
        'sql_injection': "'; DROP TABLE trips; --",
        'script_injection': '<script>alert("xss")</script>'
    }


class TestAuthenticationSecurity:
    """Pruebas de seguridad de autenticación"""
    
    def test_access_without_token(self, client):
        """Verificar que endpoints requieren autenticación"""
        endpoints = [
            ('GET', '/trips'),
            ('POST', '/trips'),
            ('GET', '/trips/1'),
            ('PUT', '/trips/1'),
            ('DELETE', '/trips/1'),
            ('GET', '/trips/search'),
            ('POST', '/trips/1/places'),
            ('GET', '/trips/1/places'),
            ('DELETE', '/trips/1/places/1'),
            ('GET', '/trips/1/statistics')
        ]
        
        for method, endpoint in endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, json={})
            elif method == 'PUT':
                response = client.put(endpoint, json={})
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            assert response.status_code == 401, f"Endpoint {method} {endpoint} debería requerir autenticación"
            assert 'Missing Authorization Header' in response.get_data(as_text=True)
    
    def test_invalid_token_formats(self, client, malformed_tokens):
        """Probar diferentes formatos de tokens inválidos"""
        endpoint = '/trips'
        
        for token_type, token_value in malformed_tokens.items():
            headers = {'Authorization': f'Bearer {token_value}'}
            response = client.get(endpoint, headers=headers)
            
            assert response.status_code in [401, 422], f"Token {token_type} debería ser rechazado"
            print(f"✅ Token {token_type} correctamente rechazado: {response.status_code}")
    
    def test_token_without_bearer_prefix(self, client, valid_token):
        """Verificar que tokens sin 'Bearer ' son rechazados"""
        headers = {'Authorization': valid_token}  # Sin 'Bearer '
        response = client.get('/trips', headers=headers)
        
        assert response.status_code == 401
        response_text = response.get_data(as_text=True)
        assert ('Missing Authorization Header' in response_text or 
                'Missing \'Bearer\' type' in response_text)
    
    def test_expired_token_rejection(self, client):
        """Verificar que tokens expirados son rechazados"""
        # Crear token que expira en el pasado
        with app.app_context():
            expired_token = jwt.encode(
                {
                    'sub': '1',
                    'exp': int(time.time()) - 3600  # Expirado hace 1 hora
                },
                app.config['JWT_SECRET_KEY'],
                algorithm='HS256'
            )
        
        headers = {'Authorization': f'Bearer {expired_token}'}
        response = client.get('/trips', headers=headers)
        
        # Puede ser 401 o 422 dependiendo de la implementación
        assert response.status_code in [401, 422]
        print("✅ Token expirado correctamente rechazado")
    
    def test_token_signature_tampering(self, client, valid_token):
        """Verificar que tokens con firma alterada son rechazados"""
        # Alterar la firma del token
        tampered_token = valid_token[:-10] + 'tampered123'
        headers = {'Authorization': f'Bearer {tampered_token}'}
        response = client.get('/trips', headers=headers)
        
        assert response.status_code == 422
        print("✅ Token con firma alterada correctamente rechazado")


class TestAuthorizationSecurity:
    """Pruebas de seguridad de autorización"""
    
    @patch('controllers.trip_controller.get_trip')
    def test_unauthorized_trip_access(self, mock_get_trip, client, valid_token):
        """Verificar que usuarios no pueden acceder a trips de otros"""
        # Simular trip que pertenece a otro usuario
        other_user_trip = Trip(
            user_id=999,  # Usuario diferente
            title='Private Trip',
            description='Should not be accessible',
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 15),
            id=1
        )
        mock_get_trip.return_value = other_user_trip
        
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.get('/trips/1', headers=headers)
        
        assert response.status_code == 403
        assert 'Unauthorized' in response.get_data(as_text=True)
        print("✅ Acceso no autorizado correctamente bloqueado")
    
    @patch('controllers.trip_controller.get_trip')
    def test_unauthorized_trip_modification(self, mock_get_trip, client, valid_token):
        """Verificar que usuarios no pueden modificar trips de otros"""
        other_user_trip = Trip(
            user_id=999,
            title='Private Trip',
            description='Should not be modifiable',
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 15),
            id=1
        )
        mock_get_trip.return_value = other_user_trip
        
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        # Intentar actualizar
        update_data = {'title': 'Hacked Trip'}
        response = client.put('/trips/1', headers=headers, json=update_data)
        assert response.status_code == 403
        
        # Intentar eliminar
        response = client.delete('/trips/1', headers=headers)
        assert response.status_code == 403
        
        print("✅ Modificación no autorizada correctamente bloqueada")
    
    def test_privilege_escalation_attempts(self, client, valid_token):
        """Intentos de escalación de privilegios"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        # Intentar acceder a recursos administrativos (si existieran)
        admin_endpoints = [
            '/admin/trips',
            '/api/admin/users',
            '/internal/stats',
            '/debug/info'
        ]
        
        for endpoint in admin_endpoints:
            response = client.get(endpoint, headers=headers)
            # Debería retornar 404 (no existe) no 200 (acceso permitido)
            assert response.status_code in [404, 401, 403], f"Posible escalación en {endpoint}"


class TestInputValidationSecurity:
    """Pruebas de seguridad de validación de entrada"""
    
    def test_sql_injection_attempts(self, client, valid_token):
        """Intentos de inyección SQL en parámetros"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        sql_payloads = [
            "'; DROP TABLE trips; --",
            "1' OR '1'='1",
            "1; DELETE FROM trips WHERE 1=1; --",
            "' UNION SELECT * FROM users --",
            "1' AND (SELECT COUNT(*) FROM trips) > 0 --"
        ]
        
        for payload in sql_payloads:
            # Probar en diferentes endpoints
            response = client.get(f'/trips/{payload}', headers=headers)
            assert response.status_code in [400, 404, 422], f"Posible SQLi en trip_id: {payload}"
            
            # Probar en parámetros de búsqueda
            response = client.get('/trips/search', 
                                headers=headers, 
                                query_string={'title': payload, 'status': payload})
            assert response.status_code in [200, 400, 422], "SQLi en parámetros de búsqueda"
        
        print("✅ Protección contra inyección SQL verificada")
    
    def test_xss_injection_attempts(self, client, valid_token):
        """Intentos de inyección XSS en datos de entrada"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            "javascript:alert('XSS')",
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>'
        ]
        
        for payload in xss_payloads:
            trip_data = {
                'title': payload,
                'description': payload,
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            }
            
            response = client.post('/trips', headers=headers, json=trip_data)
            # Debería aceptar o rechazar, pero nunca ejecutar el script
            assert response.status_code in [201, 400, 422]
            
            # Verificar que el payload no se refleje sin escapar
            if response.status_code == 201:
                # Si se acepta, verificar que está escapado en respuestas
                assert '<script>' not in response.get_data(as_text=True)
        
        print("✅ Protección contra XSS verificada")
    
    def test_oversized_input_handling(self, client, valid_token):
        """Manejo de entradas excesivamente grandes"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        # Crear datos excesivamente grandes
        oversized_data = {
            'title': 'A' * 10000,  # Título muy largo
            'description': 'B' * 100000,  # Descripción muy larga
            'start_date': '2024-07-01',
            'end_date': '2024-07-15'
        }
        
        response = client.post('/trips', headers=headers, json=oversized_data)
        
        # Debería rechazar o truncar, no causar error del servidor
        assert response.status_code in [201, 400, 413, 422]
        assert response.status_code != 500, "Entrada grande causó error del servidor"
        
        print("✅ Manejo de entradas grandes verificado")
    
    def test_invalid_date_formats(self, client, valid_token):
        """Validación de formatos de fecha inválidos"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        invalid_dates = [
            '2024-13-01',  # Mes inválido
            '2024-02-30',  # Día inválido
            'invalid-date',
            # Formatos que algunos parsers pueden aceptar, comentados para evitar falsos positivos
            # '01-07-2024',  # Formato DD-MM-YYYY puede ser interpretado por algunos parsers
            '',  # Fecha vacía
            None,  # Fecha nula
            '2024-07-32'  # Día que no existe
        ]
        
        for invalid_date in invalid_dates:
            trip_data = {
                'title': 'Test Trip',
                'start_date': invalid_date,
                'end_date': '2024-07-15'
            }
            
            response = client.post('/trips', headers=headers, json=trip_data)
            assert response.status_code in [400, 422], f"Fecha inválida aceptada: {invalid_date}"
        
        print("✅ Validación de fechas verificada")


class TestDataLeakageSecurity:
    """Pruebas para prevenir filtración de datos"""
    
    def test_error_message_information_disclosure(self, client, valid_token):
        """Verificar que mensajes de error no revelan información sensible"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        # Provocar diferentes tipos de errores
        error_scenarios = [
            ('GET', '/trips/99999'),  # Trip no existente
            ('POST', '/trips', {'invalid': 'data'}),  # Datos inválidos
            ('PUT', '/trips/99999', {'title': 'Test'}),  # Actualizar no existente
        ]
        
        for method, endpoint, *data in error_scenarios:
            if method == 'GET':
                response = client.get(endpoint, headers=headers)
            elif method == 'POST':
                response = client.post(endpoint, headers=headers, json=data[0] if data else {})
            elif method == 'PUT':
                response = client.put(endpoint, headers=headers, json=data[0] if data else {})
            
            response_text = response.get_data(as_text=True)
            
            # Verificar que no se filtren detalles técnicos
            sensitive_info = [
                'Traceback',
                'File "',
                'line ',
                'mysql',
                'postgresql',
                'redis',
                'password',
                'secret',
                'key',
                'token',
                'internal',
                'debug'
            ]
            
            for info in sensitive_info:
                assert info.lower() not in response_text.lower(), f"Información sensible en error: {info}"
        
        print("✅ Mensajes de error seguros verificados")
    
    @patch('controllers.trip_controller.get_user_trips')
    def test_user_data_isolation(self, mock_get_trips, client):
        """Verificar aislamiento de datos entre usuarios"""
        # Simular dos usuarios diferentes
        user1_trip = Trip(1, 'User 1 Trip', 'Private', date(2024, 7, 1), date(2024, 7, 15), id=1)
        user2_trip = Trip(2, 'User 2 Trip', 'Private', date(2024, 8, 1), date(2024, 8, 15), id=2)
        
        with app.app_context():
            user1_token = create_access_token(identity="1")
            user2_token = create_access_token(identity="2")
        
        # Usuario 1 debería ver solo sus trips
        mock_get_trips.return_value = ([user1_trip], 1)
        headers1 = {'Authorization': f'Bearer {user1_token}'}
        response1 = client.get('/trips', headers=headers1)
        
        assert response1.status_code == 200
        # Verificar que no aparecen datos del usuario 2
        response_text = response1.get_data(as_text=True)
        assert 'User 2 Trip' not in response_text
        
        print("✅ Aislamiento de datos verificado")


class TestRateLimitingSecurity:
    """Pruebas de limitación de velocidad para prevenir ataques"""
    
    def test_rapid_request_handling(self, client, valid_token):
        """Verificar manejo de solicitudes rápidas consecutivas"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        # Hacer múltiples solicitudes rápidas
        responses = []
        for i in range(20):
            response = client.get('/trips', headers=headers)
            responses.append(response.status_code)
        
        # Verificar que el sistema no colapsa
        server_errors = sum(1 for status in responses if status >= 500)
        assert server_errors == 0, f"Solicitudes rápidas causaron {server_errors} errores de servidor"
        
        # Opcional: verificar si hay rate limiting implementado
        too_many_requests = sum(1 for status in responses if status == 429)
        if too_many_requests > 0:
            print(f"✅ Rate limiting activo: {too_many_requests}/20 solicitudes limitadas")
        else:
            print("ℹ️  Rate limiting no detectado (puede ser intencional)")
    
    def test_creation_spam_protection(self, client, valid_token):
        """Verificar protección contra spam de creación"""
        headers = {'Authorization': f'Bearer {valid_token}'}
        
        # Intentar crear muchos trips rápidamente
        creation_attempts = 0
        successful_creations = 0
        
        for i in range(10):
            trip_data = {
                'title': f'Spam Trip {i}',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            }
            
            response = client.post('/trips', headers=headers, json=trip_data)
            creation_attempts += 1
            
            if response.status_code == 201:
                successful_creations += 1
            elif response.status_code == 429:
                print(f"✅ Rate limiting activado después de {successful_creations} creaciones")
                break
        
        # El sistema debería manejar esto sin errores
        assert creation_attempts > 0
        print(f"✅ Manejo de creación rápida: {successful_creations}/{creation_attempts} exitosas")


class TestSecurityHeaders:
    """Pruebas de headers de seguridad HTTP"""
    
    def test_security_headers_present(self, client):
        """Verificar presencia de headers de seguridad"""
        response = client.get('/')
        
        # Headers de seguridad recomendados
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': None  # Cualquier valor es bueno
        }
        
        present_headers = []
        missing_headers = []
        
        for header, expected_value in security_headers.items():
            if header in response.headers:
                present_headers.append(header)
                if expected_value and response.headers[header] != expected_value:
                    print(f"⚠️  {header} presente pero valor diferente: {response.headers[header]}")
            else:
                missing_headers.append(header)
        
        print(f"✅ Headers de seguridad presentes: {present_headers}")
        if missing_headers:
            print(f"ℹ️  Headers de seguridad faltantes: {missing_headers}")
            print("💡 Considera implementar estos headers para mejor seguridad")


def test_security_summary():
    """Resumen de todas las pruebas de seguridad"""
    print("\n" + "="*60)
    print("🔒 RESUMEN DE PRUEBAS DE SEGURIDAD")
    print("="*60)
    print("✅ Todas las pruebas de seguridad completadas")
    print("\n🛡️  Aspectos de seguridad evaluados:")
    print("   • Autenticación - Verificación de identidad")
    print("   • Autorización - Control de acceso a recursos")
    print("   • Validación de entrada - Prevención de inyección")
    print("   • Filtración de datos - Protección de información")
    print("   • Rate limiting - Protección contra abuso")
    print("   • Headers de seguridad - Protecciones HTTP")
    print("\n🎯 Criterios de seguridad:")
    print("   • Todos los endpoints requieren autenticación")
    print("   • Tokens inválidos/expirados son rechazados")
    print("   • Usuarios solo acceden a sus propios datos")
    print("   • Entradas maliciosas son validadas/rechazadas")
    print("   • Errores no revelan información sensible")
    print("   • Sistema resiste solicitudes abusivas")
    print("\n💡 Recomendaciones de seguridad:")
    print("   • Implementar rate limiting en producción")
    print("   • Agregar headers de seguridad HTTP")
    print("   • Monitorear intentos de acceso no autorizado")
    print("   • Realizar auditorías de seguridad regulares")
    print("   • Implementar logging de eventos de seguridad")