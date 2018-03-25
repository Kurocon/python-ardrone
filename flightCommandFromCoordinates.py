import math

notFoundCounter = -1000000
startCounter = 0

huegCounter = 0
has100 = False
prevFlightSpeed = -0.2

takeoff_limit = 40
notfound_limit = 20

keypoint_minsize = 80
keypoint_maxsize = 105

image_landing_cutoff = 300

def flight_reset():
    global notFoundCounter, huegCounter, startCounter, has100, prevFlightSpeed
    notFoundCounter = -1000000
    startCounter = 0
    huegCounter = 0
    has100 = False
    prevFlightSpeed = -0.2

def get_flight_command(keypoint, offset, alt):
    global notFoundCounter, huegCounter, startCounter, has100, prevFlightSpeed
    flight_speed = -0.2
    if offset is None or offset[0] * offset[0] + offset[1] * offset[1] > 0.6:
        if startCounter < takeoff_limit or notFoundCounter < notfound_limit:
            notFoundCounter += 1
            print(" NOT FOUND {}".format(notFoundCounter))
            prevFlightSpeed = prevFlightSpeed * 0.85 + 0.15 * flight_speed
            return 0, prevFlightSpeed, 0.8, 0
        else:
            print("LANDING")
            return None, None, None, None

    else:
        flight_speed = max(-0.2, (0.5 + (0.5 - offset[1])) / 2 * -0.4)
        if keypoint.size > keypoint_minsize:

            if keypoint.size >= keypoint_maxsize:
                has100 = True
            if huegCounter < 15:
                huegCounter += 1
            else:
                print("LANDING B/C OF SIZE AND POSITION")
                return None, None, None, None
        else:
            huegCounter = 0
            has100 = False

    startCounter += 1
    notFoundCounter = 0
    prevFlightSpeed = prevFlightSpeed * 0.85 + 0.15 * flight_speed

    return 0.5 * offset[0], (3+(1 - abs(offset[0]) * 2))/4 * prevFlightSpeed, 0.00 - (0.7 * offset[1]), 0.8 * offset[0]
