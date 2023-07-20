import requests
import json
import Interface_XrayCloud
import Interface_Applause
import Interface_JiraCloud

apikey = "9ff63e15-cc56-45eb-afaf-43f4d31f7c5a9c2943"
Jira_Cloud_URL = "https://meinb.atlassian.net"
ApplauseCycleID = 419447
ApplauseCycleName = Interface_Applause.Applause_GetCycleInformation(ApplauseCycleID)


baseurl = "https://xray.cloud.getxray.app/api/v1"

# Daten für den Body der Anfrage
data = {
    "client_id": "1414FB6F9D1C43DEA9170901F3725F29", # client ID von Xray Cloud
    "client_secret": "3f8b84e0ad6e6b80f9a7f1982da8cb27ed25b286fc140e86369f6f44df4254fc" # client Secret von Xray Cloud
}

XrayToken = Interface_XrayCloud.getXrayToken(baseurl, data)
TestPlanKey = Interface_JiraCloud.createTestPlan(ApplauseCycleName,Jira_Cloud_URL,ApplauseCycleID)
TestPlanKey = TestPlanKey.json()
TestPlanKey = TestPlanKey["key"]
print(TestPlanKey)
