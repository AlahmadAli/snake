import pyautogui
import time
import threading

gamescreen = None

# screen coords
x = 649
y = 321
width = 616
height = 546

# player and apple coordinates
apple_x = None
apple_y = None
player_x = None
player_y = None

playercolour = (28, 70, 158)
applecolour = (231, 71, 29)
lightgridcolour = (170, 215, 81)
darkgridcolour = (162, 209, 73)
playerlocation = []
applelocation = []

lastmoved = 0
move_delay = 0

lastdirection = None


def canmove():
    global lastmoved
    return time.time() - lastmoved >= move_delay


def ssGame():
    global gamescreen
    while True:
        gamescreen = pyautogui.screenshot(region=(x, y, width, height))
        time.sleep(0.01)


def findPlayer():
    global gamescreen, player_x, player_y
    player_x = None
    player_y = None

    if gamescreen is None:
        return

    try:
        for px in range(0, width, 7):
            for py in range(0, height, 7):
                if gamescreen.getpixel((px, py)) == playercolour:
                    player_x = float(x + px)
                    player_y = float(y + py)
                    playerlocation.append((player_x, player_y))
                    return
    except Exception as e:
        print(f"FindPlayer error: {e}")


def findApple():
    global gamescreen, apple_x, apple_y
    apple_x = None
    apple_y = None

    if gamescreen is None:
        return

    try:
        for px in range(0, width, 7):
            for py in range(0, height, 7):
                if gamescreen.getpixel((px, py)) == applecolour:
                    apple_x = float(x + px)
                    apple_y = float(y + py)
                    applelocation.append((apple_x, apple_y))
                    return
    except Exception as e:
        print(f"FindApple error: {e}")


def moveup():
    global lastmoved, lastdirection
    if apple_y is None or player_y is None:
        return False
    if lastdirection == "down":
        return False
    if apple_y < player_y - 2 and canmove():
        try:
            pyautogui.press("w")
            lastmoved = time.time()
            lastdirection = "up"
            return True
        except Exception as e:
            print(f"Move error: {e}")
    return False


def movedown():
    global lastmoved, lastdirection
    if apple_y is None or player_y is None:
        return False
    if lastdirection == "up":
        return False
    if apple_y > player_y + 2 and canmove():
        try:
            pyautogui.press("s")
            lastmoved = time.time()
            lastdirection = "down"
            return True
        except Exception as e:
            print(f"Move error: {e}")
    return False


def moveleft():
    global lastmoved, lastdirection
    if apple_x is None or player_x is None:
        return False
    if lastdirection == "right":
        return False
    if apple_x < player_x - 2 and canmove():
        try:
            pyautogui.press("a")
            lastmoved = time.time()
            lastdirection = "left"
            return True
        except Exception as e:
            print(f"Move error: {e}")
    return False


def moveright():
    global lastmoved, lastdirection
    if apple_x is None or player_x is None:
        return False
    if lastdirection == "left":
        return False
    if apple_x > player_x + 2 and canmove():
        try:
            pyautogui.press("d")
            lastmoved = time.time()
            lastdirection = "right"
            return True
        except Exception as e:
            print(f"Move error: {e}")
    return False


def smart_move():
    if apple_x is None or apple_y is None or player_x is None or player_y is None:
        return

    dx = apple_x - player_x
    dy = apple_y - player_y

    if abs(dy) > abs(dx):
        if dy > 1:
            if movedown():
                return
        elif dy < -1:
            if moveup():
                return
        if dx > 5:
            if moveright():
                return
        elif dx < -1:
            if moveleft():
                return
    else:
        if dx > 1:
            if moveright():
                return
        elif dx < -1:
            if moveleft():
                return
        if dy > 1:  #
            if movedown():
                return
        elif dy < -1:
            if moveup():
                return


def moveforever():
    while True:
        smart_move()
        time.sleep(0.03)


def avoidcollisions():
    global lastdirection
    if player_x is None or player_y is None:
        return True
    distancefromcollision = 75
    check_x, check_y = player_x, player_y

    if lastdirection == "up":
        check_y -= distancefromcollision
    elif lastdirection == "down":
        check_y += distancefromcollision
    elif lastdirection == "right":
        check_x -= distancefromcollision
    elif lastdirection == "left":
        check_x += distancefromcollision

    screen_x = int(check_x - x)
    screen_y = int(check_y - y)

    if 0 <= screen_x < width and 0 <= screen_y < height:
        pixel_color = gamescreen.getpixel((screen_x, screen_y))
        if pixel_color not in (
            applecolour,
            playercolour,
            lightgridcolour,
            darkgridcolour,
        ):
            return False
    else:
        return False

    return True


time.sleep(1)

threading.Thread(target=ssGame, daemon=True).start()
threading.Thread(target=moveforever, daemon=True).start()

print("started")

try:
    while True:
        applelocation.clear()
        playerlocation.clear()
        findPlayer()
        findApple()
        # if player_x and player_y and apple_x and apple_y:
        #     print(
        #         f"Player: ({player_x:.0f}, {player_y:.0f}), Apple: ({apple_x:.0f}, {apple_y:.0f})"
        #     )

        time.sleep(0.005)

except KeyboardInterrupt:
    print("stopped by user")
