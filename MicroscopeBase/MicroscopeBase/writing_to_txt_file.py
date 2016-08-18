txt_file = open('output.txt', 'w')

list = [3, 4, 5, 6]
txt_file.write("Hullo, Werld! {}".format(list))

txt_file.close()