# Room (id, room_status, price) (more types)
# Customer (id, name, phone, email, address)
# Reservation (id, Customer, Room, checkIn, checkOut, reservation_status [confirmed, complete, cancelled], payment_status [pending, paid])
# Payment (CreditCard, Cash)

'''
Design Patterns Used:
Singleton for Hotel Management
Factory & Strategy for Payment
'''
from abc import ABC, abstractmethod
from enum import Enum
from threading import Lock
from datetime import datetime, date
from typing import Dict, Optional
import uuid

class RoomStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    OCCUPIED = "OCCUPIED"

class RoomType(Enum):
    SINGLE = 100
    DOUBLE = 175
    DELUXE = 250
    SUITE  = 400

class Room:
    def __init__(self, id, type: RoomType):
        self._id = id
        self._type: RoomType = type
        self._status: RoomStatus = RoomStatus.AVAILABLE
        self._lock = Lock()

    def getPrice(self):
        return self._type.value

    def book(self):
        with self._lock:
            if self._status == RoomStatus.AVAILABLE:
                self._status = RoomStatus.BOOKED
            else:
                raise Exception("Room {self._id} isn't available! ")

    def checkIn(self):
        with self._lock:
            if self._status == RoomStatus.BOOKED:
                self._status = RoomStatus.OCCUPIED
            else:
                raise Exception("Room {self._id} not booked!      ")

    def checkOut(self):
        with self._lock:
            if self._status == RoomStatus.OCCUPIED:
                self._status = RoomStatus.AVAILABLE
            else:
                raise Exception("Room {self._id} already occupied!")

class Customer:
    def __init__(self, id, name, phone, email, address):
        self._id = id
        self._name = name
        self._phone = phone
        self._email = email
        self._address = address

    # Write getters and setters for name, phone, email, address
    # Only getter for id

class ReservationStatus(Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

class PaymentStatus(Enum):
    PENDING = "Pending"
    CONFIRM = "Confirm"

class PriceCalculator(ABC):
    @abstractmethod
    def calculatePrice(self, reservation) -> float:
        pass

class Reservation:
    def __init__(self, id, customer: Customer, room: Room, checkInTime: date, checkOutTime: date):
        self._id = id
        self._customer = customer
        self._room = room
        self._checkInTime = checkInTime
        self._checkOutTime = checkOutTime
        self._status = ReservationStatus.CONFIRMED
        self._payment_status = PaymentStatus.PENDING
        self._pc: PriceCalculator = SimplePriceCalculator()

        # Write getters for name, phone, email, address

    def cancel(self):
        if self._status == ReservationStatus.CONFIRMED:
            self._status = ReservationStatus.CANCELLED
            self._room.checkOut()
        else:
            raise ValueError(f"Reservation {self._id} isn't not confirmed.")

    def calculatePrice(self):
        return self._pc.calculatePrice(self)

class SimplePriceCalculator(PriceCalculator):
    def calculatePrice(self, reservation: Reservation) -> float:
        days = (reservation._checkOutTime - reservation._checkInTime).days + 1
        return days * reservation._room.getPrice()

class Payment(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def processPayment(self, amt):
        pass

class CashPayment(Payment):
    def processPayment(self, amt):
        return True

class CreditCardPayment(Payment):
    def processPayment(self, amt):
        return True

class HotelManagement:
    _instance = None
    _lock = Lock()

    def __init__(self):
        if HotelManagement._instance:
            raise Exception("This is a Singleton class. Use `HotelManagement.get_instance()` to access it.")
        self._rooms: Dict[str, Room] = {}
        self._customers: Dict[str, Customer] = {}
        self._reservations: Dict[str, Reservation] = {}

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with Lock():
                if cls._instance is None:  # Double-checked locking
                    cls._instance = cls()
        return cls._instance

    def add_customer(self, cust: Customer):
        with self._lock:
            if cust._id not in self._customers:
                self._customers[cust._id] = cust
            else:
                raise Exception(f"Customer with ID {cust._id} already exists.")

    def get_customer(self, cust_id) -> Optional[Customer]:
        return self._customers.get(cust_id, None)

    def add_room(self, room: Room):
        with self._lock:
            if room._id not in self._rooms:
                self._rooms[room._id] = room
            else:
                raise Exception(f"Room with ID {room._id} already exists.")

    def get_room(self, room_id):
        return self._rooms.get(room_id, None)

    def get_free_room(self, room_type: RoomType) -> Optional[Room]:
        pass
    #     with self._lock:
    #         for room_id in self._rooms:  # Iterate over Room objects
    #             room = self._rooms[room_id]
    #             if room._type == room_type and room._status == RoomStatus.AVAILABLE:
    #                 return room
    #         return None

    def _generate_reservation_id(self) -> str:
        return f"{uuid.uuid4().hex[:8].upper()}"

    def book_room(self, room: Room, cust: Customer, check_in_time: datetime, check_out_time: datetime) -> Reservation:
        with self._lock:
            if room._status != RoomStatus.AVAILABLE:
                raise Exception(f"Room {room._id} is not available for booking.")
            room.book()
            reservation_id = self._generate_reservation_id()
            reservation = Reservation(reservation_id, cust, room, check_in_time, check_out_time)
            self._reservations[reservation_id] = reservation
            return reservation

    def check_in(self, reservation_id: str):
        with self._lock:
            reservation = self._reservations.get(reservation_id)
            if reservation and reservation._status == ReservationStatus.CONFIRMED:
                reservation._room.checkIn()
            else:
                raise Exception(f"Reservation {reservation_id} is not valid for check-in.")

    def check_out(self, reservation_id: str, payment: Payment):
        with self._lock:
            reservation = self._reservations.get(reservation_id)
            if reservation and reservation._status == ReservationStatus.CONFIRMED:
                amount = reservation.calculatePrice()
                if payment.processPayment(amount):
                    reservation._room.checkOut()
                    reservation._payment_status = PaymentStatus.CONFIRM
                    del self._reservations[reservation_id]
                else:
                    raise Exception("Payment failed.")
            else:
                raise Exception(f"Reservation {reservation_id} is not valid for check-out.")
