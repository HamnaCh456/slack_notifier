import os
from firecrawl import JsonConfig, FirecrawlApp  
from pydantic import BaseModel, Field  
from typing import List  
import requests
from flask import Flask
import json
from google import genai
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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def writing_email(bounties_data):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are provided with bounty data... (rest unchanged)""",
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
