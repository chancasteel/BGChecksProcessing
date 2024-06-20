import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def get_gender_code(gender: str) -> str:
    """
    Get the gender code based on the provided gender string.
    
    Args:
        gender (str): The gender string.
        
    Returns:
        str: 'M' for male, 'F' for female, or 'E' for error/unknown.
    """
    gender_code = gender[0] if gender[0] in {'M', 'F'} else 'E'
    logger.debug(f"Processed gender: {gender} -> {gender_code}")
    return gender_code

def get_race_code(race: str) -> str:
    """
    Get the race code based on the provided race string.
    
    Args:
        race (str): The race string.
        
    Returns:
        str: 'W' for white, 'B' for black, 'W' for Hispanic (as white), or 'U' for unknown.
    """
    if race[0] in {'W', 'B'}:
        race_code = race[0]
    elif race[0] == 'H':
        race_code = 'W'
    else:
        race_code = 'U'
    logger.debug(f"Processed race: {race} -> {race_code}")
    return race_code

def format_name(name: str) -> str:
    """
    Format the name by removing certain characters and reordering.
    
    Args:
        name (str): The full name in "Last, First" format.
        
    Returns:
        str: Formatted name in "LAST,FIRST" format padded to 30 characters.
    """
    name = name.translate(str.maketrans("", "", "-'"))
    last_name, first_name = name.split(',', 1)
    last_name = last_name.translate({ord(i): None for i in ' ,.'})
    first_name = first_name.split(' ')[1]
    formatted_name = (last_name + ',' + first_name).ljust(30)
    logger.debug(f"Formatted name: {name} -> {formatted_name}")
    return formatted_name

def process_row(row: pd.Series) -> dict:
    """
    Process a DataFrame row and return a dictionary with formatted data.
    
    Args:
        row (pd.Series): A row of the DataFrame.
        
    Returns:
        dict: A dictionary with formatted data for each column.
    """
    processed_data = {
        'Name': format_name(row['Applicant Full Name']),
        'Gender': get_gender_code(row['Gender']).ljust(1),
        'LocalRace': get_race_code(row['Local Race']).ljust(1),
        'BirthDate': row['Date of Birth'].strftime('%Y%m%d').ljust(8),
        'DPSInfo': '3455'.ljust(4),
        'Blank': ''.ljust(9),
        'SSN': row['Social Security Number'].replace('-', '').ljust(9),
        'Blank2': ''.ljust(20),
    }
    logger.debug(f"Processed row:\n{row} -> {processed_data}")
    return processed_data

if __name__ == "__main__":
    # Read the CSV file
    file_path = r'import.csv'
    logger.info(f"Reading CSV file from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Read {len(df)} rows from {file_path}")
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])
    
    # Vectorized processing
    logger.info("Processing rows...")
    export_df = df.apply(process_row, axis=1, result_type='expand')
    export_df.drop_duplicates(subset='SSN', inplace=True)
    export_df.sort_values(by=['Name'], ascending=True, inplace=True)
    
    concatenated_data = export_df.apply(lambda row: ''.join(map(str, row)), axis=1)
        
    # Write to file
    output_file = r'export.txt'
    logger.info(f"Writing processed data to {output_file}")
    with open(output_file, 'w') as f:
        f.write('\n'.join(concatenated_data))
    logger.info(f"Wrote {len(concatenated_data)} lines to {output_file}")

