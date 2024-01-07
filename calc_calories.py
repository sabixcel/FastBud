#Function to calculate calories burned during fasting (using Basal metabolic rate); for resting day
def calculate_calories_burned(age, gender, weight_kg, height_cm, elapsed_time_hours):
    # Mifflin-St Jeor Equation constants
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Use 'male' or 'female'.")
    bmr = bmr/24 # Because bmr is calculated for a whole day
    
    calories_burned = bmr * elapsed_time_hours # Calculate calories burned during fasting

    return calories_burned

#Function to calculate the calories needed every day in function with the activity level
def calculate_calories_burned_with_activity(age, gender, weight_kg, height_cm, elapsed_time_hours, activity):
    # Sedentary: If you get minimal or no exercise, multiply your BMR by 1.2.
    # Lightly active: If you exercise lightly one to three days a week, multiply your BMR by 1.375.
    # Moderately active: If you exercise moderately three to five days a week, multiply your BMR by 1.55.
    # Very active: If you engage in hard exercise six to seven days a week, multiply your BMR by 1.725.
    # Extra active: If you engage in very hard exercise six to seven days a week or have a physical job, multiply your BMR by 1.9.
    
    activity_options = {
        "Sedentary": {"level": 1, "factor": 1.2},
        "Lightly active": {"level": 2, "factor": 1.375},
        "Moderately active": {"level": 3, "factor": 1.55},
        "Very active": {"level": 4, "factor": 1.725},
        "Extra active": {"level": 5, "factor": 1.9}
    }
    selected_activity = activity_options.get(activity)
    #activity_level_number = selected_activity["level"]
    multiplying_factor = selected_activity["factor"]

    bmr = calculate_calories_burned(age, gender, weight_kg, height_cm, elapsed_time_hours)
    calories_nedeed = bmr * multiplying_factor
    calories_nedeed = "{:.2f}".format(calories_nedeed)
    return calories_nedeed

#Function to calculate calories needed for a daily basis in resting or activity mode
def calculate_calories_needed(age, gender, weight_kg, height_cm, activity_level):
    calories_burned_resting = calculate_calories_burned(age, gender, weight_kg, height_cm, 24) #for a 24 hours
    calories_burned_active = calculate_calories_burned_with_activity(age, gender, weight_kg, height_cm, 24, activity_level)

    # Format as strings with two decimal places
    #calories_burned_resting = "{:.2f}".format(calories_burned_resting)
    #calories_burned_active = "{:.2f}".format(calories_burned_active)

    return calories_burned_resting, calories_burned_active

def calculate_bmi(weight_kg, height_cm):
    #BMI	        Weight Status
    #Below 18.5	    Underweight
    #18.5 – 24.9	Healthy Weight
    #25.0 – 29.9	Overweight
    #30.0 and Above Obesity
    height_m = height_cm/100
    bmi = weight_kg/(pow(height_m,2))
    bmi = "{:.1f}".format(bmi)
    bmi_float = float(bmi)
    status = 'Unknown'

    if bmi_float < 18.5:
        status = 'Underweight'
    elif bmi_float >= 18.5 and bmi_float <= 24.9:
        status = 'Healthy Weight'
    elif bmi_float >= 25 and bmi_float <= 29.9:
        status = 'Overweight'
    elif bmi_float >= 30:
        status = 'Obesity'

    #bmi = "{:.1f}".format(bmi)

    return status, bmi