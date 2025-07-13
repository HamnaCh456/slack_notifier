import os
from firecrawl import JsonConfig, FirecrawlApp  
from pydantic import BaseModel, Field  
from typing import List  
import requests
from flask import Flask
import json
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def scraper():  
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)
    
    class BountySchema(BaseModel):  
        title: str  
        reward: str  
        posted_date: str  
        url: str  
    
    class BountiesSchema(BaseModel):  
        bounties: List[BountySchema] = Field(..., description="List of all bounties on the page")  
    
    json_config = JsonConfig(  
        schema=BountiesSchema,  
        prompt="Extract the first 5 bounties from this page, including title, reward, posted date, and URL for each bounty"  
    )  
    
    llm_extraction_result = firecrawl_app.scrape_url(  
        'https://replit.com/bounties?status=open&order=creationDateDescending',  
        formats=["json"],  
        json_options=json_config,  
        only_main_content=False,  
        timeout=120000  
    )  
    return llm_extraction_result.json
    
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def writing_email(bounties_data):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    response = model.generate_content( 
        contents=f"""You are provided with bounty data. You must ONLY use the data provided below and nothing else. Do not invent or add any information not present in the data.
                    Data: {bounties_data}
                    Write a simple ,professional message(containing url ,amount,description of bounty/bounties,time since when its posted) about the highest paid bounty which is posted within 24 hours/1 day using ONLY the information provided above. If the data shows price ranges, mention the range exactly as given.If more than one bounty is having the same price range than mention them all in your message from the provided information ONLY.""",
    )
    return response.text

def send_slack_message(message):
    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    payload = '{"text":"%s"}' % message
    return requests.post(slack_url, data=payload).text

@app.route('/', methods=['GET'])
def driver_func():
    result = scraper()
    bounties_data = json.dumps(result, indent=1)
    message = writing_email(bounties_data)
    return send_slack_message(message)

if __name__ == '__main__':
    app.run(debug=False)
