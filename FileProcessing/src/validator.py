from exceptions import FileProcessingError, InvalidDataError, MissingFieldError


def validate_sales_record(record: dict, line_number: int) -> dict:
    """
    Validate a single sales record.
    
    Required fields: date, store_id, product, quantity, price
    Validation rules:
    - date must be in YYYY-MM-DD format
    - quantity must be a positive integer
    - price must be a positive number
    
    Returns: Validated record with converted types
    Raises: InvalidDataError or MissingFieldError
    """
    # date,store_id,product,quantity,price
    validated_record: dict = {}
    for field, value in record.items():

        # handle lack of value
        if not value:
            raise MissingFieldError(f"Line {line_number}: Missing value for {field} field.")
        
        # validate quantity field
        if field == "quantity":
            try:
                validated_quantity: int = int(value)

                if validated_quantity < 0:
                    raise InvalidDataError(f"Line {line_number}: {field} must be a positive number.")
            
            except ValueError as e:
                # print(f"{field} must be a number.\n{e}")
                raise InvalidDataError(f"Line {line_number}: Unable to convert {field} to int.")
            
            # use converted value in validated record 
            validated_record[field] = validated_quantity

        # validate price field
        elif field == "price":
            try:
                validated_price: float = float(value)

                if validated_price < 0:
                    raise InvalidDataError(f"Line {line_number}: {field} must be a positive number.")
            
            except TypeError as e:
                # print(f"{field} must be a number.\n{e}")
                raise InvalidDataError(f"Line {line_number}: Unable to convert {field} to float.")
            
            # use converted value in validated record 
            validated_record[field] = validated_price

        elif field == "date":
            split_date: list[str] = value.split("-")

            
            if len(split_date) == 3:
                # make sure each part of the date are solely numbers
                if all([x.isdigit() for x in split_date]):

                    # if make sure year, month, day have 4, 2 and 2 numbers respectively
                    if list(map(len, split_date)) != [4, 2, 2]:
                        raise InvalidDataError(f"Line {line_number}: Date ({value}) must be in YYYY-MM-DD format.")
                
                # if year, month or day isn't represented by numbers it's invalid formatting
                else:
                    raise InvalidDataError(f"Line {line_number}: Date must be in YYYY-MM-DD format.")
            
            # if there isn't a year, month and day field separated by hyphens it's invalid formatting
            else:  
                raise InvalidDataError(f"Line {line_number}: Date must be in YYYY-MM-DD format.")
        
            # no formatting issues, add record as is
            validated_record[field] = value

        # other fields remain in string form, can't be empty to get here
        else:
            validated_record[field] = value
            
    return validated_record
        
    

def validate_all_records(records):
    """
    Validate all records, collecting errors instead of stopping.
    
    Returns: Tuple of (valid_records, error_list)
    """
    valid_records: list[dict] = []
    error_list: list[str] = []
    for i, record in enumerate(records):
        try:
            validated_record: dict = validate_sales_record(record, i+2) # i + 2 to account for 0 indexing & csv headers row
            valid_records.append(validated_record)
        
        except InvalidDataError as e:
            error_list.append(str(e))

        except MissingFieldError as e:
            error_list.append(str(e))

    return (valid_records, error_list)