import Config
import requests
import json
import Interface_XrayCloud
import Interface_Applause
import Interface_JiraCloud

apikey = Config.config["Applause Platform"]["apikey"]
Jira_Cloud_URL = Config.config["Jira Cloud"]["Jira_Cloud_URL"]
ApplauseCycleID = 419447
ApplauseCycleName = Interface_Applause.Applause_GetCycleInformation(ApplauseCycleID)


baseurl = Config.config["Xray Cloud"]["URL"]

# Daten für den Body der Anfrage
data = {
    "client_id": Config.config["Xray Cloud"]["Client_ID"], # client ID von Xray Cloud
    "client_secret": Config.config["Xray Cloud"]["Client_Secret"] # client Secret von Xray Cloud
}

XrayToken = Interface_XrayCloud.getXrayToken(baseurl, data)
TestPlanKey = Interface_JiraCloud.createTestPlan(ApplauseCycleName,Jira_Cloud_URL,ApplauseCycleID)
TestPlanKey = TestPlanKey.json()

TestPlanKey = TestPlanKey["key"]
print(TestPlanKey)

CycleTestResults = Interface_Applause.Applause_GetTestCaseResults(ApplauseCycleID)
TestResults = CycleTestResults["content"]
for i in CycleTestResults["content"]:
    bolCreateTestExecution = False
    if "PASSED" in (i["status"]):
        bolCreateTestExecution = True
        print(i)
    elif "FAILED" in (i["status"]):
        bolCreateTestExecution = True
        print(i)
    if bolCreateTestExecution:
        TestCaseInformation = Interface_Applause.Applause_GetTestCaseInformation(i["testCaseId"])
        TestCaseKey = TestCaseInformation["description"]

        TestCaseKey = TestCaseKey.split("#BTS-ID")[1]
        TestCaseKey = TestCaseKey.split("#")[0]

        requestdata =  {
                    "info": {
                        "project": Config.config["Jira Cloud"]["Jira_ProjectID"],
                        "summary": "Applause Test Result ID "+str(i["id"]),
                        "description": "This execution was automatically created importing execution results from the Applause Platform",
                        "testplanKey": TestPlanKey,
                        "tests": {
                            "testKey": Config.config["Jira Cloud"]["Jira_ProjectName"]+TestCaseKey,
                            "status": i["status"]
                        }
                    }
        }
        print(requestdata)


