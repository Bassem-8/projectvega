from flask import Flask, render_template, request, redirect, url_for
import math
import random

app = Flask(__name__)

# Carbon footprint data (kg CO2 per week, generated the data from ChatGPT)
footprint_data = {
    'transport': {
        'walk': 0,
        'public': 20,
        'car_gas': 120,
        'car_electric': 40,
        'motorcycle': 60
    },
    'diet': {
        'vegan': 4,
        'vegetarian': 6,
        'occasional_meat': 20,
        'frequent_meat': 40,
        'heavy_meat': 60
    },
    'energy': {
        'renewable': 50,
        'efficient': 100,
        'average': 200,
        'high': 400
    }
}

# Eco tips
eco_tips = [
    "Unplug devices when not in use to save energy.",
    "Air dry clothes instead of using a dryer.",
    "Plant native trees in your community.",
    "Reduce air travel when possible.",
    "Buy second-hand items to reduce manufacturing demand."
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    # Get user inputs
    transport = request.form.get("transport")
    diet = request.form.get("diet")
    energy = request.form.get("energy")

    if not transport or not diet or not energy:
        return redirect(url_for("index"))

    # Calculate footprint
    weekly_footprint = (
        footprint_data['transport'][transport] +
        footprint_data['diet'][diet] +
        footprint_data['energy'][energy]
    )
    yearly_footprint = weekly_footprint * 52
    trees_needed = math.ceil(yearly_footprint / 21)

    # Determine biggest impact area
    impacts = {
        'transport': footprint_data['transport'][transport],
        'diet': footprint_data['diet'][diet],
        'energy': footprint_data['energy'][energy]
    }
    biggest_impact = max(impacts, key=impacts.get)

    # Generate suggestions based on biggest impact
    suggestions = []
    if biggest_impact == 'transport':
        suggestions = [
            "Use public transport more often",
            "Try carpooling with colleagues",
            "Consider switching to an electric vehicle",
            "Walk or bike for short distances"
        ]
    elif biggest_impact == 'diet':
        suggestions = [
            "Reduce meat consumption",
            "Choose local and seasonal produce",
            "Minimize food waste",
            "Try plant-based alternatives"
        ]
    else:
        suggestions = [
            "Switch to renewable energy sources",
            "Improve home insulation",
            "Use energy-efficient appliances",
            "Lower your thermostat by 1-2 degrees"
        ]

    # Random eco tip
    random_tip = random.choice(eco_tips)

    return render_template("results.html",
        weekly=round(weekly_footprint, 1),
        yearly=round(yearly_footprint, 1),
        trees=trees_needed,
        biggest=biggest_impact,
        suggestions=suggestions,
        tip=random_tip
    )

