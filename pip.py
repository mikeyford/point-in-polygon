import numpy as np
import matplotlib.pyplot as plt

class Geom(object):
    """Geometry Object Class"""

    def __init__(self, xy =[]):
        """Initialises Geom class"""
        self.coords = np.array(xy) 

    def getStartPoint(self):
        """Returns the first coordinates in an array stack"""
        return self.coords[0]


    def getEndPoint(self):
        """Returns the last coordinates in an array stack"""
        return self.coords[-1]

    def loadFromCSV(self, input_csv):
        """This module uses the addPoint method to load a list of x,y points in a CSV file"""
        import csv
        with open(input_csv, 'r') as incsv: 
            reader = csv.reader(incsv) 
            for row in reader: 
                try:
                    x, y = float(row[0]), float(row[1]) 
                    self.addPoint([x,y]) 
                except:
                    pass


class Point(Geom):
    """Point Object Class"""

    def addPoint(self, xy=[]):
        """This module adds a single X,Y coordinate to the point object"""
        if len(self.coords) != 0:
            print("The point already contains a coordinate. Can't add another.")
            u = raw_input("Press C then enter to change the coordinate to "+str(xy)+" or just hit enter to leave it.")
            if (u == "c") or (u == "C"): 
                self.coords = np.array(xy)
            else: 
                pass
        else: 
            self.coords = np.array(xy)

    def loadFromCSV(self, input_csv):
        """This class is not designed to load multiple points from a CSV, so tell the user"""
        print("This object is only designed to hold one point at a time. Try the Points_list() objected instead!")


class Line(Geom):
    """2D Line Object Class"""

    def addPoint(self, xy =[]):
        """Add a single point to the Line object"""
        if len(self.coords) == 0:  
            self.coords = np.array(xy) 
        else: 
            self.coords = np.vstack((self.coords,xy)) 


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
        l = len(self.coords)
        if self.coords[0, 0] > self.coords[(l/2), 0]: 
            raise ValueError("This polygon is defined in an unexpected way. You should inspect it manually to decide the direction.") 
        n_1, n_2 = 0, 0 
        i = 0
        while i < (l/2): 
            n_1 = n_1 + self.coords[i, 1] 
            i = i + 1 
        while i < l: 
            n_2 = n_2 + self.coords[i, 1] 
            i = i + 1 
        if (n_2/(l/2)) > (n_1/(l/2)): 
            return "AntiClockwise" 
        else: 
            return "Clockwise" 

    def plot(self):
        """This method plots the Polygon object, joining the last point to the first."""
        l = len(self.coords) 
        i = 0 
        x_coords, y_coords = [], [] 
        while i < l: 
            x_coords.append(self.coords[i, 0]) 
            y_coords.append(self.coords[i, 1]) 
            i = i + 1 
        x_coords.append(self.coords[0, 0]) 
        y_coords.append(self.coords[0, 1]) 
        plt.plot(x_coords, y_coords, color="c") 


    def pointInRectangle(self, point=[]):
        """This method checks if a point is in the minimum bounding rectangle for the polygon"""
        x_min, y_min = np.min(self.coords[:,0]), np.min(self.coords[:,1]) 
        x_max, y_max = np.max(self.coords[:,0]), np.max(self.coords[:,1]) 
        point_x, point_y = point[0], point[1] 
        if (point_x >= x_min) and (point_x <= x_max) and (point_y >= y_min) and (point_y <= y_max): 
            return True 
        else:
            return False

    def pointInside(self, point=[], direction="Unknown"):
        """Main point in polygon algorithm, using the casting ray technique,
        looking at each edge (or line) of the polygon and evaluating if each point will cross it passing from left to right
        Most points can be ruled out using various test, but those that can't are checked to see if the point crosses the line
        by comparing the gradient of the polygon edge with the gradient created by a line through the point and one of the vertices"""
        if self.pointInRectangle(point) == False:
            return "Outside"
        if direction == "Unknown": 
            try: 
                direction = self.getDirection() 
            except: 
                direction = "AntiClockwise" 
                print("The getDirection() method threw an error. Defaulting to an Anti Clockwise specified polygon, but you should check this manually.")
        l = len(self.coords) 
        polygon_lines = np.array([self.coords[0][0],self.coords[0][1],self.coords[1][0],self.coords[1][1]]) 
        i = 1 
        while i < (l - 1): 
            polygon_lines = np.vstack((polygon_lines,[self.coords[i][0],self.coords[i][1],self.coords[i+1][0],self.coords[i+1][1]])) 
            i = i + 1 
        polygon_lines = np.vstack((polygon_lines, [self.coords[i][0], self.coords[i][1], self.coords[0][0], self.coords[0][1]]))
        c = 0 
        boundary = "no" 
        for row in polygon_lines: 
            if (point[1] > max(row[1],row[3])) or (point[1] < min(row[1],row[3])): 
                pass 
            elif (point[0] < min(row[0],row[2])) and (point[1] == row[1] == row[3]): 
                c = c + 1 
            elif point[0] > max(row[0],row[2]):  
                pass 
            elif (point[1] == max(row[1],row[3])) and (point[0] < min(row[0],row[2])):
                pass 
            elif point[0] < min(row[0],row[2]): 
                c = c + 1 
            else: 
                up = row[1] - row[3] 
                along = row[0] - row[2] 
                if along == 0: 
                    line_gradient = "inf" 
                else: 
                    line_gradient = up / along 
                up = point[1] - row[3] 
                along = point[0] - row[2] 
                if along == 0: 
                    point_gradient = "inf" 
                else: 
                    point_gradient = up / along 
                if line_gradient == point_gradient:
                    boundary = "yes" 
                if direction == "AntiClockwise": 
                    if point_gradient > line_gradient: 
                        c = c + 1 
                if direction == "Clockwise": 
                    if point_gradient < line_gradient: 
                        c = c + 1 
        if boundary == "yes": 
            return "Boundary" 
        else: 
            if c%2 == 0: 
                return "Outside" 
            else: 
                return "Inside" 

def loadObjectFromCSV(object): 
    print("I can handle CSV files with headers and other non-coordinate information - I'll just ignore any lines in the file that don't start with numerical X,Y values.") 
    while True: 
        try: 
            print("") 
            print("Please enter the full name of the CSV file you'd like to use, including the .csv extension, then hit enter.") 
            user_file = raw_input("You'll need to specify the full path of the file if it's not in the same folder as this script.") 
            object.loadFromCSV(str(user_file)) 
            break 
        except: 
            print("Sorry, I didn't recognise that file. Please try again.") 
            print("If you're having trouble, you may wish to try moving the polygon CSV file to the same folder as this script is running and just entering the name of the file.") 
            continue 

def loadObjectManually(object): 
    while True: 
        try: 
            print("") 
            user_coords = raw_input("Please enter an X-coordinate and Y-coordinate separated by a comma. eg. 1,2 for x = 1, y = 2") 
            if (user_coords == "q") or (user_coords == "Q"): 
                break 
            user_x, user_y = user_coords.split(',') 
            object.addPoint([float(user_x), float(user_y)]) 
            print("Here's the points we've added so far...") 
            print(object.coords) 
            print("") 
            print("Enter Q if you are done adding points.") 
        except: 
            print("Sorry, that input wasn't what I was expecting. Please try again") 
            continue 

def chooseLoadMethod(): 
    while True: 
        try: 
            print("") 
            userinput = input("Please press 1 then enter to load points from a CSV. Press 2 then enter to specify individual points manually.") 
            if (userinput == 1) or (userinput == 2): 
                break 
            else: 
                raise ValueError 
        except: 
            print("Sorry, I didn't recognise that input. It should be either 1 or 2. Please try again.")
            continue 
    return userinput 

def plotPointsInPolygon(polygon_object, points_object): 
    plt.figure() 
    plt.xlabel('x-axis', fontsize=16) 
    plt.ylabel('y-axis', fontsize=16) 
    polygon_object.plot() 

    for row in points_object.coords: 
        if poly.pointInside(row, polygonDirecton) == "Outside": 
            plt.plot(row[0], row[1], 'ro')
        if poly.pointInside(row, polygonDirecton) == "Inside": 
            plt.plot(row[0], row[1], 'go') 
        if poly.pointInside(row, polygonDirecton) == "Boundary": 
            plt.plot(row[0], row[1], 'bo')

    plt.plot([], 'ro', label="Outside") 
    plt.plot([], 'go', label="Inside" ) 
    plt.plot([], 'bo', label="Boundary") 
    plt.plot([], color='c', label="Polygon") 
    plt.legend(numpoints=1, loc='upper center', fontsize=10, ncol=4, fancybox=True, shadow=True, bbox_to_anchor=(0.5, 1.05)) 
    plt.show() 










