# point-in-polygon
Script containing an algorithm to check if a point is contained within a bounding polygon (in 2D cartesian coordinates) using the casting ray technique. It was completed as a piece of coursework for CEGEG082: GIS Principals at UCL. The coursework gave a small amount of extra credit if each line of the script was described, hence the fairly excessive level of commenting.

This point in polygon script is designed to be interactively run from the python interpreter window. It can be used to load a polygon and points from a list in a CSV file, or they can be manually specified by the user. Implementing the basic algorithm was fairly quick, the main challange was in finding and solving all the various edge cases (lol!) where a point fell on the polygon's border.
