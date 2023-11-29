from abc import ABC, abstractmethod

class Vehicle(ABC):
      @abstractmethod
      def features(self):
            pass

class Car(Vehicle):
      def features(self):
            print("Toyota Fortuner")
            print("Seating capacity: 7")
            print("Fuel Capacity: 10L")

class Bike(Vehicle):
      def features(self):
           print("Royal Enfield")
           print("Seating capacity: 2")
           print("Fuel Capacity: 5L") 

class NullObject(Vehicle):
      def features(self):
            print("NULL Vehicle")

# import pdb
def check_vehicle_type(vehicle_type):
    #   pdb.set_trace()
      if isinstance(vehicle_type, Car):
            return vehicle_type.features()
      elif isinstance(vehicle_type, Bike):
            return vehicle_type.features()
      #can be scaled for more vehicle types
      return NullObject().features()

if __name__ == '__main__':
      vehicles = [Car(), Bike(), None]
      for vehicle_type in vehicles:
            check_vehicle_type(vehicle_type)
           

