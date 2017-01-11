# Functions for reading tables and databases

import glob
from database import *

# Write the read_table and read_database functions below


def read_table(table_file):
    '''(str)-> Table
    Given a table filename return the table
    REQ: table_file is a file in directory
    '''
    # Open the file holding the table
    file = open(table_file, 'r')
    # Make a counter to keeps check of the current line
    count = 0
    # Create an empty dictionary that will hold the table data
    table_dict = dict()
    # Use an elemental for loop for each line in the file
    for lines in file:
        # Strip the line of any leading whitespace
        line = lines.strip()
        # Check if the line is not empty so it does not add empty lines
        if line:
            # For the first first line of the file make that the key and title
            # for the table
            if (count == 0):
                # Make a list for every
                keys = lines.strip().split(',')
                for key in keys:
                    table_dict.update({key: []})
            else:
                for key in keys:
                    values = lines.split(',')
                    table_dict[key].append(values[keys.index(key)].strip())
            # Increase the counter to stay with the line count
            count += 1
    # Close the table file
    file.close()
    # Make a Table object with the data of table_dict
    table = Table(table_dict, table_file[:-4])
    # Return the table
    return (table)


def read_database():
    '''()-> Database
    Read all files in a directory and return a database of all the files'''
    # Make a list containing all table files in the directory
    file_list = glob.glob('*.csv')
    # Create a dictionary that will hold the filenames as keys and their table
    # As values
    database_dict = dict()
    # Make an elemental for loop for each element/ filename in filelist
    for files in file_list:
        # Remove the .csv from the file for the filename
        file_name = files[:-4]
        # Update the dictionary for it's keys
        database_dict.update({file_name: read_table(files)})
    # Create the database
    database = Database(database_dict)
    # Return the database
    return (database)
