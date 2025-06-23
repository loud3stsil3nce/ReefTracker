TankVolumeImperial = None
TankVolumeMetric = None

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
    
class RectangleTank:
    def __init__(self, length, width, height, filledHeight = 0, unit='imperial'):
        self.length = length
        self.width = width
        self.height = height
        self.filledHeight = filledHeight
        unit = unit.lower()
        if unit == 'metric':
            
            self.metricVolume = RectangleWaterVolumeCalculator(length, width, height, unit='metric')
            self.filledMetricVolume = RectangleWaterVolumeCalculator(length, width, filledHeight, unit='metric')
            length_inch = cmToInch(length)
            width_inch = cmToInch(width)
            height_inch = cmToInch(height)
            filledHeight_inch = cmToInch(filledHeight)
            self.imperialVolume = RectangleWaterVolumeCalculator(length_inch, width_inch, height_inch, unit='imperial')
            self.filledImperialVolume = RectangleWaterVolumeCalculator(length_inch, width_inch, filledHeight_inch, unit='imperial')
        else:
            self.imperialVolume = RectangleWaterVolumeCalculator(length, width, height, unit='imperial')
            self.filledImperialVolume = RectangleWaterVolumeCalculator(length, width, filledHeight, unit='imperial')
            
            length_cm = inchToCm(length)
            width_cm = inchToCm(width)
            height_cm = inchToCm(height)
            filledHeight_cm = inchToCm(filledHeight)
            self.metricVolume = RectangleWaterVolumeCalculator(length_cm, width_cm, height_cm, unit='metric')
            self.filledMetricVolume = RectangleWaterVolumeCalculator(length_cm, width_cm, filledHeight_cm, unit='metric')

        
        
            
    
    
        
        
        
        
        
        
