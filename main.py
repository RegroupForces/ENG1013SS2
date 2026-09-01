# Code for Tunnel Ave Control Subsystem
# Created by: Jianqiu (Jacky) Dong
# Date Created: 26/08/2026
# Last Modified: 01/09/2026



from pymata4 import pymata4
import time

callbackStorage: list[list[int,int]] = []
pushButtonPins = [3,4] #subject to change dependeing on actual implementation
ultrasonicSensorPins = [5] #subject to change dependeing on actual implementation
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
    Preprocess the data sent from the board and calls relavent function to act.

    Args:
        data: list
        Contains the data that is sent from the board.

    Returns:
        None
    """

    callbackStorage.append(data[:2])




def pollInstruction(board: pymata4.Pymata4, pins: list[int]):
    """
    Helper function that check for a 'switch on' signal.

    Args:
        board: pymata4.Pymata4
        The board initialised by main()

        pins: list[int]
        Specifies the pins to check from.
    
    Returns:
        action: str | None
        Returns None if no inputs are detected.
        Otherwise, return "PB" for a press of push buttons.
        Otherwise, return "US" for untrasonic sensor detection.

        
    """

    # Insert logic for integration here 
    # Return data early if US5 detected something

    # End of integration

    if len(callbackStorage) == 0:
        return


    signal = callbackStorage.pop()

    if signal[]

    pass





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
    for pin in ultrasonicSensorPins:
        board.set_pin_mode_digital_input(pin, callback)
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