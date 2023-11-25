import pdb, sys
from enum import Enum
from heapq import heappush, heappop

class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    IDLE = 'IDLE'

class RequestType(Enum):
    EXTERNAL = 'EXTERNAL'
    INTERNAL = 'INTERNAL'

class Button:
    def __init__(self, floor):
        self.floor = floor

class Request:
    def __init__(self, current_floor, desired_floor, request_type, direction):
        self.current_floor = current_floor
        self.desired_floor = desired_floor
        self.request_type = request_type
        self.direction = direction

class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.external_requests = []
        self.up_button = Button(self.floor_number)
        self.down_button = Button(-(self.floor_number))

    def request_elevator(self, desired_floor, direction):
        self.external_requests.append(Request(self.floor_number, desired_floor, RequestType.EXTERNAL, direction))

class Building:
    def __init__(self, number_of_floors) -> None:
        self.number_of_floors = number_of_floors
        self.floors = [Floor(floor_number) for floor_number in range(1, number_of_floors+1)]
        self.elevator = Elevator(0)

    def request_elevator(self, current_floor, desired_floor, direction):
        self.floors[current_floor-1].request_elevator(desired_floor, direction)

class Elevator:

    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
    def __init__(self, current_floor):
        self.current_floor = current_floor
        self.direction = Direction.IDLE
        self.upStops = []
        self.downStops = []

    def run(self):
        pdb.Pdb(stdout=sys.__stdout__).set_trace()
        while self.upStops or self.downStops:
            for floor in building.floors:
                self.processExternalRequests(floor)
            self.processRequests()
    
    def processRequests(self):
        if self.direction in [Direction.UP, Direction.IDLE]:
            self.processUpRequest()
            self.processDownRequest()
        else:
            self.processDownRequest()
            self.processUpRequest()
    
    def processUpRequest(self):
        while self.upStops:
              desired_floor, request = heappop(self.upStops)
              self.current_floor = desired_floor

              if desired_floor == request.current_floor:
                  print(f"Stopping at floor {desired_floor} to pick up people")
              else:
                  print(f"stopping at floor {desired_floor} to let people out")
        
        if self.downStops:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE
    
    def processDownRequest(self):
        while self.downStops:
              desired_floor, request = heappop(self.downStops)
              self.current_floor = desired_floor
              if abs(desired_floor) == request.current_floor:
                 print(f"Stopping at floor {abs(desired_floor)} to pick up people")
              else:
                 print(f"stopping at floor {abs(desired_floor)} to let people out")
              
        if self.upStops:
            self.direction = Direction.UP
        else:
            self.direction = Direction.IDLE
    
    def processExternalRequests(self, floor):
        for external_request in floor.external_requests:
            if external_request.direction == Direction.UP:
                self.sendUpRequest(external_request)
            else:
                self.sendDownRequest(external_request)
        floor.external_requests = []

    def sendUpRequest(self, upRequest):
        if upRequest.request_type == RequestType.EXTERNAL:
            heappush(self.upStops, (upRequest.current_floor, upRequest))
        heappush(self.upStops, (upRequest.desired_floor, upRequest))

    def sendDownRequest(self, downRequest):
        if downRequest.request_type == RequestType.EXTERNAL:
            heappush(self.downStops, (-downRequest.current_floor, downRequest))
        heappush(self.downStops, (-downRequest.desired_floor, downRequest))


if __name__ == '__main__':
   
   num_of_floors = 10
   building = Building(num_of_floors)
   building.request_elevator(4, 8, Direction.UP)
   building.request_elevator(6, 3, Direction.DOWN)

   upRequest1 = Request(building.elevator.current_floor, 5, RequestType.INTERNAL, Direction.UP)
   upRequest2 = Request(building.elevator.current_floor, 3, RequestType.INTERNAL, Direction.UP)
   downRequest1 = Request(building.elevator.current_floor, 1, RequestType.INTERNAL, Direction.DOWN)
   downRequest2 = Request(building.elevator.current_floor, 2, RequestType.INTERNAL, Direction.DOWN)

   building.elevator.sendUpRequest(upRequest1)
   building.elevator.sendUpRequest(upRequest2)
   building.elevator.sendDownRequest(downRequest1)
   building.elevator.sendDownRequest(downRequest2)

   building.elevator.run()
