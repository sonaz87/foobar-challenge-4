# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:54:32 2021

@author: lor


Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! 
Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, 
so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: 
    its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. 
You also know that if a beam hits a corner, it will bounce back in exactly the same direction. 
And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) 
that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, 
an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions 
that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. 
You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that 
[0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given 
as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], 
your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, 
you could shoot in seven different directions to hit the elite trainer 
(given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. 
As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, 
the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer 
with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting 
the elite trainer with a total shot distance of sqrt(5).

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9



"""

def solution(dimensions, your_position, trainer_position, distance):
    from math import atan2

    def calculate_distance_sq(p1):
        return p1[0]**2 + p1[1]**2
    
    
    def mirror(dimensions, your_position, trainer_position, distance):
        x_dim = int(2 * (distance // dimensions[0] )) + 1
        y_dim = int(2 * (distance // dimensions[1] )) + 1
        
        
        def generate_distances(dimension, vector, multiplier):
            count = multiplier
            grid = [vector]
            to_left, to_right = -vector, dimension-vector
            while count > 0:
                left, right = grid[0], grid[-1]
                left += to_left * 2
                right += to_right * 2
                grid = [left] + grid + [right]
                to_left, to_right = -to_right, -to_left
                count -= 1
                
            return grid
        
        
        def generate_all(x_vector, y_vector):
            grid = dict()
            for j in range(len(y_vector)):
                for i in range(len(x_vector)):
                    grid[-x_dim + i, - y_dim +j] = [x_vector[i],y_vector[j]]
            return grid
                    
        
        my_x = generate_distances(dimensions[0], your_position[0], x_dim)
        my_y = generate_distances(dimensions[1], your_position[1], y_dim)
        tra_x = generate_distances(dimensions[0], trainer_position[0], x_dim)
        tra_y = generate_distances(dimensions[1], trainer_position[1], y_dim)

        
        my_pos = generate_all(my_x, my_y)
        trainer_pos = generate_all(tra_x, tra_y)
        
        
        
        return my_pos, trainer_pos


    def move_myself_to_O(your_position, my_pos, trainer_pos, distance):
        for i in my_pos:
            my_pos[i] = [my_pos[i][0] - your_position[0], my_pos[i][1] - your_position[1]]

            
        for i in trainer_pos:
            trainer_pos[i] = [trainer_pos[i][0] - your_position[0], trainer_pos[i][1] - your_position[1]]


        return my_pos, trainer_pos
    
    def angle(p):
        return format(atan2(p[0], p[1]), ".32f")
            
    def count_valid_shots(my_pos, cpt_pos, distance):
        distance_sq = distance ** 2
        counter = 0
        checked_angles = dict()
        
        checking_order = list()


        
        x_min = 100000000000
        x_max = -100000000000
        y_min = 100000000000
        y_max = -100000000000
        
        for element in my_pos:
            if element[0] < x_min:
                x_min = element[0]
            if element[0] > x_max:
                x_max = element[0]
            if element[1] < y_min:
                y_min = element[1]
            if element[1] > y_max:
                y_max = element[1]
                

        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max +1 ):
                checking_order.append((i,j))

        checking_order.sort(key = lambda x: calculate_distance_sq(x))

        for i in checking_order:
            checked_angles[angle(my_pos[i])] = True
            if calculate_distance_sq(trainer_pos[i]) > distance_sq:
                continue
            elif angle(trainer_pos[i]) not in checked_angles:
                counter +=1
                checked_angles[angle(trainer_pos[i])] = True
                
                

        return counter
        

    my_pos, trainer_pos = mirror(dimensions, your_position, trainer_position, distance)
    my_pos, trainer_pos = move_myself_to_O(your_position, my_pos, trainer_pos, distance)
    result = count_valid_shots(my_pos, trainer_pos, distance)
    return result
    
                
            
# result = solution([3,2], [1,1], [2,1], 4)
from time import time
start = time()
result = solution([42,59], [34,44], [6,34], 5000)
print("runtime: ", time()-start)

print(result)