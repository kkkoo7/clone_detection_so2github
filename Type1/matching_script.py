import re
import pandas as pd
import json
import os

base_path = "/mnt/c/Users/kkkoo/OneDrive/Documents/VirginiaTech/Spring20/SoftwareEngineeringCS5704/Project/data/new_data_format"
data_file_delimiter = ','

def add_headers(data_file, data_file_delimiter):
	largest_column_count = 0
	with open(data_file, 'r') as temp_f:
		lines = temp_f.readlines()
		for l in lines:
			column_count = len(l.split(data_file_delimiter)) + 1
			largest_column_count = column_count if largest_column_count < column_count else largest_column_count
	temp_f.close()
	column_names = [i for i in range(0, largest_column_count)]

#in case you are comfortable this way
#df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names)

def find_clone_count_for_each_question(arr1, arr2, clones, which_answer):
	i = 0
	while(i<len(arr1) and i <len(arr2)):
		p1 = arr1[i][:arr1[i].index("_")]
		p2 = arr2[i][:arr2[i].index("_")]
		if p1 == p2:
			print(i)
			clones[p1] = clones.get(p1, dict())
			clones[p1][which_answer] = clones[p1].get(which_answer, 0) + 1
		i = i + 1
	return clones


def find_filtered_data(tb_df, clones, which_answer):
	pattern1 = r'(\d+_\d+_github.java)'
	pattern2 = r'(\d+_\d+_stack_overflow.java)'
	pattern1 = re.compile(pattern1, re.I)
	pattern2 = re.compile(pattern2, re.I)
	filtered_df = []
	for i in range(tb_df.last_valid_index()):
		m1 = pattern1.findall(tb_df.iat[i,0])
		m2 = pattern2.findall(tb_df.iat[i,0])
		if m1 and m2:
			#print(i)
			clones = find_clone_count_for_each_question(m1, m2, clones, which_answer)
	return clones

def write_to_csv(filtered_df, path):
	with open(path, 'w') as csv_file:
		for item in filtered_df:
			csv_file.write(item)
			csv_file.write('\n')

def write_to_json(output, path):
	with open(path, 'w+', encoding='utf-8') as outfile:
		json.dump(output, outfile, sort_keys = False, indent=4)

def driver(base_path):
	clones = dict()
	all_answers_number = ""
	all_answers_prefix = ""
	all_answers_suffix = "_files"
	for root, dirs, files in os.walk(base_path):
		for filename in files:
			#reading as table
			file_path = os.path.join(base_path, filename)
			#print(file_path)
			tb_df = pd.read_table(file_path)
			match = re.search(r'(\w+)_(\d+)_', filename, re.I)
			which_answer = match.group(2)
			all_answers_prefix = match.group(1)
			all_answers_number = all_answers_number + which_answer	
			clones = find_filtered_data(tb_df, clones, which_answer)
		break;
	output_data_file = "filtered_" + "java_012_files" + ".json"
	write_to_json(clones, os.path.join(base_path, output_data_file))

if __name__ == '__main__':
	print("execution started")
	driver(base_path)