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

def calculate_dist(start_point, end_point):
    return abs(start_point[0] - end_point[0]) + abs(start_point[1] - end_point[1])

def read_input(input_file):
    with open ('input/' + input_file + '.in', 'r') as file:
        first_line = [int(val) for val in file.readline().split()]
        row_nb, col_nb, car_nb, ride_nb, bonus_nb, time_nb = first_line

        ride_list = []
        for i in range(ride_nb):
            ride = [int(val) for val in file.readline().split()]
            start_point_x, start_point_y, end_point_x, end_point_y, start_time, end_time = ride
            ride_list.append(Ride(i, start_point_x, start_point_y, end_point_x, end_point_y, start_time, end_time))

        ride_list.sort(key=lambda x: x.start_time)

        car_list = []
        for i in range(car_nb):
            car_list.append(Car(i))

        my_game = Game(row_nb, col_nb, car_nb, ride_nb, bonus_nb, time_nb, ride_list, car_list)

    return my_game

def write_output(input_file, my_game):
    with open('output/' + input_file + '.out', 'w+') as file:
        for my_car in my_game.car_list:
            ride_nb = str(len(my_car.course_list))
            file.write(ride_nb)
            for my_course in my_car.course_list:
                file.write(' ' + str(my_course.number))
            file.write('\n')

    with open("data.save", 'wb+') as file:
        pickle.dump(my_game, file, pickle.HIGHEST_PROTOCOL)

def print_all_rides(my_game):
    for my_ride in my_game.ride_list:
        print(my_ride)

def print_all_cars(my_game):
    for my_car in my_game.car_list:
        print(my_car)

def calculate_score(my_game):
    course_done, course_dropped, course_not_possible, course_early, course_early_possible, score = 0, 0, 0, 0, 0, 0
    bonus = my_game.bonus_nb

    for my_ride in my_game.ride_list:
        if my_ride.affected:
            score += my_ride.distance
            course_done += 1
        else:
            course_dropped += 1
        if my_ride.early_pick:
            score += bonus
            course_early += 1
        if not my_ride.possible:
            course_not_possible += 1
        if my_ride.early_possible:
            course_early_possible += 1

    print('Done: {} Early: {} Dropped: {} Early possible: {} Not possible: {}'.format(course_done, course_early, course_dropped, course_early_possible, course_not_possible))
    print('Score: {}'.format(score))

    return score

def affect_car_ride(my_game, car_nb, ride_nb):
    my_game.ride_list[ride_nb].set_ride(my_game.car_list[car_nb])
    my_game.car_list[car_nb].set_ride(my_game.ride_list[ride_nb])

def score_ride(my_game, my_car, my_ride):
    on_ride_end_time = my_car.calc_end_ride_time(my_ride)
    on_ride_time = my_car.calc_on_ride_time(my_ride)
    ride_start_time = my_ride.start_time
    ride_dist = my_ride.distance
    time_lost = my_car.calc_lost_time(my_ride) 

    score = time_lost * 5

    if ride_start_time >= on_ride_time:
        is_early = 1
    else:
        is_early = 0

    if on_ride_end_time <= my_game.time_nb * 0.98:
        score += my_ride.score * 10

    score -= is_early * my_game.bonus_nb * my_game.bonus_nb * my_game.bonus_nb
 
    return score

def find_best_ride(my_game, car_nb):
    ride_score = []

    for i in range(my_game.ride_nb):
        if my_game.ride_list[i].affected or not my_game.ride_list[i].possible:
            continue

        score = score_ride(my_game, my_game.car_list[car_nb], my_game.ride_list[i])
        ride_score.append([i, score])

    ride_score.sort(key=lambda x: x[1])

    for nb, score in ride_score:
        if my_game.ride_list[nb].check_ride(my_game.car_list[car_nb]):
            return nb
        
    return None

def start_rides(my_game):
    still_affected = True

    while still_affected:
        still_affected = False

        for car_nb in range(my_game.car_nb):
            if not my_game.car_list[car_nb].available:
                continue
            ride_nb = find_best_ride(my_game, car_nb)
            if ride_nb is not None:
                still_affected = True
                affect_car_ride(my_game, car_nb, ride_nb)
            else:
                my_game.car_list[car_nb].disable_car()

def score_all_ride(my_game):
    rides_nb = 0
    x_sum = 0
    y_sum = 0
    for i in range(my_game.ride_nb):
        if my_game.ride_list[i].possible:
            rides_nb += 1
            x_sum += my_game.ride_list[i].start_point[0]
            y_sum += my_game.ride_list[i].start_point[1]
            
    x_sum //= rides_nb
    y_sum //= rides_nb

    center = [x_sum, y_sum]

    for i in range(my_game.ride_nb):
        if my_game.ride_list[i].possible:
            my_game.ride_list[i].score = calculate_dist(my_game.ride_list[i].end_point, center)

def result(input_file):
    print('###  ' + input_file + '  ###')
    my_game = read_input(input_file)

    print(my_game)

    score_all_ride(my_game)
    start_rides(my_game)
    write_output(input_file, my_game)
    
    score = calculate_score(my_game)
    print()
    return score


start=datetime.now()
score = 0
score += result("a_example")
score += result("b_should_be_easy")
score += result("c_no_hurry")
score += result("d_metropolis")
score += result("e_high_bonus")

print('Total score: ' + str(score))
print('Total time: ' + str(datetime.now()-start))
