from enum import Enum
class Entrance:
    def generate_ticket(self, vehicle, parking_lot):
        if parking_lot.isFull():
            print("Parking is Full!")
            return None
        
        spot_number = parking_lot.get_available_spot(vehicle.vehicleType)
        if spot_number is not None:
            ticket = Ticket(vehicle, spot_number)
            parking_lot.occupy_spot(spot_number, vehicle)
            print(f"Ticket generated for Vehicle {vehicle.vehicle_number}. Spot Number: {spot_number}")
            return ticket

class Exit:

    def process_ticket(self, ticket, parking_lot):
        spot_number = ticket.spot_number
        if parking_lot.is_valid_spot(spot_number):
            exiting_vehicle = parking_lot.get_vehicle_at_spot(spot_number)
            parking_lot.vacate_spot(spot_number)
            print(f"Vehicle {exiting_vehicle.vehicle_number} exited from Spot Number: {spot_number}")
        else:
            print("Invalid ticket. Unable to process exit.")

class Ticket:
    def __init__(self, vehicle, spot):
        self.vehicle = vehicle
        self.spot_number = spot

class Vehicle:
    def __init__(self, vehicle_number, color, model, vehicleType):
        self.vehicle_number = vehicle_number
        self.color = color
        self.model = model
        self.vehicleType = vehicleType

class VehicleType(Enum):
    Four_Wheeler = 'FourWheeler'
    Two_Wheeler = 'TwoWheeler'

class Payment:
    def __init__(self, ticket):
        self.ticket = ticket
        self.status = 'Pending'
    
    def process_payment(self):
        self.status = 'Success'

class ParkingSpot:

    def __init__(self):
        self.vehicle = None
    
    def occupy(self, vehicle):
        self.vehicle = vehicle

    def vacate(self):
        self.vehicle = None

class Two_Wheeler_Spot(ParkingSpot):
    pass

class Four_Wheeler_Spot(ParkingSpot):
    pass

class ParkingLot:
    def __init__(self, total_two_wheeler_spots, total_four_wheeler_spots):
        self.available_two_wheeler_spots = total_two_wheeler_spots
        self.available_four_wheeler_spots = total_four_wheeler_spots
        self.four_wheeler_spots = [Four_Wheeler_Spot() for _ in range(self.available_four_wheeler_spots)]
        self.two_wheeler_spots = [Two_Wheeler_Spot() for _ in range(self.available_two_wheeler_spots)]

    def isFull(self):
        return self.available_two_wheeler_spots == 0 and self.available_four_wheeler_spots == 0

    def get_available_spot(self, vehicle_type):
        if vehicle_type == 'FourWheeler':
            for i, spot in enumerate(self.four_wheeler_spots):
                if spot.vehicle is None:
                    return i+1
        if vehicle_type == 'TwoWheeler':
            for i, spot in enumerate(self.two_wheeler_spots):
                if spot.vehicle is None:
                    return i+1
        return None

    def vacate_spot(self, spot_number):
        if 1 <= spot_number <= len(self.four_wheeler_spots) and self.four_wheeler_spots[spot_number-1].vehicle is not None:
            self.four_wheeler_spots[spot_number-1].vacate()
            self.available_four_wheeler_spots += 1
            return True
        if 1 <= spot_number <= len(self.two_wheeler_spots) and self.two_wheeler_spots[spot_number-1].vehicle is not None:
            self.two_wheeler_spots[spot_number-1].vacate()
            self.available_two_wheeler_spots += 1
            return True
        return False

    def occupy_spot(self, spot_number, vehicle):

        if vehicle.vehicleType == 'FourWheeler':
            if 1 <= spot_number <= len(self.four_wheeler_spots) and self.four_wheeler_spots[spot_number-1].vehicle is None:
                self.four_wheeler_spots[spot_number-1].occupy(vehicle)
                self.available_four_wheeler_spots += 1
                return True
        if vehicle.vehicleType == 'TwoWheeler':
            if 1 <= spot_number <= len(self.two_wheeler_spots) and self.two_wheeler_spots[spot_number-1].vehicle is None:
                self.two_wheeler_spots[spot_number-1].occupy(vehicle)
                self.available_two_wheeler_spots += 1
                return True
        return False

    def get_vehicle_at_spot(self, spot_number):

        if 1 <= spot_number <= len(self.four_wheeler_spots) and self.four_wheeler_spots[spot_number-1].vehicle is not None:
            return self.four_wheeler_spots[spot_number-1].vehicle
        if 1 <= spot_number <= len(self.two_wheeler_spots) and self.two_wheeler_spots[spot_number-1].vehicle is not None:
            return self.two_wheeler_spots[spot_number-1].vehicle  
        return None
    
    def is_valid_spot(self, spot_number):
        if 1 <= spot_number <= len(self.four_wheeler_spots):
            return self.four_wheeler_spots[spot_number-1].vehicle is not None
        if 1 <= spot_number <= len(self.two_wheeler_spots):
            return self.two_wheeler_spots[spot_number-1].vehicle is not None
        return False

if __name__ == '__main__':
    parking_lot = ParkingLot(total_four_wheeler_spots=5, total_two_wheeler_spots=5)
    entrance_gate = Entrance()
    exit_gate = Exit()

    vehicle1 = Vehicle('123', 'Red', 'hyundai', 'FourWheeler')
    vehicle2 = Vehicle('124', 'Red', 'hyundai', 'FourWheeler')
    vehicle3 = Vehicle('125', 'Red', 'hyundai', 'TwoWheeler')
    vehicle4 = Vehicle('126', 'Red', 'hyundai', 'FourWheeler')
    
    ticket1 = entrance_gate.generate_ticket(vehicle1, parking_lot)
    ticket2 = entrance_gate.generate_ticket(vehicle2, parking_lot)
    ticket3 = entrance_gate.generate_ticket(vehicle3, parking_lot)
    ticket4 = entrance_gate.generate_ticket(vehicle4, parking_lot)
    
    exit_gate.process_ticket(ticket1, parking_lot)
    exit_gate.process_ticket(ticket3, parking_lot)