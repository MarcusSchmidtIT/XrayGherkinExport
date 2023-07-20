import requests
import json
import Interface_XrayCloud
import Interface_Applause

apikey = "9ff63e15-cc56-45eb-afaf-43f4d31f7c5a9c2943"

def parseGherkinToArray(parsedata):
    parsedata = parsedata.content.decode("latin1")
    test_instructions = parsedata.strip().split("\n")
    return test_instructions


# API-URL festlegen
baseurl = "https://xray.cloud.getxray.app/api/v1"

# Daten für den Body der Anfrage
data = {
    "client_id": "1414FB6F9D1C43DEA9170901F3725F29", # client ID von Xray Cloud
    "client_secret": "3f8b84e0ad6e6b80f9a7f1982da8cb27ed25b286fc140e86369f6f44df4254fc" # client Secret von Xray Cloud
}

XrayToken = Interface_XrayCloud.getXrayToken(baseurl, data)
print(XrayToken)
TestCaseKey="APPLAUSETC-58"
XrayTestCaseData = Interface_XrayCloud.getGherkinTestCase(baseurl,TestCaseKey,XrayToken)
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
        TestCaseID = Interface_Applause.Applause_TestCase_Create(31509, TestCaseName, TestCaseDescription)
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
    Interface_Applause.Applause_TestCase_AddStep(TestCaseID,value[0],value[1],index+1)
    


