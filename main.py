# Code for Tunnel Ave Control Subsystem
# Created by: Jianqiu (Jacky) Dong
# Date Created: 26/08/2026
# Last Modified: 01/09/2026



from pymata4 import pymata4
import time

callbackStorage: list[list[int,int]] = []
pushButtonPins = [3,4] #subject to change dependeing on actual implementation
ultrasonicSensorPins = (5,6) #subject to change dependeing on actual implementation, assumes (trigger pin, echo pin)
lightsPins = [8,9,10,11,12,13] #subject to change dependeing on actual implementation, assumes [red1, yellow1, green1, red2, yellow2, green2]

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




def pushBottonCheck(board: pymata4.Pymata4):
    """
    Helper function that check for a 'switch on' signal.
    Fetches signal from a predefined list.
    The signal should only be push button signals, ultrasonic sensor has other logic.

    Args:
        board: pymata4.Pymata4
        The board initialised by main()
    
    Returns:
        action: str | None
        Returns None if no valid inputs are detected.
        Otherwise, return "PB" for a press of push buttons.
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
            return "PB"

        






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
    for trigger, echo in ultrasonicSensorPins:
        board.set_pin_mode_sonar(trigger, echo, timeout = 200000)
    for pin in lightsPins:
        board.set_pin_mode_digital_output(pin)

    try:
        while True:
            #insert main cycle logic here, with logic for PB and US detections
            pass
    except KeyboardInterrupt:
        terminate(board, lightsPins)

    pass


if __name__ == "__main__":
    main()