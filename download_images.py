import os, csv
import urllib

num_lines = 0
def write_image_csv(csv_file, image_url, image_file):
    with open(csv_file, 'a') as csvfile:
        fieldnames = ['image_url', 'image_file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not image_url == '':
	    urllib.urlretrieve(image_url,image_file)
            writer.writerow({'image_url':image_url, 'image_file':image_file})
	

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
        print row
        #enter the spefic group dir
        curr_grp_name = row[0].lower()
        os.chdir(image_db_path+"/"+curr_grp_name)
        with open(curr_grp_name+".csv",'rb') as curr_grp_csvfile:
            CurrGrpDictReader = csv.reader(curr_grp_csvfile)
            next(CurrGrpDictReader)
            for grp_row in CurrGrpDictReader:
                curr_family_name = grp_row[0].lower()
                #enter family dir
                print "Current family %s" % curr_family_name
                #print os.getcwd()
                os.chdir(os.getcwd()+"/"+curr_family_name)
                with open(curr_family_name+".csv", 'rb') as curr_family_csvfile:
                    CurrFamilyDictReader = csv.reader(curr_family_csvfile)
                    next(CurrFamilyDictReader)
                    for family_row in CurrFamilyDictReader:
                        curr_specie_name = family_row[3].lower().replace(" ","_")
                        print curr_specie_name
                        #enter specie dir
                        os.chdir(os.getcwd()+"/"+curr_specie_name)
                        if not os.path.exists(curr_specie_name+"_images.csv"):
                            with open(curr_specie_name+"_images.csv",'wb') as curr_specie_img_csvfile:
                                fieldnames = ['image_url', 'image_file']
                                writer = csv.DictWriter(curr_specie_img_csvfile, fieldnames=fieldnames)
                                writer.writeheader()
                        else:
                            with open(curr_specie_name+"_images.csv",'rb') as curr_specie_img_csvfile:
                                ImagesDictReader = csv.reader(curr_specie_img_csvfile)
                                num_lines = sum(1 for row in ImagesDictReader)
                                print "Already downladed images for %s = %d" % (curr_specie_name, num_lines) 
                        with open(curr_specie_name+".csv", 'rb') as curr_specie_csvfile:
                            CurrSpecieDictReader = csv.reader(curr_specie_csvfile)
                            count = 0
                            for i in range(0,num_lines):
                                next(CurrSpecieDictReader)
                                count = count+1
                            for specie_row in CurrSpecieDictReader:
                                print specie_row
                                image_file = os.getcwd()+"/"+str(count)+".jpg"
                                write_image_csv(curr_specie_name+"_images.csv", specie_row[1], image_file)
                                count = count+1
                        #exit specie dir        
                        os.chdir("../")
                        #print os.getcwd()
                #exit family dir
                os.chdir("../")
                print os.getcwd()

#open species csv
#enter specie dir
#if image download csv does not exist create it
#else download image and append the csv
