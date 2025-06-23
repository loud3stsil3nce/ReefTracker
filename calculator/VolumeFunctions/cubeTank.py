from rectangleTank import inchToCm, cmToInch, inchToFeet

def CubeWaterVolumeCalculator(L, unit="metric"):
    if unit == 'metric':
        # cm to m³: divide by 100 to get meters, then cubic meters × 1000 = liters
        volume_m3 = (L / 100) ** 3
        return volume_m3 * 1000  # Liters
    else:
        # Inches to feet
        length = inchToFeet(L)
        CubicFeet = length ** 3
        return CubicFeet * 7.48  # Gallons
    
class CubeTank:
    def __init__(self, length, filledHeight = 0, unit='imperial'):
        self.length = length
        self.filledHeight = filledHeight
        unit = unit.lower()
        if unit == 'metric':
            
            self.metricVolume = CubeWaterVolumeCalculator(length, unit='metric')
            self.filledMetricVolume = CubeWaterVolumeCalculator(filledHeight, unit='metric')
            length_inch = cmToInch(length)
           
            filledHeight_inch = cmToInch(filledHeight)
            self.imperialVolume = CubeWaterVolumeCalculator(length_inch, unit='imperial')
            self.filledImperialVolume = CubeWaterVolumeCalculator(filledHeight_inch, unit='imperial')
        else:
            self.imperialVolume = CubeWaterVolumeCalculator(length, unit='imperial')
            self.filledImperialVolume = CubeWaterVolumeCalculator(filledHeight, unit='imperial')
            
            length_cm = inchToCm(length)
            
            filledHeight_cm = inchToCm(filledHeight)
            self.metricVolume = CubeWaterVolumeCalculator(length_cm, unit='metric')
            self.filledMetricVolume = CubeWaterVolumeCalculator(filledHeight_cm, unit='metric')
            
    
def main():
  
    tank = CubeTank(60, filledHeight=0, unit='metric') # Example usage
    print(f"Tank Volume in Imperial: {tank.imperialVolume:.2f} Gallons") 
    print(f"Tank Volume in Metric: {tank.metricVolume:.2f} Liters")                              
main()