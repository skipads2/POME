def get_dynamic_price_index(base_index, cpi_multiplier):
    """Adjusts the base price index using a CPI inflation multiplier."""
    return base_index * cpi_multiplier
