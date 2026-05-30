from dotenv import load_dotenv
import os
from groq import Groq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
load_dotenv()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

groq_api_key=os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Backend Running"}
@app.post("/chat")
async def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }