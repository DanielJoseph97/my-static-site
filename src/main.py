from textnode import *
import os
import shutil
from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title
def main():
	source_dir = "static/"
	dest_dir = "public/"
	
	#Step 1 - delete all files in destination directory
	# check if path exists, if not create it
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
		os.makedirs(dest_dir)
	else:
		os.makedirs(dest_dir)
	
	copy_files(source_dir, dest_dir)

	generate_page("content/index.md","template.html","public/index.html")
	

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

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	path_file = open(from_path) #file objects
	template_file = open(template_path)
	path_content = path_file.read() #strings
	template_content = template_file.read()
	path_content_node = markdown_to_html_node(path_content)
	path_content_html = path_content_node.to_html()
	page_title = extract_title(path_content)
	template_content = template_content.replace("{{ Title }}", page_title)
	template_content = template_content.replace("{{ Content }}", path_content_html)
	path_file.close()
	template_file.close()

	# ADD THESE DEBUG PRINTS HERE:
	print(f"DEBUG: dest_path is: {dest_path}")
	dest_dir = os.path.dirname(dest_path)
	print(f"DEBUG: dest_dir is: {dest_dir}")
	os.makedirs(dest_dir, exist_ok=True) # Ensure exist_ok=True here

	print("DEBUG: About to write file.")
	# Print the full template_content to ensure it's not empty or malformed
	print(f"DEBUG: First 500 chars of template_content: {template_content[:500]}")

	with open(dest_path,"w") as dest_file:
		dest_file.write(template_content)
	print(f"DEBUG: File successfully written to {dest_path}") # Confirm the write operation completed

	dest_dir = os.path.dirname(dest_path)
	os.makedirs(dest_dir, exist_ok=True)
	#checking if dest_path exists
	with open(dest_path,"w") as dest_file:
		dest_file.write(template_content)

main()
