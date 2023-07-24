import Config
import requests



def getXrayToken(url, data):
    response = requests.post(url+"/api/v1/authenticate", data=data)

    # Überprüfen, ob die Anfrage erfolgreich war (Status-Code 200)
    if response.status_code == 200:
        # Antwortinhalt anzeigen
        return response.json()
    else:
        print("Fehler bei der Anfrage:", response.status_code)

def getGherkinTestCase(baseurl,testcasekey,XrayToken):
    url = baseurl + "/api/v1//export/cucumber?keys="+testcasekey
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer "+str(XrayToken),
        "Accept-Charset": "UTF-8"
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response       
    else:
        print("Fehler bei der Anfrage:", response.status_code) 

