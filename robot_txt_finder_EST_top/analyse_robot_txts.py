import os
from collections import Counter

# List for disallows from file
disallow = []


def list_all_files():
    """Lists all files in robots folder"""
    os.chdir("robots")
    robot_files = os.listdir(os.curdir)
    print "[*] Found number of files:" + str(len(robot_files))
    return robot_files


def open_txt_file(file_name):
    """Opens given file
    :param file_name: file name (str)"""
    txt_file = open(file_name, "r")
    for line in txt_file:
        if "Disallow:" in line:
            pure_line = line.rstrip('\n')
            disallow_line = pure_line.split(" ")
            try:
                disallow.append(disallow_line[1])
            except IndexError:
                print "[!] Error on line: " + line.rstrip('\n')
    txt_file.close()


def get_all_disallows_from_files():
    """Opens all files in folder and gets disallow lines"""
    robot_files = list_all_files()
    for item in robot_files:
        open_txt_file(item)
    print "[*] All files processed!"
    print "[*] Items in disallow list: " + str(len(disallow))
    os.chdir("..")


def print_all_disallows_to_file():
    """Makes file with all unique disallows from files"""
    print_text = ""
    item_list = Counter(disallow).keys()
    file_name = "unique_robot_txt_disallows.txt"
    for item in item_list:
        print_text = print_text + item + "\n"
    write_to_file(file_name, print_text)


def print_top_20_disallow():
    """Makes file with top 20 disallows from files"""
    print_text = ""
    item_list = Counter(disallow).most_common(20)
    file_name = "top_20_robot_txt_disallows.txt"
    for item in item_list:
        item_text = "Item: " + item[0] + " :: Count: " + str(item[1])
        print_text = print_text + item_text + "\n"
    write_to_file(file_name, print_text)


def print_rare_disallows():
    """Makes file with all rare disallows from files"""
    # count 1=>
    print_text = ""
    item_list = Counter(disallow).items()
    file_name = "rare_robot_txt_disallows.txt"
    for item in item_list:
        if item[1] <= 1:
            print_text = print_text + item[0] + "\n"
    write_to_file(file_name, print_text)


def write_to_file(file_name, file_data):
    """Write data to file.
     :param file_name: file name (str),
     :param file_data: data (str)"""
    robot_file = open(file_name, "a+")
    robot_file.write(file_data + "\n")
    robot_file.close()
    print "[*] File created: " + file_name


if __name__ == '__main__':
    print "---------------------------------------------"
    print "-   ROBOT.TXT DISALLOW FINDER AND ANALYSER  -"
    print "---------------------------------------------"
    get_all_disallows_from_files()
    print_rare_disallows()
    print_top_20_disallow()
    print_all_disallows_to_file()
    print "[*] All done!"
