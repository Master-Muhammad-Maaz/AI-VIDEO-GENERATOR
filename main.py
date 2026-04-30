import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Direct API Key (As requested for testing)
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
        1. 'visual_prompt': Detailed English description for an AI image generator.
        2. 'audio_text': Keep the exact Hinglish words.
        3. 'duration': Assign a logical duration in seconds (3-6s).
        
        Return ONLY a JSON object.
        """
        
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.script}
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"}
        )
        
        return json.loads(completion.choices[0].message.content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
