from msvcrt import getch

def main():

    while True:

        key = ord(getch())

        if key == 27:
            return
        elif key == 72: # UP
            print ("Up button pressed!")
        elif key == 75:
            print ("Left button pressed!")
        elif key == 77:
            print ("Down button pressed!")
        elif key == 80:
            print ("Right button pressed!")


main()