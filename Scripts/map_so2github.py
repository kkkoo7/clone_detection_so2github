import pandas as pd
import os
import re
from functools import reduce
#base_path = "C:\\Users\\kkkoo\\OneDrive\\Documents\\VirginiaTech\\Spring20\\SoftwareEngineeringCS5704\\Project\\data"
base_path = '/mnt/c/Users/kkkoo/OneDrive/Documents/VirginiaTech/Spring20/SoftwareEngineeringCS5704/Project/data'
csv_file = 'JavaAllPostTop123WithGithubRepos.csv'
first_upvoted_folder = '1st_voted'
second_upvoted_folder = '2nd_voted'
third_upvoted_folder = '3rd_voted'
regex = re.compile('<code>(.*?)</code>', re.DOTALL)

def get_code_from_so_body(body):
	text = regex.findall(body)
	if text:
		text = text[0].strip('\n')
	else:
		text = ''
	return text

def createFolder(path, name, recursive=False):
	try:
		if not recursive:
			os.mkdir(os.path.join(path, name))
		else:
			os.makedirs(os.path.join(path, name), exist_ok=True)
	except FileExistsError:
		print("Dir already exist")


def get_file_name(parent_id, unique_id, is_github):
	file_name = '{}_{}'.format(parent_id, unique_id)
	file_name = '{}_{}.java'.format(file_name, 'github') if is_github else '{}_{}.java'.format(file_name, 'stack_overflow')
	return file_name


def write_to_file(file_path_array, data):
	if not os.path.exists(reduce(os.path.join, file_path_array[:-1])):
		createFolder(reduce(os.path.join, file_path_array[:-1]), '', recursive=True)
	with open(reduce(os.path.join, file_path_array), 'w+', encoding='utf-8') as out:
		out.write(data)


def extract_answer(df):
	df_so = df.drop_duplicates(['parent_id','id']).sort_values(['parent_id', 'score'], ascending=False)
	df_github = df.drop_duplicates(['parent_id', 'sample_path']).sort_values(['parent_id'])
	i = 0
	while(i<len(df_so)):
		write_to_file((base_path, first_upvoted_folder, str(df_so['parent_id'][df_so.index[i]]),get_file_name(df_so['parent_id'][df_so.index[i]], df_so['id'][df_so.index[i]], False)) ,get_code_from_so_body(df_so['body'][df_so.index[i]]))
		i += 1
		if df_so['parent_id'][df_so.index[i]] == df_so['parent_id'][df_so.index[i-1]]:
			write_to_file((base_path, second_upvoted_folder, str(df_so['parent_id'][df_so.index[i]]), get_file_name(df_so['parent_id'][df_so.index[i]], df_so['id'][df_so.index[i]], False)), get_code_from_so_body(df_so['body'][df_so.index[i]]))
			i += 1
		if df_so['parent_id'][df_so.index[i]] == df_so['parent_id'][df_so.index[i - 1]]:
			write_to_file((base_path, third_upvoted_folder, str(df_so['parent_id'][df_so.index[i]]), get_file_name(df_so['parent_id'][df_so.index[i]], df_so['id'][df_so.index[i]], False)), get_code_from_so_body(df_so['body'][df_so.index[i]]))
			i += 1
	i = 0
	while(i < len(df_github)):
		write_to_file((base_path, third_upvoted_folder, str(df_github['parent_id'][df_github.index[i]]), get_file_name(df_github['parent_id'][df_github.index[i]], 1, True)), df_github['content'][df_github.index[i]])
		write_to_file((base_path, second_upvoted_folder, str(df_github['parent_id'][df_github.index[i]]), get_file_name(df_github['parent_id'][df_github.index[i]], 1, True)), df_github['content'][df_github.index[i]])
		write_to_file((base_path, first_upvoted_folder, str(df_github['parent_id'][df_github.index[i]]) ,get_file_name(df_github['parent_id'][df_github.index[i]], 1, True)), df_github['content'][df_github.index[i]])
		j = i + 1
		while(j < len(df_github) and df_github['parent_id'][df_github.index[j]] == df_github['parent_id'][df_github.index[j-1]]):
			write_to_file((base_path, third_upvoted_folder, str(df_github['parent_id'][df_github.index[j]]), get_file_name(df_github['parent_id'][df_github.index[j]], j-i+1, True)), df_github['content'][df_github.index[j]])
			write_to_file((base_path, second_upvoted_folder, str(df_github['parent_id'][df_github.index[j]]), get_file_name(df_github['parent_id'][df_github.index[j]], j-i+1, True)), df_github['content'][df_github.index[j]])
			write_to_file((base_path, first_upvoted_folder, str(df_github['parent_id'][df_github.index[j]]), get_file_name(df_github['parent_id'][df_github.index[j]], j-i+1, True)), df_github['content'][df_github.index[j]])
			j += 1
		i = j

def main():
	createFolder(base_path, first_upvoted_folder)
	createFolder(base_path, second_upvoted_folder)
	createFolder(base_path, third_upvoted_folder)
	df = pd.read_csv(os.path.join(base_path, csv_file))
	extract_answer(df)

if __name__ == '__main__':
	main()




