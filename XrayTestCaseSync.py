import requests
import json

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
    # Testanweisungen aus dem Text extrahieren
    # soup = BeautifulSoup(parsedata, "html.parser")
    # test_instructions = []
    #for instruction in soup.find_all("Given"):
    #    test_instructions.append(instruction.text.strip())
    return test_instructions

def Applause_TestCase_Create(productID, TestCaseName, TestCaseDescription):
    apikey = "9ff63e15-cc56-45eb-afaf-43f4d31f7c5a9c2943"
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
#print(XrayTestCaseData.content)
test_instructions = parseGherkinToArray(XrayTestCaseData)
#print(len(test_instructions))
#print(test_instructions)

testcases_import = []

TestCaseName = ""
TestCaseDescription = "Do not change: #BTS-ID "+TestCaseKey+"#"
TestCaseType=""
PreviousContent=""

for i in test_instructions:
    if "Given" in i.strip():
        print(i.strip())
        TestCaseName = PreviousContent + " Python Test"
        print(TestCaseName)
        Applause_TestCase_Create(31509, TestCaseName, TestCaseDescription)
    PreviousContent=i.strip()
    


