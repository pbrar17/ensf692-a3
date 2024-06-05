# school_data.py
# Pahul Brar
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd
import numpy as np
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

# Declare any global variables needed to store the data here


# You may add your own additional classes, functions, variables, etc.
def reshape_data():
    """
    Reshapes yearly data arrays into the required format.

    This function reshapes each year's data array into a 20x3 format, 
    representing the enrollment statistics for 20 schools and 3 grades.
    """
    #This allows me to generatre a list of years from 2013 to 2023, so I can call each indvidual year's dataset
    list_of_years = [f"year_{i}" for i in range(2013, 2023)]
    # I am reshaping every year, so I can be confident every year has 20 rows for the schools, and 3 for the different grades (10,11,12)
    # By using global, I am directly affecting the datasets given above
    for year in list_of_years:
        year_array = globals()[year]
        year_array = year_array.reshape(20, 3)
        globals()[year] = year_array

def load_data():
    """
    Loads and prepares the data for analysis.

    This function reshapes the yearly data arrays, loads the school names and IDs 
    from a CSV file, and returns the necessary data structures for further analysis.

    By directly getting the names from the CSV files, I reduce the need for hardcoding any data into it, 
    as we were tasked with minimize hardcoding. 

    Returns:
    tuple: A tuple containing:
        - np.array: A 3-d array containg data for all years.
        - list: A list of unique school names.
        - list: A list of unique school IDs.
        - list: A list of array access numbers (0-19) for the 20 schools, which will be used to access elements in the 3-d np.array.
    """
    #Reshaping the data
    reshape_data()
    #Creating a 3d array from the data, which has year as the third dimension
    data = np.array([year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022])
    
    #Reading in the csv file, so I can extract the School Names and their ID's
    names_id_data = pd.read_csv("Assignment3Data.csv", header=0)
    school_names = names_id_data['School Name'].unique().tolist()
    school_ids = names_id_data['School Code'].astype(str).unique().tolist()

    #Creating a list of array indices numbers, to easily access different schools
    array_access_numbers = list(range(20))

    return data, school_names, school_ids, array_access_numbers

def get_user_selection(school_ids, school_names):
    """
    Prompts the user for a valid school name or code and returns the selection.

    This function repeatedly prompts the user for input until a valid school name or code is entered.

    Args:
        school_ids (list): A list of valid school IDs, stored as Strings.
        school_names (list): A list of valid school names, stored as Strings.

    Returns:
        String: The selected school name or ID entered by the user.
    """
    #Coninually runs until, correct input given by user 
    while True:
        try:
            selection = input("Please enter the high school name or school code: ")
            if (selection not in school_ids) and (selection not in school_names):
                raise ValueError("You must enter a valid school name or code.")
            else:
                return selection
        except ValueError as e:
            print(e)
            print(' ')

def get_school_id(school_name, schools):
    """
    Returns the school ID given the school name.

    Args:
        school_name (String): The name of the school.
        schools (dict): A dictionary mapping school IDs to school names.

    Returns:
        String: The ID of the school with the given name.
    """
    # Gets the ID
    for id, name in schools.items():
        if school_name == name:
            return id

def print_school_statistics(selection, data, school_names, school_ids, array_access_numbers):
    """
    Prints the statistics for the selected school.

    This function prints various stats for the selected school, including mean enrollments,
    highest and lowest enrollments, and total enrollments over ten years.

    Args:
        selection (String): The selected school name or ID.
        data (np.array): The data array containing enrollment statistics.
        school_names (list): A list of unique school names.
        school_ids (list): A list of unique school IDs.
        array_access_numbers (list): A list of array access numbers (0-19) for the 20 schools.
    """
    print("\n***Requested School Statistics***\n")

    #Creating a dictonary with school_ids as keys, and the names as values
    schools = dict(zip(school_ids, school_names))
    #Creating a dictonary, with school names as keys, and the array indices as their values
    school_access = dict(zip(school_names, array_access_numbers))

    #Ensuring, that the user input is the name of the school, by converting id to name using the above dictonary
    if selection not in school_names:
        selection = schools[selection]

    #Getting the school id from the above dictonary
    school_id = get_school_id(selection, schools)
    print(f"School Name: {selection}, School Code: {school_id}")
    
    #Getting the index number of the selected school
    school = school_access[selection]
    
    #Printing relevant stats
    print("Mean enrollment for Grade 10:", np.nanmean(data[:,school,0]).astype(int))
    print("Mean enrollment for Grade 11:", np.nanmean(data[:,school,1]).astype(int))
    print("Mean enrollment for Grade 12:", np.nanmean(data[:,school,2]).astype(int))
    print("Highest enrollment for a single grade:", np.nanmax(data[:,school,:]).astype(int))
    print("Highest enrollment for a single grade:", np.nanmin(data[:,school,:]).astype(int))

    #Printing stats for all the years, individually
    start = 2013
    ten_year_total = 0
    while start < 2023:
        access = start - 2013
        print("Total enrollment for " + str(start) + ":", np.nansum(data[access, school, :]).astype(int))
        ten_year_total += np.nansum(data[access, school, :])
        start += 1
    print("Total ten-year enrollment:", ten_year_total.astype(int))
    print("Mean total enrollment over 10 years:", (ten_year_total // 10).astype(int))

    #Checking for enrollments over 500
    enrollments_over_500 = np.array([])
    for x in data[:, school, :]:
        mask = x > 500
        x = x[mask]
        enrollments_over_500 = np.append(enrollments_over_500, x)
    if enrollments_over_500.size == 0:
        print("No enrollments over 500.")
    else:
        print("For all enrollments over 500, the median value was:", np.nanmedian(enrollments_over_500).astype(int))

def print_general_statistics(data):
    """
    Prints general statistics for all schools.
    
    Parameters:
        data (np.ndarray): The data array.
    """
    #Printing the general stats, that are constant for the program.
    print("\n***General Statistics for All Schools***\n")
    print("Mean enrollment in 2013:", np.nanmean(data[0, :, :]).astype(int))
    print("Mean enrollment in 2022:", np.nanmean(data[-1, :, :]).astype(int))
    print("Total graduating class of 2022:", np.nansum(data[9, :, 2]).astype(int))
    print("Highest enrollment for a single grade:", np.nanmax(data[:, :, :]).astype(int))
    print("Lowest enrollment for a single grade:", np.nanmin(data[:, :, :]).astype(int))

def main():
    """
    Main function to run the school enrollment statistics application.
    Calls all the sub functions, in proper order with correct arguments.
    """
    print("ENSF 692 School Enrollment Statistics")
    data, school_names, school_ids, array_access_numbers = load_data()
    # Print Stage 1 requirements here
    print("Shape of full data array:", data.shape)
    print("Dimensions of full data array:", data.ndim)
    print("")

    # Prompt for user input
    selection = get_user_selection(school_ids, school_names)

    # Print Stage 2 requirements here
    print_school_statistics(selection, data, school_names, school_ids, array_access_numbers)
    
    # Print Stage 3 requirements here
    print_general_statistics(data)

if __name__ == '__main__':
    main()
