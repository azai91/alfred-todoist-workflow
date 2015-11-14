"""
Common utility library
"""

def validate_coordinates(coordinates):
    """
    Validates that user inputted coordinates following format: float,float

    Args:
        coordinates: string, User inputted string to validate

    Returns:
        Boolean indicating whether or not the input string is properly formatted

    """

    if ';' in coordinates:
        coordinates = coordinates.split(';')
        long = coordinates[0]
        lat = coordinates[1] if len(coordinates[1]) else 0
    else:
        long = coordinates
        lat = 0

    try:
        float(long)
        float(lat)
        return True
    except:
        return False