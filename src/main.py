from textnode import *
import os
import shutil
def main():
	source_dir = os.path.expanduser("~/my-static-site/static/")
	dest_dir = os.path.expanduser("~/my-static-site/public/")
	
	#Step 1 - delete all files in destination directory
	# check if path exists, if not create it
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
		os.makedirs(dest_dir)
	else:
		os.makedirs(dest_dir)
	
	copy_files(source_dir, dest_dir)
	

def copy_files(source_dir, dest_dir):
	
	# Step 2 - copying files to the directory
	dir_list = os.listdir(source_dir)
	for item in dir_list:
		current_path = os.path.join(source_dir,item)
		dest_path = os.path.join(dest_dir,item)
		if os.path.isdir(current_path):
			os.makedirs(dest_path)
			copy_files(current_path, dest_path)
		else:
			shutil.copy(current_path, dest_path)
			print(f"File path being copied:{dest_path}")

main()
