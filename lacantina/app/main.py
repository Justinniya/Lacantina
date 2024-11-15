from fastapi import FastAPI
from pydantic import BaseModel
import httpx,random,os
from starlette.responses import HTMLResponse

app = FastAPI()

PAGE_ACCESS_TOKEN = "EAAf7YoJWTpwBO21NZC6i4oQGxzVkA8cBDDBlajbDtzcA9XJfAgd9sftBN5I7rGrf6DEjRsVG4eFcW5a0vr6fzl50H8B4pveg3xYhMfSKI8YL4G6i0YnpJfHGqFMiDsKqRauPGIzhbNjQqHG9UUcI3i2bezTbkCEm3lZC2FhN3RZB7p2zSaTLo14ydocwJcZD"
PAGE_ID = "223892484135695"
GRAPH_API_URL = f"https://graph.facebook.com/v12.0/{PAGE_ID}/feed"

greetings = [
    {"message": "Hello, everyone! Hope you're having an amazing day!",
     "menu": "Adobo",
     "price": 100,
     "img": "https://media.istockphoto.com/id/480105918/photo/chicken-and-pork-adobo-filipino-food.jpg?s=612x612&w=0&k=20&c=X71iXuT-hAsTWPz-7TbnauK7z4ovt2Z8r_GqCx_WpV8="},
    
    {"message": "Wishing you all a day full of smiles and positivity!",
     "menu": "Sinigang",
     "price": 120,
     "img": "https://media.istockphoto.com/id/623283160/photo/sinigang-na-baboy-filipino-cuisine.jpg?s=612x612&w=0&k=20&c=Pw2VNqaBR7M1J9jqSGsBeHCSn8eLoLQE6fQC-48cyu0="},
    
    {"message": "Good vibes only today—let's make it count!",
     "menu": "Pancit",
     "price": 150,
     "img": "https://media.istockphoto.com/id/1485348992/photo/a-large-serving-of-pancit-canton-guisado-a-popular-filipino-noodle-dish.jpg?s=612x612&w=0&k=20&c=9W_mtAPHks7Ex8aTEJRP9Lk8Hsazh6boCcQzylhUFK8="},
    
    {"message": "Hey there! Hope you're ready to conquer the day!",
     "menu": "Lechon",
     "price": 200,
     "img": "https://media.istockphoto.com/id/654608924/photo/famous-philippines-food-lechon.jpg?s=612x612&w=0&k=20&c=Yqq1DdxrI4TjxLnU0sAofPlzRIF8Z3fuJU0GrsaYMcw="},
    
    {"message": "Sending warm greetings to brighten up your day!",
     "menu": "Bicol Express",
     "price": 180,
     "img": "https://media.istockphoto.com/id/1053332722/photo/filipino-bicol-express-from-spiced-pork-in-coconut-milk-close-up-horizontal.jpg?s=612x612&w=0&k=20&c=T5eO8h8EM7W6f5E9VFjQ7pk46WzhHBSbz63ACw0DHkI="},
    
    {"message": "Happy Friday! Let's start it off with a smile!",
     "menu": "Kare-Kare",
     "price": 250,
     "img": "https://media.istockphoto.com/id/1139903539/photo/oxtails-in-peanut-gravy-filipino-flavor-kare-kare-on-brown-bowl.jpg?s=612x612&w=0&k=20&c=b5hOEx9pSi2HSnr0crjJLFi54_n1BpAJiwsUOlALifY="},
    
    {"message": "Hope you all are doing great—stay positive and keep shining!",
     "menu": "Pork Barbecue",
     "price": 170,
     "img": "https://media.istockphoto.com/id/155431877/photo/barbecue-ribs.jpg?s=612x612&w=0&k=20&c=dhgNEMKLSDT23JP3rk1VgBLSeaGeCX9mDxPg6W8otOs="},
]

async def post_to_facebook(message: str,image_url: str):
    async with httpx.AsyncClient() as client:
        payload = {
            'message': message,
            'link': image_url,
            'access_token': PAGE_ACCESS_TOKEN
        }
        # Send the POST request to Facebook's Graph API
        response = await client.post(GRAPH_API_URL, params=payload)
        
        if response.status_code == 200:
            html_content = """
           <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posting La Cantina Automation</title>
    <style>
        /* General Body Styling */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: center;
        }

        /* Page Header */
        h1 {
            color: #2d7c34;
            font-size: 36px;
            margin-top: 100px;
            font-weight: 600;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }

        /* Links Styling */
        a {
            font-size: 18px;
            color: #ffffff;
            text-decoration: none;
            background-color: #2d7c34;
            padding: 12px 24px;
            border-radius: 8px;
            margin: 10px;
            display: inline-block;
            transition: background-color 0.3s ease;
        }

        a:hover {
            background-color: #1f5b22;
        }

        /* Add some spacing between the links */
        br {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

    <h1>FastAPI Server is Running and Has Already Posted to Facebook!</h1>
    <p>Everything is working smoothly. You can view your post on Facebook.</p>
    
    <a href="https://www.facebook.com/LaCantinaPCF" target="_blank">View Post</a>
    <br>
    <a href="/">Back</a>

</body>
</html>

"""
            
            ""
            return HTMLResponse(content=html_content)
            
        else:
            return {"status": "Error", "error": response.text}
        
@app.get('/')
async def homepage():
    html_content = """
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Cantina Posting Automation</title>
    <style>
        /* General Body Styling */
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: center;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        /* Header Styling */
        h1 {
            color: #4CAF50;
            font-size: 36px;
            font-weight: 700;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        /* Link Styling */
        a {
            font-size: 18px;
            color: #ffffff;
            text-decoration: none;
            background-color: #4CAF50;
            padding: 12px 24px;
            border-radius: 8px;
            margin-top: 20px;
            transition: background-color 0.3s ease;
        }

        a:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

    <h1>Welcome to La Cantina Posting Automation Server</h1>
    <a href="/post">Post Menu</a>

</body>
</html>

"""
    return HTMLResponse(content=html_content)


@app.get('/post')
async def create_facebook_post():
    
    greeting = greetings
    all_post = "\n\n".join([f"{poster['message']} \nfor todays menu : \nmenu : {poster['menu']} - ₱{poster['price']} "for poster in greeting])+"\n📍 Riverside Strip, Paciencia T. Pison Ave, Mandurriao, Iloilo City\n⏰ Monday to Thursday (8am-10pm) and Friday to Saturday (8am-12am)\n\n#GinisangAmpalaya #HealthyAndTasty"
    result = await post_to_facebook(all_post,greeting[0]['img'])
    """poster = random.choice(greetings)
    message = (f"{poster['message']} \nfor todays menu : \n{poster['menu']} - ₱{poster['price']} \n📍 Riverside Strip, Paciencia T. Pison Ave, Mandurriao, Iloilo City\n⏰ Monday to Thursday (8am-10pm) and Friday to Saturday (8am-12am)\n\n#GinisangAmpalaya #HealthyAndTasty")
    result = await post_to_facebook(message,poster['img'])"""
    return result


"""
@app.on_event("startup")
async def startup_event():
    #Trigger Facebook post automatically when FastAPI starts.
    print("Starting FastAPI server and posting to Facebook...")
    await create_facebook_post()

@app.get("/")
async def root():
    return {"message": "FastAPI server is running and has already posted to Facebook!"}"""