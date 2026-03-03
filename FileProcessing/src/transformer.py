def calculate_totals(records: list[dict]) -> list[dict]:
    """
    Calculate line totals (quantity * price) for each record.
    Returns: Records with added 'total' field
    """
    updated_records: list[dict] = []
    for record in records:
        record["total"] = record["quantity"] * record["price"]
        updated_records.append(record)

    return updated_records

    


def aggregate_by_store(records: list[dict]) -> dict:
    """
    Aggregate sales by store_id.
    Returns: Dict mapping store_id to total sales
    """

    store_aggregate: dict = {}
    for record in records:
        store_id: str = record["store_id"]

        # if store already has sales saved, add to current value
        if store_id in store_aggregate:
            store_aggregate[store_id] += record["total"]

        # initialize store_id's total sales
        else:
            store_aggregate[store_id] = record["total"]

    return store_aggregate


def aggregate_by_product(records: list[dict]) -> dict:
    """
    Aggregate sales by product.
    Returns: Dict mapping product to total quantity sold
    """
    
    product_aggregate: dict = {}
    for record in records:
        product, quantity = record["product"], record["quantity"]
        # if product has existing quantity, add to it (not overwriting)
        if product in product_aggregate:
            product_aggregate[product] += quantity

        else:
            # initialize product quantity
            product_aggregate[product] = quantity

    return product_aggregate