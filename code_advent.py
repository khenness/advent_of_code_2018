import difflib
from fuzzywuzzy import fuzz
import datetime
import networkx as nx
import random
from collections import deque, defaultdict
import collections
import re
import sys
DEBUG = 1

def print_debug(msg):
    if DEBUG == 2 or DEBUG == 1:
        print(msg)


def read_file_into_list(filepath):
    # Read file into list of lines
    # For bigger files look into using yield and doing chunking, even just for practice
    # If the file is line-based, the file object is already a lazy generator of lines:
    # https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    with open(filepath) as fp:
        line_list = []
        line = fp.readline()
        while line:
            #print_debug(line.strip())
            line_list.append(line.strip())
            line = fp.readline()

    return line_list

def read_file_into_list_v2(filepath):
    # Read file into list of lines
    # For bigger files look into using yield and doing chunking, even just for practice
    # If the file is line-based, the file object is already a lazy generator of lines:
    # https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
    with open(filepath) as fp:
        line_list = []
        line = fp.readline()
        while line:
            #print_debug(line.strip())
            line_list.append(line.replace("\n", ""))
            line = fp.readline()

    return line_list

def parse_problem_1_string(input_string):
    return_tuple = (input_string[0], int(input_string[1:]))
    #print_debug("Found tuple - {}".format(return_tuple))
    return return_tuple

#https://adventofcode.com/2018/day/1
def day_1_part_1():

    lines = read_file_into_list("problem_1_input.txt")
    
    #print_debug("Problem 1 input data is:")
    #print_debug(lines)

    starting_value = 0

    running_total = starting_value
    for line in lines:
        mytuple = parse_problem_1_string(line)
        if mytuple[0] == '+':
            new_running_total = running_total + mytuple[1]
            #print_debug("I had the value {} and added on {} to get {}".format(running_total, mytuple[1], new_running_total))
            running_total = new_running_total
        elif mytuple[0] =='-':
            new_running_total = running_total - mytuple[1]
            #print_debug("I had the value {} and subtracted {} to get {}".format(running_total, mytuple[1], new_running_total))
            running_total = new_running_total
        else:
            raise ValueError("Found invalid input")

    answer = running_total

    answer_string = "For starting_value of {}, the answer is {}".format(starting_value, answer)



    return answer_string


def check_seen(running_total, seen_frequencies):


    times_seen = seen_frequencies.get(running_total, 0)
    times_seen += 1
    seen_frequencies[running_total] = times_seen

    if times_seen == 2:
        #print_debug("Found the answer it is {}".format(running_total))
        #print_debug("The seen_frequencies dictionary is: {}".format(seen_frequencies))
        return running_total, True

    return None, False

def day_1_part_2():
    lines = read_file_into_list("problem_1_input.txt")

    # print_debug("Problem 1 input data is:")
    # print_debug(lines)

    starting_value = 0

    seen_frequencies = {}

    answer_frequency = None

    found_answer = False
    running_total = starting_value

    list_iteration_count = 0
    while not found_answer:
        list_iteration_count+=1
        for line in lines:
            mytuple = parse_problem_1_string(line)
            if mytuple[0] == '+':
                new_running_total = running_total + mytuple[1]

                #print_debug(
                #    "I had the value {} and added on {} to get {}".format(running_total, mytuple[1], new_running_total))
                running_total = new_running_total

            elif mytuple[0] == '-':
                new_running_total = running_total - mytuple[1]


                #print_debug(
                #    "I had the value {} and subtracted {} to get {}".format(running_total, mytuple[1], new_running_total))

                running_total = new_running_total
            else:
                raise ValueError("Found invalid input")

            if not found_answer:
                answer_frequency, found_answer = check_seen(running_total, seen_frequencies)

    answer = answer_frequency

    answer_string = "For starting_value of {}, the frequency that shows up twice is {}. I had to read the list {} times to find it.".format(starting_value, answer, list_iteration_count)
    return answer_string



def check_box_pair(box1, box2):

    answer_box_1 = None
    answer_box_2 = None
    answer_letter_tuple = (None, None)

    #Given two IDs
    #Do they have exactly one character different?

    #If so, is that character in the same place?
    #If so, what are the characters that are in the same place?

    letter_differences_and_position = [(box1[i], box2[i],i) for i in range(len(box1)) if box1[i] != box2[i]]
    if len(letter_differences_and_position) == 1:
        print_debug("Looking at\nbox1 '{}' and \nbox2 '{}'\n"
                    "letter_differences_and_position is {}\n\n".format(box1,box2,letter_differences_and_position))
        return (box1, box2, (letter_differences_and_position[0][0], letter_differences_and_position[0][1]))
    #return (answer_box_1, answer_box_2, answer_letter_tuple)
    return None
def check_boxes(box_list):

    for box_i in box_list:
        for box_j in box_list:
            if box_i == box_j:
                pass
            else:
                answer_tuple = check_box_pair(box_i, box_j)
                if answer_tuple:
                    return answer_tuple
    return (None, None, None)


def day_2_part_2():
    lines = read_file_into_list("problem_2_input.txt")

    box1, box2, letter_tuple = check_boxes(lines)

    answer_string = "The two boxes that contain the santa suit are {} and {}.\n" \
                    "The letter_tuple found is {}".format(box1, box2, letter_tuple)
    return answer_string




def string_has_exactly_N_same_letters(input_string, N):

    #print_debug("Looking at input_string: "+input_string)

    count_dict = {}
    for letter in input_string:
        current_count = count_dict.get(letter, 0)
        current_count += 1
        count_dict[letter] = current_count



    if N in count_dict.values():
        #print_debug("Looking at input_string: " + input_string)
        #print_debug("count_dict is {}".format(count_dict))
        #print_debug("I found {} in the dictionary values.\n".format(N))
        return True

    return False

def how_many_have_letters_twice(lines):
    count = 0
    for line in lines:
        if string_has_exactly_N_same_letters(line, 2):
            count += 1
    return count

def how_many_have_letters_three_times(lines):
    count = 0
    for line in lines:
        if string_has_exactly_N_same_letters(line, 3):
            count += 1
    return count

def day_2_part_1():
    lines = read_file_into_list("problem_2_input.txt")

    elements_with_two_similar_letters = how_many_have_letters_twice(lines)
    elements_with_three_similar_letters = how_many_have_letters_three_times(lines)

    answer_checksum = elements_with_two_similar_letters * elements_with_three_similar_letters

    answer_string = "Num of elements with two of the same letters was {}\n" \
                    "Num of elements with three of the same letters was {}\n" \
                    "Therefore the computed checksum is {}".format(elements_with_two_similar_letters, elements_with_three_similar_letters, answer_checksum)
    return answer_string



class Rectangle:

    def make_intersection_rect(self, rectB):

        #scenario 1 - no intersection


        #scenario 2 - rectB point


        pass

    @classmethod
    def make_from_input_line(cls, line):
        # String looks like this '#1257 @ 707,747: 23x18'
        # Constructor to chop out the various bits
        print_debug("\nLooking at line '{}'".format(line))

        # Get ID
        my_list = line.split('@')
        id = int(my_list[0].replace("#","").replace(" ",""))
        print_debug("id = {}".format(id))


        # Get x_pos and ypos
        my_list = line.split(' ')
        xpos = int(my_list[2].split(',')[0])
        print_debug("xpos = {}".format(xpos))
        ypos = int(my_list[2].split(',')[1].replace(':',""))
        print_debug("ypos = {}".format(ypos))


        # Get x_length and y_length
        my_list = line.split(' ')
        x_length = int(my_list[3].split('x')[0])
        print_debug("x_length = {}".format(x_length))
        y_length = int(my_list[3].split('x')[1])
        print_debug("y_length = {}\n".format(y_length))


        return cls(id, xpos, ypos, x_length, y_length)




    def does_point_intersect(self, x, y):

        if self.x_pos <=x and \
                self.x_pos+self.x_length > x and\
                self.y_pos <= y and\
                self.y_pos+self.y_length > y :
            return True
        else:
            return False


    def __init__(self, id, x_pos, y_pos, x_length, y_length):
        self.id = id
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_length = x_length
        self.y_length = y_length

        self.intersecting_rects = []
        self.found_intersection = False



def get_max_canvas_size(lines):

    highest_x = 0
    highest_y = 0

    for line in lines:
        print_debug("\nline = '{}'".format(line))

        mylist = line.split(" ")
        x_1 = int(mylist[2].split(",")[0])
        print_debug("x_1 = {}".format(x_1))
        x_2 = int(mylist[3].split('x')[0])
        print_debug("x_2 = {}".format(x_2))

        y_1 = int(mylist[2].split(",")[1].replace(':',''))
        print_debug("y_1 = {}".format(y_1))
        y_2 = int(mylist[3].split('x')[1])
        print_debug("y_2 = {}".format(y_2))

        x_answer = x_1 + x_2
        if x_answer > highest_x:
            highest_x = x_answer

        y_answer = y_1 + y_2
        if y_answer > highest_y:
            highest_y = y_answer


    return highest_x, highest_y

def how_many_rects_does_point_intersect(x, y, rectangle_list):

    count = 0
    for rect in rectangle_list:
        check = rect.does_point_intersect(x,y)
        if check is True:
            print("got to here")
            count+=1


    return count


class Grid:

    def __init__(self):
        self.grid_x_max = 1000
        self.grid_y_max = 1000
        self.grid = [['.' for i in range(self.grid_x_max)] for j in range(self.grid_y_max)]
        self.rect_ids_candidates = []
        self.intersecting_rect_ids = []

        self.id_set = set()

        self.id_grid = [[[] for i in range(self.grid_x_max)] for j in range(self.grid_y_max)]


        self.candidate_id_dict = {}



    def get_answer_2(self):

        x = 0
        for row in self.grid:
            y = 0
            for collision_elem in row:
                # do something
                if self.grid[x][y] == "1" \
                        and len(self.id_grid[x][y]) == 1 and \
                        self.candidate_id_dict.get(self.id_grid[x][y][0]) != "invalid":
                    self.candidate_id_dict[self.id_grid[x][y][0]] = "valid"

                else:
                    for id in self.id_grid[x][y]:
                        self.candidate_id_dict[id] = "invalid"

                y += 1
            x += 1
        print_debug("")
        print_debug("candidate_id_dict = {}".format(self.candidate_id_dict))
        print_debug("")

        answer = None
        for key in self.candidate_id_dict:

            if self.candidate_id_dict[key] == "valid":
                answer = key


        return answer



    def get_answer(self):
        count = 0
        x = 0
        for list in self.grid:
            y =0
            for elem in list:
                # do something
                if self.grid[x][y] != "." and int(self.grid[x][y]) >=2:
                    count +=1
                y += 1
            x += 1

        return count

    def pretty_print(self):
        print("\nPrinting collision grid:\n")

        for list in self.grid:

            mystring = ""
            for elem in list:
                mystring= mystring + elem+" "
            print_debug(mystring)

    def pretty_print_id_grid(self):
        print_debug("\nPrinting ID grid:\n")

        for list in self.id_grid:

            mystring = ""
            for elem in list:
                mystring= mystring + str(elem)+" "
            print_debug(mystring)

        print_debug("")
        print_debug("id_set = {}".format(self.id_set))

    def add_rectangle(self, rect):

        rect_hit_another = False

        x = 0
        for list in self.grid:
            y =0
            for elem in list:
                # do something

                if rect.does_point_intersect(x,y):

                    if self.grid[x][y] == ".":
                        self.grid[x][y] = str(1)
                    else:
                        rect_hit_another = True
                        self.grid[x][y] = str(int(self.grid[x][y]) +1 )


                y+=1
            x+=1


    def add_rectangle_for_part2(self, rect):
        rect_hit_another = False

        self.id_set.add(rect.id)

        x = 0
        for list in self.grid:
            y =0
            for elem in list:
                # do something

                if rect.does_point_intersect(x, y):
                    self.id_grid[x][y].append(rect.id) # = self.id_grid[x][y]

                    if self.grid[x][y] == ".":
                        self.grid[x][y] = str(1)
                    else:

                        rect_hit_another = True
                        self.grid[x][y] = str(int(self.grid[x][y]) +1 )

                y+=1
            x+=1

        if rect_hit_another is False:
            self.rect_ids_candidates.append(rect.id)


def day_3_part_1():
    return "DISABLED - TAKES TOO LONG"
    lines = read_file_into_list("problem_3_input.txt")
    lines = read_file_into_list("problem_3_dummy_input.txt")


    rectangle_list = []
    for line in lines:
        #print_debug("Looking at line '"+line+"':")
        myRectangle = Rectangle.make_from_input_line(line)
        rectangle_list.append(myRectangle)



    my_grid = Grid()

    #my_grid.pretty_print()

    for rect in rectangle_list:
        my_grid.add_rectangle(rect)

    print_debug("rectangle_list = {}".format(rectangle_list))
    #my_grid.pretty_print()


    answer = my_grid.get_answer()

    answer_string = "number of inches = {}.".format(answer)
    return answer_string


def day_3_part_2():
    return "DISABLED - TAKES TOO LONG"
    lines = read_file_into_list("problem_3_input.txt")
    lines = read_file_into_list("problem_3_dummy_input.txt")

    rectangle_list = []
    for line in lines:
        # print_debug("Looking at line '"+line+"':")
        myRectangle = Rectangle.make_from_input_line(line)
        rectangle_list.append(myRectangle)

    my_grid = Grid()

    # my_grid.pretty_print()

    for rect in rectangle_list:
        my_grid.add_rectangle_for_part2(rect)

    print_debug("rectangle_list = {}".format(rectangle_list))
    print_debug("my_grid.rect_ids_candidates = {}".format(set(my_grid.rect_ids_candidates)))
    my_grid.pretty_print()
    my_grid.pretty_print_id_grid()

    answer = my_grid.get_answer_2()





    answer_string = "Answer = {}.".format(answer)
    return answer_string





class Schedule:

    def build_guard_dict(self):

        print_debug("\nBuilding totals:")
        for shift in self.shift_list:
            guard_string = shift["guard"]
            minutes_asleep_this_shift = 0
            for minute_char in shift["minutes_asleep"]:
                if minute_char == '#':
                    minutes_asleep_this_shift+=1

            current_guard = self.guard_dict.get(guard_string, {"minutes_asleep_total": 0})
            current_guard["minutes_asleep_total"] += minutes_asleep_this_shift

            self.guard_dict[guard_string] = current_guard
            print_debug("current guard_dict is {}".format(self.guard_dict))

        laziest_guard = None
        highest_minutes_asleep = 0
        for guard in self.guard_dict:
            if self.guard_dict[guard]["minutes_asleep_total"] > highest_minutes_asleep:
                highest_minutes_asleep = self.guard_dict[guard]["minutes_asleep_total"]
                laziest_guard = guard

        self.laziest_guard = laziest_guard
        self.highest_minutes_asleep = highest_minutes_asleep


    def get_answer_part_1(self):

        print("")
        print_debug("\nLaziest_guard is {} with a total of {} minutes\n".format(self.laziest_guard, self.highest_minutes_asleep))


        shifts_of_lazy_guard = [shift for shift in self.shift_list if shift['guard'] == self.laziest_guard]

        print_debug("\nshifts_of_lazy_guard is {}".format(shifts_of_lazy_guard))
        minute_frequencies = {}


        for shift in shifts_of_lazy_guard:
            for minute in range(60):
                if shift['minutes_asleep'][minute] == '#':
                    minute_frequencies[minute] = minute_frequencies.get(minute, 0)+1

        print_debug("\nminute_frequencies for the lazy guard is {}".format(minute_frequencies))
        print_debug("")

        highest = [0, 0]
        for minute in minute_frequencies:
            if minute_frequencies[minute] > highest[1]:
                highest[0] = minute
                highest[1] = minute_frequencies[minute]

        print_debug("favourite minute is {} with a frequency of {}\n\n\n".format(highest[0],highest[1]))

        answer_string = "The laziest guard is {} with a total of {} minutes. " \
                        "His favourite minute to sleep is {} with a frequency of {}".format(self.laziest_guard, self.highest_minutes_asleep, highest[0],highest[1])
        return answer_string

    def build_dict(self, lines):
        for line in lines:




            current_guard = None


            #guard begin shift event
            if line.split('] ')[1].split(" ")[0] == "Guard":
                print_debug("looking at line: '{}'".format(line))
                guard_string = "Guard "+line.split('] ')[1].split(" ")[1]
                print_debug("Adding {} to dictionary".format(guard_string))
                current_guard = guard_string
                print_debug("current_guard = {}".format(current_guard))
                mydate = line.split(']')[0].replace("[", "").split(" ")[0].replace("1518-","")
                print_debug("date = {}".format(mydate))


                minutes_alseep_list = ["." for _ in range(60)]
                self.shift_list.append( {"guard": guard_string, "date": mydate, "minutes_asleep": minutes_alseep_list } )
                print_debug("shift_list now equals {}".format(self.shift_list))
                print_debug("")

            #fall asleep event
            elif line.split('] ')[1].split(" ")[0] == "falls":
                print_debug("looking at line: '{}'".format(line))
                print_debug("handling a fall asleep event")


                my_minute = int(line.split(" ")[1].replace("]", "").split(":")[1])
                print_debug("my_minute = {}".format(my_minute))


                for x in range(my_minute,60):
                    self.shift_list[-1]["minutes_asleep"][x] = "#"

                print_debug("shift_list now equals {}".format(self.shift_list))
                print_debug("")

            #wake up event
            else:
                print_debug("looking at line: '{}'".format(line))
                print_debug("handling a wake up event")
                my_minute = int(line.split(" ")[1].replace("]", "").split(":")[1])
                print_debug("my_minute = {}".format(my_minute))


                for x in range(my_minute,60):
                    self.shift_list[-1]["minutes_asleep"][x] = "."
                print_debug("shift_list now equals {}".format(self.shift_list))


                print_debug("")


    def __init__(self, lines):
        self.shift_list = []

        self.guard_dict = {}

        self.build_dict(lines)

        self.highest_minutes_asleep = 0
        self.laziest_guard = None

        current_guard = None
        self.build_guard_dict()



    def pretty_print(self):
        #print("\nshift_list = {}\n".format(self.shift_list))

        print_debug("Date   ID   Minute")
        print_debug("            000000000011111111112222222222333333333344444444445555555555")
        print_debug("            012345678901234567890123456789012345678901234567890123456789")



        for shift in self.shift_list:

            print_string = shift["date"]+"  "+shift["guard"].replace("Guard ","")+"  "
            for minute_char in shift["minutes_asleep"]:
                print_string +=minute_char
            print_debug(print_string)

        #given a day, a guard ID and a minute
        
    def get_answer_part_2(self):

        #dictionary with minute as keys to dict with guard ID as keys to frequency value
        #

        minute_freq_dict = {}
        for x in range(60):
            minute_freq_dict[x] = {}

        #build dictionary
        for minute in range(60):
            for shift in self.shift_list:
                if shift["minutes_asleep"][minute] == '#':
                    guard_string = shift['guard']
                    count = minute_freq_dict[minute].get(guard_string, 0)+1
                    new_dict = {guard_string: count}
                    minute_freq_dict[minute].update(new_dict)

                    #minute_freq_dict[minute] = minute_freq_dict.get(minute, [{"guard": None, "frequency": 0}])
                    #pass

           #minute_freq_dict[minute] = {"guard": None, "frequency": 0}
        print_debug("\nminute_freq_dict is {}\n".format(minute_freq_dict))

        highest_guard_id_found = None

        highest_minute_found = 0
        highest_frequency_found = 0

        for minute in range(60):
            for guard_id in minute_freq_dict[minute]:
                #print_debug("looking at {}".format(guard))
                if minute_freq_dict[minute][guard_id] > highest_frequency_found:
                    highest_frequency_found = minute_freq_dict[minute][guard_id]
                    highest_guard_id_found = guard_id
                    highest_minute_found = minute
                pass

        answer_string = "Guard '{}' slept the most on minute {}. He did this {} times.".format(highest_guard_id_found,
                                                                                             highest_minute_found,
                                                                                             highest_frequency_found)
        return answer_string

def day_4_part1():
    lines = read_file_into_list("problem_4_dummy_input.txt")
    #lines = read_file_into_list("problem_4_input.txt")

    lines.sort()
    for line in lines:

        date_string = line.split(']')[0]
        #print(date_string)
        #print(line)
        pass
    my_schedule = Schedule(lines)
    my_schedule.pretty_print()
    answer = my_schedule.get_answer_part_1()
    answer_string = "{}".format(answer)
    return answer_string


def day_4_part2():
    lines = read_file_into_list("problem_4_dummy_input.txt")
    #lines = read_file_into_list("problem_4_input.txt")

    lines.sort()
    for line in lines:

        date_string = line.split(']')[0]
        #print(date_string)
        #print(line)
        pass
    my_schedule = Schedule(lines)
    my_schedule.pretty_print()
    answer = my_schedule.get_answer_part_2()
    answer_string = "{}".format(answer)
    return answer_string


def will_chars_annihilate(char1, char2):
    return False

class Polymer_chain:

    def __init__(self, line):
        self.polymer_chain = []
        self.build_array(line)

        self.keep_going = True
        self.first_run_done = False

    def build_array(self, line):
        for char in line:
            self.polymer_chain.append({"char": char, "exists_next_tick": True})


    def will_dict_exist_next_tick(self, dict1, dict2):
       # print_debug("Comparing {} and {}".format(dict1, dict2))
        return_value = False
        if dict1['char'] == dict2["char"] :
            # equal chars do not annhilate eg 'aa'
            return_value = True

        elif dict1['char'].lower() == dict2['char'].lower() and dict1['exists_next_tick'] is True:
            return_value = False
        else:
            return_value = True

        #print_debug("return_value is {}".format(return_value))

        return return_value



    def compute_reactions(self):

        #print_debug("\npolymer chain is {}\n".format(self.polymer_chain))
        index = 0
        for mydict in self.polymer_chain:

            #we're at the head of the list
            if index == 0:
                pass

            #we're doing the general case
            else:
                if self.will_dict_exist_next_tick(self.polymer_chain[index-1], mydict) is False:
                #mydict['exists_next_tick'] = self.will_char_exist_next_tick(mydict['char'], self.polymer_chain[index+1]['char'])
                    mydict['exists_next_tick'] = False
                    self.polymer_chain[index - 1]['exists_next_tick'] = False
            index+=1

        #print_debug("\npolymer chain is {}\n".format(self.polymer_chain))

    def apply_reactions(self):
        #print_debug("\nApplying reactions from previous tick....")
        old_length = len(self.polymer_chain)


        self.polymer_chain[:] = [mydict for mydict in self.polymer_chain if  mydict['exists_next_tick'] is True]
        new_length = len(self.polymer_chain)


        if old_length == new_length and self.first_run_done is True:
            self.keep_going = False
        self.first_run_done = True

        #for mydict in self.polymer_chain:
        #    if mydict['exists_next_tick'] is False:
        #        mydict['exists_this_tick'] = False


    def get_answer_string_part_1(self):
        final_polymer = ""
        for mydict in self.polymer_chain:
            final_polymer += mydict["char"]

        answer_string = "Final polymer string is '{}' and it has a length of {}".format(final_polymer,
                                                                                        len(final_polymer))

        return answer_string


    def get_length_part_2(self):
        final_polymer = ""
        for mydict in self.polymer_chain:
            final_polymer += mydict["char"]

        answer = len(final_polymer)

        return answer


    def compute_answer_for_part_1(self):


        #while we can keep going:  (start tick)
            # compute reactions for this tick (scan once and save results somewhere)
            # apply reactions to polymer string
            # (end tick)
        while self.keep_going is True:

        #for x in range(4):   # temporary

            print_debug("< Starting tick > \n")
            self.pretty_print()
            self.apply_reactions()
            self.compute_reactions()
            self.pretty_print()
            print_debug("\n<\ Ending tick > \n")


        return self.get_answer_string_part_1()



    def compute_answer_for_part_2(self):

        while self.keep_going is True:

        #for x in range(4):   # temporary

            #print_debug("< Starting tick > \n")
            self.pretty_print()
            self.apply_reactions()
            self.compute_reactions()
            self.pretty_print()
            #print_debug("\n<\ Ending tick > \n")


        return self.get_length_part_2()




    def pretty_print(self):
        #print_debug("polymer_chain = {}".format(self.polymer_chain))

        string_1 = ""
        string_2 = ""
        for mydict in self.polymer_chain:
            string_1 += mydict['char']

        #print_debug("\nPrinting internal state of Polymer string:")
        #print_debug(string_1)
        #print_debug(string_2)

def day_5_part1():
    lines = read_file_into_list("problem_5_dummy_input.txt")
    #lines = read_file_into_list("problem_5_input.txt")

    line = lines[0]

    my_polymer_chain = Polymer_chain(line)

    answer_string = my_polymer_chain.compute_answer_for_part_1()
    #print_debug("line is {}".format(line))

    return answer_string


def get_frequency_dict(line):
    frequency_dict = {}

    for mychar in line:
        mychar_lowered = mychar.lower()
        frequency_dict[mychar_lowered] = frequency_dict.get(mychar_lowered, 0) + 1

    return frequency_dict

def day_5_part2():
    lines = read_file_into_list("problem_5_dummy_input.txt")


    #lines = read_file_into_list("problem_5_input.txt")

    line = lines[0]

    frequency_dict = get_frequency_dict(line)
    print_debug("frequency_dict of line is {}".format(frequency_dict))

    length_dict_list = []

    for lowered_char in frequency_dict:
        print_debug("Looking at char {}:".format(lowered_char))
        new_line = line.replace(lowered_char, "").replace(lowered_char.upper(), "")

        print_debug("frequency_dict of new_line is {}".format(get_frequency_dict(new_line)))

        my_polymer_chain = Polymer_chain(new_line)
        answer = my_polymer_chain.compute_answer_for_part_2()
        length_dict_list.append({"excluded_char": lowered_char, "final_length": answer})
    #print_debug("line is {}".format(line))

    print_debug("\nlength_dict_list is {}\n".format(length_dict_list))



    min_length_found = 1000000000  # some big number
    char_found = None
    for mydict in length_dict_list:
        if mydict["final_length"] < min_length_found:
            min_length_found = mydict["final_length"]
            char_found = mydict["excluded_char"]

    answer_string = "Remove the character '{}' to get the shortest polymer found, which is {}".format(char_found, min_length_found)
    return answer_string



class Danger_Grid:


    def get_answer_part2(self):

        area = 0

        for y in range(self.Y_MAX):
            for x in range(self.X_MAX):
                if self.grid[x][y] == "##":
                    area+=1
        return area

    def get_answer_part1(self):
        answer_dict = {}
        for target in self.points_list:
            print_debug("\nLooking at target {}:".format(target))
            bounded = True
            area = 0
            for y in range(self.Y_MAX):
                for x in range(self.X_MAX):

                    #compute area
                    if target[0].lower() == self.grid[x][y].lower():
                        area+=1

                        #compute bounded
                        if x == 0 or y ==0 or x == self.X_MAX-1 or y == self.Y_MAX-1:
                            bounded = False

            print_debug("bounded is {}".format(bounded))
            print_debug("area is {}".format(area))
            answer_dict[target[0]] = {"bounded":bounded, "area": area}

        print_debug("\n\nData structure computed for part 1: \n{}\n\n".format(answer_dict))
        return answer_dict

    def is_point_a_target(self,x,y):
        for mypoint in self.points_list:
            if x == mypoint[1] and y == mypoint[2]:
                return True

        return False

    def get_closest_targets(self, x,y ):

        #print_debug("\nLooking at point ({}, {}):".format(x,y))

        #get highest manhatten distance
        min_manhatten_distance = 9999999999999999
        return_value = []
        for mypoint in self.points_list:
            manhatten_distance = abs(x-mypoint[1]) + abs(y-mypoint[2])
            if min_manhatten_distance > manhatten_distance:
                min_manhatten_distance = manhatten_distance

        # build return value
        for mypoint in self.points_list:
            manhatten_distance = abs(x - mypoint[1]) + abs(y - mypoint[2])
            if manhatten_distance == min_manhatten_distance:
                return_value.append({"target_char": mypoint[0].lower(), "manhatten_distance": manhatten_distance})

        #print_debug("return_value is {}".format(return_value))
        #self.print_grid()
        return return_value

    def initialize_distances(self):

        for y in range(self.Y_MAX):
            for x in range(self.X_MAX):
                closest_targets = self.get_closest_targets(x,y)
                if not self.is_point_a_target(x,y):
                    if len(closest_targets) > 1:
                        self.grid[x][y] = ".."
                    else:
                        self.grid[x][y] = closest_targets[0]["target_char"]



                #if my_new_letter and not self.is_point_a_target(x,y):
                #    self.grid[x][y] = my_new_letter
        print_debug("\nAfter initializing distances this is what we get:")
        self.print_grid()

    def __init__(self, lines):
        self.points_list = []
        self.grid =[]
        self.X_MAX = 10
        self.Y_MAX = 10

        #get X_MAX and Y_MAX
        for line in lines:
            curr_x = int(line.split(", ")[0])
            curr_y =int(line.split(", ")[1])
            if curr_x > self.X_MAX:
                self.X_MAX = curr_x+1
            if curr_y > self.Y_MAX:
                self.Y_MAX = curr_y+1

        #initialize grid
        for x in range(self.X_MAX):
            self.grid.append([])
            for y in range(self.Y_MAX):
                self.grid[x].append("--")

        target_name_index =0
        target_name = "T"+str(target_name_index)
        for line in lines:


            x_val = int(line.split(", ")[0])
            #print_debug("x_val = {}".format(x_val))
            y_val = int(line.split(", ")[1])
            target_name = "T" + str(target_name_index)
            self.points_list.append((target_name, x_val, y_val))
            self.grid[x_val][y_val] = target_name
            target_name_index += 1

        print_debug("Printing points:")
        for mytuple in self.points_list:
            print_debug(mytuple)

        print_debug("")
        self.print_grid()


    def print_grid(self):
        print_debug("Printing grid:")
        for y in range(self.Y_MAX):
            mystring = ""
            for x in range(self.X_MAX):
                mystring+=self.grid[x][y]+" "
            print_debug(mystring)
        print_debug("")

    def is_point_safe(self, x, y, limit):


        total_manhatten_distance = 0
        for target in self.points_list:
            manhatten_distance = abs(x-target[1]) + abs(y-target[2])
            total_manhatten_distance+=manhatten_distance

        if total_manhatten_distance < limit:
            return True
        else:
            return False





    def initialize_safe_distances(self, limit):
        print_debug("initializing safe distances where limit is {}...".format(limit))

        for y in range(self.Y_MAX):
            for x in range(self.X_MAX):
                #if not self.is_point_a_target(x, y):
                if self.is_point_safe(x,y, limit):
                    self.grid[x][y] = "##"
        pass

def day_6_part1():
    lines = read_file_into_list("problem_6_dummy_input.txt")
    #lines = read_file_into_list("problem_6_input.txt")

    my_danger_grid = Danger_Grid(lines)

    my_danger_grid.initialize_distances()

    answer_dict = my_danger_grid.get_answer_part1()

    max_area = 0
    max_char = 0
    for target in answer_dict:
        if answer_dict[target]["bounded"] is True and answer_dict[target]["area"] > max_area:
            max_char = target
            max_area = answer_dict[target]["area"]

    answer_string = "'{}' is the most dangerous target. It has a bounded area of {}.".format(max_char,max_area)
    return answer_string

def day_6_part2():
    lines = read_file_into_list("problem_6_dummy_input.txt") ; LIMIT = 32
    #lines = read_file_into_list("problem_6_input.txt") ; LIMIT = 10000


    my_danger_grid = Danger_Grid(lines)
    my_danger_grid.initialize_safe_distances(LIMIT)
    my_danger_grid.print_grid()
    answer = my_danger_grid.get_answer_part2()

    return "Answer is {}".format(answer)

class Node:
    def __init__(self, node_value):
        self.value = node_value


class Tree:
    def __init__(self, root_val):
        self.root = {root_val : None}
        self.levels = 1

    def insert(self, key, value, level):
        #I know the key is in the tree somewhere
        if self.levels == 1:
            self.root[key] = value
            self.levels+=1
        else:
            self.insert(key, value)

    def print_tree(self):
        print_debug("\n\nThe state of the tree is:")

        print_debug("{}".format(self.root))
        print_debug("levels is {}".format(self.levels))
        print_debug("")
        print_debug("")

class Directed_Graph:


    def get_root_char(self):
        #last char
        value_insertion_set = set(self.value_insertion_sequence)
        child_insertion_set = set(self.child_insertion_sequence)
        last_character = None
        try:
            last_character = child_insertion_set.difference(value_insertion_set).pop()
        except KeyError:
            pass
        return last_character

    def insert_node(self, node_value, node_child_value):
        #internal_dict1
        mylist = self.initial_dict.get(node_value, [])
        mylist.append(node_child_value)
        self.initial_dict[node_value] = mylist

        #internal_dict2
        mylist = self.computed_dict.get(node_child_value, [])
        mylist.append(node_value)
        mylist.sort(reverse=True)
        self.computed_dict[node_child_value] = mylist


        #edges
        self.edges.append((node_value, node_child_value))


        #marked dict

        self.marked_dict[node_value] = "unmarked"
        self.marked_dict[node_child_value] = "unmarked"


    def print_graph(self):
        """
        print_debug("printing state of graph:\n--------------")
        #print_debug("value_insertion_sequence is {}".format(self.value_insertion_sequence))
        #print_debug("child_insertion_sequence is {}".format(self.child_insertion_sequence))

        print_debug("initial_dict is: {}".format(self.initial_dict))

        print_debug("computed_dict is: {}".format(self.computed_dict))
        print_debug("edges list is: {}".format(self.edges))
        print_debug("\nmarked_dict is: {}".format(self.marked_dict))


        #for elem in self.initial_dict:
        #    print_debug("'{}' goes to {}".format(elem, self.initial_dict[elem]))
        """
        pass

    def build_directed_graph(self, lines):
        for line in lines:
            print_debug("\n\n\nLooking at line: \n{}".format(line))
            node_value = line.split(" ")[1]
            print_debug("node_value is {}".format(node_value))
            node_child_value = line.split(" ")[7]
            print_debug("node_child_value is {}".format(node_child_value))
            self.insert_node(node_value, node_child_value)
            self.value_insertion_sequence.append(node_value)
            self.child_insertion_sequence.append(node_child_value)

            print_debug("The state of the graph is:")
            self.print_graph()
            print_debug("")
        pass

    def get_next_level(self, input_list):

        print_debug("\ngiven input {}".format(input_list))
        return_list = []
        for mychar1 in input_list:
            try:
                list2 = self.computed_dict[mychar1]
            except KeyError:
                print_debug("couldn't find {}".format(mychar1))
                return None
            for mychar2 in list2:
                return_list.append(mychar2)

        return_list = list(set(return_list))
        #.sort(reverse=True)
        return_list.sort(reverse=True)
        print_debug("the next level is {}\n".format(return_list))

        return return_list
        pass



    def get_set_of_nodes_with_no_incoming_edge(self):

        set1 = set(self.value_insertion_sequence)
        set2 = set(self.child_insertion_sequence)

        myset = set(set1.difference(set2))



        print_debug("Set of all nodes with no incoming edge is {}".format(myset))



        return myset

    def remove_edge_from_graph(self, node_n, node_m):

        self.edges.remove((node_n, node_m))

        pass

    def get_edges(self, node_n):

        #newlist = [mytuple for mytuple in self.edges if mytuple[0] == node_n and mytuple[1] == node_m]
        try:
            returnval = self.initial_dict[node_n]
        except KeyError:
            returnval = []
        return returnval

    def do_unmarked_nodes_remain(self):

        found = False
        for node in self.marked_dict:
            if self.marked_dict[node] == "unmarked":
                found = True

        return found

    def get_next_unmarked_node(self):

        for node in sorted(self.marked_dict.keys(), reverse=True):
            if self.marked_dict[node] == "unmarked" or  self.marked_dict[node] == "temporary_mark":
                return node
        return None

    def visit(self, node_n):
        self.print_graph()
        if self.marked_dict[node_n] == "permanent_mark":
            return
        if self.marked_dict[node_n] == "temporary_mark":
            return
        print_debug("Giving {} a temporary mark".format(node_n))
        self.marked_dict[node_n] = "temporary_mark"
        for node_m in sorted(self.get_edges(node_n), reverse=False):
            self.visit(node_m)
        print_debug("Giving {} a permanant mark".format(node_n))
        self.marked_dict[node_n] = "permanent_mark"
        self.answer_list.insert(0,node_n)


    def get_answer_part_1(self):




        """
        while self.do_unmarked_nodes_remain() is True:

            next_node = self.get_next_unmarked_node()

            print_debug("next unmarked node is {}".format(next_node))
            self.visit(next_node)
            print_debug("\n")

        answer_string = None
        self.print_graph()

        answer_string_final = ""
        for elem in self.answer_list:
            answer_string_final += elem
        return answer_string_final
        """
    def __init__(self, lines):
        self.initial_dict  = {}
        self.computed_dict  = {}
        self.marked_dict = {}
        self.edges = []
        self.answer_list = []
        self.value_insertion_sequence = []
        self.child_insertion_sequence = []

        self.build_directed_graph(lines)


def solve(lines):
    G = nx.DiGraph()
    for line in lines:
        parts = line.split(" ")
        G.add_edge(parts[1], parts[7])

    #print_debug(G.draw())
    answer = ''.join(nx.lexicographical_topological_sort(G))
    return answer

def day_7_part1():
    lines = read_file_into_list("problem_7_dummy_input.txt")
    lines = read_file_into_list("problem_7_input.txt")

    #myTree = Directed_Graph(lines)
    answer = solve(lines)
    answer_string_final = "answer is {}".format(answer)
    #answer_string_final = myTree.get_answer_part_1()



    return answer_string_final






def day_7_part2():

    num_workers = 5
    num_seconds = 60

    heading = "Second   "
    heading2 = "----------------"
    for worker_num in range(num_workers):
        heading+="Worker {}   ".format(worker_num)
        heading2+="-----------"
    heading+="Done"
    print_debug(heading)
    print_debug(heading2)




    print_debug("\n\n\n")


    lines = read_file_into_list("problem_7_dummy_input.txt")
    lines = read_file_into_list("problem_7_input.txt")

    #myTree = Directed_Graph(lines)
    answer = "WIP" #solve(lines)
    answer_string_final = "answer is {}".format(answer)
    #answer_string_final = myTree.get_answer_part_1()



    return answer_string_final

class HeaderNode:


    def __init__(self):
        self.id = None
        self.num_child_nodes = None
        self.num_metadatas = None
        self.metadata_list = []
        self.child_node_list = []
        self.index = None
        pass

    def pretty_print(self):

        print_debug("Looking at node {}:\n"
                    "- num_child_nodes is {}\n"
                    "- num_metadatas is {}\n"
                    "- metadata_list is {}\n"
                    "\n".format(self.id, self.num_child_nodes,
                                           self.num_metadatas, self.metadata_list,
                                           #[node.id for node in self.child_node_list],
                                           #self.index
                                ))

class HeaderTree:



    def pop_head_node(self):

        #print_debug("self.node_list is {}".format(self.node_stack))
        mynode = self.node_stack.pop()
        self.processed_nodes.append(mynode)

        print_debug("\nRemoved node {} from node_stack".format(mynode.id))
        #simplified_node_stack_to_print = [node.id for node in self.node_stack]
        #print_debug("node_stack now looks like this: {}".format(simplified_node_stack_to_print))
        simplified_processed_nodes_to_print = [node.id for node in self.processed_nodes]

        #print_debug("processed_nodes now looks like this: {}".format(simplified_processed_nodes_to_print))
        #print_debug("Removed node {} from stack. node_stack now looks like this: {}\n".format(node.id, simplified_node_stack_to_print))
        #print_debug("num_list now looks likes this: {}".format(self.num_list))




    def add_to_stack(self, node):
        self.node_stack.append(node)
        simplified_stack_to_print = [node.id for node in self.node_stack]
        print_debug("\nAdding node {} to stack.".format(node.id))
        print_debug("node_stack now looks like this: {}".format(simplified_stack_to_print))
        print_debug("num_list now looks likes this: {}".format(self.num_list))



    def process_nodes(self):


        if self.node_stack == []:
            print_debug("\nStack is empty now.")
            return
        else:
            head_node = self.node_stack[-1]
            self.pop_head_node()

            #print_debug("head_node is {}".format(head_node.id))
            #head_node.pretty_print()

            for _ in range(head_node.num_child_nodes):

                #break the list into x number of uneven chunks

                new_node = HeaderNode()
                new_node.id = self.get_new_node_id()
                num_child_nodes =  self.num_list[0]
                new_node.num_child_nodes =num_child_nodes
                new_node.num_metadatas = self.num_list[1]



                self.add_to_stack(new_node)

                new_node.pretty_print()


            self.process_nodes()

    def generate_tree(self):

        #first node

        new_node = HeaderNode()
        new_node.id = self.get_new_node_id()
        new_node.num_child_nodes = self.num_list[0]
        num_metadatas = self.num_list[1]
        new_node.num_metadatas = num_metadatas
        index = 0

        new_node.metadata_list = self.num_list[-num_metadatas:]
        self.num_list = self.num_list[index+2:-num_metadatas]
        new_node.index = index


        self.add_to_stack(new_node)
        #self.node_stack.append(new_node)


        # rest of the nodes
        self.process_nodes()


    def __init__(self, num_list):
        self.num_list_original = num_list

        self.num_list = self.num_list_original.copy()
        self.node_list = []
        self.last_node_id_generated = None
        self.node_stack = []
        self.processed_nodes = []




        self.generate_tree()
        pass

    def get_new_node_id(self):
        return_val = None

        if self.last_node_id_generated is None:
            return_val = "A1"
        else:
            last_num = int(self.last_node_id_generated[1:])
            last_char = self.last_node_id_generated[:1]

            if last_char == "Z":
                return_val = "A" + str(last_num+1)
            else:
                return_val = chr(ord(last_char) + 1) + str(last_num)


            #return_val = "B1"


        #print_debug("get_new_node_id() has returned: {}".format(return_val))
        self.last_node_id_generated = return_val
        return return_val


    def get_column(self):
        mystring = ""
        if self.last_node_id_generated is None:
            return "  "

        else:
            for _ in self.last_node_id_generated:
                mystring+=" "

            return mystring



    def pretty_print(self):
        print_debug("\n")
        mystring = ""
        for num in self.num_list_original:
            mystring += str(num) + self.get_column()
        print_debug(mystring)

        mystring2 = ""
        for node in self.node_list:
            mystring2+=node.id
        print_debug(mystring2)

        print_debug("\n")


class ID_generator:

    def get_new_id(self):
        return_val = None

        if self.last_node_id_generated is None:
            return_val = "A1"
        else:
            last_num = int(self.last_node_id_generated[1:])
            last_char = self.last_node_id_generated[:1]

            if last_char == "Z":
                return_val = "A" + str(last_num+1)
            else:
                return_val = chr(ord(last_char) + 1) + str(last_num)

        self.last_node_id_generated = return_val
        return return_val

    def __init__(self):
        self.last_node_id_generated = None

def get_day_8_answer(myList):

    total = 0
    dictstring = ""
    for mydict in myList:
        dictstring+="\n{}".format(mydict)
        for metadata in mydict["metadatas"]:
            total += metadata

    print_debug("Given the input:\n[{}\n]\nWe get the following total: {}\n\n".format(dictstring,total))

    return total


#2  3  0  3  10  11  12  1  1  0  1  99  2  1  1  2


def construct_dict(num_list, answer, id_generator, parent_stack):
    num_children = num_list[0]
    num_metadatas = num_list[1]

    print_debug("\n")
    print_debug("num_children is {}".format(num_children))
    print_debug("num_metadatas is {}".format(num_metadatas))
    print_debug("num_list is {}".format(num_list))
    print_debug("parent_stack is {}".format(parent_stack))
    print_debug("answer is {}".format(answer))

    name = id_generator.get_new_id()
    answer[name] = {}
    parent_stack.append(name)

    if num_children == 0:
        answer[name] = {"metadata": num_list[-num_metadatas:]}


        #answer[parent]["children"] = answer[parent].get("children", []).append(name)

        return answer


    for _ in range(num_children):
        construct_dict(num_list[2:], answer, id_generator, parent_stack)
    print_debug("\n")

    return answer

    """
    
            new_dict = {}
        name = id_generator.get_new_id()

        new_dict["name"] = name
        new_dict["metadatas"] = num_list[-num_metadatas:]

        num_list = num_list[:-num_metadatas]
        answer.append(new_dict)




        if num_children == 0:
            break

        index+=2
        break

    print_debug("Given the input:\n{}\n".format(num_list))






    print_debug("\nWe get the following output:\n[")
    for entry in answer:
        print_debug("{}".format(entry))
    print_debug("]")

    #while loop
    for _ in range(1):




        num_children = num_list[index]
        name = id_generator.get_new_id()
        num_metadatas = num_list[index+1]

        #put it onto stack
        stack.append((name, num_children))




        #if head of stack has no children pop it
        if stack[0][1] == 0:
            stack.pop()





        new_dict = {}
        new_dict["name"] = name
        new_dict["metadatas"] = num_list[-num_metadatas:]



        num_list = num_list[:-num_metadatas]
        num_list=num_list[2:]
        answer.append(new_dict)



        print_debug("num_list is now: {}".format(num_list))
        index +=2
    """


class NodeForHeader:

    # [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    def __init__(self, num_list):


        self.num_children = num_list[0]
        self.num_metadata = num_list[1]
        new_num_list = num_list[2:]

        self.children = []
        self.metadata = []

        #print_debug("num_children is {}".format(self.num_children))
        #print_debug("num_metadata is {}".format(self.num_metadata))
        #print_debug("num_list is {}".format(num_list))
        print_debug("")
        for _ in range(self.num_children):
            new_node = NodeForHeader(new_num_list)
            self.children.append(new_node)
            new_num_list = new_num_list[new_node.get_size():]
        self.metadata = new_num_list[:self.num_metadata]
        #print_debug("children is {}".format(self.children))
        #print_debug("metadata is {}".format(self.metadata))

    def is_valid_index(self, index):
        try:
            test = self.children[index]
            return True
        except IndexError:
            return False
    def get_value(self):
        print_debug("")

        value = None
        if self.children == []:
            value = sum(self.metadata)

        else:
            #value = sum ([ child.get_value() for child in self.children ])

            value = sum ([self.children[metadata-1].get_value() for metadata in self.metadata if self.is_valid_index(metadata-1) is True])
            """
            val_total = 0
            print_debug("all metadata is {}".format(self.metadata))
            for metadata in self.metadata:
                print_debug("looking at metadata {}".format(metadata))
                val_to_add = 0
                try:
                    val_to_add = self.children[metadata].get_value()
                except IndexError:
                    val_to_add =0

                val_total+=val_to_add

            value = val_total
        """

        #print_debug("Node value is {}".format(value))
        #print_debug("")
        return value

    def get_size(self):

        total_child_size = 0

        for child in self.children:
            total_child_size+=child.get_size()

        my_size = 2 + self.num_metadata

        size = my_size + total_child_size

        return size

    def get_all_metadata(self):
        all_metadata = self.metadata + [m for child in self.children for m in child.get_all_metadata()]
        return all_metadata


    def get_answer_part_1(self):

        all_metadata = self.get_all_metadata()
        #mystring = ""
        print_debug("Final list of metadata was: {}".format(all_metadata))
        mystring = "Sum is {}".format(sum(all_metadata))
        return mystring

    def get_answer_part_2(self):
        return "Value of root node is {}".format(self.get_value())

def day_8_part1():
    lines = read_file_into_list("problem_8_dummy_input.txt")
    #lines = read_file_into_list("problem_8_input.txt")

    num_list_initial = lines[0].split(" ")
    num_list = [ int(x) for x in num_list_initial ]

    root = NodeForHeader(num_list)

    return root.get_answer_part_1()

def day_8_part2():
    return "DISABLED"
    lines = read_file_into_list("problem_8_dummy_input.txt")
    lines = read_file_into_list("problem_8_input.txt")

    num_list_initial = lines[0].split(" ")
    num_list = [ int(x) for x in num_list_initial ]

    root = NodeForHeader(num_list)

    return root.get_answer_part_2()


class CircleGame:

    def __init__(self, number_of_players, last_marble_points):
        self.current_marble_index = None
        self.num_players = number_of_players
        self.current_player = 0

        self.marbles = []

        self.last_marble_value = None

        self.scoreboard = {}
        self.init_scoreboard()


    def init_scoreboard(self):
        for playerID in range(1, self.num_players+1):
            self.scoreboard[playerID] = {"score": 0, "marbles": []}

    def print_scoreboard(self):

        print_debug("\n\n\nScoreboard dictionary is:\n{}\n".format(self.scoreboard))


        print_debug("\n\nThe scoreboard is:")
        for playerID in self.scoreboard:
            print_debug("Player {} has the score {}".format(playerID, self.scoreboard[playerID]["score"]))
        print_debug("\n\n")


        highest_scoring_player = 0
        highest_scoring_player_score = 0
        for playerID in self.scoreboard:
            if self.scoreboard[playerID]["score"] > highest_scoring_player_score:
                highest_scoring_player_score = self.scoreboard[playerID]["score"]
                highest_scoring_player = playerID


        #Part 2
        #winning_marbles = self.scoreboard[highest_scoring_player]["marbles"]
        #new_last_marble = winning_marbles.pop() * 100
        #winning_marbles.append(new_last_marble)
        #new_score = sum(winning_marbles)


        return_string = "Highest scoring player was player {} with a score of {}".format(highest_scoring_player, highest_scoring_player_score)
        print_debug(return_string)

        return return_string
    def get_clockwise_index_from_index(self, index):
        num_steps = int((len(self.marbles) ))

        num_steps = num_steps % (len(self.marbles))

        index = self.current_marble_index + num_steps  # % len(self.marbles)

        index = index

        return index

    def remove_marble_from_circle(self, left_index):
        pass
        print_debug("current_marble_index is {}".format(self.current_marble_index))
        #print_debug("left_index is {}".format(left_index))
        # print_debug("right_index is {}".format(right_index))

        # print_debug("Therefore our new index is {}".format(None))

        return_val = self.marbles.pop(left_index )
        # self.marbles.append(marble)

        self.current_marble_index = left_index
        print_debug("removing the marble {} at index {}".format(return_val, left_index))
        return return_val

    def insert_marble_into_circle(self, marble, left_index):
        pass
        print_debug("current_marble_index is {}".format(self.current_marble_index))
        print_debug("left_index is {}".format(left_index))
        #print_debug("right_index is {}".format(right_index))

        #print_debug("Therefore our new index is {}".format(None))

        self.marbles.insert(left_index+1, marble)
        #self.marbles.append(marble)

        self.current_marble_index = left_index+1

            #self.current_marble_index =

    def get_new_index(self, num_steps, go_clockwise=True):
        index = None
        if go_clockwise is True:
            index = self.current_marble_index + num_steps #% len(self.marbles)

            index = index % (len(self.marbles))

        else:
            index = self.current_marble_index - num_steps
            index = index % (len(self.marbles))

        return index

    def add_marble(self, current_player):
        if self.last_marble_value == None:
            self.last_marble_value = 0
            self.marbles.append(0)
        else:
            new_marble_val = self.last_marble_value +1

            if new_marble_val % 23 == 0:
                print_debug("Special case - marble is a multiple of 23")
                self.scoreboard[current_player]["score"]+=new_marble_val
                self.scoreboard[current_player]["marbles"].append(new_marble_val)
                print_debug("Adding {} to the score of player {}".format(new_marble_val, current_player))


                left_index = self.get_new_index(7, go_clockwise=False)
                print_debug("left_index is {}".format(left_index))


                removed_marble_value = self.remove_marble_from_circle(left_index)
                self.scoreboard[current_player]["score"] += removed_marble_value
                self.scoreboard[current_player]["marbles"].append(removed_marble_value)
                print_debug("Adding {} to the score of player {}".format(removed_marble_value, current_player))

                clockwise_index = self.get_clockwise_index_from_index(left_index)
                print_debug("clockwise_index from {} is {}".format(left_index, clockwise_index))
                self.current_marble_index = clockwise_index
                print_debug("current_marble_index now equals {}".format(self.current_marble_index))
                self.last_marble_value = new_marble_val
                pass


            else:
                left_index = self.get_new_index(1)
                #right_index = self.get_new_index(2)

                self.insert_marble_into_circle(new_marble_val, left_index)
                self.last_marble_value = new_marble_val
                #print_debug("Inserting new marble ({})".format(new_marble_val))

            #self.marbles.append(new_marble_val)

        pass


    def get_marbles_string(self):
        mystring = ""
        count = 0
        for marble in self.marbles:
            if count == self.current_marble_index:
                mystring+="  ("+str(marble)+")"
            else:
                mystring+="   "+str(marble)
            count+=1

        return mystring

    def step(self):
        if self.marbles == []:
            self.add_marble(self.current_player)
            self.current_marble_index = 0
            print_debug("[-]{}".format(self.get_marbles_string()))

        else:

            #self.current_marble_index = random.randint(0, len(self.marbles))
            if self.current_player == self.num_players:
                self.current_player = 1
            else:
                self.current_player+=1
            self.add_marble(self.current_player)
            print_debug("[{}]{}".format(self.current_player, self.get_marbles_string()))

        pass
        print_debug("")



def day_9_part1():
    return  "DISABLED"
    lines = read_file_into_list("problem_9_dummy_input.txt")
    #lines = read_file_into_list("problem_9_input.txt")

    line = lines[0]

    number_of_players = int(line.split(" ")[0])
    last_marble_points = int(line.split(" ")[6])

    print_debug("number_of_players is {}".format(number_of_players))
    print_debug("last_marble_points is {}".format(last_marble_points))
    print_debug("")

    myGame = CircleGame(number_of_players, last_marble_points)
    for _ in range(last_marble_points+1):
        myGame.step()
    return myGame.print_scoreboard()


class CircleGame_Part2:

    def __init__(self, number_of_players, last_marble_points, myCircle):
        self.circular_linked_list = myCircle

        self.current_marble_index = 0 #None
        self.num_players = number_of_players
        self.current_player = 0

        self.marbles = []

        self.last_marble_value = None

        self.scoreboard = {}
        self.scoreboard_p2 = {}
        self.init_scoreboard()
        self.current_marble_index_pt2 = 0
        self.currentMarble = None

        self.num_marbles = 0
    def init_scoreboard(self):
        for playerID in range(1, self.num_players+1):
            self.scoreboard[playerID] = {"score": 0, "marbles": []}
            self.scoreboard_p2[playerID] = {"score": 0, "marbles": []}
    def print_scoreboard(self):

        print("\n\n\nScoreboard dictionary for part 1 is:\n{}\n".format(self.scoreboard))

        print("\n\nThe scoreboard for part 1 is:")
        for playerID in self.scoreboard:
            print("Player {} has the score {}".format(playerID, self.scoreboard[playerID]["score"]))
        print_debug("\n\n")

        highest_scoring_player = 0
        highest_scoring_player_score = 0
        for playerID in self.scoreboard:
            if self.scoreboard[playerID]["score"] > highest_scoring_player_score:
                highest_scoring_player_score = self.scoreboard[playerID]["score"]
                highest_scoring_player = playerID

        print("\n\n\nScoreboard dictionary for part 2 is:\n{}\n".format(self.scoreboard_p2))

        print("\n\nThe scoreboard for part 2 is:")
        for playerID in self.scoreboard_p2:
            print("Player {} has the score {}".format(playerID, self.scoreboard_p2[playerID]["score"]))
        print("\n\n")

        highest_scoring_player = 0
        highest_scoring_player_score = 0
        for playerID in self.scoreboard_p2:
            if self.scoreboard_p2[playerID]["score"] > highest_scoring_player_score:
                highest_scoring_player_score = self.scoreboard_p2[playerID]["score"]
                highest_scoring_player = playerID

        return_string = "Highest scoring player for part 2 was player {} with a score of {}".format(highest_scoring_player, highest_scoring_player_score)
        print_debug(return_string)

        return return_string
    def get_clockwise_index_from_index(self, index):
        num_steps = int((len(self.marbles) ))

        num_steps = num_steps % (len(self.marbles))

        index = self.current_marble_index + num_steps  # % len(self.marbles)
        print_debug("--->> num_steps is {}".format(num_steps))
        index = index

        return index

    def get_clockwise_index_from_index_pt2(self, index):


        return self.current_marble_index




    def remove_marble_from_circle(self, left_index):
        pass
        print_debug("current_marble_index is {}".format(self.current_marble_index))
        #print_debug("left_index is {}".format(left_index))
        # print_debug("right_index is {}".format(right_index))

        # print_debug("Therefore our new index is {}".format(None))
        try:
            return_val = self.marbles.pop(left_index )
            #self.num_marbles -=1
            #return_val = self.marbles[-1]
        except IndexError:
            return_val = 0
        # self.marbles.append(marble)
        #self.current_marble_index_pt2 = left_index
        self.current_marble_index = left_index

        print_debug("removing the marble {} at index {}".format(return_val, left_index))
        return return_val

    def insert_marble_into_circle(self, marble, left_index):
        pass
        print_debug("current_marble_index is {}".format(self.current_marble_index))
        print_debug("left_index is {}".format(left_index))
        #print_debug("right_index is {}".format(right_index))

        #print_debug("Therefore our new index is {}".format(None))

        self.marbles.insert(left_index+1, marble)
        #self.marbles.append(marble)

        self.current_marble_index = left_index+1
        self.current_marble_index_pt2 = left_index+1

            #self.current_marble_index =

    def get_new_index(self, num_steps, go_clockwise=True):
        index = None
        if go_clockwise is True:
            index = self.current_marble_index + num_steps #% len(self.marbles)

            index = index % (len(self.marbles))

        else:
            index = self.current_marble_index - num_steps
            index = index % (len(self.marbles))

        return index

    def get_new_index_pt2(self, num_steps, go_clockwise=True):
        index = None
        if go_clockwise is True:
            index = self.current_marble_index_pt2 + num_steps  # % len(self.marbles)

            index = index % self.num_marbles

        else:
            index = self.current_marble_index_pt2 - num_steps
            index = index % self.num_marbles

        return index

    def p2_get_marble_N_steps(self, num_steps, go_clockwise=True):
        returned_node = None
        if go_clockwise is True:

            count = 0
            returned_node = self.currentMarble or self.circular_linked_list.first
            while count < num_steps:
                returned_node = returned_node.next
                count+=1

        else:
            count = 0
            returned_node = self.currentMarble or self.circular_linked_list.first
            while count < num_steps:
                returned_node = returned_node.prev
                count+=1


        return returned_node

    def add_marble(self, current_player):
        if self.last_marble_value == None:
            self.last_marble_value = 0
            self.marbles.append(0)


            #part 2
            new_node = DoubleLinkedNode(0)
            self.circular_linked_list.insert_at_end(new_node)
            self.num_marbles+=1
        else:
            new_marble_val = self.last_marble_value +1

            if new_marble_val % 23 == 0:
                print_debug("Special case - marble is a multiple of 23")

                #part 1

                self.scoreboard[current_player]["score"]+=new_marble_val
                self.scoreboard[current_player]["marbles"].append(new_marble_val)
                print_debug("Adding {} to the score of player {}".format(new_marble_val, current_player))
                left_index = self.get_new_index_pt2(7, go_clockwise=False)
                print_debug("left_index is {}".format(left_index))
                removed_marble_value = self.remove_marble_from_circle(left_index)
                #self.current_marble_index = left_index
                self.scoreboard[current_player]["score"] += removed_marble_value
                self.scoreboard[current_player]["marbles"].append(removed_marble_value)
                print_debug("Adding {} to the score of player {}".format(removed_marble_value, current_player))
                clockwise_index = self.get_clockwise_index_from_index_pt2(left_index)
                print_debug("clockwise_index from {} is {}".format(left_index, clockwise_index))
                self.current_marble_index = clockwise_index
                print_debug("current_marble_index now equals {}".format(self.current_marble_index))
                self.last_marble_value = new_marble_val




                #part 2
                self.scoreboard_p2[current_player]["score"]+=new_marble_val
                self.scoreboard_p2[current_player]["marbles"].append(new_marble_val)
                myindex = self.get_new_index_pt2(7, go_clockwise=False)


                self.current_marble_index = myindex


                self.current_marble_index_pt2 = myindex
                clockwise_index = self.get_clockwise_index_from_index_pt2(myindex)

                self.current_marble_index_pt2 = clockwise_index
                

                node_to_remove = self.p2_get_marble_N_steps(7, go_clockwise=False) #self.circular_linked_list.get_node(left_index)
                #clockwise_index =
                #print_debug("\n\n\n\node node_to_remove val is {}. next val is {}. prev val is {}".format(node_to_remove.data, node_to_remove.next.data, node_to_remove.prev.data))
                #print_debug("removed_marble_value for pt1 is {}".format(removed_marble_value))

                self.scoreboard_p2[current_player]["score"] += node_to_remove.data
                self.scoreboard_p2[current_player]["marbles"].append(node_to_remove.data)

                self.circular_linked_list.remove(node_to_remove)

                self.currentMarble = self.circular_linked_list.get_node(self.current_marble_index_pt2)
                #self.currentMarble = self.circular_linked_list.get_node(myindex)
                self.last_marble_value = new_marble_val
                #print_debug("")

                self.num_marbles -= 1

            else:

                self.num_marbles += 1

                #part 1
                
                #left_index = self.get_new_index(1)
                left_index = self.get_new_index_pt2(0)
                self.insert_marble_into_circle(new_marble_val, left_index)
                self.last_marble_value = new_marble_val


                #part 2
                #left_index = self.p2_get_new_index(1)]
                myindex = self.get_new_index_pt2(0)
                #myindex = self.get_new_index_pt2(0)
                self.current_marble_index_pt2 = myindex
                #self.current_marble_index  = myindex
                self.last_marble_value = new_marble_val
                new_node = DoubleLinkedNode(new_marble_val)

                neighbour = self.p2_get_marble_N_steps(1)

                self.circular_linked_list.insert_after(neighbour, new_node)
                self.currentMarble = new_node
        pass


    def get_marbles_string(self):
        mystring = ""
        count = 0
        for marble in self.marbles:
            if count == self.current_marble_index:
                mystring+="  ("+str(marble)+")"
            else:
                mystring+="   "+str(marble)
            count+=1

        return mystring


    def p2_get_marbles_string(self):
        mystring = self.circular_linked_list.get_string()

        return mystring

    def step(self):

        if self.circular_linked_list.get_node(0) is None:
            print_debug("Got to here - get_node(0) returned None")

            self.add_marble(self.current_player)
            self.current_marble_index = 0
            self.current_marble_index_pt2 = 0
            print_debug("[pt1 - p-]{}".format(self.get_marbles_string()))
            print_debug("[pt2 - p-]{}".format(self.p2_get_marbles_string()))
            #print_debug("Current node for part 2 is {}".format(self.currentMarble.data))
        else:
            pass

            #self.current_marble_index = random.randint(0, len(self.marbles))
            if self.current_player == self.num_players:
                self.current_player = 1
            else:
                self.current_player+=1
            self.add_marble(self.current_player)
            print_debug("[pt1 - p{}]{}".format(self.current_player, self.get_marbles_string()))
            print_debug("[pt2 - p{}]{}".format(self.current_player, self.p2_get_marbles_string()))
            print_debug("Current node for part 2 is {}".format(self.currentMarble.data))

        pass
        print_debug("")




#https://www.sanfoundry.com/python-program-implement-circular-doubly-linked-list/
class DoubleLinkedNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class CircularDoublyLinkedList:
    def __init__(self):
        self.first = None

    def get_node(self, index):
        current = self.first
        for i in range(index):
            current = current.next
            if current == self.first:
                return None
        return current

    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def insert_before(self, ref_node, new_node):
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node):
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.first.prev, new_node)

    def insert_at_beg(self, new_node):
        self.insert_at_end(new_node)
        self.first = new_node

    def remove(self, node):
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next

    def get_string(self):
        myString = ""
        if self.first is None:
            return
        current = self.first
        while True:
            #print(current.data, end=' ')
            myString+="   "+str(current.data)
            current = current.next
            if current == self.first:
                break
        return myString










#https://www.reddit.com/r/adventofcode/comments/a4i97s/2018_day_9_solutions/
def play_game(max_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values()) if scores else 0





def day_9_part2():




    myCircle = CircularDoublyLinkedList()


    lines = read_file_into_list("problem_9_dummy_input.txt")
    #lines = read_file_into_list("problem_9_input.txt")

    line = lines[0]

    number_of_players = int(line.split(" ")[0])
    last_marble_points = int(line.split(" ")[6]) *100

    print_debug("number_of_players is {}".format(number_of_players))
    print_debug("last_marble_points is {}".format(last_marble_points))
    print_debug("")


    game_result = str(play_game(number_of_players, last_marble_points))
    return "The answer when number_of_players is {} and last_marble_points is {} is:\n{}".format(number_of_players, last_marble_points, game_result)

    """
    myGame = CircleGame_Part2(number_of_players, last_marble_points, myCircle)
    for _ in range((last_marble_points)+1):
    #for _ in range(60):
        myGame.step()
        pass
    return myGame.print_scoreboard()
    """



    """
    for num in range(10):
        print_debug("Adding {} to list".format(num))
        new_node = DoubleLinkedNode(num)
        myCircle.insert_at_end(new_node)

    print_debug("\n\n\n\nPrinting circle:")
    myCircle.display()

    print_debug("\n\n")
    """

    """

    myList = MyLinkedList()

    for num in range(10):
        print_debug("Adding {} to list".format(num))
        myList.insert_to_end(num)

    print_debug("\n\n\n\n\n")
    print_debug("Forwards list for part 2 is:")
    print_debug("{}".format(myList.get_string()))
    print_debug("Backwards list for part 2 is:")
    print_debug("{}".format(myList.get_backwards_string()))
    print_debug("\n\n\n\n\n")

    myList.print_internal_state()

    :return:
    """


    """


    """









def day_8_part1__():
    lines = read_file_into_list("problem_8_dummy_input.txt")
    #lines = read_file_into_list("problem_8_input.txt")

    num_list_initial = lines[0].split(" ")

    num_list = [ int(x) for x in num_list_initial ]


    myTree = HeaderTree(num_list)

    myTree.pretty_print()
    for _ in num_list:
        myTree.get_new_node_id()


    #try 2

    """
    2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
    A----------------------------------
        B----------- C-----------
                         D-----
    """

    myList = [{"name": "A1",
               "children": ["B1", "C1"],
               "metadatas": [1, 1, 2]},
              {"name": "B1",
               "children": [],
               "metadatas": [10, 11, 12]},
              {"name": "C1",
               "children": ["D1"],
               "metadatas": [2]},
              {"name": "D1",
               "children": [],
               "metadatas": [99]},
              ]



    #answer = get_day_8_answer(myList)

    id_generator = ID_generator()
    answer1 = construct_dict(num_list, {}, id_generator, [])

    print_debug("answer1 is {}".format(answer1))

    #myTree.pretty_print()

    #print_debug(num_list)

    return answer1

    pass

































class Star:

    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel

    def pretty_print(self):
        print_debug("I am a star at postion {},{}. My velocity is {},{}".format(self.x_pos,
                                                                                self.y_pos,
                                                                                self.x_vel,
                                                                                self.y_vel))
class Sky:


    def init_board(self, lines):

        for line in lines:
            #print_debug("Looking at line: '{}'".format(line))


            num_list = line.split("position=<")[1].replace("> velocity=<", ",").replace(">", "").replace(" ", "").split(",")
            #print_debug("num_list is {}".format(num_list))

            x_pos = int(num_list[0])
            #print_debug("x_pos is {}".format(x_pos))

            y_pos = int(num_list[1])
            #print_debug("y_pos is {}".format(y_pos))

            x_vel = int(num_list[2])
            #print_debug("x_vel is {}".format(x_vel))

            y_vel = int(num_list[3])
            #print_debug("y_vel is {}".format(y_vel))

            #print_debug("")



            new_star = Star(x_pos, y_pos, x_vel, y_vel)

            self.star_list.append(new_star)


    def do_initial_translate_using_first_star(self):
        first_x = self.star_list[0].x_pos
        first_y = self.star_list[0].y_pos

        for star in self.star_list:
            star.x_pos = star.x_pos - first_x
            star.y_pos = star.y_pos - first_y

    def print_star_list(self):
        for star in self.star_list:
            star.pretty_print()


    def __init__(self, lines):

        self.star_list = []

        #keep these even as I divide by 2 when I print it
        #self.BOARD_HEIGHT = 128 ; self.BOARD_WIDTH = 256

        self.BOARD_HEIGHT = 40 ; self.BOARD_WIDTH = 128

        self.init_board(lines)
        self.num_steps_done = 0
        pass


    def get_approximate_points(self, star_list):
        new_star_list = []

        value_to_divide_by = 1000
        for star in self.star_list:

            #print_debug("Looking at point ({}, {}):".format(star.x_pos, star.y_pos))
            if abs(star.x_pos) > value_to_divide_by and abs(star.y_pos) > value_to_divide_by:
                new_x = int(star.x_pos / value_to_divide_by)
                new_y = int(star.y_pos / value_to_divide_by)
            else:
                new_x = star.x_pos
                new_y = star.y_pos

            #print_debug("I changed it to the point ({}, {})".format(new_x, new_y))
            #print_debug("")
            new_star_list.append((new_x, new_y))

        return new_star_list


    def translate_from_first_star(self, star_list):
        new_star_list = []
        first_x = star_list[0][0]
        first_y = star_list[0][1]

        new_star_list = [(star_pos_tuple[0] - first_x, star_pos_tuple[1] - first_y) for star_pos_tuple in star_list]

        return new_star_list



    def print_board(self):
        print_debug("\n\n\n\n\n\n\n\n")
        print_debug("Printing board:")
        print_debug("Dimensions are: (Height {} by Width {})".format(self.BOARD_HEIGHT, self.BOARD_WIDTH))

        star_points = [(star.x_pos, star.y_pos) for star in self.star_list]
        print_debug("star_points before doing any processing is {}".format(star_points))


        #do translation using first point
        #star_points = self.translate_from_first_star(star_points)


        #disabled for now, unsure if this makes sense
        #star_points = self.get_approximate_points(star_points)

        print_debug("\n\n")
        print_debug("star_points after doing processsing is {}".format(star_points))
        board_string = ""

        number_of_stars_on_board = 0
        for ypos in range(-int(self.BOARD_HEIGHT/2), int(self.BOARD_HEIGHT/2)):
            for xpos in range(-int(self.BOARD_WIDTH/2), int(self.BOARD_WIDTH/2)):

                current_pos = (xpos, ypos)
                #print_debug("")
                if current_pos in star_points:
                    number_of_stars_on_board+=1
                    if current_pos == (0, 0):
                        board_string += "*"
                    else:
                        board_string += "#"
                elif current_pos == (0, 0):
                    board_string+="+"
                else:
                    board_string+="."
            board_string+="\n"
        print_debug("\nNumber_of_stars_on_board is {}".format(number_of_stars_on_board))
        print_debug(board_string)
        print_debug("\n\n\n\n")


    def count_points_on_screen(self):

        star_points = [(star.x_pos, star.y_pos) for star in self.star_list]


        #do translation using first point
        star_points = self.translate_from_first_star(star_points)



        number_of_stars_on_board = 0
        for ypos in range(-int(self.BOARD_HEIGHT/2), int(self.BOARD_HEIGHT/2)):
            for xpos in range(-int(self.BOARD_WIDTH/2), int(self.BOARD_WIDTH/2)):

                current_pos = (xpos, ypos)
                if current_pos in star_points:
                    number_of_stars_on_board+=1

        return number_of_stars_on_board

    def step(self):
        self.num_steps_done+=1
        #print_debug("Starting step")
        for star in self.star_list:
            star.x_pos = star.x_pos + (star.x_vel)
            star.y_pos = star.y_pos + (star.y_vel)

    def step_until_at_least_N_points_on_screen(self, N):
        num_steps = 0
        while self.count_points_on_screen() < N:
            self.step()
            num_steps+=1
        pass

    def step_until_exactly_N_points_on_screen(self, N):
        num_steps = 0
        while self.count_points_on_screen() != N:
            #print_debug("N is {} and self.count_points_on_screen() is {}".format(N, self.count_points_on_screen()))
            self.step()
            num_steps+=1
        pass

        return num_steps

    def step_N(self, N):
        for _ in range(N):
            self.step()

    def get_steps_done(self):
        return self.num_steps_done


def day_10_part1():
    lines = read_file_into_list("problem_10_dummy_input.txt") ; num_stars = 10
    #lines = read_file_into_list("problem_10_input.txt") ; num_stars = 300


    mySky = Sky(lines)
    #mySky.print_star_list()
    #mySky.print_board()

    #print_debug("doing initial translate")
    mySky.do_initial_translate_using_first_star()
    #mySky.print_board()

    mySky.step_until_at_least_N_points_on_screen(num_stars)
    #mySky.step_until_exactly_N_points_on_screen(10)
    #mySky.step_N(3)
    #mySky.do_initial_translate_using_first_star()


    #mySky.step_N(10000)
    #mySky.do_initial_translate_using_first_star()
    mySky.do_initial_translate_using_first_star()

    #mySky.print_board()

    for _ in range(2):
        #mySky.do_initial_translate_using_first_star()

        mySky.step()
        mySky.print_board()

    #mySky.print_star_list()

    #print_debug("lines is {}".format(lines))
    return "Number of steps done is {}".format(mySky.get_steps_done())



class PowerGrid:

    #See this for explanation: https://computersciencesource.wordpress.com/2010/09/03/computer-vision-the-integral-image/
    def internet_answer(self):

        serial = 8772
        grid_sums, partial_sums = {}, defaultdict(int)

        power_level = lambda x, y: ((((x + 10) * y + serial) * (x + 10)) // 10 ** 2 % 10) - 5
        calculate_ps = lambda x, y: (power_level(x + 1, y + 1)
                                     + partial_sums[x, y - 1] + partial_sums[x - 1, y] - partial_sums[x - 1, y - 1])

        for j in range(300):
            for i in range(300):
                partial_sums[(i, j)] = calculate_ps(i, j)

        for size in range(2, 300):
            for j in range(size - 1, 300):
                for i in range(size - 1, 300):
                    gp = partial_sums[(i, j)] + partial_sums[(i - size, j - size)] \
                         - partial_sums[(i - size, j)] - partial_sums[(i, j - size)]
                    grid_sums[gp] = (i - size + 2, j - size + 2, size)
            if size == 3:
                x3, y3, s3 = map(str, grid_sums[max(grid_sums)])
                print("Day 11 part 1: " + x3 + "," + y3)

        print("Day 11 part 2: %d,%d,%d" % grid_sums[max(grid_sums)])


    def get_power_level(self, x, y):

        print_debug("Looking at coordinate {}, {}:".format(x, y))

        #Rack ID
        rack_id = x+10
        print_debug("rack_id is {}".format(rack_id))


        power_level_start = rack_id * y
        #print_debug("power_level_start is {}".format(power_level_start))
        power_level_with_serial_number = power_level_start + self.serial_number
        #print_debug("power_level_with_serial_number is {}".format(power_level_with_serial_number))
        power_level_times_rack = power_level_with_serial_number * rack_id
        #print_debug("power_level_times_rack is {}".format(power_level_times_rack))

        tens_digit = (power_level_times_rack // 100)%10
        #print_debug("tens_digit is {}".format(tens_digit))

        final_power = tens_digit - 5
        #print_debug("final_power is {}".format(final_power))

        #print_debug("")
        return final_power

    def init_board(self):

        for y in range(self.y_max):
            mylist = []
            for x in range(self.x_max):
                mylist.append(self.get_power_level(x,y))

            self.grid.append(mylist)

    def __init__(self):
        self.x_max = 10; self.y_max = 10

        #self.x_max = 300 ; self.y_max = 300
        self.grid = []
        self.serial_number = 8772

        self.init_board()

    def pretty_print(self):
        print_string = ""
        for mylist in self.grid:
            for x in mylist:
                if x >=0:
                    print_string += "  "+str(x)
                else:
                    print_string += " "+str(x)

            print_string+="\n"
        print_debug(print_string)

    def search_grid(self):

        answer_power = 0
        answer_x = 0
        answer_y = 0


        y=0
        for mylist in self.grid:
            x =0
            for elem in mylist:
                #do something
                print_debug("Looking at coordinate {}, {}:".format(x+1, y+1))
                found_square = True
                power_this_cell = 0
                small_grid_string = ""
                for i in range(3):
                    row_string = ""
                    for j in range(3):

                        try:
                            power = self.grid[x + i][y + j]
                            row_string += "  " + str(power)
                            power_this_cell += power

                        except IndexError:
                            found_square = False
                            #row_string += "    "
                            pass
                    small_grid_string += row_string +"\n"
                print_debug("power_this_cell is {}".format(power_this_cell))
                print_debug("small_grid_string is:\n{}".format(small_grid_string))
                print_debug("")

                if found_square is True and power_this_cell > answer_power:
                    answer_power = power_this_cell
                    answer_x = y
                    answer_y = x
                    answer_grid = small_grid_string

                x+=1
            y+=1

        answer_string = "answer_x is {}, answer_y is {}, answer_power is {}, answer_grid is \n{}".format(answer_x, answer_y, answer_power, answer_grid)
        return answer_string



    def search_grid_for_biggest(self):

        answer_power = 0
        answer_x = 0
        answer_y = 0


        y=0
        for mylist in self.grid:
            x =0
            for elem in mylist:
                #do something
                print_debug("Looking at coordinate {}, {}:".format(x+1, y+1))
                found_square = True
                power_this_cell = 0
                small_grid_string = ""
                for i in range(3):
                    row_string = ""
                    for j in range(3):

                        try:
                            power = self.grid[x + i][y + j]
                            row_string += "  " + str(power)
                            power_this_cell += power

                        except IndexError:
                            found_square = False
                            #row_string += "    "
                            pass
                    small_grid_string += row_string +"\n"
                print_debug("power_this_cell is {}".format(power_this_cell))
                print_debug("small_grid_string is:\n{}".format(small_grid_string))
                print_debug("")

                if found_square is True and power_this_cell > answer_power:
                    answer_power = power_this_cell
                    answer_x = y
                    answer_y = x
                    answer_grid = small_grid_string

                x+=1
            y+=1

        answer_string = "answer_x is {}, answer_y is {}, answer_power is {}, answer_grid is \n{}".format(answer_x, answer_y, answer_power, answer_grid)
        return answer_string


def day_11_part1():
    return "DISABLED"
    myPowerGrid = PowerGrid()
    answer = myPowerGrid.search_grid()
    myPowerGrid.pretty_print()


    #myPowerGrid.internet_answer()
    return answer




def day_11_part2():
    return "DISABLED"

    myPowerGrid = PowerGrid()
    answer = myPowerGrid.search_grid_for_biggest()
    myPowerGrid.pretty_print()


    myPowerGrid.internet_answer()
    return answer


def get_next_generation(input_state, rule_list):
    #print_debug("\n")
    #print_debug("\nInput state was: '{}'".format(input_state))

    next_state = ""

    i = 0
    for mychar in input_state:

        try:
            first_left = input_state[i-1]
        except IndexError:
            first_left = "."

        try:
            second_left = input_state[i-2]
        except IndexError:
            second_left = "."

        try:
            first_right = input_state[i+1]
        except IndexError:
            first_right = "."

        try:
            second_right = input_state[i+2]
        except IndexError:
            second_right = "."


        pattern = second_left + first_left + mychar + first_right + second_right

        output_char = "."
        for rule in rule_list:
            if pattern == rule[0]:
                output_char = rule[1]

        print_debug("For char {} at index {} the pattern is {}, therefore output is {}".format(mychar,i,pattern, output_char))
        i+=1
        pass

        next_state+=output_char


    #print_debug("Next state is:   '{}'".format(next_state))


    #print_debug("\n")

    return next_state

def get_sum_from_state(input_state):

    index = -3

    sum = 0
    for mychar in input_state:
        if mychar == "#":
            sum+=index

        index +=1
    return sum

def day12_internet_answer():
    import collections
    import re

    def nextg(cur, recipe):
        start = min(cur)
        end = max(cur)
        x = set()

        for i in range(start - 3, end + 4):
            pat = ''.join('#' if i + k in cur else '.' for k in [-2, -1, 0, 1, 2])
            if pat in recipe:
                x.add(i)

        return x

    def viz(cur):
        print(''.join('#' if i in cur else '.' for i in xrange(-5, 120)))

    # with open('day12test.txt') as f:
    with open('problem_12_input.txt') as f:
        lines = [l.rstrip('\n') for l in f]
        print(lines)

        init = lines[0][len('initial state: '):]
        recipe = set()
        for l in lines[2:]:
            if l[-1] == '#':  # I forgot this line the first time around.
                recipe.add(l[:5])

        cur = set(i for i, c in enumerate(init) if c == '#')

        # Part 1:
        for i in range(20):
            cur = nextg(cur, recipe)
        print("Part 1 - {}".format(sum(cur)))

        """
        # Part 2:
        ls = 0
        # viz(cur)
        for i in xrange(2000):
            cur = nextg(cur, recipe)
            # viz(cur)
            s = sum(cur)
            print
            i, s, s - ls
            ls = s
        print sum(cur)
        """
def day_12_part1():
    return "DISABLED"

    lines = read_file_into_list("problem_12_dummy_input.txt")
    lines = read_file_into_list("problem_12_input.txt")

    initial_state = "..."+lines[0].replace("initial state: ", "") +"..........."

    rule_list = []

    for line in lines[2:]:
        pattern = line.split(" => ")[0]
        output =  line.split(" => ")[1]
        if output == "#":
            rule_list.append((pattern, output))

    #
    print_debug("initial_state is {}".format(initial_state))
    print_debug("rule_list is {}".format(rule_list))
    print_debug("\n\n\n\n")
    #print_debug("                 1         2         3")
    print_debug("        0         0         0         0")


    for gen in range(21):
        print_string = ""

        if gen < 10:
            print_string +="{}:   ".format(gen)
        else:
            print_string += "{}:  ".format(gen)

        if gen == 0:
            current_state = initial_state
        else:
            current_state = get_next_generation(current_state, rule_list)

        for mychar in current_state:
            print_string+="{}".format(mychar)

        print_string +="     sum = {}".format(get_sum_from_state(current_state))

        print_debug(print_string)

    print_debug("\n\n\n\n")
    day12_internet_answer()

    return "WIP"









def day_12_part2():

    return "DISABLED"
    import collections
    import re

    number_of_generations = 20
    part_1_answer = "Part 1 answer - Part 1 answer is WIP"
    part_2_answer = "Part 2 answer - Part 2 answer is WIP"
    #number_of_generations = 50000000000
    def nextg(cur, recipe):
        start = min(cur)
        end = max(cur)
        x = set()

        for i in range(start - 3, end + 4):
            pat = ''.join('#' if i + k in cur else '.' for k in [-2, -1, 0, 1, 2])
            if pat in recipe:
                x.add(i)

        return x

    def viz(cur):
        print_debug(''.join('#' if i in cur else '.' for i in xrange(-5, 120)))

    # with open('day12test.txt') as f:
    with open('problem_12_input.txt') as f:
        lines = [l.rstrip('\n') for l in f]
        print_debug(lines)

        init = lines[0][len('initial state: '):]
        recipe = set()
        for l in lines[2:]:
            if l[-1] == '#':  # I forgot this line the first time around.
                recipe.add(l[:5])

        cur = set(i for i, c in enumerate(init) if c == '#')

        # Part 1:
        for i in range(number_of_generations):
            #print_debug("cur is {}".format(cur))
            cur = nextg(cur, recipe)
        part_1_answer =  "Part 1 answer - After {} generations, the answer is {}".format(number_of_generations ,sum(cur))


        # Part 2:
        cur = set(i for i, c in enumerate(init) if c == '#')
        #print_debug("\n\ntest is {}\n\n".format([ counter for counter, value in enumerate(init) if value == '#' ]))

        """

        found = False
        first_repeat = None
        first_repeat_index = None
        num_gens = 5000
        seen = []
        for i in range(num_gens):
            #print_debug("Looking at generation {}:".format(i))
            cur = nextg(cur, recipe)
            #print_debug("cur is {}".format(cur))
            if cur in seen:
                found = True
                first_repeat_index = cur
                first_repeat_index = i
            print_debug("\n")
            seen.append(cur)


        print_debug("\n\n\n\n\n")
        print_debug("first_repeat is {}".format(first_repeat))
        print_debug("first_repeat_index is {}".format(first_repeat_index))

        print_debug("\n\n\n\n\n")



        print_debug("seen_size is {}".format(len(seen)))
        print_debug("seen is {}".format(seen))
        

        part_2_answer = "Part 2 answer - After {} generations, the answer is {}".format(num_gens, sum(cur))
        """




        ls = 0
        # viz(cur)
        for i in range(2000):
            cur = nextg(cur, recipe)
            # viz(cur)
            s = sum(cur)
            print( i, s, s - ls)
            ls = s
        ans = sum(cur)
        print_debug("ans is {}".format(ans))

        # By inspection we can see that every generation after 167 adds 75
        first_part_answer = 0

        for i in range(2000):
            cur = nextg(cur, recipe)
        first_part_answer = sum(cur)

        remaining = (50000000000 - 2000) * 75
        print_debug("\nfirst_part_answer is {}".format(first_part_answer))
        print_debug("remaining is {}\n".format(remaining))
        part_2_answer = "Part 2 answer is {}".format(ans + remaining)




        return part_1_answer + "\n"+ part_2_answer






class MineCart:

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_string(self):

        mystring = ""
        mystring += "MineCart:\n".format()
        mystring += "self.x_pos is {}\n".format(self.x_pos)
        mystring += "self.y_pos is {}\n".format(self.y_pos)
        mystring += "\n"

        return mystring


class TrackSegment:

    def __init__(self, x_pos, y_pos, track_shape, left_neigbour, right_neigbour, up_neigbour, down_neigbour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.track_shape = track_shape   #EG '\', '+', '-' etc

        self.left_neigbour = left_neigbour
        self.right_neigbour = right_neigbour
        self.up_neigbour = up_neigbour
        self.down_neigbour = down_neigbour


        self.minecart = None


    def get_small_string(self):

        mystring = "Tracksegment: "
        mystring += "self.x_pos is {}, ".format(self.x_pos)
        mystring += "self.y_pos is {}, ".format(self.y_pos)
        mystring += "self.track_shape is {}. ".format(self.track_shape)
        return mystring

    def get_num_neighbours(self):
        num_neighbours = 0
        if self.left_neigbour:
            num_neighbours+=1
        if self.right_neigbour:
            num_neighbours+=1

        if self.up_neigbour:
            num_neighbours+=1

        if self.down_neigbour:
            num_neighbours+=1

        return num_neighbours

    def get_string(self):

        mystring = ""
        mystring += "TrackSegment:\n".format()
        mystring += "self.x_pos is {}\n".format(self.x_pos)
        mystring += "self.y_pos is {}\n".format(self.y_pos)
        mystring += "self.track_shape is {}\n".format(self.track_shape)


        if self.left_neigbour:
            mystring += "self.left_neigbour is:\n    {}\n".format(self.left_neigbour.get_small_string())

        if self.right_neigbour:
            mystring += "self.right_neigbour is:\n    {}\n".format(self.right_neigbour.get_small_string())

        if self.up_neigbour:
            mystring += "self.up_neigbour is:\n    {}\n".format(self.up_neigbour.get_small_string())

        if self.down_neigbour:
            mystring += "self.down_neigbour is:\n    {}\n".format(self.down_neigbour.get_small_string())


        mystring += "\n"

        return mystring


class Track:




    def internet_answer(self):
        from itertools import product
        with open('problem_13_input.txt', 'r') as ifile:
            rlmap = [list(line.strip('\n')) for line in ifile]
        carts = []
        for y, x in product(range(len(rlmap)), range(len(rlmap[0]))):
            if rlmap[y][x] in '>v<^':
                crdir = '>v<^'.index(rlmap[y][x])
                rlmap[y][x] = '-|'[crdir & 1]
                carts.append([y, x, crdir, 0, True])
        crash = False
        while len(carts) > 1:
            carts.sort(key=lambda i: tuple(i[:2]))
            for cart1 in carts:
                if not cart1[-1]:
                    continue
                if rlmap[cart1[0]][cart1[1]] == '/':
                    cart1[2] = (3, 2, 1, 0)[cart1[2]]
                elif rlmap[cart1[0]][cart1[1]] == '\\':
                    cart1[2] = (1, 0, 3, 2)[cart1[2]]
                elif rlmap[cart1[0]][cart1[1]] == '+':
                    cart1[2] = (cart1[2] + (-1, 0, 1)[cart1[3]]) & 3
                    cart1[3] = (cart1[3] + 1) % 3
                cart1[0] += (0, 1, 0, -1)[cart1[2]]
                cart1[1] += (1, 0, -1, 0)[cart1[2]]
                for cart2 in carts:
                    if cart2[-1] and cart1 is not cart2 and cart1[:2] == cart2[:2]:
                        cart1[-1] = cart2[-1] = False
                        if not crash:
                            crash = True
                            print(cart1[:2][::-1])  # 1
                        break
            carts = list(filter(lambda i: i[-1], carts))
        print(carts[0][:2][::-1])  # 2



    def __init__(self, lines):
        self.coord_to_track_dict = {}


        self.track_dict = {}

        self.minecarts = []

        self.init_track(lines)

        self.collisions = []


    def move_minecart(self):
        pass

    def step(self):
        mystring = ""
        for y in range(160):
            for x in range(160):
                found_segment = self.track_dict.get((x, y))
                if found_segment:

                    if found_segment.minecart:
                        self.move_minecart(found_segment.minecart)



        return mystring


    def run_simulation(self):
        #while True:

        #print_debug(self.pretty_print_track_dict())

        pass


    def pretty_print_track_dict(self):

        # real input is 150 x 150
        mystring = ""
        for y in range (160):
            for x in range(160):
                found_segment = self.track_dict.get((x,y))
                if found_segment:
                    mystring += found_segment.track_shape
                else:
                    mystring += " "
            mystring +="\n"

        return mystring

    def init_track(self, lines):


        print_debug("\n\n\n\n")
        y = 0
        for line in lines:
            x =0
            for mychar in line:

                if mychar != " ":
                    self.coord_to_track_dict[(x,y)] = TrackSegment(x,y, mychar, None, None, None, None)
                x+=1
            y+=1



        for key in self.coord_to_track_dict:

            my_x = key[0]
            my_y = key[1]
            my_char =  self.coord_to_track_dict[key].track_shape

            if my_char == ">" or my_char == "<" or my_char == "^" or my_char == "v":
                newMineCart = MineCart(my_x, my_y)
                self.minecarts.append(newMineCart)
                print_debug("Made new minecart {}".format(newMineCart.get_string()))

            #print_debug("my_x is {}, my_y is {}".format(my_x, my_y))

            left_neighbour = self.coord_to_track_dict.get((my_x-1, my_y))
            right_neighbour = self.coord_to_track_dict.get((my_x+1, my_y))
            up_neighbour = self.coord_to_track_dict.get((my_x, my_y-1))
            down_neighbour = self.coord_to_track_dict.get((my_x, my_y+1))

            newTrack = TrackSegment(my_x, my_y, my_char, left_neighbour, right_neighbour, up_neighbour, down_neighbour)

            print_debug("Made new track {}".format(newTrack.get_string()))
            self.track_dict[(my_x, my_y)] = newTrack




        print_debug("self.coord_to_track_dict is:")

        for key in self.coord_to_track_dict:
            #print_debug("k is {}".format(k))
            print_debug("For coord {}, the value is:\n{}".format(key, self.coord_to_track_dict[key].get_string()))

        print_debug("\n\n\n\n\n\n\n\n\n")
        print_debug("self.track_dict is:")

        for key in self.track_dict:
            #print_debug("k is {}".format(k))
            print_debug("For coord {}, the value is:\n{}".format(key, self.track_dict[key].get_string()))

        print_debug("\n\n\n\n\n\n\n\n\n")
        print_debug("self.minecarts is:")

        count = 0
        for minecart in self.minecarts:
            # print_debug("k is {}".format(k))
            print_debug("Minecart {} in minecarts is :\n{}".format(count, minecart.get_string()))
            count +=1


        print_debug("\n\n\n\n")
        print_debug("\n\nlooking at file:")
        print_debug("           01234567890")
        print_debug(" 012345678911111111112")

        count = 0
        #print_debug(lines)
        for line in lines:
            mystring = "{}".format(count)
            for mychar in line:
                mystring += mychar
            print_debug(mystring)
            count+=1
        print_debug("\n\n")


def day_13_part1():
    lines = read_file_into_list_v2("problem_13_dummy_input.txt")
    #lines = read_file_into_list_v2("problem_13_input.txt")


    myTrack = Track(lines)
    myTrack.pretty_print_track_dict()
    myTrack.run_simulation()
    myTrack.internet_answer()
    return








def main():

    print("\nScript arguments are:\n------------------------\n{}".format(sys.argv))
    print("Script start time is {}".format(str(datetime.datetime.now())))
    try:
        global DEBUG
        DEBUG = 0
        if sys.argv[1] == "debug1":
            DEBUG = 1
        if sys.argv[1] == "debug2":
            DEBUG = 2
    except:
        pass




    print("\n")
    print("Answer for Day 1 - Part 1 - 'Chronal Calibration':\n------------------------\n" + str(day_1_part_1()))
    print("\n")
    print("Answer for Day 1 - Part 2 - 'Chronal Calibration':':\n------------------------\n" + str(day_1_part_2()))
    print("\n")
    print("Answer for Day 2 - Part 1 - 'Inventory Management System':\n------------------------\n" + str(day_2_part_1()))
    print("\n")
    print("Answer for Day 2 - Part 2 - 'Inventory Management System':\n------------------------\n" + str(day_2_part_2()))
    print("\n")
    print("Answer for Day 3 - Part 1 - 'No Matter How You Slice It':\n------------------------\n" + str(day_3_part_1()))
    print("\n")
    print("Answer for Day 3 - Part 2 - 'No Matter How You Slice It':\n------------------------\n" + str(day_3_part_2()))
    print("\n")
    print("Answer for Day 4 - Part 1 - 'Repose Record':\n------------------------\n" + str(day_4_part1()))
    print("\n")
    print("Answer for Day 4 - Part 2 - 'Repose Record':\n------------------------\n" + str(day_4_part2()))
    print("\n")
    print("Answer for Day 5 - Part 1 - 'Alchemical Reduction':\n------------------------\n" + str(day_5_part1()))
    print("\n")
    print("Answer for Day 5 - Part 2 - 'Alchemical Reduction':\n------------------------\n" + str(day_5_part2()))
    print("\n")
    print("Answer for Day 6 - Part 1 - 'Chronal Coordinates':\n------------------------\n" + str(day_6_part1()))
    print("\n")
    print("Answer for Day 6 - Part 2 - 'Chronal Coordinates':\n------------------------\n" + str(day_6_part2()))
    print("\n")
    print("Answer for Day 7 - Part 1 - 'The Sum of Its Parts':\n------------------------\n" + str(day_7_part1()))
    print("\n")
    print("Answer for Day 7 - Part 2 - 'The Sum of Its Parts':\n------------------------\n" + str(day_7_part2()))
    print("\n")
    print("Answer for Day 8 - Part 1 - 'Memory Maneuver':\n------------------------\n" + str(day_8_part1()))
    print("\n")
    print("Answer for Day 8 - Part 2 - 'Memory Maneuver':\n------------------------\n" + str(day_8_part2()))
    print("\n")
    print("Answer for Day 9 - Part 1 - 'Marble Mania':\n------------------------\n" + str(day_9_part1()))
    print("\n")
    print("Answer for Day 9 - Part 2 - 'Marble Mania':\n------------------------\n" + str(day_9_part2()))
    print("\n")
    print("Answer for Day 10 - Part 1 - 'The Stars Align':\n------------------------\n" + str(day_10_part1()))
    print("\n")
    print("Answer for Day 10 - Part 2 - 'The Stars Align':\n------------------------\n" + str(day_10_part1()))
    print("\n")
    print("Answer for Day 11 - Part 1 - 'Chronal Charge':\n------------------------\n" + str(day_11_part1()))
    print("\n")
    print("Answer for Day 11 - Part 2 - 'Chronal Charge':\n------------------------\n" + str(day_11_part2()))
    print("\n")
    print("Answer for Day 12 - Part 1 - 'Subterranean Sustainability':\n------------------------\n" + str(day_12_part1()))
    print("\n")
    print("Answer for Day 12 - Part 2 - 'Subterranean Sustainability':\n------------------------\n" + str(day_12_part2()))
    print("\n")
    print("Answer for Day 13 - Part 1 - 'Mine Cart Madness':\n------------------------\n" + str(day_13_part1()))
    print("\n")
    print("Script end time is {}".format(str(datetime.datetime.now())))

main()