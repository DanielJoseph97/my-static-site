import os
import sys
import shutil
from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title

def main():
	if len(sys.argv) > 1:
		base_path = sys.argv[1]
	else:
		base_path = "/"

	source_dir = "static/"
	content_dir = "content/"
	template_file = "template.html"
	dest_dir = "docs/"
	
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
		os.makedirs(dest_dir)
	else:
		os.makedirs(dest_dir)
	
	copy_files(source_dir, dest_dir)
	generate_pages_recursive(content_dir, template_file, dest_dir, base_path)
	
def copy_files(source_dir, dest_dir):
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

def generate_page(from_path, template_path, dest_path, base_path):
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
	template_content = template_content.replace("href=\"/",f"href=\"{base_path}")
	template_content = template_content.replace("src=\"/", f"src=\"{base_path}")
	path_file.close()
	template_file.close()

	# ADD THESE DEBUG PRINTS HERE:
	# print(f"DEBUG: dest_path is: {dest_path}")
	dest_dir = os.path.dirname(dest_path)
	# print(f"DEBUG: dest_dir is: {dest_dir}")
	os.makedirs(dest_dir, exist_ok=True) # Ensure exist_ok=True here

	# print("DEBUG: About to write file.")
	# Print the full template_content to ensure it's not empty or malformed
	# print(f"DEBUG: First 500 chars of template_content: {template_content[:500]}")

	with open(dest_path,"w") as dest_file:
		dest_file.write(template_content)
	# print(f"DEBUG: File successfully written to {dest_path}") # Confirm the write operation completed

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
	dir_list = os.listdir(dir_path_content)
	for item in dir_list:
		current_path = os.path.join(dir_path_content,item)
		dest_path = os.path.join(dest_dir_path,item)
		if os.path.isdir(current_path):
			if os.path.exists(dest_path) == False:
				os.makedirs(dest_path)
			generate_pages_recursive(current_path,template_path, dest_path, base_path)
		if os.path.isfile(current_path) and item.endswith(".md"):
			dest_path = dest_path.replace(".md",".html")
			generate_page(current_path, template_path, dest_path, base_path)
main()
