import Config
import requests
import json

JiraApiKey = Config.config["Jira Cloud"]["apikey"]
IssueType_TestPlan = Config.config["Jira Cloud"]["IssueType_TestPlan"]
IssueType_TestExecution = Config.config["Jira Cloud"]["IssueType_TestExecution"]
Jira_ProjectID = Config.config["Jira Cloud"]["Jira_ProjectID"]
Jira_UserID = Config.config["Jira Cloud"]["Jira_UserID"]


def createTestPlan(Summary,baseurl,ApplauseCycleID):
    url = baseurl + "/rest/api/2/issue"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic "+JiraApiKey,
        "Accept-Charset": "UTF-8"
    }    
    data = { 
            "fields": {
                "summary": Summary,
                "issuetype": {
                    "id": IssueType_TestPlan
                },
                "project": {
                    "id": Jira_ProjectID
                },
                "description": "created automatically",
                "reporter": {
                    "id": Jira_UserID
                },
                "labels": [
                    "Applause_Cycle_"+str(ApplauseCycleID)
                ]
                }
            }
    data = json.dumps(data)
    response = requests.post(url,headers=headers,data=data)
    return response