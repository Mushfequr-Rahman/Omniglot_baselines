import csv
import os
import glob
import random
from os import listdir
from os.path import isdir, join, isfile
import cv2
import matplotlib.pyplot as plt



def read_folder(data,path,class_x):
    files= glob.glob(path)
    data_path=os.path.join('data/'+path+'/','*g')

    for file in files:
        data.append(class_x,file)
    return data


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

def split_list(datas):
    """
    Function to split the total list into a 64*nums_samples list
    """
    num_samples = 250
    output = []
    class_number = 0
    pos =0
    curr = []
    i = 0



    for data in datas:
        i+=1
        """
        if(int(data[0])==0):
            print("sample class: ", data[0])
            print("current class: ", class_number)
            print("i= ", i )
            print("Truth Value: ",((int(data[0]))==class_number))
        """
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
    print("W:" ,len(output[0]))
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
    with open('Tripletimagenetdata.csv','w+') as csv_file:
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
                 while(id3==i):
                     id3 = random.randint(0,n_classes-1)

                 negative = split_data[id3][id2]

                 sample = [anchor,positive,negative]
                 writer.writerow(sample)

    print("Triplet Csv writing completed")


def main():
    path = "mini-imagenet/python/train"
    #print("Files in directory: ", listdir(path))
    files = [f for f in listdir(path) if isdir(join(path, f))]
    #print("Files", files)
    sample_number = 600
    dataset = []

    for i in range(len(files)):
        for j in range(1,sample_number+1):
            if(j<10):
                image_path= files[i]+'/'+files[i]+'0000000'+str(j)+'.jpg'
            elif(j>=10 and j<100):
                image_path= files[i]+'/'+files[i]+'000000'+str(j)+'.jpg'
            elif(j>=100):
                image_path= files[i]+'/'+files[i]+'00000'+str(j)+'.jpg'
            #print("image_path:",image_path)
            test_path = join(path,image_path)

            if(isfile(test_path)):

                im = cv2.imread(test_path)
                im_resized = cv2.resize(im, (224, 224), interpolation=cv2.INTER_LINEAR)

                plt.imshow(cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGB))
                #plt.show()
                #print("j:" ,  j)
                curr = [i,test_path]
                #print(curr)
                dataset.append(curr)
            #print(dataset)

    print("Writing data_names in model_data.csv")
    with open('parsedimagenetdata550.csv','w+') as csv_file:
        csv_file.truncate()
        writer = csv.writer(csv_file)
        for elem in dataset:
            writer.writerow(elem)

    print("Csv writing completed")

    loadedData = readModelCSV('parsedimagenetdata550.csv')
    split_data = split_list(loadedData)
    makeTriplet(split_data,"Tripletimagenetdata.csv",250)






if __name__=="__main__":
    main()
