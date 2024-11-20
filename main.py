from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from constants import *
import prometheus_client
from openai import OpenAI
import os
import uvicorn

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


uvicorn.run(
        app,
        host="0.0.0.0",
        # log_level=os.getenv('LOG_LEVEL', "info"),
        # proxy_headers=True
    )