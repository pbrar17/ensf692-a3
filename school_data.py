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


def main():
    print("ENSF 692 School Enrollment Statistics")

    # Print Stage 1 requirements here
    i = 2013
    listOfYears = []
    while(i<2023):
        listOfYears.append(f"year_{i}")
        i +=1
    # print(listOfYears)

    for year in listOfYears:
        year_array = globals()[year]
        year_array = year_array.reshape(20, 3)
        globals()[year] = year_array
    # print(year_2013)

    data = np.array([year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022])
    
    namesIdData = pd.read_csv("Assignment3Data.csv", header= 0)
    schoolNames = namesIdData['School Name'].unique().tolist()
    # schoolNames = pd.unique(schoolNames)
    schoolIds = namesIdData['School Code'].astype(str).unique().tolist()
    arrayAccessNumbers = list(range(20))
    # [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    # schoolIds = pd.unique(schoolIds)

    # for name, code in zip(schoolNames, schoolIds):
    #     print(f"School Name: {name}, School Code: {code}")

    print("Shape of full data array:",data.shape)
    print("Dimensions of full data array:",data.ndim)


    
    # print(data)
    # print(data[0][1][1])
    # print(data[0][1])
    # print(data[1][1][1])
    # Prompt for user input
    print("")
    while(True):
        try: 
            selection = input("Please enter the high school name or school code code: ")
            if((selection not in schoolIds) and (selection not in schoolNames)):
                raise ValueError("You must enter a valid school name or code.")
            else: 
                break
        except ValueError as e:
            print(e)
            print(' ')
            continue
    schools = dict(zip(schoolIds, schoolNames))
    schoolAccess = dict(zip(schoolNames, arrayAccessNumbers))
    # print(schools)
    # print(selection)
    if(selection not in schoolNames):
        selection = schools[selection]
    # print(selection)
    # Print Stage 2 requirements here
    print("\n***Requested School Statistics***\n")

    def getID(schoolName):
        for id,name in schools.items():
            if schoolName == name:
                return id
    print("School Name: " + selection + ", School Code:" , getID(selection))
    #this is the array id, from 0-20
    school = schoolAccess[selection]
    # data[year][school][grade]
    # stuff = data[0:10,:,:][school][0]
    # grade10 = data[:,school,0]
    print("Mean enrollment for Grade 10:", np.nanmean(data[:,school,0]).astype(int))
    print("Mean enrollment for Grade 11:", np.nanmean(data[:,school,1]).astype(int))
    print("Mean enrollment for Grade 12:", np.nanmean(data[:,school,2]).astype(int))
    print("Highest enrollment for a single grade:", np.nanmax(data[:,school,:]).astype(int))
    print("Highest enrollment for a single grade:", np.nanmin(data[:,school,:]).astype(int))
    # print(data[:,school,:])

    start = 2013
    tenYear = 0
    while(start<2023):
        access = start-2013
        print(f"Total enrollment for {start}:", np.nansum(data[access,school,:]).astype(int))
        tenYear += np.sum(data[access,school,:])
        start += 1
    print("Total ten year enrollment:",  tenYear.astype(int))
    print("Mean total enrollment over 10 years:", (tenYear//10).astype(int) )

    # print(data[:,school,:])
    anArray = np.array([])
    for x in data[:,school,:]:
        mask = x>500
        # print(data[mask])
        x= x[mask]
        anArray = np.append(anArray, x)
    print("For all enrollments over 500, the median value was:",np.nanmedian(anArray).astype(int))
    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")
    print("Mean enrollment in 2013:", np.nanmean(data[0,:,:]).astype(int))
    print("Mean enrollment in 2022:", np.nanmean(data[-1,:,:]).astype(int))
    print("Total graduating class of 2022:", np.nansum(data[9,:,2]).astype(int))
    print("Highest enrollment for a single grade:", np.nanmax(data[:,:,:]).astype(int))
    print("Lowest enrollment for a single grade:", np.nanmin(data[:,:,:]).astype(int))


if __name__ == '__main__':
    main()