# DO NOT EDIT THE FOLLOWING LINES
# COURSE CPSC 231 FALL 2021
# INSTRUCTOR: Jonathan Hudson
# Wi52C3g7ZzkJ7XBcVRHY
# DO NOT EDIT THE ABOVE LINES

# INFORMATION FOR YOUR TA
# COURSE: CPSC 231 FALL 2021
# Name: Eugene Lee
# INSTRUCTOR: Jonathan Hudson
# Tutorial: Zack Hassan - T04
# ID: 30137489
# Date: Nov.23rd, 2021
# Description: This program will plot stars and constellations on a graph based on data from input files

import sys
import os
import turtle

# STARTER CONSTANTS
BACKGROUND_COLOR = "black"
WIDTH = 600
HEIGHT = 600
# AXIS CONSTANTS
AXIS_COLOR = "blue"
TICK = 5
LABEL_SIZE = 7
CENTER = 300
ZERO = 0
RATIO = 300
STEP_SIZE = 0.25
# These constants fixes the offset of the labels on the axis, found through trial and error
X_AXIS_OFFSET = 18
Y_AXIS_OFFSET_X = 16
Y_AXIS_OFFSET_Y = -7
# This constant fixes the offset of the star names, found through trial and error
NAME_OFFSET = 2
# STAR CONSTANTS
STAR_COLOR = "white"
STAR_COLOR2 = "grey"
NAME_SIZE = 5
MAG_LOWER_BOUND = -2
MAG_UPPER_BOUND = 10.5


def setup():
    """
    Setup the turtle window and return drawing pointer
    :return: Turtle pointer for drawing
    """
    turtle.bgcolor(BACKGROUND_COLOR)
    turtle.setup(WIDTH, HEIGHT, 0, 0)
    screen = turtle.getscreen()
    screen.delay(delay=0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer = turtle
    pointer.hideturtle()
    pointer.speed(0)
    pointer.up()
    return pointer


def screen_conversion(a):
    """
    Convert a numeric value (a) on graph to the actual pixel value (screen_a) of the turtle screen
    :param a: A certain value on the drawn graph that ranges from -1 to 1
    :return: (screen_a) pixel version of graph (a)
    """
    # This function converts any value into the correct scale of the 600 by 600 turtle window
    screen_a = CENTER + RATIO * a
    return screen_a


def draw_line(pointer, x1, y1, x2, y2):
    """
    Draw a straight line connecting two points (x1, y1) to (x2, y2) on the graph
    :param pointer: Turtle pointer to draw with
    :param x1: The x-value of the starting point
    :param y1: The y-value of the starting point
    :param x2: The x-value of the end point
    :param y2: THe y-value of the end point
    :return: None (just draws in turtle)
    """
    # This function is going to draw a straight line between two points on the graph when called, so need to make
    # the pointer move from the initial point to the final point with the pen down
    pointer.penup()
    pointer.goto(x1, y1)
    pointer.pendown()
    pointer.goto(x2, y2)
    pointer.penup()


def draw_x_axis_tick_label(pointer, x, label_text):
    """
    Draw an x-axis tick and label for location (x, CENTER), label is label_text
    :param pointer: Turtle pointer to draw with
    :param x: The pixel x of tick and label location on axis
    :param label_text: The string label to draw
    :return: None (just draws in turtle)
    """
    pointer.pencolor(AXIS_COLOR)
    # Adding and subtracting TICK from y will allow a straight line to be drawn as
    # an actual tick ultimately the size of 2 * TICK in each x value
    draw_line(pointer, x, CENTER + TICK, x, CENTER - TICK)
    # This part will write the appropriate x values as text, which will be the labels to the ticks
    pointer.goto(x, CENTER - X_AXIS_OFFSET)
    pointer.write(label_text, align="center", font=("Arial", LABEL_SIZE, "normal"))


def draw_y_axis_tick_label(pointer, y, label_text):
    """
    Draw an y-axis tick and label for location (CENTER, y), label is label_text
    :param pointer: Turtle pointer to draw with
    :param y: The pixel y of tick and label location on axis
    :param label_text: The string label to draw
    :return: None (just draws in turtle)
    """
    pointer.pencolor(AXIS_COLOR)
    # Adding and subtracting TICK from x will allow a straight line to be drawn as
    # an actual tick ultimately the size of 2 * TICK in each y value
    draw_line(pointer, CENTER - TICK, y, CENTER + TICK, y)
    # This part will write the appropriate y values as text, which will be the labels to the ticks
    pointer.goto(CENTER + Y_AXIS_OFFSET_X, y + Y_AXIS_OFFSET_Y)
    pointer.write(label_text, align="center", font=("Arial", LABEL_SIZE, "normal"))


def draw_axis(pointer):
    """
    Draw the x and y axis of the graph crossing the origin of screen pixel (300,300)
    :param pointer: Turtle pointer to draw with
    :return: None (just draws in turtle)
    """
    # This function will incorporate the functions above to draw the actual x and y axis on the
    # screen with the corresponding ticks and labels
    axis_min = -1
    axis_max = 1
    screen_min = screen_conversion(axis_min)
    screen_max = screen_conversion(axis_max)
    screen_step = STEP_SIZE * RATIO
    screen_step_int = int(screen_step)
    pointer.pencolor(AXIS_COLOR)
    draw_line(pointer, ZERO, CENTER, WIDTH, CENTER)  # x-axis
    draw_line(pointer, CENTER, ZERO, CENTER, HEIGHT)  # y-axis
    # Using a loop to efficiently draw the ticks and labels in the desired interval
    for i in range(screen_min, screen_max + screen_step_int, screen_step_int):
        if axis_min != 0.0:  # getting rid of the 0s for a cleaner look
            draw_x_axis_tick_label(pointer, screen_min, axis_min)
            draw_y_axis_tick_label(pointer, screen_min, axis_min)
        screen_min += screen_step
        axis_min += STEP_SIZE


def file_check(file):
    """
    Check a file to see if it actually exists within the same directory as this python file
    :param file: The file to check for
    :return: A file that exists within the directory
    """
    # Error check a file to see if it actually exists, and loop until a valid file name is inputted
    while file != "":
        if os.path.isfile(file) is False:
            print("The path entered isn't a valid filename: " + file)
            file = input("Enter the name of the input file with star information (ex. stars_all.dat): ")
        else:
            return file
    # If an empty string is entered, exit displaying a message
    sys.exit("No filename was entered. Program exiting!")


def expected_usage():
    """
    Check each different possibilities of input specified in the assignment description and prompt until the
    appropriate file name is inputted for all scenarios. Also keeps track of whether -name is triggered or not
    :return: The string of the checked file and the boolean value of whether or not -name was triggered
    """
    length = len(sys.argv)
    name_tracker = False
    # No argument and is just the .py name, so need to prompt for a valid star file name
    if length == 1:
        file = input("Enter the name of the input file with star information (ex. stars_all.dat): ")
        checked_file = file_check(file)
        return checked_file, name_tracker
    # Indicated that the names must show, but need to prompt for a valid star file name
    elif length == 2 and sys.argv[1] == "-names":
        file = input("Enter the name of the input file with star information (ex. stars_all.dat): ")
        checked_file = file_check(file)
        name_tracker = True
        return checked_file, name_tracker
    # A star file name is inputted, need to make sure it is valid
    elif length == 2:
        star_file = sys.argv[1]
        checked_star_file = file_check(star_file)
        return checked_star_file, name_tracker
    # A star file name is inputted so need to make sure it is valid, and names must show
    elif length == 3 and sys.argv[2] == "-names":
        star_file = sys.argv[1]
        checked_star_file = file_check(star_file)
        name_tracker = True
        return checked_star_file, name_tracker
    # A star file name is inputted so need to make sure it is valid, and names must show
    elif length == 3 and sys.argv[1] == "-names":
        star_file = sys.argv[2]
        checked_star_file = file_check(star_file)
        name_tracker = True
        return checked_star_file, name_tracker
    # Two star file names were inputted with no indication of a name, so results in an error
    elif length == 3 and sys.argv[1] != "-names" and sys.argv[2] != "-names":
        sys.exit("Invalid argument as neither of the inputs were '-names'")
    # Too many arguments are inputted, so results in an error
    elif length > 3:
        sys.exit("Too many arguments were given")


def read_star_file(star_file):
    """
    Read a file and store the necessary information within a list and a dictionary
    :param star_file: The inputted star file that provides all the data
    :return: The list and dictionary created, each storing its corresponding data about stars
    """
    try:
        star_file = open(star_file)
        star_list = []
        star_dict = {}
        # Assign the x, y, mag, and names into the correct variables
        for line in star_file:
            strip_line = line.strip()
            new_line = strip_line.split(",")
            x = float(new_line[0])
            y = float(new_line[1])
            if MAG_LOWER_BOUND < float(new_line[4]) <= MAG_UPPER_BOUND:
                mag = float(new_line[4])
            if new_line[6] != "":
                names = new_line[6].split(";")
            else:
                names = None
            # Store the variables into tuples, then the tuples into a list
            star_tuple = (x, y, mag, names)
            star_list.append(star_tuple)
            if names is not None:
                for name in names:
                    stripped_name = name.strip()
                    # For stars with names, print out where the star is located at along with its magnitude
                    if stripped_name != "":
                        star_dict[stripped_name] = star_tuple
                        print(stripped_name + " is at (" + str(x) + "," + str(y) + ") with magnitude " + str(mag))
        return star_list, star_dict
    # An except block for the possibility that there are not enough entries in a line
    except IndexError:
        sys.exit("Star file does not have the required amount of entries separated by commas")
    # An except block for if an invalid file is inputted
    except:
        sys.exit("Invalid file input, can't read file")
    # Always close files
    finally:
        star_file.close()


def draw_stars(pointer, star_list, name_tracker):
    """
    Draws the stars by using the information from star_list, which will come from the read_star_file function
    :param pointer: Turtle pointer to draw with
    :param star_list: The list that contains the x, y, mag, name values of stars
    :param name_tracker: The boolean value will determine whether name of stars are drawn or not
    :return: None (just draws in turtle)
    """
    # Need to convert the x and y value of the star location into the correct ratio of the turtle screen
    for star in star_list:
        x = star[0]
        y = star[1]
        mag = star[2]
        names = star[3]
        screen_x = screen_conversion(x)
        screen_y = screen_conversion(y)
        if names is None:
            pointer.pencolor(STAR_COLOR2)
        else:
            pointer.pencolor(STAR_COLOR)
            # Only drawing the names if the name tracker is triggered
            if name_tracker:
                pointer.penup()
                pointer.goto(screen_x + NAME_OFFSET, screen_y + NAME_OFFSET)
                pointer.write(names[0], font=("Arial", NAME_SIZE, "normal"))
        # Actually drawing the dots which will represent the stars
        diameter = 10 / (mag + 2) # Did not use constants as these values were given directly in the assignment description
        pointer.penup()
        pointer.goto(screen_x, screen_y)
        pointer.dot(diameter)


def read_constellation_file(constellation_file):
    """
    Read a constellation file and store the necessary information within a list
    :param constellation_file: The inputted constellation file that provides the name of the stars
    :return: The list created, which stores the name of the stars for each side of the constellation
    """
    # Error checking the constellation file to ensure that it is of the correct type
    try:
        file = open(constellation_file)
    except:
        while os.path.isfile(constellation_file) is False and constellation_file != "":
            print("The path entered isn't a valid filename: " + str(constellation_file))
            constellation_file = input("Enter a constellations file (Ex. BigDipper.dat): ")
        if constellation_file == "":
            return []
        else:
            file = open(constellation_file)
    try:
        # Creating the list which will store the star names as a tuple
        constellation_list = []
        constellation_set = set()
        constellation_name = file.readline()
        stripped_constellation_name = constellation_name.strip()
        for line in file:
            strip_line = line.strip()
            new_line = strip_line.split(",")
            # Skip over the constellation name in the first line of file and also any false input only carrying one name
            if new_line != constellation_name:
                start_star = new_line[0]
                end_star = new_line[1]
                constellation_tuple = (start_star, end_star)
                constellation_list.append(constellation_tuple)
                constellation_set.add(start_star)
                constellation_set.add(end_star)
        # Print the set of stars when a valid constellation file is inputted
        print(str(stripped_constellation_name) + " constellation contains " + str(constellation_set))
        return constellation_list
    # An except block for the possibility that there are not enough entries in a line
    except IndexError:
        sys.exit("Constellation file does not have the required amount of entries separated by commas")
    # Always close files
    finally:
        file.close()


def draw_constellations(pointer, color, constellation_list, star_dict):
    """
    Draws the constellations using the constellation_list and the star_dict
    :param pointer: Turtle pointer to draw with
    :param color: The color of pointer used to draw the constellation
    :param constellation_list: Provides the names of the stars to connect
    :param star_dict: Can use the star name as a key to find the star's information
    :return: None (just draws in turtle)
    """
    try:
        for star in constellation_list:
            # Acquire the names of the two stars that needs to be connected
            start_star = star[0]
            end_star = star[1]
            # Acquire the stars' location on the graph
            start_star_tuple = star_dict[start_star]
            x1 = start_star_tuple[0]
            y1 = start_star_tuple[1]
            end_star_tuple = star_dict[end_star]
            x2 = end_star_tuple[0]
            y2 = end_star_tuple[1]
            # Convert the stars' location on the graph into its actual pixel location on the screen
            screen_x1 = screen_conversion(x1)
            screen_y1 = screen_conversion(y1)
            screen_x2 = screen_conversion(x2)
            screen_y2 = screen_conversion(y2)
            pointer.pencolor(color)
            draw_line(pointer, screen_x1, screen_y1, screen_x2, screen_y2)
    # Error check for the possibility of invalid names within the file used to draw
    except KeyError:
        sys.exit("The name within the inputted constellation file is not a valid key")


def color_converter(constellation_counter):
    """
    Get the constellation's color based on counter of how many constellations have been drawn
    :param constellation_counter: Keeps track of how many constellations have been drawn so far
    :return: The color for pointer to draw with
    """
    # Dividing using % 3 to make this if statement work for infinitely many constellations
    constellation_number = constellation_counter % 3
    if constellation_number == 0:
        color = "red"
    elif constellation_number == 1:
        color = "green"
    else:
        color = "yellow"
    return color


def main():
    """
    Main constellation program
    :return: None
    """
    pointer = setup()
    # Handle arguments
    star_file, name_tracker = expected_usage()
    # Read star information from file (function)
    star_list, star_dict = read_star_file(star_file)
    # Draw Axes (function)
    draw_axis(pointer)
    # Draw Stars (function)
    draw_stars(pointer, star_list, name_tracker)
    # Loop getting filenames
    x = True
    constellation_counter = 0
    while x:
        constellation_file = input("Enter a constellations file (Ex. BigDipper.dat): ")
        if constellation_file == "":
            x = False
        # Read constellation file (function)
        else:
            constellation_list = read_constellation_file(constellation_file)
            if len(constellation_list) == 0:
                x = False
            else:
                # Determining the pencolor of constellation
                color = color_converter(constellation_counter)
                # Draw Constellation (function)
                draw_constellations(pointer, color, constellation_list, star_dict)
                constellation_counter += 1
        # Draw bounding box (Bonus) (function)
        pass


main()


print("\nClick on window to exit!\n")
turtle.exitonclick()
