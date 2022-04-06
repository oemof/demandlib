import pandas as pd

def read_DWD_weather_file(weather_file_path):
    """Read and interpolate "DWD Testreferenzjahr" files."""
    # The comments in DWD files before the header are not commented out.
    # Thus we have to search for the line with the header information:
    header_row = None
    with open(weather_file_path, 'r') as rows:
        for number, row in enumerate(rows, 1):
            # The header is the row before the appearance of '***'
            if '***' in row:
                header_row = number - 1
                break

    # Plausibility check:
    if header_row is None:
        logger.error('Error: Header row not found in weather file. '
                     'Is the data type "DWD" correct? Exiting...')
        logger.error('File is: ' + weather_file_path)
        exit()

    # Read the file and store it in a DataFrame
    weather_data = pd.read_csv(
        weather_file_path,
        delim_whitespace=True,
        skiprows=header_row-1,
        index_col=['MM', 'DD', 'HH'],
        usecols=['MM', 'DD', 'HH', 'B', 'D', 't', 'WG', 'RF', 'WR', 'N', 'p'],
        comment='*',
        )

    # Rename the columns to the TRNSYS standard:
    weather_data.rename(columns={'B': 'IBEAM_H',
                                 'D': 'IDIFF_H',
                                 't': 'TAMB',
                                 'WG': 'WSPEED',
                                 'RF': 'RHUM',
                                 'WR': 'WDIR',
                                 'N': 'CCOVER',
                                 'p': 'PAMB'},
                        inplace=True)

    # Add an 'HOUR' column:
    weather_data['HOUR'] = range(1, 8761)

    # Make sure all columns are in the correct order
    # weather_data = weather_data.reindex(columns=['HOUR', 'IBEAM_H', 'IDIFF_H',
    #                                              'TAMB', 'WSPEED', 'RHUM',
    #                                              'WDIR', 'CCOVER', 'PAMB'])

    # print weather_data
    return weather_data
