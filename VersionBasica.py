"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 4
NPED = 2
TIME_CARS_NORTH = 0.5  # a new car enters each 0.5s
TIME_CARS_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (2, 3) # normal 10s, 3s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.patata = Value('i', 0)
        
        #SOUTH = 1
        #NORTH = 0
        
        #Usaremos lo siguientes valores para ver cuantos coches/peatones hay 
        #en el puente
        self.cochesS=Value('i', 0)
        self.cochesN=Value('i', 0)
        self.peat=Value('i', 0)

        self.pasar_surUP=Condition(self.mutex)
        self.pasar_nortUP=Condition(self.mutex)
        self.pasar_peatUP=Condition(self.mutex)
        
        
    def pasar_sur(self):
        return self.peat.value == 0 and self.cochesN.value == 0 
            
    def pasar_nort(self):
        return self.peat.value == 0 and self.cochesS.value == 0 
    
    def pasar_peat(self):
        return self.cochesN.value==0 and self.cochesS.value ==0 
    
    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        
        if direction==1:
            self.pasar_surUP.wait_for(self.pasar_sur)
            self.cochesS.value +=1
            
        if direction == 0:
             self.pasar_nortUP.wait_for(self.pasar_nort)
             self.cochesN.value +=1
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        self.patata.value += 1
        if direction==1:
            self.cochesS.value -=1
            self.pasar_peatUP.notify_all()
            self.pasar_nortUP.notify_all()
        if direction==0:
            self.cochesN.value -=1
            self.pasar_peatUP.notify_all()
            self.pasar_surUP.notify_all()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.pasar_peatUP.wait_for(self.pasar_peat)
        self.peat.value +=1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.peat.value -=1
        if self.peat.value == 0:
            self.pasar_surUP.notify_all()    
            self.pasar_nortUP.notify_all()
        self.mutex.release()

    def __repr__(self) -> str:
        return f'Monitor: {self.patata.value}'

def delay_car_north() -> None:
    a=random.normalvariate(TIME_IN_BRIDGE_CARS[0], TIME_IN_BRIDGE_CARS[1])
    if a<0:
        a=0
    time.sleep(a)

def delay_car_south() -> None:
    a=random.normalvariate(TIME_IN_BRIDGE_CARS[0], TIME_IN_BRIDGE_CARS[1])
    if a<0:
        a=0
    time.sleep(a)

def delay_pedestrian() -> None:
    a=random.normalvariate(TIME_IN_BRIDGE_PEDESTRIAN[0], TIME_IN_BRIDGE_PEDESTRIAN[1])
    if a<0:
        a=0
    time.sleep(a)

def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")



def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/time_cars))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars_north = Process(target=gen_cars, args=(NORTH, TIME_CARS_NORTH, monitor))
    gcars_south = Process(target=gen_cars, args=(SOUTH, TIME_CARS_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_north.start()
    gcars_south.start()
    gped.start()
    gcars_north.join()
    gcars_south.join()
    gped.join()


if __name__ == '__main__':
    main()
