
import sys
DEBUG = 1

def print_debug(msg):
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
            print_debug("I had the value {} and added on {} to get {}".format(running_total, mytuple[1], new_running_total))
            running_total = new_running_total
        elif mytuple[0] =='-':
            new_running_total = running_total - mytuple[1]
            print_debug("I had the value {} and subtracted {} to get {}".format(running_total, mytuple[1], new_running_total))
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
        print_debug("Found the answer it is {}".format(running_total))
        print_debug("The seen_frequencies dictionary is: {}".format(seen_frequencies))
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

                print_debug(
                    "I had the value {} and added on {} to get {}".format(running_total, mytuple[1], new_running_total))
                running_total = new_running_total

            elif mytuple[0] == '-':
                new_running_total = running_total - mytuple[1]


                print_debug(
                    "I had the value {} and subtracted {} to get {}".format(running_total, mytuple[1], new_running_total))

                running_total = new_running_total
            else:
                raise ValueError("Found invalid input")

            if not found_answer:
                answer_frequency, found_answer = check_seen(running_total, seen_frequencies)

    answer = answer_frequency

    answer_string = "For starting_value of {}, the frequency that shows up twice is {}. I had to read the list {} times to find it.".format(starting_value, answer, list_iteration_count)
    return answer_string


def string_has_N_same_letters(input_string, N):

    return True

def how_many_have_letters_twice(lines):
    count = 0
    for line in lines:
        if string_has_N_same_letters(line, 2):
            count += 1
    return count

def how_many_have_letters_three_times(lines):
    count = 0
    for line in lines:
        if string_has_N_same_letters(line, 2):
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

def main():

    print("\nScript arguments are:\n------------------------\n{}".format(sys.argv))

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
main()