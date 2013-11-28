import pygame, sys, math, datetime
import ConfigParser
import Generic
from Generic import *
from pygame.sprite import *
from random import randint

"""
 " Banner
 "   This sprite implements the main interface banner; displaying power, time remaining,
 "   the current score and the wind speed.
 "
 "   Banner inherits from Sprite to allow layered drawing in the game loop
"""
class Banner(Sprite):
    image = None                # The banner surface
    rect = None                 # Banner rectangle
    power = None                # The current power percentage
    timeRemaining = 0           # The time remaining in seconds
    startTimeRem = 0            # The number of seconds remaining at the start of the game
    points = None               # The number of points obtained
    windSpeed = None            # The wind speed in knots
    bannerFont = None           # Generic font for all banner text

    """
     " Constructor
     "   @param power: the initial power setting (default = 0)
     "   @param timeRemaining: the initial amount of time remaining in seconds (default = 120)
     "   @param points: the initial number of points (default = 0)
     "   @param windSpeed: the initial wind speed (default = 2)
    """
    def __init__(self, power = 0, timeRemaining = 120, points = 0, windSpeed = 1):
        Sprite.__init__(self)
        Banner.image = pygame.image.load("..\\Resources\\banner.png")
        Banner.rect = Banner.image.get_rect()
        Banner.bannerFont = pygame.font.SysFont("Segoe UI Semibold", 20)
        Banner.power = power
        Banner.points = points
        Banner.timeRemaining = timeRemaining
        Banner.startTimeRem = timeRemaining
        Banner.windSpeed = windSpeed
        
    """
     " Set Power
     "   Sets the power shown on the power gauge
    """
    @staticmethod
    def setPower(power): Banner.power = power
    
    """
     " Get Power
     "   Gets the current power setting
    """
    @staticmethod
    def getPower(): return Banner.power

    """
     " Adjust Points
     "   This method increases or decreases the total number of points obtained
     "   Upon a point change, the difficulty is re-evaluated
     "
     "   @param points: the number of points to increase (+ve) or decrease (-ve)
    """
    @staticmethod
    def adjustPoints(points):
        if (points < 0):
            if (Banner.points < math.fabs(points)):
                Banner.points = 0
            else:
                Banner.points += points
        else:
            Banner.points += points

        # Re-evaluate the difficulty
        Banner.adjustDifficulty(Banner.getPoints(), Banner.getTimeRemaining())
    
    """
     " Reset Points
     "   This method resets the number of points to zero
    """
    @staticmethod
    def resetPoints(): Banner.points = 0

    """
     " Get Points
     "   Gets the number of points currently scored by the user
    """
    @staticmethod
    def getPoints(): return Banner.points

    """
     " Adjust Time Remaining
     "   This method increases or decreases the total time remaining in the game
     "
     "   @param time: the number of second to increment (+ve) or decremenet (-ve)
    """
    @staticmethod
    def adjustTimeRemaining(time):
        if (time < 0):
            if (Banner.timeRemaining < math.fabs(time)):
                Banner.timeRemaining = 0
            else:
                Banner.timeRemaining += time
        else:
            Banner.timeRemaining += time
    
    """
     " Reset Time Remaining
     "   This method resets the time remaining to the number of seconds originally
     "   passed to the constructor
    """
    @staticmethod
    def resetTimeRemaining(): Banner.timeRemaining = Banner.startTimeRem

    """
     " Get Time Remaining
     "   Gets the number of seconds remaining in the game
    """
    @staticmethod
    def getTimeRemaining(): return Banner.timeRemaining
    
    """
     " Set Wind Speed
     "   Sets the current wind speed (in knots)
    """
    @staticmethod
    def setWindSpeed(windSpeed):
        Banner.windSpeed = windSpeed

    """
     " Get Wind Speed
     "   Gets the current wind speed (in knots)
    """
    @staticmethod
    def getWindSpeed(): return Banner.windSpeed

    """
     " Update
     "   Updates the entire banner surface to reflect any changes in power, score,
     "   time or wind speed
    """
    @staticmethod
    def update():
        # Reset the background image to preserve transparency
        Banner.image = pygame.image.load("..\\Resources\\banner.png")

        # Colour the time remaining according to limits
        timeColour = (84, 223, 0)
        if (Banner.timeRemaining <= 10):
            timeColour = (222, 0, 4)
        elif (Banner.timeRemaining <= 20):
            timeColour = (255, 142, 0)

        # Calculate the minutes and seconds remaining in play
        minsRemaining, secsRemaining = divmod(Banner.timeRemaining, 60)

        # Power indicator rectangle creation
        if (Banner.power != 0):
            powerRect = pygame.Rect(11, 10, math.ceil(math.fabs(Banner.power) * 1.6), 20);
            pygame.draw.rect(Banner.image, (math.fabs(math.floor((Banner.power) * 2.5)), 200, 70), powerRect, 0)

        # Construct game status text
        score = Banner.bannerFont.render("Score: " + str(Banner.points), True, (39, 39, 39))
        time = Banner.bannerFont.render("%02d:%02d" % (minsRemaining, secsRemaining), True, timeColour)
        windSpeed = Banner.bannerFont.render("Wind speed: " + str(Banner.windSpeed) + "kts", True, (39, 39, 39))
        
        # Draw updated text to the banner image
        Banner.image.blit(score, (182, 5))
        Banner.image.blit(time, (425, 5))
        Banner.image.blit(windSpeed, (720, 5))

        # Check if the game has ended
        if (Banner.getTimeRemaining() <= 0):
            pygame.event.post(pygame.event.Event(Generic.EVENT_GAME_OVER))

    """
     " Adjust Difficulty
     "   Evaluates the current game state and adjusts the difficulty accordingly by
     "   introducing wind changes and more butterflies
     "
     "   @param points: the number of points currently obtained
     "   @param timeRemaining: the number of seconds remaining in the game
    """
    @staticmethod
    def adjustDifficulty(points, timeRemaining):
        if ((points % 100 is 0) or (points % 100 is 1)):
            for index, diff in enumerate(Generic.DIFFICULTY):
                Generic.DIFFICULTY[index] = (diff[0], diff[1], diff[2], False)
        else:
            for index, diff in enumerate(Generic.DIFFICULTY):
                if ((diff[3] is False) and (diff[0] is points)):
                    Generic.DIFFICULTY[index] = (diff[0], diff[1], diff[2], True)
                    pygame.event.post(pygame.event.Event(Generic.EVENT_DIFFICULTY_ADJUSTMENT, { 'windSpeedAdjustment': diff[1], 'addButterfly': diff[2] }))


"""
 " Grass
 "   Object defining the grass layer
"""
class Grass(Sprite):
    image = None    # Grass image
    rect = None     # Grass rectangle

    """
     " Constructor
    """
    def __init__(self):
        Sprite.__init__(self)
        if (Grass.image is None):
            Grass.image = pygame.image.load("..\\Resources\\grass.png")
        Grass.rect = [0, 415]


"""
 " Ground
 "   Object defining the ground layer
"""
class Ground(Sprite):
    image = None    # Ground image
    rect = None     # Ground rectangle

    def __init__(self):
        Sprite.__init__(self)
        if (Ground.image is None):
            Ground.image = pygame.image.load("..\\Resources\\ground.png")
        Ground.rect = [0, 487]

"""
 " Tree
 "   Object defining the tree layer
"""
class Tree(Sprite):
    image = None    # Tree image
    rect = None     # Tree rectangle

    def __init__(self):
        Sprite.__init__(self)
        if (Tree.image is None):
            Tree.image = pygame.image.load("..\\Resources\\tree.png")
        Tree.rect = [572, 78]


"""
 " Archer Legs
 "   Object defining the lower static section of the archer
"""
class ArcherLegs(Sprite):
    image = None    # Archer legs image
    rect = None     # Archer legs rectangle

    def __init__(self):
        Sprite.__init__(self)
        if (ArcherLegs.image is None):
            ArcherLegs.image = pygame.image.load("..\\Resources\\archerLegs.png")
        ArcherLegs.rect = [40, 410]

"""
 " Archer Torso
 "   Object defining the upper rotatable section of the archer
"""
class ArcherTorso(Sprite):
    image = None    # Archer torso image
    rect = None     # Archer torso rectangle

    def __init__(self):
        Sprite.__init__(self)
        if (ArcherTorso.image is None):
            ArcherTorso.image = pygame.image.load("..\\Resources\\archerTorso.png")
        ArcherTorso.rect = ArcherTorso.image.get_rect()
        ArcherTorso.rect.x = -2
        ArcherTorso.rect.y = 305

    """
     " Update
     "   Updates the angle of the archer torso. The image is reloaded to avoid
     "   bluring
     "
     "   @param angle: the angle in radians to rotate the archer torso by
    """
    def update(self, angle):
        self.image = pygame.image.load("..\\Resources\\archerTorso.png")
        self.image, self.rect = rotateCenter(self.image, self.rect, math.degrees(angle))

"""
 " Arrow Sprite
 "   Sprite defining functionality for an arrow and the flight of an arrow. Air
 "   resistance is not taken into account.
"""
class Arrow(Sprite):
    image = None                # Arrow image
    rect = None                 # Arrow rectangle
    fired = False               # True if the arrow has been fired
    flying = False              # True if the arrow is in a flying state
    initialVelocity = 0         # The velocity that the arrow was fired at (in meters per second)
    initialPosition = [0, 0]    # The initial position of the arrow
    previousCenter = [0, 0]     # The previous center location of the arrow

    """
     " Constructor
    """
    def __init__(self):
        Sprite.__init__(self)
        if (Arrow.image is None):
            Arrow.image = pygame.image.load("..\\Resources\\arrow.png")
        self.rect = self.image.get_rect()
        self.update(0)

    """
     " Update
     "   Updates the arrow position and angle based on the previous location
     "   of the arrow
     "   
     "   @param angle: the angle of the arrow in radians
    """
    def update(self, angle):
        # Reload the image to prevent bluring
        self.image = pygame.image.load("..\\Resources\\arrow.png")

        # Static rotation
        if (self.flying == False):
            self.rect = self.image.get_rect()
            self.rect.center = [-4, 364]
            self.rect.x, self.rect.y = rotatePoint(self.rect, [24, 410], angle)

        # Rotate the arrow about the center
        self.image, self.rect = rotateCenter(self.image, self.rect, math.degrees(angle))
        self.previousCenter = self.rect.center

    """
     " Fire
     "   Fires the arrow, saving the initial velocity and initial position for
     "   further calculations
     "
     "   @param power: the percentage of power when the mouse was released
     "   @param windSpeed: the current wind speed
    """
    def fire(self, power, windSpeed):
        self.fired = True
        self.flying = True
        self.initialVelocity = calculateVelocity(power, windSpeed)
        self.initialPosition = self.rect.center
        
    """
     " Fly
     "   Moves and rotates the arrow along the parabolic path calculated with
     "   standard equations of motion, excluding any effects of air resistance
     "
     "   @param time: seconds since the arrow was fired
     "   @param initialAngle: initial angle that the arrow was fired at
     "   @param angle: the angle at the current time
    """
    def fly(self, time, initialAngle):
        if (time != 0):
            # Calculation of arrow position
            x = self.initialVelocity * time * math.cos(initialAngle)
            y = self.initialVelocity * time * math.sin(initialAngle) - ((Generic.ACCELERATION_DUE_TO_GRAVITY * math.pow(time, 2)) / 2)

            # Apply the changes
            self.rect.centerx = (x * Generic.PIXELS_PER_METER) + self.initialPosition[0]
            self.rect.centery = self.initialPosition[1] - (y * Generic.PIXELS_PER_METER)

            # Rotate the arrow
            angle = -(math.atan2(self.previousCenter[1] - self.rect.centery, self.previousCenter[0] - self.rect.centerx)) + math.pi
            self.update(angle)

            # Checks the bounds of the arrow
            if (self.rect.bottom >= Generic.WINDOW_HEIGHT - 16) or (self.rect.left > Generic.WINDOW_WIDTH) or (self.rect.right < 0):
                self.flying = False


"""
 " Cloud Sprite
 "   Generic sprite for several types of clouds
"""
class Cloud(Sprite):
    image = None    # Cloud image
    rect = None     # Cloud rectangle

    """
     " Constructor
     "   @param image: the location of the cloud image to load
     "   @param location: the top-left location of the cloud
    """
    def __init__(self, image, location):
        Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    """
     " Update
     "   Updates the position of the cloud, wrapping round if the rectangle
     "   travels off the renderable area
     "
     "   @param cloudSpeed: the speed of the clouds
    """
    def update(self, cloudSpeed):
        self.rect.x += cloudSpeed
        if (self.rect.left > Generic.WINDOW_WIDTH):
            self.rect.right = 0
        elif (self.rect.right < 0):
            self.rect.left = Generic.WINDOW_WIDTH

"""
 " Apple Sprite
 "   Generic sprite to randomise apple colour and handle the collision of arrow
 "   and apple by showing a hitsplat
"""
class Apple(Sprite):
    image = None        # Apple image
    rect = None         # Apple rectangle
    mask = None         # Generic apple mask for pixel-perfect collisions
    appleHit = False    # True if the apple has been hit
    appleType = 0       # The apple type (see Generic.APPLE_*)
    splat = None        # The apple splat graphic
    splatXPos = 0       # The current X-position in the hitsplat sheet
    pointsPerApple = 0  # The number of points awarded per apple hit (type dependant)
    timePerApple = 0    # The number of seconds awarded per apple hit (type dependant)
    appleInitTicks = 0  # The number of game ticks when the apple was last changed
    appleTimeout = 0    # The number of milliseconds the apple lives for before changing type

    """
     " Constructor
     "   @param location: the center location of the apple
     "   @param time: number of game ticks when the apple was initialised
    """
    def __init__(self, location, time):
        Sprite.__init__(self)
        self.load(location, time)
        if (Apple.mask is None):
            Apple.mask = pygame.mask.from_surface(self.image)

    """
     " Load
     "   Loads the core settings for an individual apple. Type and timeout
     "   are randomised and all other resources are loaded according to this
     "   random selection
     "
     "   @param location: the center location of the apple
     "   @param time: number of game ticks when the apple was initialised
    """
    def load(self, location, time):
        # Randomise the apple type and timeout
        self.appleType = randint(Generic.APPLE_GOOD, Generic.APPLE_SPECIAL)
        self.appleTimeout = randint((((-self.appleType + 2) * 3000) + 1000), 20000)

        # Record the initial settings
        self.appleInitTicks = time
        self.appleHit = False
        self.splatXPos = 0

        # Load the appropriate apple and hitplat resources
        if (self.appleType == Generic.APPLE_BAD):
            self.image = pygame.image.load("..\\Resources\\appleBad.png")
            self.splat = pygame.image.load("..\\Resources\\hitsplatBrown.png")
            self.pointsPerApple = Generic.POINTS_PER_BAD_APPLE
            self.timePerApple = Generic.TIME_PER_BAD_APPLE
        elif (self.appleType == Generic.APPLE_SPECIAL):
            self.image = pygame.image.load("..\\Resources\\appleSpecial.png")
            self.splat = pygame.image.load("..\\Resources\\hitsplatBlue.png")
            self.pointsPerApple = Generic.POINTS_PER_SPECIAL_APPLE
            self.timePerApple = Generic.TIME_PER_SPECIAL_APPLE
        else:
            self.image = pygame.image.load("..\\Resources\\appleGood.png")
            self.splat = pygame.image.load("..\\Resources\\hitsplatRed.png")
            self.pointsPerApple = Generic.POINTS_PER_GOOD_APPLE
            self.timePerApple = Generic.TIME_PER_GOOD_APPLE

        # Store and update the location of the apple
        self.rect = self.image.get_rect()
        self.rect.center = location

    """
     " Hit
     "   Triggers a hitsplat to show in place of the apple, giving feedback to the user
     "   regarding the success of their shot
    """
    def hit(self):
        if (self.appleHit is False):
            # Update the sprite surface
            self.rect, self.image = Generic.getImagePart(self.rect, self.image, self.splat, 62, 47, self.splatXPos, self.rect.center)
            
            # Add 500ms to the timeout to avoid double-hitting
            self.appleTimeout += 500

            # Trigger an event to update the hitsplat in further loops
            pygame.event.post(pygame.event.Event(Generic.EVENT_APPLE_HIT, { 'apple': self }))

            # Update the score
            Banner.adjustPoints(self.pointsPerApple)
            Banner.adjustTimeRemaining(self.timePerApple)
            self.appleHit = True

    """
     " Update
     "   Updates the hitsplat. It is assumed that this method will be called only when
     "   the apple has been hit, this condition is not checked
    """
    def update(self):
        # Move to the next sprite on the sheet
        self.splatXPos += 47

        # Update the sprite surface
        self.rect, self.image = Generic.getImagePart(self.rect, self.image, self.splat, 62, 47, self.splatXPos, self.rect.center)

        # Only request further updates while there are sprites to draw
        if (self.splatXPos < 752):
            pygame.event.post(pygame.event.Event(Generic.EVENT_APPLE_HIT, { 'apple': self }))

    """
     " Change
     "   Reloads the apple provided the current apple has timed out
    """
    def change(self, thisFrameTicks):
        if (thisFrameTicks > (self.appleInitTicks + self.appleTimeout)):
            self.load(self.rect.center, thisFrameTicks)

"""
 " Butterfly Sprite
 "   Animated sprite flips between three images drawn on butterfly*.png graphics. A
 "   generic hitplat is shown when the butterfly is hit.
"""
class Butterfly(Sprite):
    image = None			# Current butterfly image
    rect = None				# Butterfly rectangle
    mask = None				# Mask of the largest butterfly sprite
    butterflyHit = False	# True if the butterfly has been hit
    butterflyHitTicks = 0   # Number of game ticks when the butterfly was hit
    butterflyType = 0		# The butterfly type (see Generic)
    butterfly = None		# Butterfly sprite sheet
    butterflyXPos = 0		# Current X position on the butterfly sprite sheet
    splat = None			# The butterfly splat sprite sheet
    splatXPos = 0			# Current X position on the splat sprite sheet
    pointsPerButterfly = 0	# Points awarded for hitting a butterfly
    timePerButterfly = 0	# Time awarded for hitting a butterfly
    initialTicks = 0		# Number of game ticks when the sprite was initialised
    butterflyTimeout = 0    # Number of game ticks after the initial path to
    butterflyFlightTime = 0 # Number of game ticks the butterfly will be flying for
    butterflyPath = 0       # Butterfly path ID (see Generic.BUTTERFLY_PATH)

    """
     " Constructor
     "   @param time: number of ticks when the butterfly is initialised
    """
    def __init__(self, time):
        Sprite.__init__(self)   # Initialise the sprite
        self.load(time)         # Load a butterfly onto the surface

        # Mask the default butterfly position
        if (Butterfly.mask is None):
            Butterfly.mask = pygame.mask.from_surface(self.image)
        
    """
     " Load
     "   Clears the changable variables and randomises the butterfly type and colour to
     "   create the appearance of a new butterfly instance.
     "
     "   @param time: number of ticks when the butterfly is initialised
    """
    def load(self, time):
        # General instance varaible initialisation
        self.butterflyHitTicks = 0
        self.butterflyXPos = 0
        self.splatXPos = 0
        self.butterflyType = randint(Generic.BUTTERFLY_ORANGE, Generic.BUTTERFLY_YELLOW)
        self.butterflyTimeout = randint(((-self.butterflyType + 2) * 6000) + 1000, 15000)
        self.butterflyPath = randint(0, len(Generic.BUTTERFLY_PATH) - 1)
        self.butterflyFlightTime = randint((len(Generic.BUTTERFLY_PATH[self.butterflyPath]) * 1000) - 1000, (len(Generic.BUTTERFLY_PATH[self.butterflyPath]) * 1000) + 3000)
        self.splat = pygame.image.load("..\\Resources\\hitsplatOrange.png")
        self.initialTicks = time
        self.butterflyHit = False
        self.splatXPos = 0
        self.pointsPerButterfly = Generic.POINTS_PER_BUTTERFLY
        self.timePerButterfly = Generic.TIME_PER_BUTTERFLY

        # Load the appropriate butterfly resources
        if (self.butterflyType == Generic.BUTTERFLY_ORANGE):
            self.butterfly = pygame.image.load("..\\Resources\\butterflyOrange.png")
        elif (self.butterflyType == Generic.BUTTERFLY_PINK):
            self.butterfly = pygame.image.load("..\\Resources\\butterflyPink.png")
        else:
            self.butterfly = pygame.image.load("..\\Resources\\butterflyYellow.png")
        
        # Update the sprite surface
        self.rect, self.image = Generic.getImagePart(self.rect, self.image, self.butterfly, 26, 35, self.butterflyXPos)
        
    """
     " Hit
     "   Triggers the hitsplat for the butterfly and adjusts the points and time accordingly
     "   An event is posted to the main loop so the hitsplat can be drawn again in further loops
    """
    def hit(self, thisFrameTicks):
        if (self.butterflyHit is False):
            # Record the hit
            self.butterflyHit = True
            self.butterflyHitTicks = thisFrameTicks

            # Update the sprite surface
            self.rect, self.image = Generic.getImagePart(self.rect, self.image, self.splat, 65, 92, self.splatXPos, self.rect.center)
        
            # Post an event to update the hitsplat in the next loop
            pygame.event.post(pygame.event.Event(Generic.EVENT_BUTTERFLY_HIT, { 'butterfly': self }))

            # Update the score
            Banner.adjustPoints(self.pointsPerButterfly)
            Banner.adjustTimeRemaining(self.timePerButterfly)

    """
     " Update
     "   Updates the butterfly image and location based on a random selection from preset Bezier
     "   curves defined in Generic.BUTTERFLY_PATH.
     "
     "   @param thisFrameTicks: the ticks when the function was called
    """
    def update(self, thisFrameTicks):
        if (self.butterflyHit is False):
            # Loop back to the start of the image if we reached the end
            if (self.butterflyXPos == 70):
                self.butterflyXPos = 0
        
            # Update the sprite surface
            self.rect, self.image = Generic.getImagePart(self.rect, self.image, self.butterfly, 26, 35, self.butterflyXPos)
            self.butterflyXPos += 35

            # Move the butterfly until the timeout has been reached
            if ((thisFrameTicks - self.initialTicks) < self.butterflyFlightTime):
                self.rect.center = getBezierPoint((thisFrameTicks - self.initialTicks) / (self.butterflyFlightTime * 1.0), Generic.BUTTERFLY_PATH[self.butterflyPath])
            else:
                self.butterflyHit = True
                self.butterflyHitTicks = thisFrameTicks
                self.rect.center = [-50, -50]
        elif (thisFrameTicks - self.butterflyHitTicks > self.butterflyTimeout):
            self.load(thisFrameTicks)
        
    """
     " Update Splat
     "   Updates the splat graphic at a fixed location, the point where the butterfly was hit.
     "   A new event is posted to keep the splat updating while there are more images to show.
    """
    def updateSplat(self):
        # Update the sprite surface
        self.rect, self.image = Generic.getImagePart(self.rect, self.image, self.splat, 65, 92, self.splatXPos, self.rect.center)

        # Move along to the next image
        self.splatXPos += 92

        # Post an event to update the hitsplat in the next loop
        if (self.splatXPos <= 1472):
            pygame.event.post(pygame.event.Event(Generic.EVENT_BUTTERFLY_HIT, { 'butterfly': self }))

"""
 " Pause Overlay
 "   This sprite implements the pause overlay graphic, which is displayed when
 "   the user presses the p key during gameplay
"""
class Pause(Sprite):
    image = None    # Pause overlay image
    rect = None     # Pause overlay rectangle

    def __init__(self):
        Sprite.__init__(self)
        if (Pause.image is None):
            Pause.image = pygame.image.load("..\\Resources\\pause.png")
        Pause.rect = Pause.image.get_rect()

"""
 " Help Overlay
 "   This sprite implements the help overlay graphic, which is displayed when
 "   the user presses the h key during gameplay
"""
class Help(Sprite):
    image = None    # Help overlay image
    rect = None     # Help overlay rectangle

    def __init__(self):
        Sprite.__init__(self)
        if (Help.image is None):
            Help.image = pygame.image.load("..\\Resources\\help.png")
        Help.rect = Help.image.get_rect()

"""
 " Restart Overlay
 "   This sprite implements the restart overlay graphic. The user's score and current
 "   highscore are both displayed on this page.
 "
 "   The page can be triggered at any time via the r key or when the timer reaches zero
"""
class Restart(Sprite):
    image = None            # Restart overlay image
    rect = None             # Restart overlay rectangle
    scoreFont = None        # The user's score font
    highscoreFont = None    # The user's highscore font 

    """
     " Constructor
    """
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("..\\Resources\\restart.png")

        # Initialise the fonts
        self.scoreFont = pygame.font.SysFont("Segoe UI Semibold", 140)
        self.highscoreFont = pygame.font.SysFont("Segoe UI Semibold", 14)
        self.rect = self.image.get_rect()

        # Get the highscore
        highscore = Restart.getHighscore()
        if (Banner.getPoints() > highscore):
            highscore = Banner.getPoints()
            Restart.updateHighscore(highscore)

        # Construct text
        score = self.scoreFont.render(str(Banner.points), True, (255, 255, 255))
        highscore = self.highscoreFont.render("Highscore: " + str(highscore), True, (255, 255, 255))
        
        # Position the text in the center of the window
        scoreRect = score.get_rect(center = (Generic.WINDOW_WIDTH / 2, Generic.WINDOW_HEIGHT / 2))
        highscoreRect = highscore.get_rect(center = (Generic.WINDOW_WIDTH / 2, (Generic.WINDOW_HEIGHT / 2) + 85))

        # Draw updated text to the surface
        self.image.blit(score, scoreRect)
        self.image.blit(highscore, highscoreRect)

    """
     " Get Highscore
     "   Gets the current highscore stored in settings.ini
    """
    @staticmethod
    def getHighscore():
        config = ConfigParser.RawConfigParser()
        config.read('settings.ini')
        return config.getint('SCORE', 'highscore')

    """
     " Update Highscore
     "   Updates the current highscore stored in settings.ini
     "   @param highscore: the new highscore to write
    """
    @staticmethod
    def updateHighscore(highscore):
        config = ConfigParser.RawConfigParser()
        config.add_section('SCORE')
        config.set('SCORE', 'highscore', str(highscore))
        with open('settings.ini', 'wb') as configfile:
            config.write(configfile)
