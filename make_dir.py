import os
import csv

groups_csv = "groups.csv"

dir_mode = 0775
current_dir = os.getcwd()
base_path = current_dir +"/image_db"

def make_dir(name):
    path = base_path+"/"+name
    try:
        os.mkdir(path, dir_mode)
    except OSError:
        print("Directory %s already exists" % path)

def make_family_dir(name):
    file_name = name+".csv"
    with open(file_name) as family_csvfile:
        reader = csv.DictReader(family_csvfile)
	for row in reader:
            path = name+"/"+row['family_name'].lower()
	    make_dir(path)
    family_csvfile.close()
    os.rename(current_dir + "/" + file_name, base_path + "/" + name + "/" + file_name)

try:
    os.mkdir(base_path, dir_mode)
except OSError:
    print("Directory %s already exists" % base_path)

with open(groups_csv) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
	print(row['group_name'])
        make_dir(row['group_name'].lower())
	make_family_dir(row['group_name'].lower())
csvfile.close()
#Move groups.csv to image_db
os.rename(current_dir+"/"+groups_csv, base_path+"/"+groups_csv)	
