import os,csv
from os.path import isdir
import shutil,errno

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

dst_dir  = "/root/tf_bird_files/bird_photos"
list_file = open("first_list.txt", 'rb')
temp_list = list_file.readlines()
bird_list = []

for bird in temp_list:
    bird_list.append(bird.lower().replace(" ","_").strip())
print bird_list

current_path = os.getcwd()
image_db_path = current_path+"/image_db"
print "image_db dir exists - %s" % (os.path.isdir(image_db_path))
#cd to images_db
os.chdir(image_db_path)
#open groups.csv
with open('groups.csv', 'rb') as groups_csvfile:
    GroupsDictReader = csv.reader(groups_csvfile)
    next(GroupsDictReader)
    for row in GroupsDictReader:
        #enter the spefic group dir
        curr_grp_name = row[0].lower()
        os.chdir(image_db_path+"/"+curr_grp_name)
        with open(curr_grp_name+".csv",'rb') as curr_grp_csvfile:
            CurrGrpDictReader = csv.reader(curr_grp_csvfile)
            next(CurrGrpDictReader)
            for grp_row in CurrGrpDictReader:
                curr_family_name = grp_row[0].lower()
                #enter family dir
                #print "Current family %s" % curr_family_name
		for dir in os.listdir(os.getcwd()):
		    current_path = os.getcwd()+"/"+curr_family_name
		    if isdir(current_path):
                    	os.chdir(current_path)
			for specie_dir in os.listdir(os.getcwd()):
		    	    current_path = os.getcwd()+"/"+specie_dir
			    if(specie_dir in bird_list and isdir(current_path)):
				#print bird_list.index(specie_dir)
				copyanything(specie_dir,dst_dir+"/"+specie_dir)
				print specie_dir
				bird_list.remove(specie_dir)
			os.chdir("../")	
