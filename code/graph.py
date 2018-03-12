from math import log
from datetime import datetime
import pickle

class Ride():
    def __init__(self, number, start_point_x, start_point_y, end_point_x, end_point_y, start_time, end_time):
        self.number = number
        self.start_point = [start_point_x, start_point_y]
        self.end_point = [end_point_x, end_point_y]
        self.start_time = start_time
        self.end_time = end_time
        self.distance = calculate_dist(self.start_point, self.end_point)
        self.early_end = self.start_time + self.distance
        self.picked_time = 0
        self.arrival = 0
        self.affected = False
        self.early_pick = False
        self.score = 0
        self.possible = self.check_possible()
        self.early_possible = self.check_early_possible()
        self.later_start = self.end_time - self.distance

    def check_possible(self):
        if self.end_time < calculate_dist([0, 0], self.start_point) + self.distance:
            return False
        else:
            return True

    def check_early_possible(self):
        if self.start_time < calculate_dist([0, 0], self.start_point):
            return False
        else:
            return True

    def set_ride(self, my_car):
        self.affected = True
        car_on_start = my_car.calc_start_ride_time(self)
        car_on_end = my_car.calc_end_ride_time(self)
        self.picked_time = car_on_start
        self.arrival = car_on_end
        if self.picked_time <= self.start_time:
            self.early_pick = True

    def check_ride(self, my_car):
        end_ride_time = my_car.calc_end_ride_time(self)
        if end_ride_time <= self.end_time:
            return True
        return False

    def score_b_ride(self, my_ride):
        dist = calculate_dist(self.end_point, my_ride.start_point)
        return dist

    def __str__(self):
        return "Ride: {}\nStart pos: {} End pos: {} Distance: {}\nStart time: {} End time: {} Pick : {} Arrival: {}\nAffected: {} Early: {} Possible: {} Early Possible: {}\n".format(self.number, self.start_point, self.end_point, self.distance, self.start_time, self.end_time, self.picked_time, self.arrival, self.affected, self.early_pick, self.possible, self.early_possible)

class Car():
    def __init__(self, number):
        self.number = number
        self.pos = [0, 0]
        self.course_list = []
        self.avail_time = 0
        self.next_end_pos = [0, 0]
        self.available = True
        self.loose_time = 0

    def set_ride(self, my_ride):
        self.loose_time += self.calc_start_ride_time(my_ride) - self.avail_time
        self.avail_time = self.calc_end_ride_time(my_ride)
        self.next_end_pos = my_ride.end_point
        self.course_list.append(my_ride)

    def calc_end_ride_time(self, my_ride):
        ride_start_time = self.calc_start_ride_time(my_ride)
        ride_done_time = ride_start_time + my_ride.distance
        return ride_done_time

    def calc_start_ride_time(self, my_ride):
        car_to_start = self.calc_on_ride_time(my_ride)
        ride_start_time = max(car_to_start, my_ride.start_time)
        return ride_start_time

    def calc_lost_time(self, my_ride):
        car_to_start = self.calc_on_ride_dist(my_ride)
        wait_time = my_ride.start_time - self.calc_on_ride_time(my_ride)
        return max(car_to_start, wait_time)

    def calc_on_ride_time(self, my_ride):
        car_to_start = self.calc_on_ride_dist(my_ride) + self.avail_time
        return car_to_start

    def calc_on_ride_dist(self, my_ride):
        car_to_start = calculate_dist(self.next_end_pos, my_ride.start_point)
        return car_to_start   

    def disable_car(self):
        self.available = False

    def __str__(self):
        return "Car: {} Loose time: {}\n".format(self.number, self.loose_time)

class Game():
    def __init__(self, row_nb, col_nb, car_nb, ride_nb, bonus_nb, time_nb, ride_list, car_list):
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.car_nb = car_nb
        self.ride_nb = ride_nb
        self.bonus_nb = bonus_nb
        self.time_nb = time_nb
        self.ride_list = ride_list
        self.car_list = car_list

    def __str__(self):
        return "Row: {} Col: {} Car nb: {} Ride nb: {} Bonus price: {} Time: {}\n".format(self.row_nb, self.col_nb, self.car_nb, self.ride_nb, self.bonus_nb, self.time_nb)


def load_data():
    with open('data.save', 'rb') as input:
        my_game = pickle.load(input)
    return my_game

def print_all_rides(my_game):
    for my_ride in my_game.ride_list:
        print(my_ride)

def print_all_cars(my_game):
    for my_car in my_game.car_list:
        print(my_car)

def create_graph(my_game):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.lines as mlines
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(1)
    ax = Axes3D(fig)


    plt.title('Position and end time of cars')
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    ax.set_zlabel('Time')

    xc = [my_car.next_end_pos[0] for my_car in my_game.car_list]
    yc = [my_car.next_end_pos[1] for my_car in my_game.car_list]
    zc = [my_car.avail_time for my_car in my_game.car_list]

    ax.scatter(xc, yc, zc)
 

    plt.figure(2)  
    plt.title('Rides not done') 
    plt.xlabel('X position')
    plt.ylabel('Y position')
    xs = [my_ride.start_point[0] for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]
    ys = [my_ride.start_point[1] for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]

    xe = [my_ride.end_point[0] for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]
    ye = [my_ride.end_point[1] for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]

    plt.scatter(xs, ys, marker='o', color='green', zorder=4)
    plt.scatter(xe, ye, marker='o', color='red', zorder=3)
    plt.scatter(xc, yc, marker='o', color='blue', zorder=5)
    plt.plot([xs, xe], [ys, ye], color='green', zorder=2)


    plt.figure(3)   
    plt.title('Time lost by car')
    plt.xlabel('Car nb')
    plt.ylabel('Time lost')
    ic = [my_car.number for my_car in my_game.car_list]
    lc = [my_car.loose_time for my_car in my_game.car_list]

    plt.scatter(ic, lc, marker='o', color='blue', zorder=4)

    fig = plt.figure(4)
    ax = Axes3D(fig)

    plt.title('End position and end time of courses not done')
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    ax.set_zlabel('Time')

    xc = [my_ride.end_point[0] for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]
    yc = [my_ride.end_point[1] for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]
    zc = [my_ride.end_time for my_ride in my_game.ride_list if not my_ride.affected and my_ride.possible]

    ax.scatter(xc, yc, zc)

    plt.show()


def result():
    my_game = load_data()
    # print_all_rides(my_game)
    create_graph(my_game)
    #print(my_game)

result()
