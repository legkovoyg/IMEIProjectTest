import uvicorn
import requests
import os
from fastapi import FastAPI
from models import enums, models
from dotenv import load_dotenv
import json

app = FastAPI()
load_dotenv()
token = os.getenv("API_KEY")

@app.post("/api/check-imei")
async def get_imei(request: models.IMEIResponse):
    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    body = json.dumps({
        "deviceId":
            f"{request.imei}"
        ,
        "serviceId": 15,
        "duplicateProcessingType": "reprocess"
    })
    response = requests.post(url, headers=headers, data=body)
    response_str = response.text
    parsed_data = json.loads(response_str)
    parsed_obj = models.IMEIResponseParsed.parse_obj(parsed_data)
    if parsed_obj.status == enums.ResponseEnum.SUCCESSFUL:
        return parsed_obj
    else:
        return {"message": "У вас странный IMEI!"}

if  __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)