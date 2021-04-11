# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:09:49 2021

Team: SORA
Olivia Hobbs 
Daniel Nelson 
Alexandra Mullen
Nathan Byerley


"""
#import required libraries
import os #need this library to change file locations
import argparse #need argparse library to take inputs from the commandline
import datetime #date time library, need to make a date time variable.
import pandas
import geopandas as gpd
#from area import area #use to calculate area of imported KML file     
import matplotlib.pyplot as plt 
import fiona
from mpl_toolkits.axes_grid1 import make_axes_locatable

    
def FilterFlights (aoi, flights, start_date, end_date, min_altitude, max_altitude, path):
    '''
    The job of this function is to receive the input selection parameters that will be used to filter the dataframe of flights.
    It will return a geodataframe containing only the desired flights.
    
    Author: Daniel Nelson
    Parameters
    ----------
    aoi : TYPE KML
        Input area of interest in KML format
    flights : TYPE STRING
        A csv containing the list of flights in ottawa
    start_date : TYPE DATETIME
        the start date to filter flights by
    end_date : TYPE DATETIME
        the end date to filter flights by
    min_altitude : TYPE INT
        lowest altitude to filter by
    max_altitude : TYPE INT
        highest altitude to filter by
    path : TYPE STRING
        chosen directory for files

    Returns
    -------
    LocationFiltered : TYPE GEODATAFRAME
        Geodataframe with the flights that meet the selection parameters

    '''
    
    #set the chosen directory
    os.chdir(path)
    #read in the flights csv
    FlightsTOFilter = pandas.read_csv(flights)
    
    #set the date column in the flights csv to datetime 
    FlightsTOFilter['FLIGHT_EVENT_DATE'] = pandas.to_datetime(FlightsTOFilter['FLIGHT_EVENT_DATE'], format='%y-%m-%d %H:%M:%S')
    #filter the flights by date   
    #FlightsTOFilter.set_index(['FLIGHT_EVENT_DATE'])
    DateFiltered = FlightsTOFilter[(FlightsTOFilter['FLIGHT_EVENT_DATE'] > start_date) & (FlightsTOFilter['FLIGHT_EVENT_DATE'] <= end_date)]
    #filter the flights by altitude
    min_altitude = int(min_altitude)
    max_altitude = int(max_altitude)
    DateFiltered.set_index(['FLIGHT_FIX_ALTITUDE_ESTAB_FT'])
    AltitudeFiltered = DateFiltered.loc[min_altitude:max_altitude]
    #set the area of interest crs
    areatoclip = aoi
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
    polygonclip = gpd.read_file(areatoclip)
    polygonclip.set_crs('EPSG:4326')
    #covert the dataframe to a geodataframe
    AltitudeFiltered_to_Geo = gpd.GeoDataFrame(AltitudeFiltered, geometry=gpd.points_from_xy(AltitudeFiltered.FLIGHT_FIX_LONGITUDE_DEG, AltitudeFiltered.FLIGHT_FIX_LATITUDE_DEG), crs="EPSG:4326")
    #clip the flights so that only those within the aoi remain
    LocationFiltered = gpd.clip(AltitudeFiltered_to_Geo, polygonclip)
    LocationFiltered.drop_duplicates(subset='NATIONAL_FLIGHT_ID', keep="last")

    #Give user warning if no flights are within selection.
    if LocationFiltered.shape[0] == 0:
        print("No flights within selected area, altitude and date.")
        
    
    return LocationFiltered


def AirRisk(aoi,flights,start_date_time_obj,end_date_time_obj,min_altitude,max_altitude, path):
    """
    AirRisk will take in a geodataframe from FilterFlights and calculate air risk based on flights entering the area of interest. 
    It will output 2 .txt files, one named "Count", that demonstrates the amount of flights in the area of interest and "Area", 
    which is a file containing the area of the area of interest in km^3. 

    Author: Alexandra Mullen
    Parameters
    ----------
    aoi : TYPE KML
        Input area of interest in KML format
    flights : TYPE STRING
        A csv containing the list of flights in ottawa
    start_date : TYPE DATETIME
        the start date to filter flights by
    end_date : TYPE DATETIME
        the end date to filter flights by
    min_altitude : TYPE INT
        lowest altitude to filter by
    max_altitude : TYPE INT
        highest altitude to filter by
    path : TYPE STRING
        chosen directory for files

    Returns
    -------
    None.

    """
    
    os.chdir(path)
    
    areatoclip = aoi
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
    polygonclip = gpd.read_file(areatoclip)
    polygonclip.set_crs('EPSG:4326')
    Area = polygonclip.to_crs('EPSG:3979')
    
    #using area library to calculate square meter (library defaults to m2) from area of interest determined in FilterFlights function
    m2= int(pandas.to_numeric(Area['geometry'].area))
    GoodFlights = FilterFlights(aoi, flights, start_date_time_obj, end_date_time_obj, min_altitude, max_altitude, path)
    #converting m2 dataframe to km3
    km2 = m2/10**6
    #counting flights passed in from filter function
    number_of_rows= GoodFlights.shape[0]
    #opening a .txt file to write final integer
    f=open("AirRisk.txt", 'w')
    #writing integer created above to .txt 
    f.write(str(number_of_rows))
    f.write (" flights.\n")
    f.write("Area: ")
    f.write(str(km2))
    f.write(" sq. km.")
    #closing .txt file
    f.close()


def popdens(aoi,pop,flights,start_date_time_obj,end_date_time_obj,min_altitude,max_altitude,path): 
    """
    
    Author: Olivia Hobbs 
    Parameters
    ----------
    aoi : TYPE KML
        Input area of interest in KML format
    pop : TYPE SHP
        A shapefile with the population density as attribute and census tracts from STATCAN
    path : TYPE STRING
        chosen directory for files

    Returns
    -------
    None.

    """
    
    GoodFlights = FilterFlights(aoi, flights, start_date_time_obj, end_date_time_obj, min_altitude, max_altitude, path)
    
    os.chdir(path)
    #Establish file path and bring in popdens shapefile 
    map_df = gpd.read_file(pop)
    #load in AOI to layer map 
    #KML is funky so needs the extra line below
    map_df.head()
    map_df.set_crs
    map_df.set_crs('EPSG:4326')
    areatoclip = aoi
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
    polygonclip = gpd.read_file(areatoclip)
    polygonclip.set_crs('EPSG:4326')
    DensityAOI= gpd.clip(map_df, polygonclip)

    #Filter only census tracts that contain flights
    Census_Mask = gpd.sjoin(DensityAOI, GoodFlights, op='contains')

    #Get list of population densities and ID
    PolygonNames = Census_Mask['CTUID'].tolist()
    PolygonDensity = Census_Mask['PopDen'].tolist()

    #Write Population density for each tract to file
    f=open("Density.txt", 'w')
    f.write("All census tracts that contain at least one flight\n")
    f.write("Census Tract CTUID: Population Density\n")
    i = 0
    for p in PolygonNames:
        f.write(str(PolygonNames[i])) 
        f.write(": ")
        f.write(str(PolygonDensity[i]))
        f.write("\n")
        i = i + 1
    f.close()


def main ():
    '''
    Main function, take all of the users inputs through the commandline
	Responsible for retrieving the user inputs, then running the appropriate functions based on selection.
    Author of this function: Nathan Byerley
    
    Returns
    -------
    None.

    '''   
    print("For help with formmating type -h")#this print statement is here to help the user access help
    
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@',epilog='Please make sure all required files are in the same folder')#a friendly reminder if help is needed
    parser.add_argument("path", help = "Enter the exact file path for the files of interest.")#first input required in command line
    parser.add_argument("flights", help = 'Flights file name with extention')#second input required in command line
    parser.add_argument("pop", help = 'population density file name with extention') #3rd input
    parser.add_argument("aoi", help = 'area of interest file name with extention') #4th input 
    parser.add_argument("start_date_time", help = 'date and time for start of flight, format YY-MM-DD H:M:S') #5th input
    parser.add_argument("end_date_time", help = 'date and time for end of flight, format YY-MM-DD H:M:S') #6th input
    parser.add_argument("min_altitude", help = 'minimum altitude of flight') #7th input
    parser.add_argument("max_altitude", help = 'maximum altitude of flight') #8th input
    args = parser.parse_args()
    
    path = args.path #makes a variable called path from the input for the file path
    flights = args.flights #makes a variable for the flight list file name
    pop = args.pop #makes a variable for the population dencity file name
    aoi = args.aoi #makes a variable for the area of interest file name
    start_date_time_str = args.start_date_time
    start_date_time_obj = datetime.datetime.strptime(start_date_time_str,'%y-%m-%d %H:%M:%S')#transforms the input for datetime into a date time object
    end_date_time_str = args.end_date_time
    end_date_time_obj = datetime.datetime.strptime(end_date_time_str,'%y-%m-%d %H:%M:%S')
    min_altitude = args.min_altitude #makes variable for the flight's minimum altitude
    max_altitude = args.max_altitude #makes variable for the flight's maximum altitude

    os.chdir(path)#used to access the file that the user is looking for
    print(path,"\n")
    
    print (flights,"\n") #prints the name of the file
    
    print (pop,"\n") #prints the name of the file
   
    print (aoi,"\n") #prints the name of the file
    
    print('start time:',start_date_time_obj) #these print statements are used just to show that it's working
    print('end time',end_date_time_obj)
    print('min', min_altitude)
    print('max', max_altitude)
    print("No formatting erros with the input.")
    popdens(aoi,pop,flights,start_date_time_obj,end_date_time_obj,min_altitude,max_altitude,path)
    AirRisk(aoi, flights, start_date_time_obj, end_date_time_obj, min_altitude, max_altitude, path) 
    

if __name__ == '__main__':
    #Run the main function
    main()
