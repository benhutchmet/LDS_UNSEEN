"""
download_ERA5_jasmin.py
========================

This script sends a request to the CDS API to download the ERA5 data for a specific domain in monthly chunks at the hourly resolution.

Usage:
======

    $ python download_ERA5_jasmin.py --year <year> --start_month <start_month> --end_month <end_month>

Arguments:
==========

    --year : int : year of the data to download
    --start_month : int : month of the data to download (1-12)
    --end_month : int : month of the data to download (1-12)
    
Returns:
========

    netcdf files : .nc : netcdf files saved to the /gws/nopw/j04/canari/users/benhutch/ERA5 folder.

Author:
=======

    Ben W. Hutchins, University of Reading, 2025
"""

# Local imports
import os
import cdsapi
import argparse

# Define a function to check the files which exist
def check_files_exist():
    """
    Check the files which already exist in the target directory.
    """

    # Set up the target directory
    target_dir = '/gws/nopw/j04/canari/users/benhutch/ERA5/SOTCES'

    # Check if the target directory exists
    if not os.path.exists(target_dir):
        # make the directory
        os.makedirs(target_dir)

    # Set up the years to check for
    years = list(range(2024, 2025 + 1))  # Adjust the range as needed

    # Set up the months to check for
    months = list(range(1,13))

    # Set up a list for the missing files
    missing_files = []

    # Loop over the years and months
    for year in years:
        for month in months:
            # if year is 2025 and month is 3 or greater, skip
            if year == 2025 and month >= 3:
                continue

            # Set up the file name
            file_name = f'ERA5_EU_SOTCES_{year}_{str(month).zfill(2)}.nc'

            # Check if the file exists
            if os.path.exists(target_dir + file_name):
                print(f'File exists for year: {year} and month: {month}')
            else:
                print(f'File does not exist for year: {year} and month: {month}')
                missing_files.append(file_name)

    return missing_files

# define the function to download the ERA5 data
def download_ERA5_to_jasmin(
    year: int,
    month: int,
) -> None:
    """
    Download ERA5 data for a given year and month to be used in jasmin.
    
    Parameters
    ----------
    
    year: int
        The year to download data for.
    
    month: int
        The month to download data for.

    Returns
    -------

    None

    """

    m = str(month).zfill(2) # make sure it is 01, 02 etc

    if m in ['04','06','09','11']:
        days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
    elif m in ['01','03','05','07','08','10','12']:
        days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    else:
        if year in [1940,1944,1948,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016,2020,2024]:
            days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']
        else:
            days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']

    #print(str(YEAR))
    #print(str(MONTH))
    y = str(year)

    target = '/gws/nopw/j04/canari/users/benhutch/ERA5/SOTCES/ERA5_EU_SOTCES_' + y + '_' + m + '.nc'

    # if the file already exists, skip
    if os.path.exists(target):
        print(f'File already exists: {target}')
        return None

    client = cdsapi.Client()

    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_temperature",
            "mean_sea_level_pressure",
            "total_precipitation",
            "100m_u_component_of_wind",
            "100m_v_component_of_wind",
            "10m_wind_gust_since_previous_post_processing",
            "surface_net_solar_radiation"
        ],
        "year": [y],
        "month": [m],
        "day": days,
        "time": [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": [72, -40, 34, 35]
    }
    
    client.retrieve(dataset, request, target)
    
    return None

# define the main function
def main():
    
    # set up the argument parser
    parser = argparse.ArgumentParser(description='Download ERA5 data for RACC')
    year = parser.add_argument('--year', type=int, help='Year to download data for')
    start_month = parser.add_argument('--start_month', type=int, help='Month to download data for (1-12)')
    end_month = parser.add_argument('--end_month', type=int, help='End month to download data for (1-12)')

    # parse the arguments
    args = parser.parse_args()

    # Print the arguments
    print('=====================================')
    print('Downloading ERA5 data for the following arguments:')
    print(f'Year: {args.year}')
    print(f'Start Month: {args.start_month}')
    print(f'End Month: {args.end_month}')
    print('=====================================')

    missing_files = check_files_exist()

    # Print the missing files
    print('=====================================')
    print('Missing files:')
    print(missing_files)
    print('=====================================')

    # return None

    # loop over the months
    for month in range(args.start_month, args.end_month + 1):
        print(f'Downloading data for year: {args.year}, month: {month}')
        # Call the download function
        download_ERA5_to_jasmin(
            year=args.year,
            month=month,
        )

    return None

# run the main function
if __name__ == '__main__':
    main()