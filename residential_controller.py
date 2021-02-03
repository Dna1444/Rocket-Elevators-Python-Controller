import time

elevator_id = 1
floor_request_button_id = 1
call_button_id = 1
door_id = 1

#my column class
class Column :

    def __init__(self, id, status, amountOfFloors, amountOfElevator):
        self.elevator_list = []
        self.call_button_list = []
        self.id = id
        self.status = status
        self.amount_of_floors = amountOfFloors
        self.amount_of_elevator = amountOfElevator

        self.createCallButtons(amountOfFloors)
        self.createElevators(amountOfElevator, amountOfFloors)
# method for making my call buttons
    def createCallButtons(self, amountOfFloors):
        number_of_floor = amountOfFloors
        button_floor = 1
        
        for i in range(number_of_floor):
            if button_floor < amountOfFloors:
                call_button = CallButton(call_button_id, "off", button_floor, "up")
                self.call_button_list.append(call_button)
                call_button_id + 1
            if button_floor > 1:
               call_button = CallButton(call_button_id, "off", button_floor, "down")
               self.call_button_list.append(call_button)
               call_button_id + 1
            
            button_floor += 1
# method for making my elevators
    def createElevators(self, amountOfElevator, amountOfFloors):
        number_of_elevator = amountOfElevator
        for i in range(number_of_elevator):
            elevator = Elevator(elevator_id, "idle", amountOfFloors, 1)
            self.elevator_list.append(elevator)
            elevator_id + 1

    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floor_request_list.append(floor)
        elevator.sortFloorList()
        elevator.move()
        elevator.operateDoors()
        return elevator

        
    def findElevator(self, floor, direction):
        bestElevatorInformation = {
            "bestElevator": None,
            "bestScore": 5,
            "referenceGap": 10000000}
        

        for elevator in self.elevator_list:
            if floor == elevator.position and elevator.status == "idle":
                bestElevatorInformation = self.checkIfElevatorIsBetter(1, elevator, bestElevatorInformation, floor)
            elif floor > elevator.position and elevator.direction == "up" and direction == elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformation, floor)
            elif floor < elevator.position and elevator.direction == "down" and direction == elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformation, floor)
            elif elevator.status == "idle":
                bestElevatorInformation = self.checkIfElevatorIsBetter(3, elevator, bestElevatorInformation, floor)
            else:
                bestElevatorInformation = self.checkIfElevatorIsBetter(4, elevator, bestElevatorInformation, floor)

        return bestElevatorInformation["bestElevator"]
    

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestElevatorInformation, floor):
        if scoreToCheck < bestElevatorInformation["bestScore"]:
            bestElevatorInformation['bestScore'] = scoreToCheck
            bestElevatorInformation["bestElevator"] = newElevator
            bestElevatorInformation["referenceGap"] = abs(newElevator.position - floor)

        elif bestElevatorInformation["bestScore"] == scoreToCheck:
            gap = abs(newElevator.position - floor)
            if bestElevatorInformation["referenceGap"] > gap:
                bestElevatorInformation["bestElevator"] = newElevator
                bestElevatorInformation["referenceGap"] = gap
            
        return bestElevatorInformation
   
    def checkRequestList(self):  #only use for senario 3 
        for elevator in self.elevator_list:
            if elevator.floor_request_list != []:
                elevator.sortFloorList()
                elevator.move()
                elevator.operateDoors()

class CallButton:
    def __init__(self, id, status, floor, direction):
        self.id = id
        self.status = status
        self.floor = floor
        self.direction = direction


class Elevator(Column):
    def __init__(self, id, status, amountOfFloors, currentFloor):
        self.id = id
        self.status = status
        self.direction = "null"
        self.amount_of_floor = amountOfFloors
        self.position = currentFloor
        self.door = Door(door_id, "close")
        self.floor_request_button = []
        self.floor_request_list = []

        self.createFloorRequestButton(amountOfFloors)
    #making my button in each elevator made
    def createFloorRequestButton(self, amountOfFloors):
        button_floor = 1
        for i in range(amountOfFloors):
            floorRequestButton = FloorRequestButton(i + 1, "off", button_floor)
            self.floor_request_button.append(floorRequestButton)
            
            button_floor += 1
    #requesting a floor once inside elevator
    def requestFloor(self, floor):
        self.floor_request_list.append(floor)
        self.sortFloorList()
        self.move()
        self.operateDoors()
        
        
    #move the elevator in the right direction
    def move(self):
        while self.floor_request_list != []:
            destination = self.floor_request_list[0]
            self.status = "moving"
            print("elevator", self.id, " is moving")
            if self.position < destination:
                self.direction = "up"
                while self.position < destination:
                    self.position += 1
                    print("elevator", self.id, " moving to floor", self.position,)
            elif self.position > destination:
                self.direction = "down"
                while self.position > destination:
                    self.position -= 1
                    print("elevator", self.id, " moving to floor", self.position,)
            self.status = "idle"
            self.direction = "null"
            print("elevato", self.id,"is stopped" )
            self.floor_request_list.pop(0)
    #sort my floor list
    def sortFloorList(self):
        if self.direction == "up":
            self.floor_request_list.sort()
        else:
            self.floor_request_list.sort(reverse= True)
    #open door and close after 5 sec
    def operateDoors(self):
        self.door.status = "open"
        print(self.door.status, "door")
        print("please wait 5 seconds")
        time.sleep(5)
        self.door.status = "close"
        print(self.door.status)







class Door:
    def __init__(self, id, status):
        self.id = id
        self.status = status

class FloorRequestButton:
    def __init__(self, id, status, floor):
        self.id = id
        self.status = status
        self.floor = floor





def senario1():
    C1 = Column(1, "online", 10, 2)
    C1.elevator_list[0].position = 2
    C1.elevator_list[1].position = 6
    scenario = C1.requestElevator(3, "up")
    scenario.requestFloor(7)
    
def senario2():
    C1 = Column(1, "online", 10, 2)
    C1.elevator_list[0].position = 10
    C1.elevator_list[1].position = 3
    scenario = C1.requestElevator(1, "up")
    scenario.requestFloor(6)
    scenario1 = C1.requestElevator(3, "up")
    scenario1.requestFloor(5)
    scenario1 = C1.requestElevator(9, "down")
    scenario1.requestFloor(2)
 

def senario3():
    C1 = Column(1, "online", 10, 2)
    C1.elevator_list[0].position = 10
    C1.elevator_list[1].position = 3
    C1.elevator_list[1].status = "moving"
    C1.elevator_list[1].floor_request_list.append(6)
    scenario = C1.requestElevator(3, "down")
    scenario.requestFloor(2)
    C1.checkRequestList()
    scenario1 = C1.requestElevator(10, "down")
    scenario1.requestFloor(3)


senario1()


