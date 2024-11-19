from fastapi import FastAPI
from pydantic import BaseModel
import httpx,random,os,json,openai
from starlette.responses import HTMLResponse
from typing import Dict,List

app = FastAPI()

PAGE_ACCESS_TOKEN = "EAAf7YoJWTpwBO21NZC6i4oQGxzVkA8cBDDBlajbDtzcA9XJfAgd9sftBN5I7rGrf6DEjRsVG4eFcW5a0vr6fzl50H8B4pveg3xYhMfSKI8YL4G6i0YnpJfHGqFMiDsKqRauPGIzhbNjQqHG9UUcI3i2bezTbkCEm3lZC2FhN3RZB7p2zSaTLo14ydocwJcZD"
PAGE_ID = "223892484135695"
GRAPH_API_URL = f"https://graph.facebook.com/v12.0/{PAGE_ID}/feed"
GRAPH_API_URL_PHOTOS = f"https://graph.facebook.com/v12.0/{PAGE_ID}/photos"
photos = []
greetings = []
 
class Items(BaseModel):
    message: str
    menu: str
    price: int
    img: str
async def post_to_facebook():
    async with httpx.AsyncClient() as client:
        print("\n\nUploading to Facebook\n")
        """openai.api_key = "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"
        
        response = openai.Completion.create(
        model="gpt-4o-mini",  
        prompt="give me a wonderfull intro and outro for my restaurant in just 5 sentences and base on this📍 Riverside Strip, Paciencia T. Pison Ave, Mandurriao, Iloilo City ⏰ Monday to Thursday (8am-10pm) and Friday to Saturday (8am-12am) #GinisangAmpalaya #HealthyAndTasty",
        max_tokens=100
        )
        message = response.choices[0].text.strip()"""
        payload = {
            'message': "Welcome to Lacantina",
            'attached_media': '',
            'access_token': PAGE_ACCESS_TOKEN,
            'published': 'true'
        }
        attached_media = json.dumps([{'media_fbid': media_id} for media_id in photos])
        payload['attached_media'] = attached_media
        response = await client.post(GRAPH_API_URL, params=payload)
        
        if response.status_code == 200:
            print("\n\nUploaded to Facebook Successfully\n")
            greetings = []
            
        else:
            print( response.text)
async def git_photo_id(image_urls: list,caption:list):
    async with httpx.AsyncClient() as client:

        num = 0
        print("\n\nPreparing Image and Caption\n\n")
        for i in image_urls:
            payload = {
                'message':f'{caption[num]}',
                'url': i,
                'access_token': PAGE_ACCESS_TOKEN,
                'published': 'false'
            }
            
            # Send the POST request to Facebook's Graph API
            response = await client.post(GRAPH_API_URL_PHOTOS, params=payload)
            
            if response.status_code == 200:
                response_json = response.json()
                photo_id = response_json.get('id')
                if photo_id:
                    print(f"\nSuccessfully prepared the image: {photo_id} with the caption : {payload['message']}\n")
                    photos.append(photo_id)
                    num += 1
                    
                else:
                    print(f"Error: Missing 'id' in response for image {i}")
            else:
                print(f"Error uploading image {i}: {response.text}")
                return {"status": "Error", "error": response.text}
        print("\n\nReady for Upload\n")
        return await post_to_facebook()

@app.post('/')
async def create_facebook_post(item: List[Items]):
    for finalValue in item:
        greetings.append(finalValue.dict())
    
    greeting = greetings
    captions = [f"{poster['message']} \nfor todays menu : \nmenu : {poster['menu']} - ₱{poster['price']} \n📍 Riverside Strip, Paciencia T. Pison Ave, Mandurriao, Iloilo City\n⏰ Monday to Thursday (8am-10pm) and Friday to Saturday (8am-12am)\n\n#GinisangAmpalaya #HealthyAndTasty"for poster in greeting]
    photos = [i['img'] for i in greeting]
    result = await git_photo_id(photos,captions)
    return result






"""@app.on_event("startup")
async def startup_event():
    #Trigger Facebook post automatically when FastAPI starts.
    print("Starting FastAPI server and posting to Facebook...")
    await create_facebook_post()"""