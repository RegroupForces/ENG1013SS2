# Code for Tunnel Ave Control Subsystem
# Created by: Jianqiu (Jacky) Dong
# Date Created: 26/08/2026
# Last Modified: 01/09/2026



from pymata4 import pymata4

def callback(data: list):
    """
    Callback function provided to the board.
    Preprocess the data sent from the board and stores it in a global list.

    Args:
        data: list
        Contains the data that is sent from the board.

    Returns:
        None
    """
    pass




def pollInstruction(board: pymata4.Pymata4, pins: list[int]):
    """
    Helper function that check for a 'switch on' signal.

    Args:
        board: pymata4.Pymata4
        The board initialised by main()

        pins: list[int]
        Specifies the pins to check from.
    
    Returns:

        
    """

    # Insert logic for integration here 
    # Return data early if US5 detected something

    # End of integration




    pass





def main():
    """
    Main function.
    Contains all main logic for this subsystem.
    
    Args:
        None
    
    Returns:
        None
    """

    board = pymata4.Pymata4()

    pushButtonPins = [3,4] #subject to change dependeing on actual implementation
    ultrasonicSensorPins = [5] #subject to change dependeing on actual implementation

    for pin in pushButtonPins:
        board.set_pin_mode_digital_output()



    pass


if __name__ == "__main__":
    main()