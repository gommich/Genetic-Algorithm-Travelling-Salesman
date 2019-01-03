# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import sys


class Location():

    def __init__(self,x,y,name):
        self.name=name
        self.x=x
        self.y=y

    def distance(self, B):
        xDist = abs(self.x-B.x)
        yDist = abs(self.y-B.y)
        distance = np.sqrt((xDist**2)+(yDist**2))
        return distance

    def display(self):
        return "(" + str(self.x) + "," + str(self.y) + ","+str(self.name)+")"

class Route:
    def __init__ (self,route):
        self.distance=0.0
        self.route=route

    def route_length(self):
        path_length=0
        for i in range(1,len(self.route)+1):
            A = self.route[i-1]
            B=""
            if i==len(self.route):
                B=self.route[0]
            else:
                # tack on the start of the route at the end
                B=self.route[i]
            path_length+=A.distance(B)
        self.distance = path_length
        return self.distance



class AnnealingHelper:
    def __init__ (self,initial_temp):
        self.initial_temp = initial_temp

    def cool(self,method,iteration,alpha):
        return {
        'linear': self.initial_temp/(1+alpha*iteration),
        'quadratic': self.initial_temp/(1+alpha*(iteration**2)),
        'exponential': self.initial_temp*(alpha**iteration),
        'logarithmical':self.initial_temp/(1+alpha*math.log(iteration+1))
        }[method]

    def newNeighbour(self,current):
        index1 = random.randint(0,len(current)-1)
        index2 = random.randint(0,len(current)-1)

        temp1 = current[index1]
        temp2 = current[index2]

        current[index1] = temp2
        current[index2] = temp1

        return current

    def accept(self,old,new,temp,k):
        if (new<old):
            return 1

        # put K constant
        ratio = (old-new)/(k*temp)
        return np.exp(ratio)


class SimAnneal:
    def run(self,data, cooling_method, alpha, initial_temperature, ep,k):

        helper = AnnealingHelper(initial_temperature)

        current_temperature = initial_temperature

        #best and current solution
        best_sol = data
        current_sol = data

        best_solution_list=[]
        current_solution_list = []


        i=1
        epsilon=0
        print(data.distance)
        while (current_temperature>1):


            #gen neighbour
            currroute = []
            currroute.extend(current_sol.route)
            neighbour_route = helper.newNeighbour(currroute)
            neighbour = Route(neighbour_route)


            current_dist = current_sol.distance

            neighbour_dist = neighbour.route_length()

            probability = helper.accept(current_dist,neighbour_dist,current_temperature,k)

            if random.random()<probability:
                current_sol = neighbour
                current_solution_list.append(current_sol.distance)


            if neighbour_dist < current_dist:

                best_sol=neighbour
                best_solution_list.append(best_sol.distance)


            old_temperature = current_temperature
            current_temperature = helper.cool(cooling_method,i,alpha)
            epsilon = old_temperature-current_temperature
            if i%100 == 0:
                print("Current Temp:", current_temperature)
            if epsilon < ep:
                break

            i+=1

        print("Best distance",best_sol.distance)
        plt.plot(current_solution_list)
        plt.ylabel('Weight/Distance')
        plt.xlabel('Iteration')
        plt.show()

if __name__ == "__main__":
    
    filename = sys.argv[1]
    cooling_method = sys.argv[2]
    alpha = float(sys.argv[3])
    iterations = int(sys.argv[4])
    epsilon = float(sys.argv[5])
    k = float(sys.argv[6])

    file = open('Data/'+filename,'r')


    arr = []
    for line in file:
         arr.append(line.split())

    #remove text
    arr = arr[6:]
    del arr[-1]

    locations=[]
    for r in arr:
        c = Location(int(r[1]),int(r[2]),r[0])
        locations.append(c)

    random.shuffle(locations)
    initial_route = Route(locations)
    initial_route.route_length()

    s = SimAnneal()
    
    s.run(initial_route,cooling_method,alpha,iterations,epsilon,k)

    
