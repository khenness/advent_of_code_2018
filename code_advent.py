import difflib
from fuzzywuzzy import fuzz
import datetime

import sys
DEBUG = 1

def print_debug(msg):
    if DEBUG == 1:
        print(msg)

def print_good_debug(msg):
    if DEBUG == 1:
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
                if not self.is_point_a_target(x, y):
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

def main():

    print("\nScript arguments are:\n------------------------\n{}".format(sys.argv))
    print("Script start time is {}".format(str(datetime.datetime.now())))
    try:
        global DEBUG
        DEBUG = 0
        if sys.argv[1] == "debug":
            DEBUG = 1
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
    print("Script end time is {}".format(str(datetime.datetime.now())))

main()