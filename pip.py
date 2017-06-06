"""This point in polygon script is designed to be interactively run from the python interpreter window.
It can be used to load a polygon and points from a CSV file, or you can manually specify them yourself.
Please run the script and follow the instructions!
(If you wish call the methods manually, execute the script from within the python interpreter and hit M at the first prompt.)"""

import numpy as np
import matplotlib.pyplot as plt
import time

class Geom(object):
    """2D Geometry Object Class"""

    def __init__(self, xy =[]):
        """Initialises Geom class"""
        self.coords = np.array(xy) #create a numpy array for the xy coordinate list

    def getStartPoint(self):
        """Returns the first coordinates in an array stack"""
        return self.coords[0]


    def getEndPoint(self):
        """Returns the last coordinates in an array stack"""
        return self.coords[-1]

    def loadFromCSV(self, input_csv):
        """This module uses the addPoint method to load a list of x,y points in a CSV file"""
        import csv #imports the csv module
        with open(input_csv, 'r') as incsv:  #temporarily open the input csv file
            reader = csv.reader(incsv) #create reader object
            for row in reader: #iterate through each row in the CSV
                try: #attempt the following
                    x, y = float(row[0]), float(row[1]) #gets the values in column 1 and 2 of the CSV row, convert them to decimal
                    self.addPoint([x,y]) #use the addPoint method to add the values to the object
                except: #if try gives an error
                    pass  # This skips the row an error is thrown by the lines above, because it doesn't contain X,Y info.


class Point(Geom):
    """2D Point Object Class"""

    def addPoint(self, xy=[]):
        """This module adds a single X,Y coordinate to the point object"""
        if len(self.coords) != 0: #checks if the point object already contains a coordinate
            print("The point already contains a coordinate. Can't add another.")  #info for the user
            u = raw_input("Press C then enter to change the coordinate to "+str(xy)+" or just hit enter to leave it.") #ask the user what they want to do
            if (u == "c") or (u == "C"): #do this if the user entered C to change the coordinate
                self.coords = np.array(xy) #change the coordinate
            else: #the user does not enter C to change the coordinate
                pass #do nothing
        else: #the point is already empty
            self.coords = np.array(xy) #define the XY coordinate

    def loadFromCSV(self, input_csv):
        """This class is not designed to load multiple points from a CSV, so tell the user"""
        print("This object is only designed to hold one point at a time. Try the Points_list() objected instead!")


class Line(Geom):
    """2D Line Object Class"""

    def addPoint(self, xy =[]):
        """Add a single point to the Line object"""
        if len(self.coords) == 0:  # Tests if the Line object is empty
            self.coords = np.array(xy) #Creates the first row
        else: #The Line object already contains some points
            self.coords = np.vstack((self.coords,xy)) #Stack the new point on existing point(s)


class Points_list(Line):
    """2D List of Points"""

    def returnPoint(self, index=int):
        """Returns the specified point in the list"""
        return self.coords[index]


class Polygon(Line):
    """2D Polygon Object"""

    def getEndPoint(self):
        """Returns the first point instead of the last, so the Polygon is joined."""
        return self.getStartPoint()

    def getDirection(self):
        """This method does a quick test to see which direction the polygon was specified in.
        If the average y-values in the second half of the polygon's points are larger than the average in first half then it's assumed to be anti-clockwise, and vice versa.
        This is important because the point in polygon algorithm's success depends on the direction of specification."""
        l = len(self.coords) #get the number of vertices in the polygon
        if self.coords[0, 0] > self.coords[(l/2), 0]: #This test checks the x-value of the first point is to the left of the x-value half way though. If this fails it assumes that the Clockwise/AntiClockwise definition is not relevant.
            raise ValueError("This polygon is defined in an unexpected way. You should inspect it manually to decide the direction.") #Raises an error if this method doesn't expect to be able to determine the polygon's specification direction.
        n_1, n_2 = 0, 0 #defines a couple of variables to count the y-values
        i = 0 #defines an index variable to iterate through the vertices
        while i < (l/2): #iterates through the first half of the polygon's vertices
            n_1 = n_1 + self.coords[i, 1] #count the y-values
            i = i + 1 #advance to the next vertex
        while i < l: #iterates through the second half of the polygon's vertices
            n_2 = n_2 + self.coords[i, 1] #count the y-values
            i = i + 1 #advance to the next vertex
        if (n_2/(l/2)) > (n_1/(l/2)): #test if the average of the y-values in the second half is larger than the first half
            return "AntiClockwise" #return direction
        else: #the first half had greater y-values
            return "Clockwise" #return direction

    def plot(self):
        """This method plots the Polygon object, joining the last point to the first."""
        l = len(self.coords) #get the number of vertices in the polygon
        i = 0 #creates an index to iterate through
        x_coords, y_coords = [], [] #creates two empty lists to add values that should be plotted to
        while i < l: #iterate through all the vertices of the polygon
            x_coords.append(self.coords[i, 0]) #add the x-value of the vertex to the x-values list
            y_coords.append(self.coords[i, 1]) #add the y-value of the vertex to the y-values list
            i = i + 1 #advance the index
        x_coords.append(self.coords[0, 0]) #adds the first x-value to the end of the list of x-values, to join the polyon up
        y_coords.append(self.coords[0, 1]) #adds the first y-value to the end of the list of y-values, to join the polygon up
        plt.plot(x_coords, y_coords, color="c") #plot the polygon


    def pointInRectangle(self, point=[]):
        """This method checks if a point is in the minimum bounding rectangle for the polygon"""
        x_min, y_min = np.min(self.coords[:,0]), np.min(self.coords[:,1]) #gets the lowest x and y-values in the Polygon object
        x_max, y_max = np.max(self.coords[:,0]), np.max(self.coords[:,1]) #gets the highest x and y-values in the Polygon object
        point_x, point_y = point[0], point[1] #gets the x and y-values of the point in seperate variables
        if (point_x >= x_min) and (point_x <= x_max) and (point_y >= y_min) and (point_y <= y_max): #tests if the point is inside the minimum rectangle
            return True #returns boolean
        else: #point is outside the rectangle
            return False #returns boolean

    def pointInside(self, point=[], direction="Unknown"):
        """Main point in polygon algorithm, using the casting ray technique
        I'm looking at each edge (or line) of the polygon and evaluating if each point will cross it passing from left to right
        Most points can be ruled out using various test, but those that can't are checked to see if the point crosses the line
        by comparing the gradient of the polygon edge with the gradient created by a line through the point and one of the vertices"""
        if self.pointInRectangle(point) == False: #Do the minimum bounding rectangle check first
            return "Outside" #Stop here and return Outside if it's false
        if direction == "Unknown": #if the direction was not specified by the user, the default Unknown starts the test method
            try: #do this
                direction = self.getDirection() #set the direction to the result of that test
            except: #if it gives an error (probably because the polygon starts from the right)
                direction = "AntiClockwise" #just assume the polygon is specified anticlockwise
                print("The getDirection() method threw an error. Defaulting to an Anti Clockwise specified polygon, but you should check this manually.") #message for the user
        l = len(self.coords) #get the number of vertices in the polygon
        polygon_lines = np.array([self.coords[0][0],self.coords[0][1],self.coords[1][0],self.coords[1][1]]) #create a numpy array with the first pair of vertices
        i = 1 #set the index to iterate
        while i < (l - 1): #iterate to the second last point (since the loop goes to i+1)
            polygon_lines = np.vstack((polygon_lines,[self.coords[i][0],self.coords[i][1],self.coords[i+1][0],self.coords[i+1][1]])) #create a row in the array for each pair of vertices
            i = i + 1 #advance the index
        polygon_lines = np.vstack((polygon_lines, [self.coords[i][0], self.coords[i][1], self.coords[0][0], self.coords[0][1]])) #add the last entry in the polygon to the first, so that it's joined up
        c = 0 #set a variable for the number of times the ray crosses a line
        boundary = "no" #set a boundary variable to no initially
        for row in polygon_lines: #iterate through each row of the polygon edge array
            if (point[1] > max(row[1],row[3])) or (point[1] < min(row[1],row[3])): #tests if the point y-value is outside both y-values for the edge
                pass #stop checking here if test is true, since the ray definitely can't cross
            elif (point[0] < min(row[0],row[2])) and (point[1] == row[1] == row[3]): #tests for the special case where the point is directly to the left of a horizontal polygon edge
                c = c + 1 #add a cross in this case to ensure the correct result
            elif point[0] > max(row[0],row[2]):  #tests if point x-value is to the right of the maximum x-value from edge
                pass #stop checking here if true, since ray definitely won't cross
            elif (point[1] == max(row[1],row[3])) and (point[0] < min(row[0],row[2])): #Tests for the special case where point directly to the left of the top of vertex
                pass #stop checking since we will count the vertex of the next edge as a cross for this line
            elif point[0] < min(row[0],row[2]): #checks the points not yet excluded to see if the point x-value is below the edge's minimum x-value
                c = c + 1 #if true, ray definitely will cross so add one cross to the counter
            else: #none of the previous tests were true, so the point must be in the minimum bounding rectangle for the edge
                up = row[1] - row[3] #get the distance between the vertices' y-values
                along = row[0] - row[2] #get the distance between the vertices' x-values
                if along == 0: #check if we're going to divide by zero
                    line_gradient = "inf" #just set the gradient manually since that would throw an error
                else: #we're not trying to divide by zero
                    line_gradient = up / along #get the gradient of the line joining the two vertices
                up = point[1] - row[3] #get the distance between the point and the second vertex y-value
                along = point[0] - row[2] #get the distance between the point and the second vertex x-value
                if along == 0: #check for dividing by zero again
                    point_gradient = "inf" #set it manually if so
                else: #not trying to divide by zero so
                    point_gradient = up / along #get the gradient of the line joining the point and vertex
                if line_gradient == point_gradient: #test if the two gradients are the same
                    boundary = "yes" #if so, it must be a boundary, so re-set the variable
                if direction == "AntiClockwise": #use this test if the polygon is specified anti-clockwise, since we're using the second vertex in the edge array to test the gradient
                    if point_gradient > line_gradient: #test if the point gradient is a larger value than the edge gradient
                        c = c + 1 #if true, the point's ray must cross the line so add a cross
                if direction == "Clockwise": #use this test if the polygon is specified clockwise, since we're using the second vertex in the edge array to test the gradient
                    if point_gradient < line_gradient: #test if the point gradient is a smaller value that the edge gradient
                        c = c + 1 #if true, the points ray must cross the line so add a cross
        if boundary == "yes": #tests if the boundary variable was changed
            return "Boundary" #return that the point is on a boundary
        else: #the boundary variable is still set to no
            if c%2 == 0: #test if the number of crosses is even
                return "Outside" #returns that point is outside the polygon
            else: #the number of crosses is odd
                return "Inside" #returns that point is inside the polygon

def loadObjectFromCSV(object): #define a function to load a user CSV to the argument object, and handles wrong input
    print("I can handle CSV files with headers and other non-coordinate information - I'll just ignore any lines in the file that don't start with numerical X,Y values.") #information for user
    while True: #loop which keeps attempting the following, unless broken
        try: #do this
            print("") #UI clarity
            print("Please enter the full name of the CSV file you'd like to use, including the .csv extension, then hit enter.") #information for user
            user_file = raw_input("You'll need to specify the full path of the file if it's not in the same folder as this script.") #take user's input file location
            object.loadFromCSV(str(user_file)) #load into object
            break #if object is loaded, break the while loop
        except: #if the loadFromCSV method gives an error
            print("Sorry, I didn't recognise that file. Please try again.") #inform user the file didn't load
            print("If you're having trouble, you may wish to try moving the polygon CSV file to the same folder as this script is running and just entering the name of the file.") #information for user
            continue #go back to try again

def loadObjectManually(object): #define a function for the user to load the object in the argument manually, if they prefer
    while True: #loop which keeps attempting the following, unless broken
        try: #do this
            print("") #UI clarity
            user_coords = raw_input("Please enter an X-coordinate and Y-coordinate separated by a comma. eg. 1,2 for x = 1, y = 2") #get user coordinates as raw input
            if (user_coords == "q") or (user_coords == "Q"): #if the user enters Q to signal they are done
                break #exit the while loop
            user_x, user_y = user_coords.split(',') #split the user input into variables
            object.addPoint([float(user_x), float(user_y)]) #add the user input to the object
            print("Here's the points we've added so far...") #info for user
            print(object.coords) #give the coordinates in the object so far for the user
            print("") #UI clarity
            print("Enter Q if you are done adding points.") #info for user on how to signal they are done adding points
        except: #do this if an error is thrown when adding points to the object
            print("Sorry, that input wasn't what I was expecting. Please try again") #information for the user
            continue #try again

def chooseLoadMethod(): #define a function for the user to choose how to load an object
    while True: #loop which keeps running until it gets the correct input
        try: #do this
            print("") #UI clarity
            userinput = input("Please press 1 then enter to load points from a CSV. Press 2 then enter to specify individual points manually.") #set user input to variable
            if (userinput == 1) or (userinput == 2): #if the user input is valid
                break #escape the loop
            else: #otherwise
                raise ValueError #give an error to be handled below
        except: #if an error is raised from the linen above
            print("Sorry, I didn't recognise that input. It should be either 1 or 2. Please try again.") #inform the user their input could not be understood
            continue #try again
    return userinput #user input was valid, so return it

def plotPointsInPolygon(polygon_object, points_object): #define a function to plot the polygon and points in the argument
    plt.figure() #initiate matplotlib figure
    plt.xlabel('x-axis', fontsize=16) #label the x-axis
    plt.ylabel('y-axis', fontsize=16) #label the y-axis
    polygon_object.plot() #plot the polygon object

    for row in points_object.coords: #loop through points object
        if poly.pointInside(row, polygonDirecton) == "Outside": #if the point is marked Outside
            plt.plot(row[0], row[1], 'ro') #make the point a red circle
        if poly.pointInside(row, polygonDirecton) == "Inside": #if the point is marked Inside
            plt.plot(row[0], row[1], 'go') #make the point a green circle
        if poly.pointInside(row, polygonDirecton) == "Boundary": #if the point is marked Boundary
            plt.plot(row[0], row[1], 'bo') #make the point a blue circle

    plt.plot([], 'ro', label="Outside") #create a label for the red circles
    plt.plot([], 'go', label="Inside" ) #create a label for the green circles
    plt.plot([], 'bo', label="Boundary") #create a label for the blue circles
    plt.plot([], color='c', label="Polygon") #create a label for the polygon
    plt.legend(numpoints=1, loc='upper center', fontsize=10, ncol=4, fancybox=True, shadow=True, bbox_to_anchor=(0.5, 1.05)) #set display options for the labels
    plt.show() #display with the defined matplotlib figures

#The main script begins here
print("") #UI clarity
print("Hi. Welcome to Point in Polygon. This script is designed to be run interactively from Python interpreter window.") #info for user
time.sleep(1) #short delay for improved user experience
userinput = raw_input("If you'd rather call the functions yourself manually, please type M and hit enter. Otherwise just hit enter to get started.") #give an option for the user to call script manually, instead of using interactive script
if (userinput == "m") or (userinput == "M"): #if the user chooses to use the programme manually
    pass #skip interative section
else: #otherwise, enter this subscript
    print("Great. Let's get going.") #info for user
    time.sleep(1) #short delay for improved user experience
    print("Our first step is to create the polygon. Would you like to load your polygon from a CSV file or specify the vertices one by one?") #ask the user what they want to do
    time.sleep(1) #short delay for improved user experience
    userinput = chooseLoadMethod() #user the chooseLoadMethod() function to define a variable which indicates their choice
    print("") #UI clarity
    poly = Polygon() #create an empty polygon object
    if userinput == 1: #if the user entered 1
        loadObjectFromCSV(poly) #initiate the loadObjectFromCSV function
        print("Successfully loaded polygon from CSV file!") #information for user

    if userinput == 2: #if the user entered 2
        print("Option 2 selected. Let's create a polygon by entering some individual points.") #information for user
        loadObjectManually(poly) #initiate the loadObjectManually function
        print("Finished creating polygon from individual points!") #info for user
    time.sleep(1) #short delay for user experience
    print("") #UI clarity
    print("Say, if you know, it would be useful if you could let me know which direction your polygon was specified in.") #ask if the user knows which direction the polygon is specified in
    print("(It's fine if you're not sure - I can also do a little test myself in that case.)") #info for user
    while True: #keep doing this loop until it's broken
        try: #attempt this
            print("") #UI clarity
            userinput = input("Enter 1 if your polygon points are specified anti-clockwise, 2 if they are clockwise, or 3 if you're not sure!") #get user input as variable
            if (userinput == 1) or (userinput == 2) or (userinput == 3): #if the user gives the expected input
                break #escape the while loop
            else: #otherwise
                raise ValueError #raise error to be handled below
        except: #if line above raises an error
            print("Sorry, I didn't recognise that input. It should be either 1, 2 or 3. Please try again.") #tell user their input wasn't correct
            continue #do the try again

    polygonDirecton = "Unknown" #set a polygon direction variable to Unknown as default
    if userinput == 1: #if user input for polygon direction was 1
        polygonDirecton = "AntiClockwise" #set the direction variable to Anti-Clockwise
    if userinput == 2: #if the user input for polygon direction was 2
        polygonDirecton = "Clockwise" #set the direction variable to Clockwise

    time.sleep(1) #delay for user experience
    print("") #UI clarity
    print("Wow...This is going well so far. Now, let's load a list of points to test if they are in the polygon we loaded.") #info for user
    print("Same deal as before: Do you have a list of points in a CSV file you'd like to check, or would you like to enter them manually?") #ask the user if the want to load from CSV or enter manually
    userinput = chooseLoadMethod() #set a variable for the user's decision
    print("") #UI clarity

    points = Points_list() #create an empty list object
    if userinput == 1: #if the user input was 1
        print("Option 1 selected. Let's load the points from a CSV file.") #info for user
        loadObjectFromCSV(points) #use the loadObjectFromCSV function
        print("Successfully loaded points from CSV file!") #info for user
    if userinput == 2: #if the user input was 2
        print("Option 2 selected. Let's create a polygon by entering some individual points.") #info for user
        loadObjectManually(points) #use the loadObjectManually function
        print("Finished creating points list from individual points!") #info for user
    time.sleep(1) #delay to enhance user experience
    print("OK. Let's plot the polygon and classify the points you provided!...") #message for user
    time.sleep(1) #delay to enhance user experience

    plotPointsInPolygon(poly, points) #call the function for plotting the points in the polygon










