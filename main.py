# Code for Tunnel Ave Control Subsystem
# Created by: Jianqiu (Jacky) Dong
# Date Created: 26/08/2026
# Last Modified: 02/09/2026
# Version 1.0



from pymata4 import pymata4
import time

callbackStorage: list[list[int,int]] = []
pushButtonPins = [3,4] #subject to change dependeing on actual implementation
ultrasonicSensorPins = (5,6) #subject to change dependeing on actual implementation, assumes (trigger pin, echo pin)
trafficLightsPins = [8,9,10,11,12,13] #subject to change dependeing on actual implementation, assumes [red4, yellow4, green4, red5, yellow5, green5]
pedestrianLightsPins = [14,15] #subject to change dependeing on actual implementation, assumes [red, green]



def terminate(board: pymata4.Pymata4, outPins: list[int]):
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
    time.sleep(0.5)
    for pin in outPins:
        board.digital_write(pin, 0)
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

    callbackStorage.append(data[:2])




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
    for pin in trafficLightsPins:
        board.set_pin_mode_digital_output(pin)
    for pin in pedestrianLightsPins:
        board.set_pin_mode_digital_output(pin)

    #below keeps record of the status of the traffic lights. True = on, False = off
    #[red, yellow, green]
    TL4 = [False, False, False]
    TL5 = [False, False, False]
    cycleCounter = 0 #counter for timer
    cycleState = 0 #current state of the subsystem. 
    # If 0, TL4 is green. 
    # Elseif 1, TL4 is yellow in transition cycle.
    # Elseif 2, TL5 is green.
    # ELseif 3, TL5 is yellow in transition cycle.
    
    # Initial setup for system:
    # TL4 is green, all else red
    board.digital_write(trafficLightsPins[0], 0)
    board.digital_write(trafficLightsPins[1], 0)
    board.digital_write(trafficLightsPins[2], 1)
    board.digital_write(trafficLightsPins[3], 1)
    board.digital_write(trafficLightsPins[4], 0)
    board.digital_write(trafficLightsPins[5], 0)
    board.digital_write(pedestrianLightsPins[0], 1)
    board.digital_write(pedestrianLightsPins[1], 0)
    TL4 = [False, False, True]
    TL5 = [True, False, False]

    try:
        while True:
            # the main cycle operates every 1 second. This is subject to change for integration with ultrasonic sensor.
            buttonResult = pushButtonCheck(board)
            if buttonResult is not None:
                #Logic for detecting a Push Button press
                print(f"Push Button {buttonResult} is pressed.")
                time.sleep(2)
                if TL5[0]:
                    # TL5 is red, turn TL4 to yellow
                    board.digital_write(trafficLightsPins[0], 0)
                    board.digital_write(trafficLightsPins[1], 1)
                    board.digital_write(trafficLightsPins[2], 0)
                    time.sleep(3)
                    #turn TL4 to red
                    board.digital_write(trafficLightsPins[0], 1)
                    board.digital_write(trafficLightsPins[1], 0)
                else:
                    # TL5 is not red, turn TL5 to yellow
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
    pass


if __name__ == "__main__":
    main()