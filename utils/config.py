import json

def load_config(config_file='config.json'):
    """
    Load configuration from a JSON file.

    This function attempts to read and parse a JSON configuration file.
    If the file is not found or cannot be parsed, it returns an empty dictionary.

    Args:
    config_file (str): The path to the JSON configuration file. Defaults to 'config.json'.

    Returns:
    dict: A dictionary containing the configuration data if successful, otherwise an empty dictionary.
    """
    try:
        # Attempt to open and read the config file
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Handle the case where the config file doesn't exist
        print(f"Config file '{config_file}' not found.")
        return {}
    except json.JSONDecodeError:
        # Handle the case where the JSON in the config file is invalid
        print(f"Error decoding JSON from '{config_file}'.")
        return {}

def setup_tesseract(config):
    """
    Set up the Tesseract OCR engine.

    This function configures the Tesseract OCR engine by setting its executable path
    based on the provided configuration.

    Args:
    config (dict): A dictionary containing configuration settings.
                   Expected to have a 'tesseract_path' key with the path to the Tesseract executable.

    Returns:
    None
    """
    import pytesseract
    
    # Set the Tesseract executable path from the config
    # If 'tesseract_path' is not in config, this will implicitly use the default path
    pytesseract.pytesseract.tesseract_cmd = config.get('tesseract_path')
