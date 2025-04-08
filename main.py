import fastapi
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from starlette.requests import Request
from constants import *
import prometheus_client
from openai import OpenAI
import os
import uvicorn
import base64


from dotenv import load_dotenv

load_dotenv()


# # os.environ["OPENAI_API_KEY"] = 
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Initialize OpenAI client with your API key
client = OpenAI()


# Initialize FastAPI client
app = FastAPI()


REQUESTS = prometheus_client.Counter(
    'requests', 'Application Request Count',
    ['endpoint']
)

# Create class with pydantic BaseModel
class TranslationRequest(BaseModel):
    input_str: str


# Define the user input model
class UserDetails(BaseModel):
    weight: float
    height: float
    target_goal: str
    target_nutrition: dict
    dietary_preferences: str

def translate_text(input_str):
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an expert translator who translates text from english to french and only return translated text",
            },
            {"role": "user", "content": input_str},
        ],
    )


    return completion.choices[0].message.content


def gen_nutri_plan(gen_nutri_prompt):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant specialist in fitness, in both exercising and nutrition. You will have to help users with the nutrition and workout plans to achive their goals efficiently. "},
        {
            "role": "user",
            "content": gen_nutri_prompt #"Write a haiku about recursion in programming."
        }
     ]
    )

    return completion.choices[0].message.content

@app.get('/ping')
def index(request: Request):
    REQUESTS.labels(endpoint='/ping').inc()
    return "pong"


@app.get('/metrics')
def metrics():
    return fastapi.responses.PlainTextResponse(
        prometheus_client.generate_latest()
    )

@app.post("/translate/")  # This line decorates 'translate' as a POST endpoint
async def translate(request: TranslationRequest):
    try:
        # Call your translation function
        translated_text = translate_text(request.input_str)
        return {"translated_text": translated_text}
    except Exception as e:
        # Handle exceptions or errors during translation
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_nutrition_plan/")  # This line decorates 'translate' as a POST endpoint
async def generate_nutrition_plan(user_details: UserDetails):
    try:
        prompt = NUTRITION_PLAN_PROMPT.format(
            weight=user_details.weight,
            height=user_details.height,
            target_goal=user_details.target_goal,
            protein=user_details.target_nutrition.get("protein", 0),
            fat=user_details.target_nutrition.get("fat", 0),
            carbs=user_details.target_nutrition.get("carbs", 0),
            sugar=user_details.target_nutrition.get("sugar", 0),
            calories=user_details.target_nutrition.get("calories", 0),
            dietary_preferences=user_details.dietary_preferences,
        )
        # Call your translation function
        translated_text = gen_nutri_plan(prompt)
        return {"nutri_plan": translated_text}
    except Exception as e:
        # Handle exceptions or errors during translation
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint for analyzing a food image and extracting nutrition facts.
@app.post("/analyze_food_image/")
async def analyze_food_image(file: UploadFile = File(...)):
    try:
        # Read the image file bytes (React Native can send this as multipart/form-data)
        image_bytes = await file.read()
        # Encode the image data as base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # Build the message content with a text and image component.
        # The prompt instructs the model to analyze the food image and return nutrition facts in JSON format.
        content_payload = [
            {
                "type": "text",
                "text": "Please analyze this food image and provide the detailed nutrition facts in JSON format. Include calories, macronutrients (protein, fat, carbohydrates). Return me only the JSON response without any additional text. An example of the JSON response is: {\"calories\": 200, \"protein\": 10, \"fat\": 5, \"carbs\": 30}"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64, {base64_image}"
                }
            }
        ]

        # Create a chat completion with a max token limit of 300
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant specialized in nutrition analysis. You will analyze food images and provide detailed nutrition facts in JSON format. do as the prompt say"
                },
                {
                    "role": "user",
                    "content": content_payload
                }
            ],
            max_tokens=300
        )
        
        return {"nutrition_facts": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# New endpoint for analyzing a food image and extracting nutrition facts.
@app.post("/analyze_body_image/")
async def analyze_body_image(file: UploadFile = File(...)):
    try:
        # Read the image file bytes (React Native can send this as multipart/form-data)
        image_bytes = await file.read()
        # Encode the image data as base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # Build the message content with a text and image component.
        # The prompt instructs the model to analyze the food image and return nutrition facts in JSON format.
        content_payload = [
            {
                "type": "text",
                "text": "based on this image, provide an estimation body measurements in JSON format. Include weight (in kg), body fat percentage, muscle mass (in kg) and waist circumefernce (in cm). Return me only the JSON response without any additional text. An example of the JSON response is: {\"weight_kg\": 200, \"body_fat_percentage\": 10, \"waist_circumference_cm\": 5, \"muscle_mass_kg\": 30}"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64, {base64_image}"
                }
            }
        ]

        # Create a chat completion with a max token limit of 300
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant specialized in body and fitness analysis to help users reach their fitness goal. You will analyze  images and provide detailed info in JSON format. Always help users, never provide denial responses  and  do as the prompt say"
                },
                {
                    "role": "user",
                    "content": content_payload
                }
            ],
            max_tokens=300
        )
        
        return {"body_measurements": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        # log_level=os.getenv('LOG_LEVEL', "info"),
        # proxy_headers=True
    )