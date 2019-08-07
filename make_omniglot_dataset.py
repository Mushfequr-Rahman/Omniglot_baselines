"""
Omniglot CSV files creation for Triplet Newtwork
"""


#Initialize Imports:
import csv
import os
import glob
import random
from os import listdir
from os.path import isdir, join, isfile
import cv2
import matplotlib.pyplot as plt

def split_list(datas):
    """
    Function to split the total list into a 64*nums_samples list
    """
    num_samples = 18
    output = []
    class_number = 0
    pos =0
    curr = []
    i = 0
    total_classes =  int(datas[-1][0]) +1
    print("Total classes:" , total_classes)

    for data in datas:
        i+=1

        if(int(data[0])==0):
            print("sample class: ", data[0])
            print("current class: ", class_number)
            print("i= ", i )
            print("Truth Value: ",((int(data[0]))==class_number))

        if((int(data[0]))==class_number):
            print("Appending List: ", len(curr))
            curr.append(data)
            pos +=1

        if(pos == num_samples):
            #print("Current length: ", len(curr))
            output.append(curr)
            class_number+=1
            curr = []
            pos = 0







    print("L:" ,len(output))
    print("W:" ,len(output[1]))
    print("output: ", output[0])
    assert(len(output)==total_classes)
    return output

def makeTriplet(split_data,filename,datapoints):
    """
    Function to write Triplet Data to a csv file inorder to load it to the data DataLoader
    """
    import csv
    import random
    n_datapoints = datapoints
    n_classes = len(split_data)
    n_samples = len(split_data[0])
    with open(filename,'w+') as csv_file:
        csv_file.truncate()
        writer = csv.writer(csv_file)
        if(n_datapoints>n_samples):
            return None


        for i in range(n_classes):
             for j in range(n_datapoints):
                 curr = []
                 indicator = random.randint(1,5)
                 x = i
                 if(indicator%2==0):
                     x= random.randint(0,n_classes-1)
                     print("X: ", x)


                 id1 = random.randint(0,n_samples-1)
                 id2 = random.randint(0,n_samples-1)
                 print("ID1: ", id1)
                 print("ID2: ",  id2)

                 while(id1==id2):
                      id2 = random.randint(0,n_samples-1)

                 anchor = split_data[x][id1]
                 positive = split_data[i][id2]

                 id3 = random.randint(0,n_classes-1)
                 print("Negative class number: ", id3)
                 negative_classes = len(split_data[id3])
                 print("Negative Classes: ", negative_classes)
                 ncn = random.randint(0,negative_classes-1)
                 while(id3==i):
                     id3 = random.randint(0,n_classes-1)

                 negative = split_data[id3][ncn]

                 sample = [anchor,positive,negative]
                 writer.writerow(sample)

    print("Triplet Csv writing completed")


def readModelCSV(filename):
      '''
      1-by-N(videos)
      '''
      dataContainer = []
      with open(filename) as infile:
          for line in infile:
              line = line.replace('"', '')
              line = line.replace('\n','')
              data = line.split(",")
              dataContainer.append(data)
      print("Lenght of CSV: ", len(dataContainer))
      print("Width of CSV: ", len(dataContainer[0]))
      return dataContainer



def main():
    PATH= "omniglot/python/images_background"
    class_count = 0
    sample_list = []
    #Initialize loop to go through all the Characters and make a csv file
    languages = [L for L in listdir(PATH) if isdir(join(PATH, L))]
    characters = [C for  C in listdir(PATH) if isdir(join(PATH, C))]
    for language in languages:


        language_path = join(PATH,language)
        print("Language Path: ", language_path)
        characters = [C for  C in listdir(language_path) if isdir(join(language_path, C))]

        for character in characters:
            print(character)
            character_path = join(language_path,character)
            print("Character Path: " , character_path)

            for sample in  listdir(character_path):
                print(sample)
                image_path = join(character_path,sample)
                print("IMAGE PATH:" ,image_path)
                holder = [class_count,image_path]
                sample_list.append(holder)
            class_count+=1



    print("Number of Classes: ", class_count)
    print("Shape of First CSV:[%d,%d] "%(len(sample_list),len(sample_list[0])))


    """
    Write File to Csv
    """
    print("Writing data_names in model_data.csv")
    with open('parsedOmniglotdata.csv','w+') as csv_file:
        csv_file.truncate()
        writer = csv.writer(csv_file)
        for elem in sample_list:
            writer.writerow(elem)

    print("Csv writing completed")

    """
    Make Triplet Csv
    """

    loadedData = readModelCSV('parsedOmniglotdata.csv')
    split_data = split_list(loadedData)
    makeTriplet(split_data,"TripletOmniglotdata.csv",10)





if __name__=="__main__":
    main()
