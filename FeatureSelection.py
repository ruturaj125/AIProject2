from array import *
import numpy as np
import csv
import random
import copy
import math
import os.path
from os import path

print("## Feature Selection Algorithm ##")
#file = input("Enter dataset file name: ")
# file = "small_dataset.txt"
file = "large_dataset.txt"
while not path.exists(file):
	print("File does not exist.")
	# file = input("Enter dataset file name: ")

with open(file) as f:
	reader = csv.reader(f, delimiter = ' ', skipinitialspace = True)
	first_row = next(reader)
	num_cols = len(first_row)

yes = open(file, 'r')
lines = yes.readlines()
all_classes = []
for i in lines:
	all_classes.append(i.split()[0])
print(all_classes)

all_features = []
for i in range(1, num_cols):
	f = open(file,'r')
	lines = f.readlines()
	result = []
	for x in lines:
		result.append(x.split()[i])
	all_features.append(result)
f.close()

# for i in range(len(all_features)):
# 	print(all_features[i])

# f = open(file,'r')
# lines = f.readlines()
# result = []
# for x in lines:
# 	result.append(x.split(' ')[1])
# f.close()
# print(all_features[0][0])

print("Choose search method:")
print("	1] Forward Selection:")
print("	2] Backward Elimination:")
# algorithm = input()
algorithm="1"
if (algorithm == str(1)):
	print("forward selection")
	forward_selection()

elif (algorithm == str(2)):
	print("backward elimination")
	backward_elimination()

else:
	print("Try again!")
