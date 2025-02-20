import os
import shutil
import csv
import ast

def remove_changed_methods(root_dir='.'):
    """
    Remove all folders named "changed-methods" starting from the root directory.
    """
    for current_root, dirs, files in os.walk(root_dir, topdown=False):
        for d in dirs:
            if d == "changed-methods":
                full_path = os.path.join(current_root, d)
                shutil.rmtree(full_path)
                print(f"Removed: {full_path}")

def process_csv(csv_file="results-with-build-information.csv"):
    """
    Process each line of the CSV file and create directories/files as specified.
    """
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            # Skip empty lines or header rows
            if not row or row[0] == "project":
                continue

            project = row[0]
            merge_commit = row[1]
            class_name = row[2]
            method = row[3]
            left_modifications_str = row[4]
            right_modifications_str = row[7]

            # Convert string representations of lists to actual lists of integers
            try:
                left_modifications = ast.literal_eval(left_modifications_str)
            except Exception:
                left_modifications = []
            try:
                right_modifications = ast.literal_eval(right_modifications_str)
            except Exception:
                right_modifications = []

            # Build directory paths (OBS2: "changed-methods" is literal)
            project_path = os.path.join(project)
            merge_commit_path = os.path.join(project_path, merge_commit)
            changed_methods_path = os.path.join(merge_commit_path, "changed-methods")
            class_path = os.path.join(changed_methods_path, class_name)
            method_path = os.path.join(class_path, method)

            # Create necessary directories
            os.makedirs(method_path, exist_ok=True)

            # Define file paths for the files to be created
            left_right_file = os.path.join(method_path, "left-right-lines.csv")
            right_left_file = os.path.join(method_path, "right-left-lines.csv")

            # Create the "left-right-lines.csv" file
            with open(left_right_file, "w", encoding="utf-8") as lr_file:
                for value in left_modifications:
                    lr_file.write(f"{class_name},sink,{value}\n")
                for value in right_modifications:
                    lr_file.write(f"{class_name},source,{value}\n")

            # Create the "right-left-lines.csv" file
            with open(right_left_file, "w", encoding="utf-8") as rl_file:
                for value in left_modifications:
                    rl_file.write(f"{class_name},source,{value}\n")
                for value in right_modifications:
                    rl_file.write(f"{class_name},sink,{value}\n")

            print(f"Processed: {project}/{merge_commit}/{class_name}/{method}")

def main():
    #Remove all "changed-methods" folders before starting the process
    remove_changed_methods()

    # Process the CSV file
    process_csv()

if __name__ == '__main__':
    main()
