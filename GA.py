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
        x_d = math.fabs(self.x-B.x)
        y_d = math.fabs(self.y-B.y)
        distance = np.sqrt((x_d*x_d)+(y_d*y_d))
        return distance

class Individual:
    def __init__ (self,route):
        self.fitness=0.0
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

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1/self.route_length()
        return self.fitness



class GeneticAlgorithm():


    #prefer k to be large
    def tournamentSelection(self,k,Individuals):
        best_parent = ""
        for i in range (k):
            index=random.randint(0,len(Individuals)-1)
            individual=Individuals[index]
            if (best_parent == "") or individual.getFitness()>best_parent.getFitness():
                best_parent = individual

        return best_parent


    #ordered crossover
    #Rate = crossover rate: generally 0.70>
    def ordered_crossover(self,P1,P2,rate):
        length = len(P1.route)
        child_subset_1 = []
        child_subset_2 = []
        if (random.random()<rate):
            index1 = random.randint(0,length-1)
            index2 = random.randint(0,length-1)

            A = min(index1,index2)
            B = max(index1,index2)

            for i in range(A, B):
                child_subset_1.append(P1.route[i])

            for p in P2.route:
                if p not in child_subset_1:
                    child_subset_2.append(p)

            child = child_subset_1 + child_subset_2
            Child = Individual(child)

            return Child
            """
            This was my original crossover function crossover function didn't work
            as it created individuals with repeated cities.


            length = len(Parent1.route)
            point=random.randint(0,length-1)

            subset1 = Parent1.route[0:point]
            subset2 = Parent2.route[point:length]
            subset3 = Parent1.route[point:length]
            subset4 = Parent2.route[0:point]

            child1route = subset1 + subset2
            child2route = subset4 + subset3

            Child1 = Individual(child1route)
            Child2 = Individual(child2route)
            if(length!=len(child1route) or length!=len(child2route)):

                raise ValueError('Length of parent:',length, "length of child:",len(child1route),len(child2route))

            return Child1, Child2
            """
        return None


    #simple mutation
    #Seems best to give each gene a (rate%) chance of mutation
    def mutate (self,individual,rate):
        for index1 in range(len(individual.route)):
            if (random.random()<rate):
                index2 = random.randint(0,len(individual.route)-1)

                temp1 = individual.route[index1]
                temp2 = individual.route[index2]

                individual.route[index1] = temp2
                individual.route[index2] = temp1

                return individual
        return individual

    def allRouteFitness(self,population):
        allFitness = []
        for i in population:
            allFitness.append(i.getFitness())
        return allFitness

    def allRouteDistances(self,population):
        allDistances=[]
        for i in population:
            allDistances.append(i.route_length())
        return allDistances


    def run(self,population,generations,cross_rate,mut_rate,k):

        print("Results:")
        n = len(population)
        Parents = population
        History=[]
        History.append(min(self.allRouteDistances(Parents)))

        for i in range(generations):
            Children = []
            while len(Children)<n:

                Parent1 = self.tournamentSelection(k,Parents)
                Parent2 = self.tournamentSelection(k,Parents)
                Child = self.ordered_crossover(Parent1, Parent2, cross_rate)
                if Child != None:
                    Child = self.mutate(Child,mut_rate)
                    Child.route_length()
                    Children.append(Child)

            Parents = Children

            fitness_results = self.allRouteFitness(Parents)
            distance_results = self.allRouteDistances(Parents)
            print("Generation",i)
            print("Best Fitness:",max(fitness_results))
            print("Best Distance:",min(distance_results))
            History.append(min(distance_results))

            print("----------------")
        plt.plot(History)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()

if __name__ == "__main__":

    filename = sys.argv[1]
    population_size = int(sys.argv[2])
    generations = int(sys.argv[3])
    crossover_rate = float(sys.argv[4])
    mutation_rate = float(sys.argv[5])
    tournament_size = int(sys.argv[6])



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

    routeList=[]
    for i in range(population_size):
        random_route = random.sample(locations, len(locations))
        random_route = Individual(random_route)
        random_route.route_length()
        routeList.append(random_route)

    GA = GeneticAlgorithm()


    GA.run(routeList,generations, crossover_rate,mutation_rate,tournament_size)
