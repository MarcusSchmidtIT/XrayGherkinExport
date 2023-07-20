import requests
import json

JiraApiKey = "bWFyY3VzQHNjaG1pZHQtaXQuc2VydmljZXM6QVRBVFQzeEZmR0YwX3JkdlBYVW1UMXpJRTA3NlBLejF1d2hZMDVTR0RYcnBab0IzcDJtSWkzNTFpc3VIbmppZkN4S25JODNSTDY5VVZ4RUFLQk1pTUFweHQ3NGFXMEY3elRWQVlnWm1qVm1LREVKeDlFcDNOSTRmYXFpcjUzVnkxeVhiYVBnQjZXWjBRSFpJaWt6aHFJUjNpdk5hZnhiZ0tJRENYRTV2Zmc4RklkaEpETDBuV3c0PUNEM0JBRDIw"
IssueType_TestPlan = 10058
IssueType_TestExecution = 10059
Jira_ProjectID = 10005
Jira_UserID = "5f959c90632c62007127fafe"


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