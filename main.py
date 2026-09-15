# Code for Tunnel Ave Control Subsystem
# Created by: Jianqiu (Jacky) Dong
# Date Created: 26/08/2026
# Last Modified: 02/09/2026
# Version 1.2



from pymata4 import pymata4
import time

callbackStorage: list[list[int,int]] = []
pushButtonPins = [3] #subject to change dependeing on actual implementation
# ultrasonicSensorPins = (5,6) #subject to change dependeing on actual implementation, assumes (trigger pin, echo pin)
shiftRegisterPins = [4,5,6] #assumes (SER, RCLK, SRCLK)
"""Shift Register has the following ocrrospondence:
binary          decimal light
00000001        1       PL_Red
00000010        2       PL_Green
00000100        4       TL4_Red
00001000        8       TL4_Yellow
00010000        16      TL4_Green
00100000        32      TL5_Red
01000000        64      TL5_Yellow
10000000        128     TL5_Green
"""
# trafficLightsPins = [6,7,8,9,10,11] #subject to change dependeing on actual implementation, assumes [red4, yellow4, green4, red5, yellow5, green5]
# pedestrianLightsPins = [4,5] #subject to change dependeing on actual implementation, assumes [red, green]
SER = shiftRegisterPins[0]
RCLK = shiftRegisterPins[1]
SRCLK = shiftRegisterPins[2]

light_patterns = {
    "PL_Red"    :   0b00000001,
    "PL_Green":     0b00000010,
    "TL4_Red"   :   0b00000100,
    "TL4_Yellow":   0b00001000,
    "TL4_Green" :   0b00010000,
    "TL5_Red"   :   0b00100000,
    "TL5_Yellow":   0b01000000,
    "TL5_Green" :   0b10000000,
}


DEBUG_MESSAGES = {
    0: "TL4 green for 20s",
    1: "TL4 yellow transition to TL5",
    2: "TL5 green for 10s",
    3: "TL5 tellow transition to TL4"
}


def setLightState(light_state: int, val: bool|int, *bits: int):
    """
    Helper function to set the light_state.

    Args:
        light_state: int
        A number of 8 bits in length. This represents the current state of the lights.

        val: bool|int
        Determines if the bits should be set HIGH or LOW.
        
        *bits: list[int]
        The value to change. This should have the format of:
            8 bits in length
            all 0 except for 1
    """
    if val: #setting pins to HIGH, if the target pin is already HIGH then it has no effect.
        for bit in bits:
            light_state = light_state | bit
    else:   #setting pins to LOW
        for bit in bits:
            light_state = light_state & ~bit
    return light_state

def setShiftRegisterPins(board: pymata4.Pymata4, val: int):
    """
    Helper function to set the shift regester value.

    Args:
        board: pymata4.Pymata4
        Reference to the board

        val: int
        The value to set the shift regester to.

    Returns:
        None
    """
    for i in range(8):
        bit = (val >> i) & 1
        board.digital_write(SER, bit)
        board.digital_write(SRCLK, 1)
        # time.sleep(0.01)
        board.digital_write(SRCLK, 0)

    board.digital_write(RCLK, 1)
    board.digital_write(RCLK, 0)

    return None


    



def terminate(board: pymata4.Pymata4):
    """
    Helper function that safely shuts off the board.

    Args:
        board: pymata4.Pymata4
        Board to shutdown. 

        outPins: list[int]
        The pins that are output pins. These pins will be set to 0 (LOW)
    Returns:
        None
    """
    print(f"Terminating")
    time.sleep(0.5)
    setShiftRegisterPins(board, 0)
    board.shutdown()
    quit()



def callback(data: list):
    """
    Callback function provided to the board.
    Preprocess the data and stores it in a predefined list.

    Args:
        data: list
        Contains the data that is sent from the board.

    Returns:
        None
    """
    # print(data)
    callbackStorage.append(data[1:3])




def pushButtonCheck():
    """
    Helper function that check for a 'switch on' signal.
    Fetches signal from a predefined list (callbackStorage).
    The signal should only be push button signals, ultrasonic sensor has other logic.
    Clears callbackStorage upon returning

    Args:
        None
    
    Returns:
        action: int | None
        Returns None if no valid inputs are detected.
        Otherwise, return the pin number that was pressed for a press of push button.
    """

    # Insert logic for integration here 
    # Return data early if US5 detected something

    # End of integration
    global callbackStorage
    print(callbackStorage)
    if len(callbackStorage) == 0:
        return

    while len(callbackStorage) > 0:
        signal = callbackStorage.pop()

        if signal[1] == 1:
            # Detected a Pushbotton Press
            callbackStorage = []
            return signal[0]

        






def main():
    """
    Main function.
    Contains all main logic for this subsystem.
    Main logic loop:
        Check for input from PB1, PB2 and US5
        If signal detected:
            Act accordingly
        Check normal cycle
        Sleep for 1 second
        
    
    Args:
        None
    
    Returns:
        None
    """

    
    board = pymata4.Pymata4()


    for pin in pushButtonPins:
        board.set_pin_mode_digital_input(pin, callback)
    # for trigger, echo in ultrasonicSensorPins:
    #     board.set_pin_mode_sonar(trigger, echo, timeout = 200000)
    # for pin in trafficLightsPins:
    #     board.set_pin_mode_digital_output(pin)
    # for pin in pedestrianLightsPins:
    #     board.set_pin_mode_digital_output(pin)
    for pin in shiftRegisterPins:
        board.set_pin_mode_digital_output(pin)

    # state for the light. This is stored in binary, to see which pin corrospond to which light, see the top of this file.
    light_state = 0

    cycleCounter = 0 #counter for timer
    cycleState = 0 #current state of the subsystem. 

    # Initially set the shift regester to 0
    setShiftRegisterPins(board, 0)

    # Assumes the subsystem starts in the TL4 is green cycle.
    light_state = setLightState(light_state, 1, light_patterns["PL_Red"], light_patterns["TL4_Green"], light_patterns["TL5_Red"])
    setShiftRegisterPins(board, light_state)

    try:
        while True:
            print(f"Current Cycle Time: {cycleCounter + 1}")
            print(f"Current state is: {DEBUG_MESSAGES[cycleState]}")
            # the main cycle operates every 1 second. This is subject to change for integration with ultrasonic sensor.
            buttonResult = pushButtonCheck()
            if buttonResult is not None:
                #Logic for detecting a Push Button press
                print(f"Push Button is pressed.")
                time.sleep(2)
                if light_state & light_patterns["TL5_Red"]:
                    # TL5 is red, turn TL4 to yellow
                    print("Turning TL4 to yellow")
                    light_state = setLightState(light_state, 1, light_patterns["TL4_Yellow"])
                    light_state = setLightState(light_state, 0, light_patterns["TL4_Red"], light_patterns["TL4_Green"])
                    setShiftRegisterPins(board, light_state)
                    time.sleep(3)
                    #turn TL4 to red
                    light_state = setLightState(light_state, 1, light_patterns["TL4_Red"])
                    light_state = setLightState(light_state, 0, light_patterns["TL4_Yellow"], light_patterns["TL4_Green"])
                    setShiftRegisterPins(board, light_state)
                else:
                    # TL5 is not red, turn TL5 to yellow
                    print("Turning TL5 to yellow")
                    light_state = setLightState(light_state, 1, light_patterns["TL5_Red"])
                    light_state = setLightState(light_state, 0, light_patterns["TL5_Yellow"], light_patterns["TL5_Green"])
                    setShiftRegisterPins(board, light_state)
                    time.sleep(3)
                    #turn TL5 to red
                    light_state = setLightState(light_state, 1, light_patterns["TL5_Red"])
                    light_state = setLightState(light_state, 0, light_patterns["TL5_Yellow"], light_patterns["TL5_Green"])
                    setShiftRegisterPins(board, light_state)

                #set PL1/2 to green
                    light_state = setLightState(light_state, 1, light_patterns["PL_Green"])
                    light_state = setLightState(light_state, 0, light_patterns["PL_Red"])
                    setShiftRegisterPins(board, light_state)
                time.sleep(3)
                #set PL1/2 to flashing red
                light_state = setLightState(light_state, 0, light_patterns["PL_Green"])
                setShiftRegisterPins(board, light_state)
                for _ in range(4):
                    light_state = setLightState(light_state, 1, light_patterns["PL_Red"])
                    setShiftRegisterPins(board, light_state)
                    time.sleep(0.25)
                    light_state = setLightState(light_state, 0, light_patterns["PL_Red"])
                    setShiftRegisterPins(board, light_state)
                    time.sleep(0.25)
                light_state = setLightState(light_state, 1, light_patterns["PL_Red"])
                setShiftRegisterPins(board, light_state)
                # PLs is now red, change TL4 to green and start new main cycle from here
                light_state = 0
                light_state = setLightState(light_state, 1, light_patterns["PL_Red"], light_patterns["TL4_Green"], light_patterns["TL5_Red"])
                setShiftRegisterPins(board, light_state)
                cycleCounter = 0
                cycleState = 0
                continue

            # This is the main cycle
            if cycleCounter >= 20 and cycleState == 0:
                # If TL4 has been green for 20 sec
                # Turn TL4 to yellow
                light_state = setLightState(light_state, 1, light_patterns["TL4_Yellow"])
                light_state = setLightState(light_state, 0, light_patterns["TL4_Red"], light_patterns["TL4_Green"])
                setShiftRegisterPins(board, light_state)
                cycleCounter = 0
                cycleState = 1
                continue

            elif cycleCounter >= 3 and cycleState == 1:
                # If TL4 has passed the 3 second yellow light
                # Turn TL4 to red and TL5 to green
                light_state = setLightState(light_state, 1, light_patterns["TL4_Red"], light_patterns["TL5_Green"])
                light_state = setLightState(light_state, 0, light_patterns["TL4_Yellow"], light_patterns["TL4_Green"], light_patterns["TL5_Red"], light_patterns["TL5_Yellow"])
                setShiftRegisterPins(board, light_state)
                cycleCounter = 0
                cycleState = 2
                continue


            elif cycleCounter >= 10 and cycleState == 2:
                # If TL5 has been green for 10 sec
                # Turn TL5 to yellow
                light_state = setLightState(light_state, 1, light_patterns["TL5_Red"])
                light_state = setLightState(light_state, 0, light_patterns["TL5_Yellow"], light_patterns["TL5_Green"])
                setShiftRegisterPins(board, light_state)
                cycleCounter = 0
                cycleState = 3
                continue

            elif cycleCounter >= 3 and cycleState == 3:
                # If TL5 has passed the 3 second yellow light
                # Turn TL5 to red and TL4 to green
                light_state = setLightState(light_state, 1, light_patterns["TL4_Green"], light_patterns["TL5_Red"])
                light_state = setLightState(light_state, 0, light_patterns["TL4_Red"], light_patterns["TL4_Yellow"], light_patterns["TL5_Yellow"], light_patterns["TL5_Green"])
                setShiftRegisterPins(board, light_state)
                cycleCounter = 0
                cycleState = 0
                continue

            else:
                # Nothing important happens in cycle, increment counter
                cycleCounter += 1

            #Universal sleep for all cycles
            time.sleep(1)
        
    
    except KeyboardInterrupt:
        terminate(board)
  

    

    """
    # this is the old code to be deleted later

    try:
        while True:
            print(f"Cycle Counter = {cycleCounter}")
            print(f"Cycle State = {cycleState}")
            # the main cycle operates every 1 second. This is subject to change for integration with ultrasonic sensor.
            buttonResult = pushButtonCheck()
            if buttonResult is not None:
                #Logic for detecting a Push Button press
                print(f"Push Button {buttonResult} is pressed.")
                time.sleep(2)
                if TL5[0]:
                    # TL5 is red, turn TL4 to yellow
                    print("Turning TL4 to yellow")
                    board.digital_write(trafficLightsPins[0], 0)
                    board.digital_write(trafficLightsPins[1], 1)
                    board.digital_write(trafficLightsPins[2], 0)
                    time.sleep(3)
                    #turn TL4 to red
                    board.digital_write(trafficLightsPins[0], 1)
                    board.digital_write(trafficLightsPins[1], 0)
                    board.digital_write(trafficLightsPins[2], 0)
                else:
                    # TL5 is not red, turn TL5 to yellow
                    print("Turning TL5 to yellow")
                    board.digital_write(trafficLightsPins[3], 0)
                    board.digital_write(trafficLightsPins[4], 1)
                    board.digital_write(trafficLightsPins[5], 0)
                    time.sleep(3)
                    #turn TL5 to red
                    board.digital_write(trafficLightsPins[3], 1)
                    board.digital_write(trafficLightsPins[4], 0)

                #set PL1/2 to green
                board.digital_write(pedestrianLightsPins[0], 0)
                board.digital_write(pedestrianLightsPins[1], 1)
                time.sleep(3)
                #set PL1/2 to flashing red
                board.digital_write(pedestrianLightsPins[1], 0)
                for _ in range(4):
                    board.digital_write(pedestrianLightsPins[0], 1)
                    time.sleep(0.25)
                    board.digital_write(pedestrianLightsPins[0], 0)
                    time.sleep(0.25)
                board.digital_write(pedestrianLightsPins[0], 1)
                # PLs is now red, change TL4 to green and start new main cycle from here
                board.digital_write(trafficLightsPins[0], 0)
                board.digital_write(trafficLightsPins[2], 1)
                cycleCounter = 0
                cycleState = 0
                continue

            # This is the main cycle
            if cycleCounter >= 20 and cycleState == 0:
                # If TL4 has been green for 20 sec
                # Turn TL4 to yellow
                board.digital_write(trafficLightsPins[0], 0)
                board.digital_write(trafficLightsPins[1], 1)
                board.digital_write(trafficLightsPins[2], 0)
                TL4 = [False, True, False]
                cycleCounter = 0
                cycleState = 1
                continue

            elif cycleCounter >= 3 and cycleState == 1:
                # If TL4 has passed the 3 second yellow light
                # Turn TL4 to red and TL5 to green
                board.digital_write(trafficLightsPins[0], 1)
                board.digital_write(trafficLightsPins[1], 0)
                board.digital_write(trafficLightsPins[2], 0)
                board.digital_write(trafficLightsPins[3], 0)
                board.digital_write(trafficLightsPins[4], 0)
                board.digital_write(trafficLightsPins[5], 1)
                TL4 = [True, False, False]
                TL5 = [False, False, True]
                cycleCounter = 0
                cycleState = 2
                continue


            elif cycleCounter >= 10 and cycleState == 2:
                # If TL5 has been green for 10 sec
                # Turn TL5 to yellow
                board.digital_write(trafficLightsPins[3], 0)
                board.digital_write(trafficLightsPins[4], 1)
                board.digital_write(trafficLightsPins[5], 0)
                TL5 = [False, True, False]
                cycleCounter = 0
                cycleState = 3
                continue

            elif cycleCounter >= 3 and cycleState == 3:
                # If TL5 has passed the 3 second yellow light
                # Turn TL5 to red and TL4 to green
                board.digital_write(trafficLightsPins[0], 0)
                board.digital_write(trafficLightsPins[1], 0)
                board.digital_write(trafficLightsPins[2], 1)
                board.digital_write(trafficLightsPins[3], 1)
                board.digital_write(trafficLightsPins[4], 0)
                board.digital_write(trafficLightsPins[5], 0)
                TL4 = [False, False, True]
                TL5 = [True, False, False]
                cycleCounter = 0
                cycleState = 0
                continue

            else:
                # Nothing important happens in cycle, increment counter
                cycleCounter += 1

            #Universal sleep for all cycles
            time.sleep(1)
        
    
    except KeyboardInterrupt:
        terminate(board, trafficLightsPins + pedestrianLightsPins)
        """


if __name__ == "__main__":
    main()