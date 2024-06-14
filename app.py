from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    return bmr

def calculate_keto_macros(calories):
    protein_ratio = 0.25
    carb_ratio = 0.05
    fat_ratio = 0.70

    protein_calories = calories * protein_ratio
    carb_calories = calories * carb_ratio
    fat_calories = calories * fat_ratio

    protein_grams = protein_calories / 4
    carb_grams = carb_calories / 4
    fat_grams = fat_calories / 9

    return protein_grams, carb_grams, fat_grams

def suggest_keto_diet(weight, height, age, gender):
    activity_multiplier = 1.2

    bmr = calculate_bmr(weight, height, age, gender)
    daily_calories = bmr * activity_multiplier

    protein, carbs, fats = calculate_keto_macros(daily_calories)

    return {
        'Daily Calories': daily_calories,
        'Protein (grams)': protein,
        'Carbs (grams)': carbs,
        'Fats (grams)': fats
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        
        diet_suggestion = suggest_keto_diet(weight, height, age, gender)

        return render_template('index.html', diet=diet_suggestion)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
