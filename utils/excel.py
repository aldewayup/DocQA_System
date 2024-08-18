import pandas as pd

def save_to_excel(data, file_path):
    """
    Save data to an Excel file using pandas.

    This function takes a list of data and saves it to an Excel file
    with predefined column names.

    Args:
    data (list): A list of lists or tuples, where each inner list/tuple
                 contains values for Serial Number, Question, Answer,
                 Source, and Page Number.
    file_path (str): The path where the Excel file will be saved.

    Returns:
    None
    """
    try:
        # Create a pandas DataFrame from the data
        # Specify column names explicitly for clarity
        df = pd.DataFrame(data, columns=['Serial Number', 'Question', 'Answer', 'Source', 'Page Number'])
        
        # Save the DataFrame to an Excel file
        # index=False prevents writing row indices to the Excel file
        df.to_excel(file_path, index=False)
        
        # Print a success message
        print(f"Results successfully saved to {file_path}")
    except Exception as e:
        # If an error occurs, print an error message
        print(f"Error saving results to Excel: {e}")
