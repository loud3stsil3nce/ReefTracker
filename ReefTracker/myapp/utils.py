def inchToCm(inches):
    return inches * 2.54

def cmToInch(cm):
    return cm / 2.54

def inchToFeet(inches):
    return inches / 12


def RectangleWaterVolumeCalculator(L1, W1, H1, unit="metric"):
    if unit == 'metric':
        # cm to m³: divide by 100 to get meters, then cubic meters × 1000 = liters
        volume_m3 = (L1 / 100) * (W1 / 100) * (H1 / 100)
        return volume_m3 * 1000  # Liters
    else:
        # Inches to feet
        length = inchToFeet(L1)
        width = inchToFeet(W1)
        height = inchToFeet(H1)
        CubicFeet = length * width * height
        return CubicFeet * 7.48  # Gallons
        