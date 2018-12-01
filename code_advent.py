

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
            
#https://adventofcode.com/2018/day/1
def problem_1():

    lines = read_file_into_list("problem_1_input.txt")
    
    print_debug("Problem 1 input data is:")
    print_debug(lines)




    #print(read_data)


def main():
    global DEBUG
    DEBUG = 0


    print("\n")
    print("Answer for 'Day 1: Chronal Calibration':\n------------------------\n" + str(problem_1()))
    print("\n")
main()