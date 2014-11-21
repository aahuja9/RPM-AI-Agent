# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.


from PIL import Image
import os

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem

    def Solve(self, problem):

        #if problem.getName() == "2x1 Basic Problem 01":
        figures = problem.getFigures()
        prevPath = ""
        for figure in figures:
            path = figures[figure].getPath()

            savePath = path[:-5] + "Processed Images/"

            #Create the Processed Images folder if it doesn't exist
            if not os.path.exists(savePath):
                os.makedirs(savePath)

            # Check to see if we're still on the same problem; if not, clear the previous runs images
            if prevPath == "":
                prevPath = savePath
            if prevPath != savePath:
                self.removeProcessedFiles(savePath)
            else:
                prevPath = savePath

            self.decolorize(path, savePath, figure)
            self.colorize(savePath + figure + ".png")

        return "6"

    def decolorize(self, path, savePath, figure):

        # Open the image
        image = Image.open(path)

        # Convert from 3-channel RBG representation to just luminance
        grayscale = image.convert('L')

        # Define a filter to run on every pixel of the image
        def filter(value):
            if value == 255:
                # Only keep pure-white pixels as white
                return 255
            else:
                # Any gray pixels will become black
                return 0

        # Apply the filter and save the modified image
        blackwhite = grayscale.point(filter, '1')
        blackwhite.save(savePath + figure + '.png')

        return

    def removeProcessedFiles(self, path):
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            try:
                if os.path.isfile(filepath):
                    os.unlink(filepath)
            except:
                print("ERROR")
        return

    def colorize(self, imagePath):

        image = Image.open(imagePath)

        DISTINCT_COLORS = [(0x00, 0xFF, 0x00), (0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), (0x01, 0xFF, 0xFE), (0xFF, 0xA6, 0xFE), (0xFF, 0xDB, 0x66), (0x00, 0x64, 0x01), (0x01, 0x00, 0x67), (0x95, 0x00, 0x3A), (0x00, 0x7D, 0xB5), (0xFF, 0x00, 0xF6), (0xFF, 0xEE, 0xE8), (0x77, 0x4D, 0x00), (0x90, 0xFB, 0x92), (0x00, 0x76, 0xFF), (0xD5, 0xFF, 0x00), (0xFF, 0x93, 0x7E), (0x6A, 0x82, 0x6C), (0xFF, 0x02, 0x9D), (0xFE, 0x89, 0x00), (0x7A, 0x47, 0x82), (0x7E, 0x2D, 0xD2), (0x85, 0xA9, 0x00), (0xFF, 0x00, 0x56), (0xA4, 0x24, 0x00), (0x00, 0xAE, 0x7E), (0x68, 0x3D, 0x3B), (0xBD, 0xC6, 0xFF), (0x26, 0x34, 0x00), (0xBD, 0xD3, 0x93), (0x00, 0xB9, 0x17), (0x9E, 0x00, 0x8E), (0x00, 0x15, 0x44), (0xC2, 0x8C, 0x9F), (0xFF, 0x74, 0xA3), (0x01, 0xD0, 0xFF), (0x00, 0x47, 0x54), (0xE5, 0x6F, 0xFE), (0x78, 0x82, 0x31), (0x0E, 0x4C, 0xA1), (0x91, 0xD0, 0xCB), (0xBE, 0x99, 0x70), (0x96, 0x8A, 0xE8), (0xBB, 0x88, 0x00), (0x43, 0x00, 0x2C), (0xDE, 0xFF, 0x74), (0x00, 0xFF, 0xC6), (0xFF, 0xE5, 0x02), (0x62, 0x0E, 0x00), (0x00, 0x8F, 0x9C), (0x98, 0xFF, 0x52), (0x75, 0x44, 0xB1), (0xB5, 0x00, 0xFF), (0x00, 0xFF, 0x78), (0xFF, 0x6E, 0x41), (0x00, 0x5F, 0x39), (0x6B, 0x68, 0x82), (0x5F, 0xAD, 0x4E), (0xA7, 0x57, 0x40), (0xA5, 0xFF, 0xD2), (0xFF, 0xB1, 0x67), (0x00, 0x9B, 0xFF), (0xE8, 0x5E, 0xBE)]

        # Walk through an image pixel by pixel
        def walk(image):
            width, height = image.size
            # Go through each pixel sequentially
            for index, pixel in enumerate(image.getdata()):
                # Calculate the current position
                x = index % width
                y = index / width
                # Yield the current position and value
                yield (x,y,pixel)

        # Convert the image to RGB (assume it's currently black and white)
        image = image.convert('RGB')
        width, height = image.size
        colorindex = 0
        # Color each connected section of black pixels
        while True:
            # Choose a new color
            color = DISTINCT_COLORS[colorindex]
            colorindex += 1

            # Find the first black pixel
            blackpixel = None
            for x, y, pixel in walk(image):
                # Found the first black pixel
                if pixel == (0, 0, 0):
                    blackpixel = (x,y)
                    break
            if not blackpixel:
                # No more black pixels, the image is fully colored
                break

            # Keep track of neighboring black pixels
            neighbors = [blackpixel]
            # Keep finding neighbors until we don't find any more black pixels
            while len(neighbors) > 0:
                # Make a new list of the current neighbors
                processing = list(neighbors)
                # Clear the neighbors we are going to process from the list
                neighbors = []
                # Process each of the neighbors
                for x,y in processing:
                    # Color this neighbor
                    image.putpixel((x,y), color)
                    # Find all of the neighboring pixels
                    new = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                    # Go through the neighbors
                    for x,y in new:
                        if (x,y) in neighbors:
                            # Already added, skip
                            continue
                        if x < 0 or x >= width:
                            # Invalid x value, skip
                            continue
                        if y < 0 or y >= height:
                            # Invalid y value, skip
                            continue
                        if image.getpixel((x,y)) != (0, 0, 0):
                            # Non-black pixel, skip
                            continue
                        # Add the neighboring black pixel to be processed
                        neighbors.append((x,y))
        image.save(imagePath[:-4] + '-Colored.png')

        return

    def cropObject(self):

        #TODO: crop out differently colored objects into separate images

        return