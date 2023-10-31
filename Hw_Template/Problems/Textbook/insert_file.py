import os

# Get the current working directory (the directory where the script is located)
directory = os.getcwd()

# Get the list of files in the directory
files = os.listdir(directory)

for k in range(len(files)-1, -1, -1):
    if files[k].endswith(".py"):
        files.pop(k)


# Som Tom-foolery to get the appropriate prefix for the directory we are in
prefix = files[1].split('.')[0][:-1]


# Set the starting number for the file names
start = int(input("What position do you want the new file to be in (enter an integer)? "))

# Set the ending number for the file names to the number of filtered files
end = len(files)

if start > end:
    start = end


# Iterate over the numbers in the range
for i in range(end, start-1, -1):
    # Construct the old and new file names
    old_file_name = f'{prefix}{i}.tex'
    new_file_name = f'{prefix}{i+1}.tex'
    print(old_file_name, new_file_name)


    # Use the os.rename function to rename the file
    os.rename(os.path.join(directory, old_file_name),
              os.path.join(directory, new_file_name))

with open(f'{prefix}{start}.tex', 'w') as f:
    f.write("This file has been inserted.")

print('Done!')
