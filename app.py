#from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Retrieve data from the POST request
    data = request.get_json()

    # Extract input values
    pa = float(data['pa'])
    # sand = float(data['sand'])
    silt = float(data['silt'])
    clay = float(data['clay'])
    slope_length = float(data['slopeLength'])
    slope_steepness = float(data['slopeSteepness'])
    crop_type = data['cropType']
    tillage_method = data['tillageMethod']
    practice_factor = data['practiceFactor']
    # land_use_factor = float(data['landUseFactor'])

    # Calculate R using the provided formula
    R = 81.5 + 0.3 * pa

    # Calculate K using the formula
    K = 0.002 + 0.003 * (silt + clay)

    # Calculate LS using the formula
    m = 0.5  # Empirical constant
    n = 1.0  # Empirical constant
    LS = (slope_length / 22.1) ** m * (abs(slope_steepness) / 0.0896) ** n

    crop_type_value = 0.0
    if crop_type == 'GrainCorn':
        crop_type_value = 0.40
    elif crop_type == 'SilageCornBeansCanola':
        crop_type_value = 0.50
    elif crop_type == 'Cereals':
        crop_type_value = 0.35
    elif crop_type == 'SeasonalHorticulturalCrops':
        crop_type_value = 0.50
    elif crop_type == 'FruitTrees':
        crop_type_value = 0.10
    elif crop_type == 'HayAndPasture':
        crop_type_value = 0.02

    tillage_method_value = 0.0
    if tillage_method == 'AutumnPlough':
        tillage_method_value = 1.0
    elif tillage_method == 'SpringPlough':
        tillage_method_value = 0.9
    elif tillage_method == 'MulchTillage':
        tillage_method_value = 0.6
    elif tillage_method == 'RidgeTillage':
        tillage_method_value = 0.35
    elif tillage_method == 'ZoneTillage':
        tillage_method_value = 0.25
    elif tillage_method == 'NoTill':
        tillage_method_value = 0.25
    
    practice_factor_value = 0.0
    if practice_factor == 'UpDown':
        practice_factor_value = 1.0
    elif practice_factor == 'CrossSlope':
        practice_factor_value = 0.75
    elif practice_factor == 'ContourFarming':
        practice_factor_value = 0.50
    elif practice_factor == 'StripCroppingCross':
        practice_factor_value = 0.37
    elif practice_factor == 'StripCroppingContour':
        practice_factor_value = 0.25

    # Calculate P using the provided formula
    #P = 0.1 * conservation_practice_factor + 0.2 * land_use_factor

    # Calculate soil loss (A) using the USLE formula
    C = crop_type_value * tillage_method_value
    A = R * K * LS * C * practice_factor_value

    # Prepare the response
    result = {
        'R': R,
        'K': K,
        'LS': LS,
        'C': C,
        'P': practice_factor_value,
        'soilLoss': A
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)