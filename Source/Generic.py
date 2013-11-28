import pygame, math

"""
 " Constants
"""
# Window properties
WINDOW_WIDTH                =   900
WINDOW_HEIGHT               =   500
FRAMERATE                   =   30

# Gameplay properties
POINTS_PER_GOOD_APPLE       =   1
POINTS_PER_BAD_APPLE        =   0
POINTS_PER_SPECIAL_APPLE    =   2
TIME_PER_GOOD_APPLE         =   2
TIME_PER_BAD_APPLE          =   -2
TIME_PER_SPECIAL_APPLE      =   5
POINTS_PER_BUTTERFLY        =   0
TIME_PER_BUTTERFLY          =   -20

# Power gauge speed modifier
POWER_MODIFIER              =   6

# Apple types
APPLE_GOOD                  =   0
APPLE_BAD                   =   1
APPLE_SPECIAL               =   2

# Butterfly types
BUTTERFLY_ORANGE            =   0
BUTTERFLY_PINK              =   1
BUTTERFLY_YELLOW            =   2

# User events
EVENT_APPLE_HIT             =   pygame.USEREVENT + 1
EVENT_BUTTERFLY_HIT         =   pygame.USEREVENT + 2
EVENT_GAME_OVER             =   pygame.USEREVENT + 3
EVENT_DIFFICULTY_ADJUSTMENT =   pygame.USEREVENT + 4

# Physical constants
ACCELERATION_DUE_TO_GRAVITY =   9.81
KNOTS_TO_METERS_PER_SECOND  =   0.51444
PIXELS_PER_METER            =   100

# Butterfly bezier path points
BUTTERFLY_PATH              =   [[[-10, 200], [100, 400], [300, 10], [500, 700], [750, -50]],
                                 [[-10, -10], [100, 400], [30, 60], [100, 400], [600, 400], [910, 200]],
                                 [[950, -10], [700, 550], [400, 20], [200, 550], [-10, -10]],
                                 [[500, -20], [30, 700], [600, 40], [950, -20]]]

# Apple locations
APPLE_LOCATIONS             =   [[663, 115], [736, 102], [711, 141], [777, 143], [672, 170],
                                 [750, 176], [621, 205], [801, 196], [738, 221], [673, 247],
                                 [628, 256], [786, 261], [839, 259], [606, 291], [734, 283],
                                 [666, 311], [846, 309]]

# Clouds
CLOUDS                      =   [("..\\Resources\\cloud02.png", [-700, -220]), ("..\\Resources\\cloud01.png", [-300, -205]),
                                 ("..\\Resources\\cloud01.png", [50, -210]), ("..\\Resources\\cloud02.png", [500, -200])]

# Game difficulty adjustments
DIFFICULTY                  =   [(10, 2, False, False), (15, 3, True, False), (30, 1, False, False), (50, -1, True, False),
                                 (70, -2, False, False), (90, -3, True, False), (100, 1, False, False), (120, 2, True, False),
                                 (135, -1, False, False), (150, 2, False, False), (170, -1, True, False), (180, -3, True, False)]

"""
 " Rotate Center
 "   Rotates a surface around it's center point, with anti-aliasing
 "
 "   @param image: the surface to rotate
 "   @param rect: the rectangle associated with the surface
 "   @param angle: the angle in degrees to rotate the image by
"""
def rotateCenter(image, rect, angle):
    rotatedImage = pygame.transform.rotozoom(image, angle, 1)
    rotatedRect = rotatedImage.get_rect(center = rect.center)
    return rotatedImage, rotatedRect

"""
 " Rotate Point
 "   Rotates a rectangle around a specific point
 "
 "   @param rect: the rectangle to rotate
 "   @param point: the point to rotate the rectangle about
 "   @param angle: the angle in radians to rotate through
"""
def rotatePoint(rect, point, angle):
    sinAngle = math.sin(angle)
    cosAngle = math.cos(angle)
    newX = point[0] - (cosAngle * (rect.centerx - point[0]) - sinAngle * (rect.centery - point[1]))
    newY = point[1] + (sinAngle * (rect.centerx - point[0]) + cosAngle * (rect.centery - point[1]))
    return newX, newY

"""
 " Calculate Velocity
 "   Calculates the velocity of the arrow given power and cloud speed by taking the square
 "   root of the power multiplied by 1.2. Cloud speed is converted from knots to meters
 "   per second and added to the overall velocity
 "
 "   @param power: the percentage of the power bar filled
 "   @param cloudSpeed: the current speed of the clouds in knots
"""
def calculateVelocity(power, cloudSpeed):
    return (math.sqrt(power) * 1.2 + (cloudSpeed * KNOTS_TO_METERS_PER_SECOND))

"""
 " Bernstein
 "   @param i: ith point
 "   @param n: total number of points
 "   @param t: time value between 0 and 1
"""
def bernstein(i, n, t):
    return math.factorial(n) / (math.factorial(i) * math.factorial(n - i)) * math.pow(t, i) * math.pow(1 - t, n - i)

"""
 " Get Bezier Point
 "   Gets a point on a bezier curve that fits the points given, at the time given
 "
 "   @param t: time value between 0 and 1
 "   @param points: list of points to calculate the curve path
"""
def getBezierPoint(t, points):
    result = [0, 0]
    numElements = len(points) - 1
    for i in range(numElements + 1):
        result[0] += points[i][0] * bernstein(i, numElements, t)
        result[1] += points[i][1] * bernstein(i, numElements, t)
    return result

"""
 " Get Image Part
 "   Gets a certain part of an image, returning a surface and its rectangle
 "
 "   @param rect: rectangle describing the surface
 "   @param surface: surface to draw the image part on
 "   @param image: the surface containing the full image
 "   @param height: height in pixels to extract from the image
 "   @param width: width in pixels to extract from the image
 "   @param position: the top left coordinate to start extracting from
 "   @param location: center coordinates to re-position the surface at (default = None)
"""
def getImagePart(rect, surface, image, height, width, position, location = None):
    rect = pygame.Rect(position, 0, width, height)
    surface = pygame.Surface(rect.size, flags = pygame.SRCALPHA)
    surface.blit(image, (0, 0), rect)
    if (location is not None):
        rect.center = location
    return rect, surface
