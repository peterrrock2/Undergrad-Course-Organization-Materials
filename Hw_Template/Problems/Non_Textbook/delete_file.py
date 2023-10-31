import os

# Get the current working directory (the directory where the script is located)
directory = os.getcwd()

# Get the list of files in the directory
files = os.listdir(directory)

# Not the fastest, but we don't really care for this script
remove_list = []
for item in files:
    if not item.endswith(".tex"):
        remove_list.append(item)
        
for thing in remove_list:
    files.remove(thing)

# Som Tom-foolery to get the appropriate prefix for the directory we are in
prefix = files[0].split('.')[0][:-1]


# Set the starting number for the file names
start = int(
    input("What problem number would you like to delete (enter an integer)? "))

# Set the ending number for the file names to the number of filtered files
end = len(files)

os.remove(f'{prefix}{start}.tex')

# Iterate over the numbers in the range
for i in range(start+1, end+1):
    # Construct the old and new file names
    old_file_name = f'{prefix}{i}.tex'
    new_file_name = f'{prefix}{i-1}.tex'

    # Use the os.rename function to rename the file
    os.rename(os.path.join(directory, old_file_name),
              os.path.join(directory, new_file_name))


print('Done!')
