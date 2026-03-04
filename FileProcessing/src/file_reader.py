from exceptions import FileProcessingError, InvalidDataError, MissingFieldError

def parse_line(line: str) -> dict:
    """Parse the CSV line and return a dictionary Record of the fields"""
    data_split: list[str] = line.strip().split(",")
                
    data: dict = {
        "date": data_split[0],
        "store_id": data_split[1],
        "product": data_split[2],
        "quantity": data_split[3],
        "price": data_split[4]
    }
    return data

def read_csv_file(filepath: str) -> list[dict]:
    """
    Read a CSV file and return a list of dictionaries.
    
    Should handle:
    - FileNotFoundError
    - UnicodeDecodeError (try utf-8, then latin-1)
    - Empty files
    
    Returns: List of dictionaries (one per row)
    Raises: FileProcessingError with descriptive message
    """

    # date,store_id,product,quantity,price
    records: list[dict] = list()

    try:
        # attempt to read file in utf-8 and append each record
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                # skip column heading line
                if i == 0:
                    continue
                records.append(parse_line(line))

    except UnicodeDecodeError as e:
        # print(f"Error using Unicode encoding to read file.")

        # attempt to read file with latin-1 encoding instead
        with open(filepath, "r", encoding="latin-1") as f:
            for i, line in enumerate(f):
                # skip column heading line
                if i == 0:
                    continue
                records.append(parse_line(line))

    except FileNotFoundError as e:
        # print(f"Couldn't find file.\n{e}")
        raise FileProcessingError()


    return records
    

