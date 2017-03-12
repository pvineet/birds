import os,csv

train_dir = "train"
dir_mode=0755
os.mkdir(train_dir, dir_mode)

#add group.csv file exist check

f = open("image_db/groups.csv", "rb")
lines = csv.reader(f)
for line in lines:
    print line[0]
