elevator_id = 1
floor_request_button_id = 1
call_button_id = 1
door_id = 1

#my column class
class Column :

    def __init__(self, cId, status, amountOfFloors, amountOfElevator):
        self.elevator_list = []
        self.call_button_list = []
        self.id = cId
        self.status = status
        self.amount_of_floors = amountOfFloors
        self.amount_of_elevator = amountOfElevator

        self.createCallButtons(amountOfFloors)
        self.createElevators(amountOfElevator)

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

    def createElevators(self, amountOfElevator):
        number_of_elevator = amountOfElevator
        for i in range(number_of_elevator):
            elevator = Elevator(elevator_id, "idle", number_of_elevator, 1)
            
class CallButton:
    def __init__(self, id, status, floor, direction):
        self.button_id = id
        self.button_status = status
        self.button_floor = floor
        self.button_direction = direction


class Elevator:
    def __init__(self, id, status, amountOfFloors, currentFloor):
        self.elevator_id = id
        self.elevator_status = status
        self.amount_of_floor = amountOfFloors
        self.elevator_position = currentFloor
        door = Door(door_id, "close")
        self.floor_request_button = []
        self.floor_request_list = []


class Door:
    def __init__(self, door_id, status):
        pass



C1 = Column(1, "online", 10, 2)
i = 0
# while len(C1.call_button_list) > i:
  
#     print(C1.call_button_list[i].button_floor)
#     print(C1.call_button_list[i].button_direction)
#     i += 1