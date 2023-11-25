import heapq
import math
from heapq import heappush, heappop
from datetime import datetime, timedelta
class Car:
    def __init__(self, car_id, car_type, price_per_hour) -> None:
        self.car_id = car_id
        self.car_type = car_type
        self.price_per_hour = price_per_hour
        self.is_booked = False

class Reservation:
    def __init__(self, reservation_id, user, vehicle, start_time, end_time) -> None:
        self.reservation_id = reservation_id
        self.user = user
        self.vehicle = vehicle
        self.start_tume = start_time
        self.end_time = end_time

class Bill:
    def __init__(self, bill_id, reservation, total_amount ) -> None:
        self.bill_id = bill_id
        self.reservation = reservation
        self.total_amount = total_amount

class User:
    def __init__(self, user_id, name) -> None:
        self.user_id = user_id
        self.name = name
        self.reservations = []
        self.bills = []

class Station:
    def __init__(self, id, location):
        self.station_id = id
        self.location = location
        self.available_cars = []
        self.booked_cars = []
    
    def add_car(self, car):
        self.available_cars.append(car)
    
    def book_car(self, car):
        car.is_booked = True
        self.available_cars.remove(car)
        self.booked_cars.append(car)

    def drop_car(self, car):
        car.is_booked = False
        self.available_cars.append(car)
        self.booked_cars.remove(car)

class RentalSystem:
    def __init__(self):
        self.stations = []
    
    def add_station(self, station):
        self.stations.append(station)
    
    def search_cars(self, car_type, user_location):
        available_stations = []
        for station in self.stations:
            available_cars = [car for car in station.available_cars if car.car_type == car_type]
            if available_cars:
                price_per_hour = min(car.price_per_hour for car in available_cars)
                distance_to_user = self.calculate_distance(station.location, user_location)
                heappush(available_stations, (price_per_hour, distance_to_user, station))

        result_stations = [station for _, _, station in heapq.nsmallest(len(available_stations), available_stations)]
        return result_stations
    
    @staticmethod
    def calculate_distance(location1, location2):
        x1, y1 = location1
        x2, y2 = location2
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def book_car(self, user, car_type, pickup_location, drop_location, duration_hours):
        pickup_location, drop_location = int(pickup_location), int(drop_location)
        user_location = self.stations[pickup_location-1].location
        available_stations = self.search_cars(car_type, user_location)

        if not available_stations:
            print("No available cars matching the criteria.")
            return
        
        selected_station = available_stations[0]
        selected_car = next((car for car in selected_station.available_cars if car.car_type == car_type), None)
        
        if not selected_car:
            print("No available cars of the specified type.")
            return
        
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=duration_hours)
        reservation_id = len(user.reservations) + 1
        reservation = Reservation(reservation_id, user, selected_car, start_time, end_time)
        bill_id = len(user.bills) + 1
        total_amount = duration_hours * selected_car.price_per_hour
        bill = Bill(bill_id, reservation, total_amount)
        print(f"Booking successful! Reservation ID: {reservation.reservation_id}, "
              f"Pickup Station: {selected_station.station_id}, Drop Station: {drop_location}, "
              f"Total Amount: ${bill.total_amount}") 
        
        selected_station.book_car(selected_car)
        user.reservations.append(reservation)
        user.bills.append(bill)
    
    def drop_car(self, user, reservation_id, drop_station):
        drop_station = int(drop_station)
        reservation = next((res for res in user.reservations if res.reservation_id == reservation_id), None)

        if not reservation:
            print("Invalid reservation ID.")
            return

        if reservation.end_time < datetime.now():
            print("Invalid drop time. Reservation has already ended.")
            return
        
        station = self.stations[drop_station-1]
        station.drop_car(reservation.vehicle)

        print(f"Car dropped successfully at Station {station.station_id}. "
              f"Reservation ID: {reservation.reservation_id}")

if __name__ == '__main__':

    # create a car
    suv = Car(1, "SUV", 100)

    # create a rental system
    rental_system = RentalSystem()
    
    station = Station(1, (0, 0))
    station.add_car(suv)
    rental_system.add_station(station)

    #searching
    car_type_to_search = "SUV"
    user_location = (0, 0)

    result_stations = rental_system.search_cars(car_type_to_search, user_location)
    print(f"Available {car_type_to_search} Cars:")
    for station in result_stations:
        print(f"Station ID: {station.station_id}, Location: {station.location}")
        for car in station.available_cars:
            if car.car_type == car_type_to_search:
                print(f"   Car ID: {car.car_id}, Price per Hour: ${car.price_per_hour}")

    user = User(1, "Kishor")
    reservation_id = 1
    rental_system.book_car(user, car_type_to_search, 1, 1, 3)
    rental_system.drop_car(user, reservation_id, 1)

    






        

















# from typing import List
# import heapq
# from datetime import datetime, timedelta
# import math

# class Car:
#     def __init__(self, car_id, car_type, price_per_hour):
#         self.car_id = car_id
#         self.car_type = car_type
#         self.price_per_hour = price_per_hour
#         self.is_booked = False

# class Reservation:
#     def __init__(self, reservation_id, user, vehicle, start_time, end_time):
#         self.reservation_id = reservation_id
#         self.user = user
#         self.vehicle = vehicle
#         self.start_time = start_time
#         self.end_time = end_time

# class Bill:
#     def __init__(self, bill_id, reservation, total_amount):
#         self.bill_id = bill_id
#         self.reservation = reservation
#         self.total_amount = total_amount

# class Station:
#     def __init__(self, station_id, location):
#         self.station_id = station_id
#         self.location = location
#         self.available_cars = []
#         self.booked_cars = []

#     def add_car(self, car):
#         self.available_cars.append(car)

#     def book_car(self, car):
#         car.is_booked = True
#         self.available_cars.remove(car)
#         self.booked_cars.append(car)

#     def drop_car(self, car):
#         car.is_booked = False
#         if car in self.booked_cars:
#             self.booked_cars.remove(car)
#             self.available_cars.append(car)
#         else:
#             print("Error: Trying to drop a car that is not booked at this station.")


# class RentalSystem:
#     def __init__(self):
#         self.stations = []

#     def add_station(self, station):
#         self.stations.append(station)

#     @staticmethod
#     def calculate_distance(location1, location2):
#         # Simple Euclidean distance for demonstration purposes
#         x1, y1 = location1
#         x2, y2 = location2
#         return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#     def search_cars(self, car_type, user_location):
#         # Search for available cars and stations
#         available_stations = []
#         for station in self.stations:
#             available_cars = [car for car in station.available_cars if car.car_type == car_type]
#             if available_cars:
#                 price_per_hour = min(car.price_per_hour for car in available_cars)
#                 distance_to_user = self.calculate_distance(station.location, user_location)
#                 heapq.heappush(available_stations, (price_per_hour, distance_to_user, station))

#         result_stations = [station for _, _, station in heapq.nsmallest(len(available_stations), available_stations)]
#         return result_stations

#     def book_car(self, user, car_type, pickup_station, drop_station, duration_hours):
#         pickup_station, drop_station = int(pickup_station), int(drop_station)
#         user_location = self.stations[pickup_station-1].location
#         available_stations = self.search_cars(car_type, user_location)

#         if not available_stations:
#             print("No available cars matching the criteria.")
#             return

#         selected_station = available_stations[0]
#         selected_car = next((car for car in selected_station.available_cars if car.car_type == car_type), None)

#         if not selected_car:
#             print("No available cars of the specified type.")
#             return

#         start_time = datetime.now()
#         end_time = start_time + timedelta(hours=duration_hours)
#         reservation_id = len(user.reservations) + 1
#         reservation = Reservation(reservation_id, user, selected_car, start_time, end_time)
#         bill_id = len(user.bills) + 1
#         total_amount = duration_hours * selected_car.price_per_hour
#         bill = Bill(bill_id, reservation, total_amount)

#         print(f"Booking successful! Reservation ID: {reservation.reservation_id}, "
#               f"Pickup Station: {selected_station.station_id}, Drop Station: {drop_station}, "
#               f"Total Amount: ${bill.total_amount}")

#         # Mark the car as booked
#         selected_station.book_car(selected_car)
#         # Add reservation and bill to user's records
#         user.reservations.append(reservation)
#         user.bills.append(bill)

#     def drop_car(self, user, reservation_id, drop_station):
#         drop_station = int(drop_station)
#         reservation = next((r for r in user.reservations if r.reservation_id == reservation_id), None)

#         if not reservation:
#             print("Invalid reservation ID.")
#             return

#         if reservation.end_time < datetime.now():
#             print("Invalid drop time. Reservation has already ended.")
#             return

#         drop_station_obj = self.stations[drop_station - 1]
#         drop_station_obj.drop_car(reservation.vehicle)

#         print(f"Car dropped successfully at Station {drop_station_obj.station_id}. "
#               f"Reservation ID: {reservation.reservation_id}")

# # Example Usage:
# if __name__ == "__main__":
#     # Create car types
#     suv = Car(1, "SUV", 11)
#     sedan = Car(2, "Sedan", 12)
#     hatchback = Car(3, "Hatchback", 10)
#     bike = Car(4, "Bike", 8)

#     # Create Rental System
#     rental_system = RentalSystem()

#     # Create Stations
#     station1 = Station(1, (0, 0))
#     station1.add_car(suv)
#     station1.add_car(sedan)
#     rental_system.add_station(station1)

#     station2 = Station(2, (1, 1))
#     station2.add_car(sedan)
#     station2.add_car(hatchback)
#     rental_system.add_station(station2)

#     station3 = Station(3, (2, 2))
#     station3.add_car(bike)
#     rental_system.add_station(station3)

#     # User Books a Car
#     class User:
#         def __init__(self, user_id, name):
#             self.user_id = user_id
#             self.name = name
#             self.reservations = []
#             self.bills = []

#     user1 = User(1, "John Doe")
#     rental_system.book_car(user1, "Sedan", 1, 2, 2)

#     # Drop Car
#     reservation_id = 1
#     rental_system.drop_car(user1, reservation_id, 2)











