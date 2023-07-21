import Config
import requests
import json

apikey = Config.config["Applause Platform"]["apikey"]

def Applause_TestCase_Create(productID, TestCaseName, TestCaseDescription):
    url = "https://api.applause.com/v2/test-cases"
    data = { "description": TestCaseDescription,
            "estimatedTime": { 
            "hours": 0,
            "minutes": 1,
            },
            "name": TestCaseName,
            "productId": productID
            }
    json_body = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "X-Api-Key": apikey
    }
    response = requests.post(url, data=json_body, headers=headers)
    print(response.status_code)
    return response.text

def Applause_TestCase_AddStep(TestCaseID,Action,Expected,StepNr):
    url = "https://api.applause.com/v2/test-cases/"+str(TestCaseID)+"/steps"
    data = { "expectedResult": Expected,
            "instruction": Action,
            "name": "",
            "stepNumber": StepNr
            }
    json_body = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "X-Api-Key": apikey
    }
    response = requests.post(url, data=json_body, headers=headers)
    print(response.status_code)

def Applause_GetCycleInformation(ApplauseCycleID):
    url = "https://api.applause.com/v2/test-cycles/"+str(ApplauseCycleID)
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "X-Api-Key": apikey
    }
    CycleInformation = requests.get(url,headers=headers)
    CycleInformation = CycleInformation.json()
    CycleName = CycleInformation["name"]
    return CycleName    