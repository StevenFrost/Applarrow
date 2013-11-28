import pygame, sys, math
import Generic, Elements
from pygame.locals import *

"""
 " Applarrow main entry point
"""
def main():
    """
     " Assorted game variables
    """
    cursor              =   [0, 0]     # Current cursor (x, y) position
    windSpeed           =   1          # The speed of the wind in knots
    arrowAngle          =   0          # The current angle of the arrow (determined by cursor position)
    arrowFiredAngle     =   0          # The angle the current arrow was fired at
    currentArrow        =   None       # The active arrow
    mouseDown           =   False      # True if the left mouse button is in the down position
    timeArrowFired      =   0          # Ticks when the active arrow was fired
    timeDecrementCount  =   0          # Milliseconds since the timer ticked over (reset every 1000ms)
    paused              =   False      # True if the game is in the paused state
    help                =   False      # True if the game help is currently shown
    gameOver            =   False      # True is the game has ended
    restart             =   False      # True if the game is due to restart
    restartDrawn        =   False      # True if the restart overlay has been drawn

    """
     " Element layers
     "   These layers define the draw order for all game elements, with the
     "   lowest layer having the smallest number
    """
    elements = pygame.sprite.LayeredUpdates()
    archerLayer     =   0
    treeLayer       =   1
    appleLayer      =   2
    arrowLayer      =   3
    butterflyLayer  =   4
    cloudLayer      =   5
    topLayer        =   6
    pauseLayer      =   7
    helpLayer       =   8
    restartLayer    =   9

    """
     " Redraw Elements
     "   Redraws only parts of the main surface that have changed since the last
     "   time this function was called
     "
     "   @param screen: the main surface to draw to
     "   @param base: the base background image surface
    """
    def redrawElements(screen, base):
        # Clear the screen
        elements.clear(screen, base)

        # Update the banner
        Elements.Banner.setWindSpeed(windSpeed);
        Elements.Banner.update()

        # Redraw any updated rectangles
        updatedRectangles = elements.draw(screen) + [Elements.Banner.rect]
        pygame.display.update(updatedRectangles)

    """
     " Get Arrow
     "   Returns the arrow at the specified index. -1 Returns the most recent arrow
     "
     "   @param index: the index of the arrow to get (default = -1)
    """
    def getArrow(index = -1):
        return elements.get_sprites_from_layer(arrowLayer)[index]

    """
     " Update Arrow
     "   Updates the arrow and archer torso angles based on the cursor position. The new
     "   arrow/torso angle is returned
     "
     "   @param arrow: the arrow instance to update
     "   @param torso: the torso instance to update
    """
    def updateArrow(arrow, torso):
        # Calculate the new torso and arrow angle
        angleRad = -(math.atan2(cursor[1] - 366, cursor[0] - 50))
        angleDeg = math.degrees(angleRad)

        # Limit the rotation
        if (angleDeg > 49):
            angleRad = math.radians(49)
        elif (angleDeg < -42):
            angleRad = math.radians(-42)

        # Update the torso and arrow angles
        torso.update(angleRad)
        arrow.update(angleRad)

        # Return the calculated angle
        return angleRad

    """
     " Reset Game
     "   Resets all changable elements in the game for a restart.
     "
     "   @param elements: the layered group of game elements
    """
    def resetGame(elements):
        # Game variables
        windSpeed = 1
        
        # Reset banner information
        Elements.Banner.setPower(0)
        Elements.Banner.setWindSpeed(windSpeed)
        Elements.Banner.resetTimeRemaining()
        Elements.Banner.resetPoints()

        # Reset apples
        elements.remove_sprites_of_layer(appleLayer)
        for location in Generic.APPLE_LOCATIONS:
            elements.add(Elements.Apple(location, 0), layer = appleLayer)

        # Reload arrow, removing previous arrows
        elements.remove_sprites_of_layer(arrowLayer)
        elements.add(Elements.Arrow(), layer = arrowLayer)
        currentArrow = getArrow()
        arrowAngle = updateArrow(currentArrow, archerTorso)

        # Remove butterflies
        elements.remove_sprites_of_layer(butterflyLayer)
        elements.add(Elements.Butterfly(0), layer = butterflyLayer)

        # Return modified variables
        return arrowAngle, currentArrow, windSpeed


    # Window initialisation
    pygame.init()
    pygame.display.set_caption("Applarrow")
    screen = pygame.display.set_mode((Generic.WINDOW_WIDTH, Generic.WINDOW_HEIGHT), pygame.DOUBLEBUF)

    # Clock
    gameClock = pygame.time.Clock()
    lastFrameTicks = pygame.time.get_ticks()
    ticksOnMouseDown = lastFrameTicks

    # Layered element initialisation
    elements.add(Elements.Tree(), layer = treeLayer)
    elements.add(Elements.Banner(), layer = topLayer)
    elements.add(Elements.Grass(), layer = topLayer)
    elements.add(Elements.Ground(), layer = topLayer)
    archerTorso = Elements.ArcherTorso()
    elements.add(Elements.ArcherLegs(), layer = archerLayer)
    elements.add(archerTorso, layer = archerLayer)
    elements.add(Elements.Arrow(), layer = arrowLayer)
    elements.add(Elements.Butterfly(0), layer = butterflyLayer)
    for location in Generic.APPLE_LOCATIONS:
        elements.add(Elements.Apple(location, 0), layer = appleLayer)
    for cloud in Generic.CLOUDS:
        elements.add(Elements.Cloud(cloud[0], cloud[1]), layer = cloudLayer)

    # Fetch the last arrow element
    currentArrow = getArrow()

    # Draw the background graphic to the screen
    skyImg = pygame.image.load("..\\Resources\\sky.png")
    screen.blit(skyImg, [0, 0])

    # If the highscore is 0, display the help layer
    if (Elements.Restart.getHighscore() == 0):
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_h, mod=None))

    # Update the entire display to draw static objects
    pygame.display.update()

    while (True):
        # Game events
        gameClock.tick(Generic.FRAMERATE)
        events = pygame.event.get()

        # Top-level events not concerned with user input related to gameplay
        for event in events:
            if (event.type == pygame.KEYUP):
                if (event.key == K_p and (help is False and gameOver is False)):
                    # Set the paused state
                    paused = not paused

                    # Pause the game
                    if (paused is True):
                        elements.add(Elements.Pause(), layer = pauseLayer)
                        redrawElements(screen, skyImg)
                    else:
                        elements.remove_sprites_of_layer(pauseLayer)
                elif (event.key == K_h and (paused is False and gameOver is False)):
                    # Set the help state
                    help = not help

                    # Display the help layer
                    if (help == True):
                        elements.add(Elements.Help(), layer = helpLayer)
                        redrawElements(screen, skyImg)
                    else:
                        elements.remove_sprites_of_layer(helpLayer)
                elif (event.key == K_r and (paused is False and help is False)):
                    if (gameOver is False):
                        gameOver = True
                    else:
                        gameOver = False
                        restart = True
            elif (event.type == Generic.EVENT_APPLE_HIT):
                # Dislpay the apple hitsplat
                event.apple.update()
            elif (event.type == Generic.EVENT_BUTTERFLY_HIT):
                # Display the butterfly hitsplat
                event.butterfly.updateSplat()
            elif (event.type == Generic.EVENT_GAME_OVER):
                # Report that the game is over
                gameOver = True
            elif (event.type == Generic.EVENT_DIFFICULTY_ADJUSTMENT):
                # Adjust the wind speed
                windSpeed = event.windSpeedAdjustment

                # Add a butterfly if requested
                if (event.addButterfly is True):
                    elements.add(Elements.Butterfly(0), layer = butterflyLayer)
            elif (event.type == pygame.QUIT):
                # Exit the game
                sys.exit(0)

        # Handle the end of the game
        if (gameOver is True):
            if (restartDrawn is False):
                elements.add(Elements.Restart(), layer = restartLayer)
                redrawElements(screen, skyImg)
                restartDrawn = True
        elif (restart == True):
            arrowAngle, currentArrow, windSpeed = resetGame(elements)
            elements.remove_sprites_of_layer(restartLayer)
            restart = False
            restartDrawn = False

        if (paused is False and help is False and gameOver is False):
            # Time calculation
            thisFrameTicks = pygame.time.get_ticks()
            ticksSinceLastFrame = thisFrameTicks - lastFrameTicks
            lastFrameTicks = thisFrameTicks
            timeDecrementCount += ticksSinceLastFrame

            # Events related to user input that alters the gameplay
            for event in events:
                if (event.type == pygame.MOUSEMOTION and (currentArrow.fired == False)):
                    cursor = event.pos
                    arrowAngle = updateArrow(currentArrow, archerTorso)
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    mouseDown = True
                    ticksOnMouseDown = thisFrameTicks
                elif (event.type == pygame.MOUSEBUTTONUP):
                    mouseDown = False
                    if (currentArrow.fired == False):
                        timeArrowFired = thisFrameTicks
                        arrowFiredAngle = arrowAngle
                        currentArrow.fire(Elements.Banner.getPower(), windSpeed)

            # Arrow flight conditional
            if (currentArrow.fired == True):
                if (currentArrow.flying == True):
                    # Move the arrow
                    currentArrow.fly(((lastFrameTicks - timeArrowFired) / 1000.0), arrowFiredAngle)

                    # Detect apple collisions
                    for apple in elements.get_sprites_from_layer(appleLayer):
                        if ((apple.appleHit is False) and (pygame.sprite.collide_mask(currentArrow, apple))):
                            apple.hit()
                        
                    # Detect butterfly collisions
                    for butterfly in elements.get_sprites_from_layer(butterflyLayer):
                        if ((butterfly.butterflyHit is False) and (pygame.sprite.collide_mask(currentArrow, butterfly))):
                            butterfly.hit(thisFrameTicks)
                else:
                    # Load a new arrow
                    elements.add(Elements.Arrow(), layer = arrowLayer)
                    currentArrow = getArrow()
                    arrowAngle = updateArrow(currentArrow, archerTorso)
            elif (mouseDown == True):
                # Update the power gauge
                Elements.Banner.setPower(-(math.cos(math.radians((thisFrameTicks - ticksOnMouseDown) / Generic.POWER_MODIFIER)) * 50) + 50)

            # Update the timer
            if timeDecrementCount > 1000 and Elements.Banner.getTimeRemaining() != 0:
                Elements.Banner.adjustTimeRemaining(-1)
                timeDecrementCount = 0

            # Apple changes
            for apple in elements.get_sprites_from_layer(appleLayer):
                apple.change(thisFrameTicks)

            # Butterfly changes
            for butterfly in elements.get_sprites_from_layer(butterflyLayer):
                butterfly.update(thisFrameTicks)

            # Cloud movement
            for cloud in elements.get_sprites_from_layer(cloudLayer):
                cloud.update(windSpeed)

            # Redraw changed elements on the screen
            redrawElements(screen, skyImg)

if __name__ == "__main__":
	main()
