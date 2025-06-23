RandysRecipeCa = {
    "name": "Randy's Recipe Calcium",
    "description": "A recipe for a calcium solution based on Randy's method.",
    "SolutionPPM": 37000} # per liter
AquaForestCaPlusLiquid = {
    "name": "AquaForest Ca Plus Liquid",
    "description": "AquaForest Ca Plus Liquid is a concentrated calcium solution.",
    "SolutionPPM": 200000} # per liter

def calculate_dosage(targetPPMIncrease, waterVolumeL, SolutionPPM):
    #Calculate the dosage in milliliters needed to achieve a target PPM increase
    dosage_L = (targetPPMIncrease * waterVolumeL) / SolutionPPM
    dosage_mL = dosage_L * 1000  # Convert liters to milliliters
    return dosage_mL

TankParams = {
    "name": "My Tank",
    "Calcium": 420,
    "Alkalinity": 8.5,
    "Magnesium": 1300,
    "VolumeL": 100,  # Example volume in liters
    "Unit": "metric",  # or 'imperial'
    "GoalCalciumPPM": 450,  # Desired calcium level in PPM
    
    
}

def CheckParams(TankParams):
    if TankParams["Calcium"] < TankParams["GoalCalciumPPM"]:
        targetPPMIncrease = TankParams["GoalCalciumPPM"] - TankParams["Calcium"]
        waterVolumeL = TankParams["VolumeL"]
        SolutionPPM = RandysRecipeCa["SolutionPPM"]
        print(calculate_dosage(targetPPMIncrease=targetPPMIncrease, waterVolumeL=waterVolumeL, SolutionPPM=SolutionPPM), "mL")

CheckParams(TankParams)