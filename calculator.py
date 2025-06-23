def inchToCm(inches):
    return inches * 2.54

def cmToInch(cm):
    return cm / 2.54

def inchToFeet(inches):
    return inches / 12

def WaterVolumeCalculatorInches(L1, W1, H1): # inches
    
    length = inchToFeet(L1) # Convert to feet
    width = inchToFeet(W1) # Convert to feet
    height = inchToFeet(H1) # Convert to feet
    CubicFeet = length * width * height 
    # Calculate cubic feet
    return CubicFeet*7.48 # Convert to gallons (1 cubic foot = 7.48 gallons)
    
def WaterVolumeCalculatorCm(L1, W1, H1): # centimeters
    L2 = cmToInch(L1) # Convert to inches
    W2 = cmToInch(W1) # Convert to inches   
    H2 = cmToInch(H1) # Convert to inches
    Gal = WaterVolumeCalculatorInches(L2, W2, H2) # Use the inches function
    return Gal*3.785411784 # Convert to liters (1 gallon = 3.785411784 liters)
    
def main():
    print(f"{WaterVolumeCalculatorInches(24, 12, 16):.2f} Gallons") # Example usage
    print(f"{WaterVolumeCalculatorCm(60, 30, 40):.2f} Liters") # Example usage
main()