from datetime import datetime, timedelta

# Constants
MJD_2008_JAN_01 = 54466  # MJD for 2008-01-01 00:00:00
SECONDS_IN_DAY = 86400  # Number of seconds in a day

# Function to convert MJD to UTC seconds relative to 2008-01-01
def mjd_to_utc_seconds(mjd):
    delta_mjd = mjd - MJD_2008_JAN_01
    utc_seconds = delta_mjd * SECONDS_IN_DAY
    return utc_seconds

# Function to convert UTC seconds (relative to 2008-01-01) to MJD
def utc_seconds_to_mjd(utc_seconds):
    delta_days = utc_seconds / SECONDS_IN_DAY
    mjd = MJD_2008_JAN_01 + delta_days
    return mjd

# Function to convert MJD to Gregorian date
def mjd_to_gregorian(mjd):
    jd = mjd + 2400000.5  # Convert MJD to Julian Date
    gregorian_date = datetime(1858, 11, 17) + timedelta(days=(jd - 2400000.5))
    return gregorian_date

# Function to convert Gregorian date to MJD
def gregorian_to_mjd(gregorian_date):
    base_date = datetime(1858, 11, 17)
    delta_days = (gregorian_date - base_date).days + (gregorian_date - base_date).seconds / SECONDS_IN_DAY
    mjd = delta_days
    return mjd

# Example conversions
example_mjd = 57715.000000295
utc_seconds = mjd_to_utc_seconds(example_mjd)
gregorian_date = mjd_to_gregorian(example_mjd)

# Display the conversion results
example_utc_seconds = 2.802251030000003e+008
converted_mjd = utc_seconds_to_mjd(example_utc_seconds)
converted_gregorian_date = mjd_to_gregorian(converted_mjd)

example_gregorian_date = datetime(2017, 11, 17, 3, 57, 46)
converted_mjd_from_date = gregorian_to_mjd(example_gregorian_date)

# Display the results in an organized manner
results = {
    "Example MJD": example_mjd,
    "UTC Seconds from MJD": utc_seconds,
    "Gregorian Date from MJD": gregorian_date,
    "Converted MJD from UTC Seconds": converted_mjd,
    "Converted Gregorian Date": converted_gregorian_date,
    "Converted MJD from Gregorian Date": converted_mjd_from_date,
}

print(results)