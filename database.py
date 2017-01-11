class Table():

    '''A class to represent a SQuEaL table'''

    def __init__(self, table_dict={}, table_name=''):
        '''(Table) -> NoneType
        Initialize this table. Create a dictionary to store the table'''
        # Initialize the required starter variables that represent the table
        # and it's name
        self._table = table_dict
        self._table_name = table_name

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        # Set the table to the dictionary provided
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        # Return the table
        return self._table

    def add_column(self, new_column):
        '''(Table, dict of {str: list of str})
        Add a new column to the Table by adding another dictionary
        REQ: new_column must be of the form:
            column_name: list_of_values

        '''
        # Add the new dictionary into the table
        self._table.update(new_column)

    def remove_column(self, column_name):
        '''(Table, str) -> NoneType
        Given the name of a column remove that column from the Table
        REQ: None'''
        # Make sure the column is a key in the table
        if (column_name in self._table):
            # Remove the column
            self._table.pop(column_name)

    def remove_columns(self, column_list):
        '''(Table, list of str) -> NoneType
        Given the names of the columns we want to keep, remove the columns
        that are not in that list
        REQ: column_list only contain keys in self._table'''
        # Create a placeholder dictionary to represent the table
        dict_rep = self._table
        # Make a list of the columns in the table
        table_column_list = list(dict_rep.keys())
        # Create a for loop for columns in the table
        for columns in table_column_list:
            # Check if column in the table is not in column_list
            if columns not in column_list:
                # Remove the column
                self.remove_column(columns)

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.num_rows()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))

    def num_rows(self):
        '''(Table) -> int
        Find the number of rows in a table
        '''
        # Set the number of rows equal to 0 by default
        rows = 0
        # Make a list of the keys / columns
        key_list = list(self._table.keys())
        # Check if there is at least 1 column
        if (len(key_list) > 0):
            # Get the number of rows from one of the columns
            rows = len(self._table[key_list[0]])
        return rows

    def __str__(self):
        '''(Table) -> str
        Outputs a string representation of a table'''
        # Make a string value to hold the result
        result = ''
        # Make a dictionary to represent the table
        dict_rep = self._table
        # Find the number of columns in the table
        columns = list(dict_rep.keys())
        # Add the table's name to the result
        result = self._table_name + '\n'
        # Add the columns to the result
        result += (', '.join(columns)) + '\n'
        # Find the number of rows in the table
        rows = self.num_rows()
        # Create a for loop for the number of rows in the table
        for row in range(rows):
            # Make a list to contain the current rows info
            cur_column = []
            # Create a elemental for loop for every column in columns
            for column in columns:
                # Add each column's value at that specific row to cur_column
                cur_column.append(dict_rep[column][row])
            # Add each new row to result
            result += (', '.join(cur_column)) + '\n'
        # return the result
        return result[:-1]

    def make_cartesian(self, table1, table2):
        '''(Table, Table, Table) -> NoneType'''
        # Find the number of rows for each table
        row_table1 = table1.num_rows()
        row_table2 = table2.num_rows()
        # Check if either of the tables have no rows and make it equal to 1
        if (row_table1 == 0):
            row_table1 = 1
        if (row_table2 == 0):
            row_table2 = 1
        # Create two placeholder dictionaries to represent the tables
        dict_rept1 = table1._table
        dict_rept2 = table2._table
        # Add the updated columns of table1 to the new table
        self.add_column(self.merge(dict_rept1, row_table1, row_table2, True))
        # Add the columns of table2 to the new table
        self.add_column(self.merge(dict_rept2, row_table1, row_table2, False))

    def merge(self, dict_table, row_table1, row_table2, is_t1):
        '''(Table, dict of {str: list of values}, int, int, bool) -> 
        dict of {str: list of values}
        Given a dictionary of the table, the number of rows in table 1 and
        table 2 and whether or not we are adding columns for table 1 or 2
        return a formatted dictionary with the length of (rows of table 1 *
        rows of table 2)
        REQ: dict_table is in proper SQuEaL format
        REQ: row_table1 != 0
        REQ: row_table2 != 0
        REQ: is_t1 has none'''
        # Get the columns of the table
        columns = list(dict_table.keys())
        cur_column = {}
        # Make the dictionary for the new table with the columns as ke
        for col in columns:
            cur_column.update({col: []})
        # Create a for loop for rows in table 1
        for row in range(row_table1):
            # Create a for loop for rows in table 2
            for row2 in range(row_table2):
                # Create an elemental for loop for each column
                for column in columns:
                    # Check if we are changing table 1 or table 2
                    if is_t1 is True:
                        # Add the modified column to the dictonary
                        cur_column[column].append(dict_table[column][row])
                    else:
                        # Add the modified column to the dictonary
                        cur_column[column].append(dict_table[column][row2])
        # Return the new dictionary representing the table
        return cur_column

    def remove_row(self, row_number):
        '''(Table, int) -> NoneType
        Given a row number delete the row
        REQ: row_number has none
        '''
        # Create an elemental for loop for each column is the table
        for columns in self._table.keys():
            # Remove the value at row_number from each columns
            self._table[columns].pop(row_number)

    def remove_rows(self, condition, equal_condition, compare_columns_bool):
        '''(Table, list of str, bool, bool) -> NoneType
        Remove the rows that do not meet the conditions
        REQ: condition is not empty
        REQ: equal_condition is not empty
        REQ: compare_columns_bool is not empty
        '''
        # Check if we are checking each column is equal to the condition
        if equal_condition is True:
            # Check if we are comparing a column with another column
            if not compare_columns_bool:
                # If we are not than make a for loop for each row in the table
                for rows in range(len(self._table[condition[0]])-1, -1, -1):
                    # If the column to compare is not equal to the value
                    # remove the row from the table
                    if (self._table[condition[0]][rows] != condition[1]):
                        self.remove_row(rows)
            else:
                # If we are than make a for loop for each row in the table
                for rows in range(len(self._table[condition[0]])-1, -1, -1):
                    # If the column to compare is not equal to the other column
                    # remove the row from the table
                    if (self._table[condition[0]][rows] != self._table[
                            condition[1]][rows]):
                        self.remove_row(rows)
        # Check if we are checking each column is greater than the condition
        else:
            # Check if we are comparing a column with another column
            if not compare_columns_bool:
                # Make a for loop for each row in the table
                for rows in range(len(self._table[condition[0]])-1, -1, -1):

                    if (condition[1].isnumeric() and self._table[condition[0]][
                            rows].isnumeric()):
                        # If they are then convert the values into a float and
                        # check if the column value is greater than the
                        # condition value if it is not than remove the row
                        if (float(self._table[condition[0]][rows]) <= float(
                                condition[1])):
                            self.remove_row(rows)
                    else:
                        # If the column to compare is less than or equal to the
                        # value remove the row from the table
                        if (self._table[condition[0]][rows] <= condition[1]):
                            self.remove_row(rows)
            else:
                # Make a for loop for each row in the table
                for rows in range(len(self._table[condition[0]])-1, -1, -1):
                    # Check if both columns are numbers
                    if (self._table[condition[1]][rows].isnumeric() and
                            self._table[condition[0]][rows].isnumeric()):
                        # If they are then convert the values into a float and
                        # check if the column value is less than or equal to
                        # condition value if it is not than remove the row
                        if (float(self._table[condition[0]][rows]) <= float(
                                self._table[condition[1]][rows])):
                            self.remove_row(rows)
                    else:
                        # If the column to compare is less than or equal to the
                        # other column remove the row from the table
                        # Check if both compared values are numbers
                        if (self._table[condition[0]][rows] <= self._table[
                                condition[1]][rows]):
                            self.remove_row(rows)


class Database():

    '''A class to represent a SQuEaL database'''

    def __init__(self, database_dict={}):
        '''(Database) -> NoneType
        Initialize this Database. Create a dictionary to store the database'''
        # Create a dictionary to repesent the database
        self._database = database_dict

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._database = new_dict

    def add_table(self, new_table):
        '''(Database, dict of {str: list of Table})
        Add a new table to the Database by adding another dictionary onto the
        original
        new_table must have the format:
            table_name: table
        '''
        self._table.update(new_table)

    def get_table(self, table_name):
        '''(Database, str) -> Table
        Given a table's name return the table'''
        return self._database[table_name]

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database

    def __str__(self):
        ''''''
        result = ''
        for keys in self._database:
            result += (self._database[keys].__str__()) + '\n' + '\n'
        return result[:-2]
