import time


floor_request_button_id = 1

door_id = 1

#my column class
class Column :

    def __init__(self, id, status, amountOfFloors, amountOfElevator):
        self.elevatorsList = []
        self.callButtonsList = []
        self.ID = id
        self.status = status
        self.amountOfFloors = amountOfFloors
        self.amountOfElevators = amountOfElevator

        self.createCallButtons(amountOfFloors)
        self.createElevators(amountOfElevator, amountOfFloors)
# method for making my call buttons
    def createCallButtons(self, amountOfFloors):
        number_of_floor = amountOfFloors
        button_floor = 1
        call_button_id = 1
        
        for i in range(number_of_floor):
            if button_floor < amountOfFloors:
                call_button = CallButton(call_button_id, "off", button_floor, "up")
                self.callButtonsList.append(call_button)
                call_button_id += 1
            if button_floor > 1:
               call_button = CallButton(call_button_id, "off", button_floor, "down")
               self.callButtonsList.append(call_button)
               call_button_id += 1
            
            button_floor += 1
# method for making my elevators
    def createElevators(self, amountOfElevator, amountOfFloors):
        number_of_elevator = amountOfElevator
        elevator_id = 1
        for i in range(number_of_elevator):
            elevator = Elevator(elevator_id, "idle", amountOfFloors, 1)
            self.elevatorsList.append(elevator)
            elevator_id += 1
    #function that will call elevator to the floor your on
    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.sortFloorList()
        elevator.move()
        elevator.operateDoors()
        return elevator

     #send point to each elevator to find the best one   
    def findElevator(self, floor, direction):
        bestElevatorInformation = {
            "bestElevator": None,
            "bestScore": 5,
            "referenceGap": 10000000}
        

        for elevator in self.elevatorsList:
            if floor == elevator.currentFloor and elevator.status == "idle":
                bestElevatorInformation = self.checkIfElevatorIsBetter(1, elevator, bestElevatorInformation, floor)
            elif floor > elevator.currentFloor and elevator.direction == "up" and direction == elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformation, floor)
            elif floor < elevator.currentFloor and elevator.direction == "down" and direction == elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformation, floor)
            elif elevator.status == "idle":
                bestElevatorInformation = self.checkIfElevatorIsBetter(3, elevator, bestElevatorInformation, floor)
            else:
                bestElevatorInformation = self.checkIfElevatorIsBetter(4, elevator, bestElevatorInformation, floor)

        return bestElevatorInformation["bestElevator"]
    
    #use point to check witch elevator is better
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestElevatorInformation, floor):
        if scoreToCheck < bestElevatorInformation["bestScore"]:
            bestElevatorInformation['bestScore'] = scoreToCheck
            bestElevatorInformation["bestElevator"] = newElevator
            bestElevatorInformation["referenceGap"] = abs(newElevator.currentFloor - floor)

        elif bestElevatorInformation["bestScore"] == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if bestElevatorInformation["referenceGap"] > gap:
                bestElevatorInformation["bestElevator"] = newElevator
                bestElevatorInformation["referenceGap"] = gap
            
        return bestElevatorInformation
   
    def checkRequestList(self):  #only use for senario 3 
        for elevator in self.elevatorsList:
            if elevator.floorRequestList != []:
                elevator.sortFloorList()
                elevator.move()
                elevator.operateDoors()

class CallButton:
    def __init__(self, id, status, floor, direction):
        self.ID = id
        self.status = status
        self.floor = floor
        self.direction = direction


class Elevator(Column):
    def __init__(self, id, status, amountOfFloors, currentFloor):
        self.ID = id
        self.status = status
        self.direction = "null"
        self.amountOfFloors = amountOfFloors
        self.currentFloor = currentFloor
        self.door = Door(door_id, "close")
        self.floorRequestButtonsList = []
        self.floorRequestList = []

        self.createFloorRequestButton(amountOfFloors)
    #making my button in each elevator made
    def createFloorRequestButton(self, amountOfFloors):
        button_floor = 1
        for i in range(amountOfFloors):
            floorRequestButton = FloorRequestButton(i + 1, "off", button_floor)
            self.floorRequestButtonsList.append(floorRequestButton)
            
            button_floor += 1
    #requesting a floor once inside elevator
    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.sortFloorList()
        self.move()
        self.operateDoors()
        
        
    #move the elevator in the right direction
    def move(self):
        while self.floorRequestList != []:
            destination = self.floorRequestList[0]
            self.status = "moving"
            print("elevator", self.ID, " is moving")
            if self.currentFloor < destination:
                self.direction = "up"
                while self.currentFloor < destination:
                    self.currentFloor += 1
                    print("elevator", self.ID, " moving to floor", self.currentFloor,)
            elif self.currentFloor > destination:
                self.direction = "down"
                while self.currentFloor > destination:
                    self.currentFloor -= 1
                    print("elevator", self.ID, " moving to floor", self.currentFloor,)
            self.status = "idle"
            self.direction = "null"
            print("elevato", self.ID,"is stopped" )
            self.floorRequestList.pop(0)
    #sort my floor list
    def sortFloorList(self):
        if self.direction == "up":
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse= True)
    #open door and close after 5 sec
    def operateDoors(self):
        self.door.status = "open"
        print(self.door.status, "door")
        print("please wait 2 seconds")
        time.sleep(2)
        self.door.status = "close"
        print(self.door.status)







class Door:
    def __init__(self, id, status):
        self.ID = id
        self.status = status

class FloorRequestButton:
    def __init__(self, id, status, floor):
        self.ID = id
        self.status = status
        self.floor = floor





def senario1():
    C1 = Column(1, "online", 10, 2)
    C1.elevatorsList[0].currentFloor = 2
    C1.elevatorsList[1].currentFloor = 6
    scenario = C1.requestElevator(3, "up")
    scenario.requestFloor(7)
    
def senario2():
    C1 = Column(1, "online", 10, 2)
    C1.elevatorsList[0].currentFloor = 10
    C1.elevatorsList[1].currentFloor = 3
    scenario = C1.requestElevator(1, "up")
    scenario.requestFloor(6)
    scenario1 = C1.requestElevator(3, "up")
    scenario1.requestFloor(5)
    scenario1 = C1.requestElevator(9, "down")
    scenario1.requestFloor(2)
 

def senario3():
    C1 = Column(1, "online", 10, 2)
    C1.elevatorsList[0].currentFloor = 10
    C1.elevatorsList[1].currentFloor = 3
    C1.elevatorsList[1].status = "moving"
    C1.elevatorsList[1].floorRequestList.append(6)
    scenario = C1.requestElevator(3, "down")
    scenario.requestFloor(2)
    C1.checkRequestList()
    scenario1 = C1.requestElevator(10, "down")
    scenario1.requestFloor(3)

senario2()