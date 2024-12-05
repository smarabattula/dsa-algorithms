# Pizza builder
# Base - (material, cost)   = 1 (Ex: Cheese, Thin Crust)
# Toppings - (name, cost)  >= 0 (Ex: Onion, Chicken, Tomato)
# Size - (name, cost, mx)   = 1 (Ex: Regular, Large)
# Dough - (name, cost)      = 1 (Ex: Sourdough, Wheat)

'''
NOTE:
In Pizza class, Getters and setters can be skipped to save time

Design Patterns used:
Builder & Clone Patterns for Creating Pizza (PizzaBuilder)
Strategy Pattern for Calculating Price (PriceCalculator)

'''
from abc import ABC, abstractmethod
from enum import Enum
from copy import deepcopy

class Ground(ABC):
    # class-level attributes
    _name: str
    _price: float

    # @abstractmethod
    def getName(self):
        return self._name

    def getPrice(self):
        return self._price

class Base(Ground):
    def __init__(self):
        pass

class CheeseBase(Base):
    def __init__(self):
        self._name = "Cheese Base"
        self._price = 2.5

class ThinCrustBase(Base):
    def __init__(self):
        self._name = "Thin Crust Base"
        self._price = 2.75

class DoughTypes(Enum):
    SourDough = 2.5
    WheatDough = 1.5

class Dough(Ground):
    def __init__(self, dough_type):
        self._name = dough_type.name
        self._price = dough_type.value

class ToppingTypes(Enum):
    Tomato = 0.75
    Onion = 0.5
    Chicken = 1.0

class Topping(Ground):
    def __init__(self, topping_type):
        self._name = topping_type.name
        self._price = topping_type.value

class PizzaSize(Enum):
    Regular = (6 , 1.0)
    Medium  = (8 , 1.5)
    Large   = (10, 2.0)

class Size(Ground):
    _price = 8.0
    def __init__(self, pizza_size):
        self._radius, self._multiplier = pizza_size.value
        self._name = pizza_size.name

    def getMultiplier(self):
        return self._multiplier

class PriceCalculator:
    @abstractmethod
    def calculatePrice(self):
        pass

class Pizza:
    def __init__(self, base: Base = None, size: Size = None, dough: Dough = None, toppings: list[Topping] = [], pc :PriceCalculator = None):
        self._base: Base = base
        self._size: Size = size
        self._dough: Dough = dough
        self._toppings: list[Topping] = list(toppings)
        self._pc: PriceCalculator = pc

    def getBase(self):
        return self._base

    def setBase(self, base):
        self._base = base

    def getSize(self):
        return self._size

    def setSize(self, size):
        self._size = size

    def getDough(self):
        return self._dough

    def setDough(self, dough):
        self._dough = dough

    def getToppings(self):
        return self._toppings

    def addTopping(self, topping):
        self._toppings.append(topping)

    def getPizzaPrice(self):
        return self._pc.calculatePrice(self)

    def setPriceCalculator(self, pc):
        self._pc = pc

    def validate(self):
        if not self._base or not self._size or not self._dough:
            raise ValueError("Base, Size, and Dough are required to build a pizza.")
        return True

    def clone(self):
        # new_pizza = Pizza(self._base, self._size, self._dough, self._toppings, self._pc)
        return deepcopy(self)

class SimpleCalculator(PriceCalculator):
    def calculatePrice(self, pizza: Pizza) -> float:
        total_price = 0.0
        total_price += pizza.getBase().getPrice() + pizza.getDough().getPrice()
        for topping in pizza.getToppings():
            total_price += topping.getPrice()

        total_price += pizza.getSize().getPrice()
        total_price *= pizza.getSize().getMultiplier()
        return total_price

class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()
        self._pizza.setPriceCalculator(SimpleCalculator())

    def setBase(self, base):
        self._pizza.setBase(base)
        return self

    def setSize(self, size):
        self._pizza.setSize(size)
        return self

    def setDough(self, dough):
        self._pizza.setDough(dough)
        return self

    def addTopping(self, topping):
        self._pizza.addTopping(topping)
        return self

    def setPriceCalculator(self, pc):
        self._pizza.setPriceCalculator(pc)
        return self

    def build(self):
        if self._pizza.validate():
            built_pizza = deepcopy(self._pizza)  # Create a deepcopy to avoid shared references
            self._pizza = Pizza()  # Reset builder for a new pizza
            self._pizza.setPriceCalculator(SimpleCalculator())
            return built_pizza
        else:
            raise Exception("Size / Base / Dough missing!")

