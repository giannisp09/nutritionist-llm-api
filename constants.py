"BMI: [user's BMI]"

nutrition_plan_prompt = """Given the following user details:

    Weight: 86
    Height: 185
    
    Target Goal: Muscle Gain
    Targtet nutrition info: protein: 210 grams, fat: 98 grams, carbs: 460 grams, sugar: <92 grams, calorie intake : 3449 calories
    Dietary Preferences: none

Generate a detailed 7-day nutrition plan (do not return less than 7 days) that aligns with their goal in the following JSON format. also return only the JSON response. Each day corresponds to a number (0 = Monday, 1 = Tuesday, etc.). Each meal should include its name, a short description, a recipe, calorie count, protein, carb, and fat breakdown, as well as a sequence number representing the order of meals for the day.

'''json
{
  days: [
    {
      day: 0,
      meals: [
        {
          name: "Oatmeal with Protein Powder",
          recipe: "",
          description: "High-protein oatmeal breakfast.",
          calories: 600,
          proteins: 30,
          carbs: 60,
          fats: 15,
          sequence: 1,
          day: "mon"
        },
        {
          name: "Chicken Quinoa Salad",
          recipe: "Combine grilled chicken breast, cooked quinoa, mixed greens, avocado, cucumber, and a vinaigrette dressing.",
          description: "Light and nutritious salad for lunch.",
          calories: 700,
          proteins: 40,
          carbs: 70,
          fats: 20,
          sequence: 2,
          day: "mon"
        },
        {
          name: "Protein Shake",
          recipe: "Blend a scoop of protein powder with almond milk, a banana, and a tablespoon of peanut butter.",
          description: "Post-workout protein shake.",
          calories: 500,
          proteins: 35,
          carbs: 40,
          fats: 15,
          sequence: 3,
          day: "mon"
        },
        {
          name: "Steak with Sweet Potatoes",
          recipe: "Grill a lean steak and serve with baked sweet potatoes and steamed broccoli.",
          description: "Hearty dinner for muscle repair.",
          calories: 800,
          proteins: 60,
          carbs: 60,
          fats: 25,
          sequence: 4,
          day: "mon"
        },
        {
          name: "Greek Yogurt with Nuts",
          recipe: "Mix Greek yogurt with a handful of mixed nuts and a drizzle of honey.",
          description: "Protein-rich bedtime snack.",
          calories: 600,
          proteins: 25,
          carbs: 30,
          fats: 35,
          sequence: 5,
          day: "mon"
        }
      ]
    },
    {
      day: 1,
      meals: [
        {
          name: "Meal name",
          recipe: "Meal recipe",
          description: "Meal description",
          calories: 0,
          proteins: 0,
          carbs: 0,
          fats: 0,
          sequence: 1,
          day: "tue"
        }
        // Continue for day 1 and the rest of the week
      ]
    }
  ]
}'''

Make sure each day has 4 to 5 meals in this format, with proper distribution of macronutrients and variety, considering the user's dietary preferences and goals."""


# constants.py

NUTRITION_PLAN_PROMPT = """Given the following user details:

    Weight: {weight}
    Height: {height}
    
    Target Goal: {target_goal}
    Target nutrition info: protein: {protein} grams, fat: {fat} grams, carbs: {carbs} grams, sugar: < {sugar} grams, calorie intake: {calories} calories
    Dietary Preferences: {dietary_preferences}

Generate a detailed 7-day nutrition plan (do not return less than 7 days) that aligns with their goal in the following JSON format. also return only the JSON response. Each day corresponds to a number (0 = Monday, 1 = Tuesday, etc.). Each meal should include its name, a short description, a recipe, calorie count, protein, carb, and fat breakdown, as well as a sequence number representing the order of meals for the day.

'''json
{{
  "days": [
    {{
      "day": 0,
      "meals": [
        {{
          "name": "Oatmeal with Protein Powder",
          "recipe": "",
          "description": "High-protein oatmeal breakfast.",
          "calories": 600,
          "proteins": 30,
          "carbs": 60,
          "fats": 15,
          "sequence": 1,
          "day": "mon"
        }},
        {{
          "name": "Chicken Quinoa Salad",
          "recipe": "Combine grilled chicken breast, cooked quinoa, mixed greens, avocado, cucumber, and a vinaigrette dressing.",
          "description": "Light and nutritious salad for lunch.",
          "calories": 700,
          "proteins": 40,
          "carbs": 70,
          "fats": 20,
          "sequence": 2,
          "day": "mon"
        }}
        // Continue for all meals and all days
      ]
    }}
  ]
}}
'''

Make sure each day has enough meals to match calorie intake in this format, with proper distribution of macronutrients and variety, considering the user's dietary preferences and goals. Do not output plan that does not meet user target nutrion metrics (protein, fat , carbs and calories)"""
