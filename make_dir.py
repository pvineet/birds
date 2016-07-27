import os
import csv

groups_csv = "groups.csv"
dir_mode = 0775
current_dir = os.getcwd()
base_path = current_dir +"/image_db"

def make_group_dirs(name):
    path = base_path+"/"+name
    try:
        os.mkdir(path, dir_mode)
    except OSError:
        print "Directory %s already exists" % path
    

try:
    os.mkdir(base_path, dir_mode)
except OSError:
    print "Directory %s already exists" % base_path

with open(groups_csv) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
	print row['group_name']
        make_group_dirs(row['group_name'].lower())	
