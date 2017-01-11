from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def run_query(database, input_query):
    '''(Database, str) -> Table
    Given a database run the query on the database and return the 
    resulting table
    REQ: input_query follow SQuEaL Syntax
    REQ: database is not empty
    '''
    # Seperate each token in the query
    input_query = input_query.replace(',', ' ')
    # Make a list with every element being a token
    query_list = input_query.split()
    # Find the columns that we want to keep
    column_list = query_list[
        get_tokens_index(query_list, 'start') + 1:get_tokens_index(
            query_list, 'from')]
    # Do a check to confirm whether or not the where token was found
    if ('where' in query_list[len(column_list):]):
        # If the where token is found then find the tables used from up to the
        # Where token and make conditions_list anything after the where token
        table_list = query_list[
            get_tokens_index(query_list, 'from') + 1:get_tokens_index(
                query_list, 'where')]
        conditions_list = query_list[len(column_list) + len(table_list) + 1:]
    else:
        # If the where token is not found then make table_list up to the end of
        # the list
        table_list = query_list[get_tokens_index(query_list, 'from') + 1:]
        conditions_list = []
    # Create a new table from the cartesian product of all the tables
    cartesian_table = Table()
    # for each table in table_list make the cartesian product of the
    # cartesian_table and current table in the list
    for tables in table_list:
        cartesian_table = cartesian_product(
            cartesian_table, database.get_table(tables))
    # Do a check to see if there are any conditions
    if (len(conditions_list) > 0):
        # For each condition in conditions_list
        for conditions in conditions_list:
            # Check if the condition uses and equal token or greater than token
            if '=' in conditions:
                # If the condition is an equal token then split the condition
                # by the equal token
                condition_list = conditions.split('=')
                # Check the condition is a value or column name
                if ("'" in conditions):
                    # If the condition is a value then remove the quotations
                    # and make a boolean that states we are checking for equal
                    # a column equal to the value
                    condition_list[1] = condition_list[1][1:-1]
                    equal_bool = True
                    column_bool = False
                else:
                    # Else the condition is a column comparison so
                    # make a boolean that states we are checking for equal
                    # a column equal to a columns
                    equal_bool = True
                    column_bool = True
                # Remove the unnecassary rows that don't make the conditions
                cartesian_table.remove_rows(condition_list, equal_bool,
                                            column_bool)
            elif '>' in conditions:
                # If we are use a greater than token then split the condition
                # by the '>' token
                condition_list = conditions.split('>')
                if ("'" in conditions):
                    # If the condition is a value then remove the quotations
                    # and make a boolean that states we are checking for
                    # a colum ngreater then a values
                    condition_list[1] = condition_list[1][1:-1]
                    equal_bool = False
                    column_bool = False
                else:
                    # Else the condition is a column comparison so
                    # make a boolean that states we are checking for greater
                    # than tokens and columns
                    equal_bool = False
                    column_bool = True
                # Remove the unnecassary rows that don't make the conditions
                cartesian_table.remove_rows(condition_list, equal_bool,
                                            column_bool)
    # Check if we are using all the columns in the table
    if ('*' not in column_list):
        # If we are not using all the columns that remove the columns that are
        # not in column_list
        cartesian_table.remove_columns(column_list)
    # Return the new table
    return(cartesian_table)


def get_tokens_index(query_list, token):
    '''(lsit of str, str)-> int
    Given an inputted query and a token find the index of the token
    REQ: len(query_list) > 0

    >>> get_tokens_index(['apple', 'banana'], 'banana')
    1
    >>> get_tokens_index(['1', 'banana'], '1')
    0
    '''
    # Create a variable that will hold the position of the token in the query
    token_index = int()
    # Use a for loop for each element in the list
    for elements in range(0, len(query_list), 1):
        # Check if the current index in the query is the token
        if(query_list[elements] == token):
            # If it is make token_index equal to the current index
            token_index = elements
    # Return token_index
    return token_index


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    Given two tables return a new table containing the two given tables
    REQ: table1 follow proper table format
    REQ: table2 follow proper table format
    
    '''
    # Create and make a new table to hold the cartesian product of the two
    # given tables
    new_table = Table({})
    new_table.make_cartesian(table1, table2)
    # Return the new table
    return new_table

if(__name__ == "__main__"):
    # Get the query inputed
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    # Run the program until a blank line is entered
    while (query != ''):
        # Using the input create a SQuEaL table
        table = run_query(read_database(), query)
        # Print the table
        print(table)
        # Get the user input again
        query = input("Enter a SQuEaL query, or a blank line to exit:")
