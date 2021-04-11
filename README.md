# 09repo for SORA Group. 
For any questions or concerns please email oliviahobbs@cmail.carleton.ca or alexandramull25@gmail.com

To run this code with your own inputs you will need your own Ottawa_CSV_Short.csv that is in the same format as the sample provided with the flight data. You will also need to change your parameters in args.txt being sure to match the formatting exactly. The aoi1.kml is where you substitue in your own area of interest for the RPAS flight path, this file must be in KML format. Make sure that all files are in the same working folder which you will notate in the command line when you call this program ( SORAcode.py)

SORAcode.py - is the python file which you call to run our program from command line 
License - is the file with information regarding the license and usage permissions for our code we utilized the MIT license 
AirRisk.txt - is a sample output that comes from the Airrisk function that is in SORAcode.py, it gives the amount of flights in the area of interest and km^2 of area of interest
Density.txt - is a sample output from the results from the Ground risk function from SORAcode.py, it gives the census tract ID(CTUID) and the population density for it for each flight
OttawaPopDens.cpg - this file is needed for OttawaPopDens.shp, they need to be in the same folder for the code to work
OttawaPopDens.dbf - this file is needed for OttawaPopDens.shp, they need to be in the same folder for the code to work
OttawaPopDens.prj- this file is needed for OttawaPopDens.shp, they need to be in the same folder for the code to work
OttawaPopDens.shp- this file contains the information for the census data of Ottawa, it is used for the ground risk function 
OttawaPopDens.shx- this file is needed for OttawaPopDens.shp, they need to be in the same folder for the code to work
Ottawa_CSV_Short.csv - this file is the sample input for the filter flights function from SORAcode.py 
aoi1.kml - This file is the sample input area of interest used for SORAcode.py, it is important that this file is KML formatted 
args.txt - this file is the sample input for the main function in SORAcode.py, the formatting and spacing is very important to run this program correctly 
