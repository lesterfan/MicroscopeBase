import os
import time

def delete_file(file_dir):
    try:
        delete_file("new_feature.txt")
    except Exception:
        print "File doesn't exist!"

def create_file(file_dir):
    txt_file = open(file_dir, 'w')

    list = [3, 4, 5, 6]
    txt_file.write("Hullo, Werld! {}".format(list))
    
    txt_file.close()


def create_dir(file_dir):
    try:
        os.makedirs(file_dir)
    except OSError:
        print "Error!"
        pass

def delete_dir(file_dir):
    try:
        os.rmdir(file_dir)
    except OSError:
        print "Error!"
        pass


def main():
    create_file("new_feature")
    delete_dir("new_feature")
    delete_file("new_feature")
    # create_dir("new-directory")
    # delete_dir("new-directory")

    print time.strftime("%m_%d_%y_%H_%M_%S") + "HELLO!"
    


if __name__ == "__main__":
    main()