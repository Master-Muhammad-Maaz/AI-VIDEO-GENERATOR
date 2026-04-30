import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Setup: Taaki aapki website backend se connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel par deploy karte waqt yahan domain name aayega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Direct API Key for Testing
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

class ScriptRequest(BaseModel):
    script: str

@app.post("/generate-scenes")
async def generate_scenes(request: ScriptRequest):
    try:
        system_prompt = """
        You are a specialized AI for video production. 
        Convert the Hinglish script into a sequence of scenes.
        
        Rules:
        1. 'visual_prompt': Highly detailed English description for an AI image generator (8k, cinematic, realistic).
        2. 'audio_text': Keep the exact Hinglish words provided by the user.
        3. 'duration': Assign a logical duration in seconds (3-6s).
        
        Output Format:
        {
            "scenes": [
                {"scene_number": 1, "visual_prompt": "...", "audio_text": "...", "duration": 5},
                ...
            ]
        }
        Return ONLY a valid JSON object.
        """
        
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.script}
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"}
        )
        
        # AI ka response JSON format mein convert karke return karna
        return json.loads(completion.choices[0].message.content)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Check API Key or Connection.")

# Deployment ke liye (Local testing ke liye zaruri nahi, par GitHub/Render ke liye achha hai)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
