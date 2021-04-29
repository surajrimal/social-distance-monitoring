import os
import glob
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--train', help="Percentage of train data", default=0.8)

directory = './image'

args = parser.parse_args()

count = 0
train = open("train_person.txt", "w+")
test = open("test_person.txt", "w+")
val = open("val_person.txt", "w+")
filenames = [x for x in os.listdir(directory) if not x.endswith(".txt") and not x.endswith(".xml") ]
random.shuffle(filenames)

for filename in filenames:
    if ( filename.endswith(".jpg") or filename.endswith(".png") ) and count < 0.8 * len(filenames):
        train.write("./image/"+filename+"\n")
        count += 1
    elif ( filename.endswith(".jpg") or filename.endswith(".png") ) and count < (1-0.8)*len(filenames)/2 + 0.8*len(filenames):
        test.write("./image/"+filename+"\n")
        count += 1
    elif (filename.endswith(".jpg") or filename.endswith(".png")):
        val.write("./image/"+filename+"\n")
        count += 1

train.close()
test.close()
val.close()