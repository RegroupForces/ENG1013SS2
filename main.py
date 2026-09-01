# Code for Tunnel Ave Control Subsystem
# Created by: Jianqiu (Jacky) Dong
# Date Created: 26/08/2026
# Last Modified: 01/09/2026



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




def pushButtonCheck(board: pymata4.Pymata4):
    """
    Helper function that check for a 'switch on' signal.
    Fetches signal from a predefined list (callbackStorage).
    The signal should only be push button signals, ultrasonic sensor has other logic.
    Clears callbackStorage upon returning

    Args:
        board: pymata4.Pymata4
        The board initialised by main()
    
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
                    board.digital_write(trafficLightsPins[2], 0)
                    board.digital_write(trafficLightsPins[1], 1)
                    time.sleep(3)
                    #turn TL4 to red
                    board.digital_write(trafficLightsPins[1], 0)
                    board.digital_write(trafficLightsPins[0], 1)

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
                board.digital_write(trafficLightsPins[2], 0)
                board.digital_write(trafficLightsPins[1], 1)


            #Logic for main cycle


                
    except KeyboardInterrupt:
        terminate(board, trafficLightsPins + pedestrianLightsPins)

    pass


if __name__ == "__main__":
    main()