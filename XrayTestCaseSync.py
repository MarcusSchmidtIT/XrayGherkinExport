import Config
import requests
import json
import Interface_XrayCloud
import Interface_Applause

apikey = Config.config["Applause Platform"]["apikey"]

def parseGherkinToArray(parsedata):
    parsedata = parsedata.content.decode("latin1")
    test_instructions = parsedata.strip().split("\n")
    return test_instructions


# API-URL festlegen
baseurl = Config.config["Xray Cloud"]["URL"]

# Daten für den Body der Anfrage
data = {
    "client_id": Config.config["Xray Cloud"]["Client_ID"], # client ID von Xray Cloud
    "client_secret": Config.config["Xray Cloud"]["Client_Secret"] # client Secret von Xray Cloud
}

XrayToken = Interface_XrayCloud.getXrayToken(baseurl, data)
print(XrayToken)
TestCaseKey="APPLAUSETC-67"
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

print(testcases_import)
for index, (key, value) in enumerate(testcases_import.items()):
    Interface_Applause.Applause_TestCase_AddStep(TestCaseID,value[0],value[1],index+1)
    


