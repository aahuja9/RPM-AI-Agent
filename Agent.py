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
import string
from glob import glob
import shutil
import platform


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    objAlphabet = list(string.printable[:-6])
    currentChar = 0
    figList2x1 = ["A", "B", "C", "1", "2", "3", "4", "5", "6"]
    figList2x2 = ["A", "B", "C", "1", "2", "3", "4", "5", "6"]
    figList3x3 = ["A", "B", "C", "D", "E", "F", "G", "H", "1", "2", "3", "4", "5", "6"]
    objectInfo = {}

    def __init__(self):
        self.currentChar = 0
        self.objectInfo = {}
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
        self.currentChar = 0
        #if problem.getName() == "2x1 Basic Problem 09":
        # Initialize problem information
        print self.objAlphabet
        #print self.objAlphabet.index("/")
        probType = problem.getProblemType()
        probName = problem.getName()
        print probName
        figures = problem.getFigures()
        rootPath = ""  # File path to root folder of problem
        figList = ""
        savePath = ""  # Path to saved, processed images

        #Set fig list to the corresponding problem type
        if probType == "2x1 (Image)":
            figList = self.figList2x1
        elif probType == "2x2 (Image)":
            figList = self.figList2x2
        elif probType == "3x3 (Image)":
            figList = self.figList3x3

        # Pre-process the images for determination logic
        for figure in figures:
            path = figures[figure].getPath()
            rootPath = path[:-5]
            # print rootPath
            savePath = self.cleanPaths(path)
            self.decolorize(path, savePath, figure)
            self.colorize(savePath + figure + ".png")

        # Find object attributes and write them to file
        objPath = savePath + 'Cropped Objects/'
        objsList = glob(os.path.join(objPath, '*.png'))

        shutil.copyfile(rootPath + probName.replace(" ", "") + ".txt", rootPath + "GeneratedRep.txt")

        for figure in figList:
            with open(rootPath + "GeneratedRep.txt", "a") as repFile:
                repFile.write("\n" + figure)
                for object in sorted(objsList):
                    figureID = object[-15:-14]
                    if figureID == figure:
                        objectID = object[-13:-12]
                        repFile.write("\n" + "    " + objectID)
                        repFile.write("\n" + "        shape:" + str(self.findShape(object)))
                        # Find fill
                        repFile.write("\n" + "        fill:" + self.findFill(object))
                        # find Rotation
                        repFile.write("\n" + "        angle:" + str(self.findRotation(object)))
                        # Find Positionals
                        repFile.write("\n" + self.findPosition(figureID, objectID))

                        # Pass written file to "old" agent for processing of propositional representation
                        # TODO: old agent logic inserted here

        return "6"

    def cleanPaths(self, path):
        prevPath = ""
        savePath = path[:-5] + "Processed Images/"
        croppedPath = savePath + "Cropped Objects/"

        # Create the Processed Images folder if it doesn't exist
        if not os.path.exists(savePath):
            os.makedirs(savePath)
            os.makedirs(croppedPath)

        if not os.path.exists(croppedPath):
            os.makedirs(croppedPath)

        # Check to see if we're still on the same problem; if not, clear the previous runs images
        if prevPath == "":
            prevPath = savePath
        if prevPath != savePath:
            self.removeProcessedFiles(savePath)
            self.removeProcessedFiles(croppedPath)
        else:
            prevPath = savePath

        return savePath

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

        DISTINCT_COLORS = [(0x00, 0xFF, 0x00), (0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), (0x01, 0xFF, 0xFE),
                           (0xFF, 0xA6, 0xFE), (0xFF, 0xDB, 0x66), (0x00, 0x64, 0x01), (0x01, 0x00, 0x67),
                           (0x95, 0x00, 0x3A), (0x00, 0x7D, 0xB5), (0xFF, 0x00, 0xF6), (0xFF, 0xEE, 0xE8),
                           (0x77, 0x4D, 0x00), (0x90, 0xFB, 0x92), (0x00, 0x76, 0xFF), (0xD5, 0xFF, 0x00),
                           (0xFF, 0x93, 0x7E), (0x6A, 0x82, 0x6C), (0xFF, 0x02, 0x9D), (0xFE, 0x89, 0x00),
                           (0x7A, 0x47, 0x82), (0x7E, 0x2D, 0xD2), (0x85, 0xA9, 0x00), (0xFF, 0x00, 0x56),
                           (0xA4, 0x24, 0x00), (0x00, 0xAE, 0x7E), (0x68, 0x3D, 0x3B), (0xBD, 0xC6, 0xFF),
                           (0x26, 0x34, 0x00), (0xBD, 0xD3, 0x93), (0x00, 0xB9, 0x17), (0x9E, 0x00, 0x8E),
                           (0x00, 0x15, 0x44), (0xC2, 0x8C, 0x9F), (0xFF, 0x74, 0xA3), (0x01, 0xD0, 0xFF),
                           (0x00, 0x47, 0x54), (0xE5, 0x6F, 0xFE), (0x78, 0x82, 0x31), (0x0E, 0x4C, 0xA1),
                           (0x91, 0xD0, 0xCB), (0xBE, 0x99, 0x70), (0x96, 0x8A, 0xE8), (0xBB, 0x88, 0x00),
                           (0x43, 0x00, 0x2C), (0xDE, 0xFF, 0x74), (0x00, 0xFF, 0xC6), (0xFF, 0xE5, 0x02),
                           (0x62, 0x0E, 0x00), (0x00, 0x8F, 0x9C), (0x98, 0xFF, 0x52), (0x75, 0x44, 0xB1),
                           (0xB5, 0x00, 0xFF), (0x00, 0xFF, 0x78), (0xFF, 0x6E, 0x41), (0x00, 0x5F, 0x39),
                           (0x6B, 0x68, 0x82), (0x5F, 0xAD, 0x4E), (0xA7, 0x57, 0x40), (0xA5, 0xFF, 0xD2),
                           (0xFF, 0xB1, 0x67), (0x00, 0x9B, 0xFF), (0xE8, 0x5E, 0xBE)]

        # Walk through an image pixel by pixel
        def walk(image):
            width, height = image.size
            # Go through each pixel sequentially
            for index, pixel in enumerate(image.getdata()):
                # Calculate the current position
                x = index % width
                y = index / width
                # Yield the current position and value
                yield (x, y, pixel)

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
                    blackpixel = (x, y)
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
                for x, y in processing:
                    # Color this neighbor
                    image.putpixel((x, y), color)
                    # Find all of the neighboring pixels
                    new = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                    # Go through the neighbors
                    for x, y in new:
                        if (x, y) in neighbors:
                            # Already added, skip
                            continue
                        if x < 0 or x >= width:
                            # Invalid x value, skip
                            continue
                        if y < 0 or y >= height:
                            # Invalid y value, skip
                            continue
                        if image.getpixel((x, y)) != (0, 0, 0):
                            # Non-black pixel, skip
                            continue
                        # Add the neighboring black pixel to be processed
                        neighbors.append((x, y))
        coloredPath = imagePath[:-4] + '-Colored.png'
        image.save(coloredPath)
        self.isolateObjects(coloredPath, colorindex)

    def isolateObjects(self, imagePath, numColors):
        image = Image.open(imagePath)

        DISTINCT_COLORS = [(0x00, 0xFF, 0x00), (0x00, 0x00, 0xFF), (0xFF, 0x00, 0x00), (0x01, 0xFF, 0xFE),
                           (0xFF, 0xA6, 0xFE), (0xFF, 0xDB, 0x66), (0x00, 0x64, 0x01), (0x01, 0x00, 0x67),
                           (0x95, 0x00, 0x3A), (0x00, 0x7D, 0xB5), (0xFF, 0x00, 0xF6), (0xFF, 0xEE, 0xE8),
                           (0x77, 0x4D, 0x00), (0x90, 0xFB, 0x92), (0x00, 0x76, 0xFF), (0xD5, 0xFF, 0x00),
                           (0xFF, 0x93, 0x7E), (0x6A, 0x82, 0x6C), (0xFF, 0x02, 0x9D), (0xFE, 0x89, 0x00),
                           (0x7A, 0x47, 0x82), (0x7E, 0x2D, 0xD2), (0x85, 0xA9, 0x00), (0xFF, 0x00, 0x56),
                           (0xA4, 0x24, 0x00), (0x00, 0xAE, 0x7E), (0x68, 0x3D, 0x3B), (0xBD, 0xC6, 0xFF),
                           (0x26, 0x34, 0x00), (0xBD, 0xD3, 0x93), (0x00, 0xB9, 0x17), (0x9E, 0x00, 0x8E),
                           (0x00, 0x15, 0x44), (0xC2, 0x8C, 0x9F), (0xFF, 0x74, 0xA3), (0x01, 0xD0, 0xFF),
                           (0x00, 0x47, 0x54), (0xE5, 0x6F, 0xFE), (0x78, 0x82, 0x31), (0x0E, 0x4C, 0xA1),
                           (0x91, 0xD0, 0xCB), (0xBE, 0x99, 0x70), (0x96, 0x8A, 0xE8), (0xBB, 0x88, 0x00),
                           (0x43, 0x00, 0x2C), (0xDE, 0xFF, 0x74), (0x00, 0xFF, 0xC6), (0xFF, 0xE5, 0x02),
                           (0x62, 0x0E, 0x00), (0x00, 0x8F, 0x9C), (0x98, 0xFF, 0x52), (0x75, 0x44, 0xB1),
                           (0xB5, 0x00, 0xFF), (0x00, 0xFF, 0x78), (0xFF, 0x6E, 0x41), (0x00, 0x5F, 0x39),
                           (0x6B, 0x68, 0x82), (0x5F, 0xAD, 0x4E), (0xA7, 0x57, 0x40), (0xA5, 0xFF, 0xD2),
                           (0xFF, 0xB1, 0x67), (0x00, 0x9B, 0xFF), (0xE8, 0x5E, 0xBE)]

        # Generator: Walk through an image pixel by pixel
        def walk(image):
            width, height = image.size
            # Go through each pixel sequentially
            for index, pixel in enumerate(image.getdata()):
                # Calculate the current position
                x = index % width
                y = index / width
                # Yield the current position and value
                yield (x, y, pixel)

        width, height = image.size
        image = image.convert('RGB')
        currentColor = 0
        seen = []

        for x, y, pixel in walk(image):
            if pixel != (255, 255, 255) and pixel not in seen:
                seen.append(pixel)

        numColors = len(seen)

        # Find the first pixel of the current color
        while True:
            # Don't search for further pixels if we have exhausted the available colors

            color = DISTINCT_COLORS[currentColor]
            currentColor += 1

            if currentColor > numColors:
                break
            print color
            # Find the first colored pixel that's not the color we're cropping
            coloredPixel = None
            for x, y, pixel in walk(image):
                if pixel != (255, 255, 255) and pixel != color:
                    # print x, y, pixel
                    coloredPixel = (x, y)
                    break
            if not coloredPixel:
                # Keep going until we find the colored pixel
                break

            # Track neighboring non-current colored pixels
            neighbors = [coloredPixel]

            # Keep finding neighboring non-current colored pixels until we can't find any more
            while len(neighbors) > 0:
                # Make list of the current pixels considered
                processing = list(neighbors)
                # Neighbors have been added to the processing list; clear the neighbors list
                neighbors = []
                for x, y in processing:
                    # White out this neighbor
                    image.putpixel((x, y), (255, 255, 255))
                    # Find all the neighbor pixels
                    new = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                    for x, y, in new:
                        if (x, y) in neighbors:
                            # Added, skip
                            continue
                        if x < 0 or x >= width:
                            # Not valid
                            continue
                        if y < 0 or y >= height:
                            # Not valid
                            continue
                        if image.getpixel((x, y)) == (255, 255, 255) or image.getpixel((x, y)) == color:
                            # This pixel is targeted for cropping, skip it and do NOT whiteout
                            continue

                        # If passed all conditions, add pixel to the neighbors of those that need to be whited out
                        neighbors.append((x, y))

            # Save the image to a new directory
            figure = imagePath[-13:-12]
            croppedPath = os.path.join(imagePath[:-13] + "Cropped Objects/")
            self.currentChar += 1
            isolatedPath = croppedPath + figure + "-" + self.objAlphabet[self.currentChar] + "-Cropped.png"
            image.save(isolatedPath)

            # Crop the isolated image to just the object and no extra whitespace
            self.cropObject(isolatedPath, color)

            # Reopen the original image and isolate the next object
            image = Image.open(imagePath)

    def cropObject(self, path, color):
        image = Image.open(path)
        width, height = image.size
        leftmost = width
        uppermost = height
        rightmost = 0
        bottomost = 0

        def walk(image):
            width, height = image.size
            # Go through each pixel sequentially
            for index, pixel in enumerate(image.getdata()):
                # Calculate the current position
                x = index % width
                y = index / width
                # Yield the current position and value
                yield (x, y, pixel)

        # Walk the image and find the rightmost, leftmost, bottommost and uppermost pixels to use for cropping the object
        for x, y, pixel in walk(image):
            if pixel != (255, 255, 255) and pixel == color:
                if x > rightmost:
                    rightmost = x
                if x < leftmost:
                    leftmost = x
                if y > bottomost:
                    bottomost = y
                if y < uppermost:
                    uppermost = y

        cropCoords = (leftmost, uppermost, rightmost, bottomost)

        #Store the current object and its color and cropCoords for later use
        objectID = path[-15:-12]
        self.objectInfo[objectID] = info = {}
        info['color'] = color
        info['coords'] = cropCoords
        # Crop the image with the ascertained coordinates and then save the image
        image = image.crop(cropCoords)
        image.save(path)

    def findShape(self, path):
        image = Image.open(path)
        width, height = image.size
        total = width * height
        print path

        def walk(image):
            width, height = image.size
            # Go through each pixel sequentially
            for index, pixel in enumerate(image.getdata()):
                # Calculate the current position
                x = index % width
                y = index / width
                # Yield the current position and value
                yield (x, y, pixel)

        # Walk the image and find the rightmost, leftmost, bottommost and uppermost pixels to use for cropping the object
        prevLine = -1
        outerWhite = 0.
        firstPixels = {}
        lastPixels = {}
        firstFound = None

        # Find the first and last non-white pixels in a row of the image and store them
        for x, y, pixel in walk(image):

            if y > prevLine:
                firstFound = False

            if pixel != (255, 255, 255) and firstFound is False:
                firstFound = True
                firstPixels[y] = (x, y)
            if pixel != (255, 255, 255):
                lastPixels[y] = (x, y)

            prevLine = y

        # Iterate over each line again and count all the pixels prior to the first non-white pixel and after the last non-white pixel
        for x, y, pixel in walk(image):
            try:
                firstX = firstPixels[y][0]
                lastX = lastPixels[y][0]

                if x < firstX or x > lastX:
                    outerWhite += 1
            except KeyError:
                pass

        # Calculate the ratio between the total number of pixels and the white pixels outside the shape; use this as an estimation of similar objects
        ratio = outerWhite / total
        return ratio

    def findFill(self, path):
        image = Image.open(path)
        width, height = image.size

        def walk(image):
            width, height = image.size
            # Go through each pixel sequentially
            for index, pixel in enumerate(image.getdata()):
                # Calculate the current position
                x = index % width
                y = index / width
                # Yield the current position and value
                yield (x, y, pixel)

        # Walk the image and find the rightmost, leftmost, bottommost and uppermost pixels to use for cropping the object
        prevLine = -1
        innerWhite = 0.
        innerTotal = 0.
        firstPixels = {}
        lastPixels = {}
        firstFound = None
        fillEstimate = None

        # Find the first and last non-white pixels in a row of the image and store them
        for x, y, pixel in walk(image):
            if y > prevLine:
                firstFound = False

            if pixel != (255, 255, 255) and firstFound is False:
                firstFound = True
                firstPixels[y] = (x, y)
            if pixel != (255, 255, 255):
                lastPixels[y] = (x, y)

            prevLine = y

        # Iterate over each line again and count all the pixels prior to the first non-white pixel and after the last non-white pixel
        for x, y, pixel in walk(image):
            try:
                firstX = firstPixels[y][0]
                lastX = lastPixels[y][0]

                if x > firstX or x < lastX:
                    innerTotal += 1
                    if pixel == (255, 255, 255):
                        innerWhite += 1
            except KeyError:
                pass

        whitePercent = innerWhite / innerTotal * 100
        # print innerWhite, innerTotal
        # print path, " ", whitePercent

        if whitePercent > 70:
            fillEstimate = "no"
        elif whitePercent < 70:
            fillEstimate = "yes"

        # TODO: account for half filled objects

        return fillEstimate

    def findRotation(self, path):
        # TODO: implement logic to find centroid, vertices, and comparable rotation between each other object

        return 0

    def findPosition(self, figureID, objectID):

        aboveStr = ""
        insideStr = ""
        leftOfStr = ""

        object = figureID + "-" + objectID
        currLeft, currUpper, currRight, currBottom = self.objectInfo.get(object)['coords']

        # For each object in this figure that is not the current object we're looking at, compare crop coordinates
        for key in self.objectInfo:
            if key != object and (figureID + "-") in key:
                compLeft, compUpper, compRight, compBottom = self.objectInfo.get(key)['coords']

                # Check if current object is above the comparison object
                if currBottom < compUpper:
                    aboveStr += (key[2:3] + ", ")
                # Check if hte current object is left-of the comparison object
                if currRight < compLeft:
                    leftOfStr += (key[2:3] + ", ")
                if (currLeft < compLeft and currUpper < compUpper) and (currRight > compRight and currBottom > compBottom):
                    insideStr += (key[2:3] + ", ")

        # Build position string; compilation of all positional values
        positionStr = ""
        if aboveStr != "":
           positionStr += "        above:" + aboveStr[:-2] + "\n"

        if insideStr != "":
            positionStr += "        inside:" + insideStr[:-2] + "\n"

        if leftOfStr != "":
            positionStr += "        left-of:" + leftOfStr[:-2] + "\n"

        return positionStr


