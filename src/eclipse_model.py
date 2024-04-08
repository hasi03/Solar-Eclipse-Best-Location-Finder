import numpy as np

def eclipse_model(latitudes, longitudes):
    """
    Predict the longitude of an eclipse given the latitude and coefficients of the polynomial curve.
    """
    coefficients = np.polyfit(latitudes, longitudes, deg=2)

    return coefficients

