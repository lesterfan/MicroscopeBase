
def main():

    lines = [line.rstrip('\n') for line in open("History/map_history.txt")]

    for line in lines:
        L = line.split(" ")
        print L

    # print lines

if __name__ == "__main__":
    main()
