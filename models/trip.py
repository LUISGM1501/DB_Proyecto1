# models/trip.py
from datetime import datetime, date
from zoneinfo import ZoneInfo
from decimal import Decimal

class Trip:
    def __init__(self, user_id, title, description, start_date, end_date, 
                 status='planned', budget=None, id=None):
        # Inicializa un nuevo objeto Trip con los detalles del viaje
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        # Convierte las fechas de inicio y fin a objetos date si no lo son
        self.start_date = start_date if isinstance(start_date, date) else date.fromisoformat(start_date)
        self.end_date = end_date if isinstance(end_date, date) else date.fromisoformat(end_date)
        self.status = status
        # Convierte el presupuesto a Decimal si no es None
        self.budget = budget if budget is None else Decimal(str(budget))
        # Establece las fechas de creación y actualización a la hora actual en UTC
        self.created_at = datetime.now(ZoneInfo("UTC"))
        self.updated_at = datetime.now(ZoneInfo("UTC"))
        self.places = []  # Lista de lugares visitados en el viaje
        self.expenses = []  # Lista de gastos del viaje

    # to_dict: Convierte el objeto Trip a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            # Convierte las fechas a formato ISO si están definidas
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            # Convierte el presupuesto a float si está definido
            "budget": float(self.budget) if self.budget else None,
            # Convierte las fechas de creación y actualización a formato ISO si están definidas
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            "updated_at": self.updated_at.isoformat() if hasattr(self, 'updated_at') else None,
            "places": self.places,
            "expenses": self.expenses
        }

    @property
    def duration_days(self):
        """Calcula la duración del viaje en días"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    def is_active(self):
        """Determina si el viaje está actualmente en progreso"""
        today = date.today()
        return (self.start_date <= today <= self.end_date and 
                self.status == 'in_progress')

    def is_completed(self):
        """Determina si el viaje ya terminó"""
        today = date.today()
        return (self.end_date < today or self.status == 'completed')

class TripPlace:
    def __init__(self, trip_id, place_id, visit_date=None, visit_order=None, 
                 notes=None, rating=None, id=None):
        # Inicializa un nuevo objeto TripPlace con los detalles del lugar visitado
        self.id = id
        self.trip_id = trip_id
        self.place_id = place_id
        # Convierte la fecha de visita a un objeto date si no lo es
        self.visit_date = visit_date if isinstance(visit_date, date) else (
            date.fromisoformat(visit_date) if visit_date else None
        )
        self.visit_order = visit_order
        self.notes = notes
        self.rating = rating
        # Establece la fecha de creación a la hora actual en UTC
        self.created_at = datetime.now(ZoneInfo("UTC"))

    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "place_id": self.place_id,
            # Convierte la fecha de visita a formato ISO si está definida
            "visit_date": self.visit_date.isoformat() if self.visit_date else None,
            "visit_order": self.visit_order,
            "notes": self.notes,
            "rating": self.rating,
            # Convierte la fecha de creación a formato ISO si está definida
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') else None
        }

class TripExpense:
    def __init__(self, trip_id, category, description, amount, expense_date, 
                 place_id=None, id=None):
        # Inicializa un nuevo objeto TripExpense con los detalles del gasto
        self.id = id
        self.trip_id = trip_id
        self.category = category  # 'transport', 'accommodation', 'food', 'activities', 'other'
        self.description = description
        # Convierte el monto a Decimal
        self.amount = Decimal(str(amount))
        # Convierte la fecha del gasto a un objeto date si no lo es
        self.expense_date = expense_date if isinstance(expense_date, date) else date.fromisoformat(expense_date)
        self.place_id = place_id
        # Establece la fecha de creación a la hora actual en UTC
        self.created_at = datetime.now(ZoneInfo("UTC"))

    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "category": self.category,
            "description": self.description,
            # Convierte el monto a float
            "amount": float(self.amount),
            # Convierte la fecha del gasto a formato ISO si está definida
            "expense_date": self.expense_date.isoformat() if self.expense_date else None,
            "place_id": self.place_id,
            # Convierte la fecha de creación a formato ISO si está definida
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') else None
        }