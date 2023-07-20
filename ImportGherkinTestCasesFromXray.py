import requests
import json

apikey = "9ff63e15-cc56-45eb-afaf-43f4d31f7c5a9c2943"

def getXrayToken(url, data):
    response = requests.post(url+"/authenticate", data=data)

    # Überprüfen, ob die Anfrage erfolgreich war (Status-Code 200)
    if response.status_code == 200:
        # Antwortinhalt anzeigen
        return response.json()
    else:
        print("Fehler bei der Anfrage:", response.status_code)

def getGherkinTestCase(testcasekey):
    url = baseurl + "/export/cucumber?keys="+testcasekey
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer "+XrayToken,
        "Accept-Charset": "UTF-8"
    }
    response = requests.get(url,headers=headers)
    return response

def parseGherkinToArray(parsedata):
    parsedata = parsedata.content.decode("latin1")
    test_instructions = parsedata.strip().split("\n")
    return test_instructions

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


# API-URL festlegen
baseurl = "https://xray.cloud.getxray.app/api/v1"

# Daten für den Body der Anfrage
data = {
    "client_id": "1414FB6F9D1C43DEA9170901F3725F29", # client ID von Xray Cloud
    "client_secret": "3f8b84e0ad6e6b80f9a7f1982da8cb27ed25b286fc140e86369f6f44df4254fc" # client Secret von Xray Cloud
}

XrayToken = getXrayToken(baseurl, data)
print(XrayToken)
TestCaseKey="APPLAUSETC-58"
XrayTestCaseData = getGherkinTestCase(TestCaseKey)
test_instructions = parseGherkinToArray(XrayTestCaseData)

testcases_import = {}

TestCaseName = ""
TestCaseDescription = "Do not change: #BTS-ID "+TestCaseKey+"#"
TestCaseType=""
PreviousContent=""
TestCasesCount = 1
TestCaseID = 0
for i in test_instructions:
    if "Given" in i.strip():
        TestCaseName = PreviousContent + " Python Test"
        TestCaseID = Applause_TestCase_Create(31509, TestCaseName, TestCaseDescription)
        TestCaseType="Step"
        testcases_import['Step '+str(TestCasesCount)] = [i.strip(),"Done"]
        TestCasesCount += 1
    elif "When" in i.strip():
        TestCaseType="Step"
        testcases_import['Step '+str(TestCasesCount)] = [i.strip()]
        testcases_import['Step '+str(TestCasesCount-1)].append("")
        TestCasesCount += 1
    elif "Then" in i.strip():
        TestCaseType="Result"
        testcases_import['Step '+str(TestCasesCount-1)].append(i.strip())
    elif "And" in i.strip():
        if TestCaseType == "Step":
            testcases_import['Step '+str(TestCasesCount-1)][0] = testcases_import['Step '+str(TestCasesCount-1)][0]
        elif TestCaseType == "Result":
            testcases_import['Step '+str(TestCasesCount-1)][1] = testcases_import['Step '+str(TestCasesCount-1)][1] + " " + i.strip()
    PreviousContent=i.strip()

for index, (key, value) in enumerate(testcases_import.items()):
    Applause_TestCase_AddStep(TestCaseID,value[0],value[1],index+1)
    


