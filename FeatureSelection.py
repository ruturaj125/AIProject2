import numpy as np
import csv
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import copy
from os import path

# nearest neighbor algorithm
def nearest_neighbor(curr_features, fake, real):
	number = 0.0
	#euclidian distance calculated
	for i in range(len(curr_features)):
		number = number + ((float(all_features[curr_features[i] - 1][real]) - float(all_features[curr_features[i] - 1][fake]))**2)
	return number



# leave one out cross validation for forward selection
def k_fold_forward(x, j):	#current set of features and one added
	num_correct = 0
	x.append(j)
	for i in range(len(all_classes)):
		closest = 999999999999999		# random big number for the distance
		closest_index = 99999999999999	# random big number for the closest index
		for k in range(len(all_classes)):
			if not(i == k):
				distance = nearest_neighbor(x, i, k)
				if distance < closest:
					closest = distance
					closest_index = k
		if all_classes[i] == all_classes[closest_index]:
			num_correct = num_correct + 1
	accuracy = num_correct/len(all_classes)	#calculating accuracy
	return accuracy,x

# leave one out cross validation for backward elimination
def k_fold_backward(x, j):
	num_correct = 0
	x = x[x != j]
	for i in range(len(all_classes)):
		closest = 999999999999999
		closest_index = 99999999999999
		for k in range(len(all_classes)):
			if not(i == k):
				distance = nearest_neighbor(x, i, k)
				if distance < closest:
					closest = distance
					closest_index = k
		if all_classes[i] == all_classes[closest_index]:
			num_correct = num_correct + 1
	accuracy = num_correct/len(all_classes)
	return accuracy, x

# Define Default rate
def no_features():
	print("On the 0th level of search tree")
	print("->Considering no features")
	if all_classes.count('1.0000000e+00') > all_classes.count('2.0000000e+00'):
		accuracy = all_classes.count('1.0000000e+00')/len(all_classes)

	else:
		accuracy = all_classes.count('2.0000000e+00')/len(all_classes)

	print("Accuracy: " + str(accuracy) + "\n")

# for output csv file
dict = {'Features': [],
		'Accuracy': [],
		}

df = pd.DataFrame(dict)



# Feature Selection forward selection
def forward_selection(df):
	no_features()
	curr_set_features = []
	good_accuracies = []
	more_features = []
	considered_features = []
	for i in range(1, num_cols):
		print("On the level " + str(i) + " of search tree")
		feature_to_add_at_level = 0
		best_accuracy = 0
		for j in range(1, num_cols):
			x = copy.deepcopy(curr_set_features)
			# least_num_wrong = 1000
			if j not in curr_set_features:
				print("->Considering the feature " + str(j))
				accuracy,list_features = k_fold_forward(x, j)
				print("Accuracy: " + str(round(accuracy,2)), " Features considered:", list_features)
				if accuracy > best_accuracy:
					best_accuracy = accuracy
					feature_to_add_at_level = j
					considered_features = list_features
		curr_set_features.append(feature_to_add_at_level)
		good_accuracies.append(best_accuracy)
		print("Best Accuracy: " + str(round(best_accuracy, 2)), " Feature considered:", feature_to_add_at_level)
		df_2 = pd.DataFrame({'Features': [considered_features], 'Accuracy': [round(best_accuracy, 2)]})
		df = df.append(df_2)
		y = copy.deepcopy(curr_set_features)
		more_features.append(y)
		maxpos = good_accuracies.index(max(good_accuracies))
		print("On level " + str(i) + " added feature " + str(feature_to_add_at_level) + " to current set\n")
	print("The best accuracy: " + str(max(good_accuracies)))
	print("Features: " + str(more_features[maxpos]))
	return df


def backward_elimination(df):

	curr_set_features = np.arange(1, num_cols, 1)
	good_accuracies = []
	more_features = []
	considered_features = []
	for i in range(1, num_cols):
		print("On the level " + str(i) + " of the search tree")
		feature_to_sub_at_level = 0
		best_accuracy = 0
		for j in range(1, num_cols):
			x = copy.deepcopy(curr_set_features)
			# print(x)
			if j in curr_set_features:
				print("->Considering removing the  feature " + str(j))
				accuracy, list_features = k_fold_backward(x, j)
				print("Accuracy: " + str(round(accuracy,2)), " Features considered:", list_features)
				if accuracy > best_accuracy:
					best_accuracy = accuracy
					feature_to_sub_at_level = j
					considered_features = list_features
		curr_set_features = curr_set_features[curr_set_features != feature_to_sub_at_level]
		good_accuracies.append(best_accuracy)
		print("Best Accuracy: " + str(round(best_accuracy, 2)), " Feature dropped:", feature_to_sub_at_level)
		df_2 = pd.DataFrame({'Features': [considered_features], 'Accuracy': [round(best_accuracy, 2)]})
		df = df.append(df_2)
		y = copy.deepcopy(curr_set_features)
		more_features.append(y)
		maxpos = good_accuracies.index(max(good_accuracies))
		print("On level " + str(i) + " removed feature " + str(feature_to_sub_at_level) + " from the current set\n")
	print("The best accuracy: " + str(max(good_accuracies)))
	print("Features " + str(more_features[maxpos]))
	return df


print("## Feature Selection Algorithm ##")
file = input("Enter dataset file name: ")
# file = "small_dataset.txt"
# file = "large_dataset.txt"
while not path.exists(file):
	print("File does not exist.")
	file = input("Enter dataset file name: ")

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

print("Choose search method:")
print("	1] Forward Selection:")
print("	2] Backward Elimination:")
algorithm = input()
# algorithm="2"
if (algorithm == str(1)):
	print("forward selection")
	df = forward_selection(df)

elif (algorithm == str(2)):
	print("backward elimination")
	df = backward_elimination(df)

else:
	print("Try again!")

df.to_csv("output_features1.csv", encoding='utf-8', index=False, sep =';')