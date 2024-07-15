from openai import AsyncOpenAI
import base64
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import HTTPException

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_fingerprint(file):
    try:
        # Read the uploaded image file
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode("utf-8")

        # Create the payload for the OpenAI API request
        messages = [
            {
                "role": "system",
                # "content": "Given an image of a fingerprint, determine or guess the type of fingerprint: Simple Arch, Tented Arch, Plain Loop, Reverse Loop, Double Loop, Plain Whorl, or Peacock Whorl. Briefly explain the distinctive features that led to your conclusion. Then, provide directions for the user to locate the core and delta, if they exist."
                "content": "Given an image of a fingerprint, determine the type of fingerprint. Briefly explain the distinctive features that led to your conclusion. Then, provide directions for the user to locate the core and delta, if they exist."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        # Send the request to OpenAI API
        response = await client.chat.completions.create(
            # model="gpt-4-vision-preview",
            model="gpt-4o",
            messages=messages,
            max_tokens=1000
        )
        response_string = response.choices[0].message.content
        modified_response = response_string.replace("**", "*")

        return JSONResponse(content={"description": modified_response})

    except Exception as e:
        print(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")