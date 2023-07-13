

import 'dart:io';
import 'package:http/http.dart' as http;

void main(){

  // Xray Token generieren
  String client_id = "1414FB6F9D1C43DEA9170901F3725F29";
  String client_secret = "3f8b84e0ad6e6b80f9a7f1982da8cb27ed25b286fc140e86369f6f44df4254fc";

  String getTokenBody = '{ "client_id": "$client_id","client_secret": "$client_secret" }';

  Xray_GenerateToken(getTokenBody:getTokenBody);

  

  // Auslesen des Test Cases aus Xray

  // Daten aus Stream auslesen / entpacken

  // Test Cases parsen

  //

}

void Xray_GenerateToken({required String getTokenBody}) async {
  print(getTokenBody);

  var _XrayRequestURL = Uri.https("xray.cloud.getxray.app","/api/v1/authenticate");
  print(_XrayRequestURL);
  var response = await http.post(_XrayRequestURL,body: getTokenBody);
  print('Response body: ${response.body}');

   /*  HttpRequest.request(_XrayRequestURL,method: 'POST',sendData: getTokenBody, requestHeaders: {'Content-Type':'application/json;charset=UTF-8'}).then((response){
    print(response.responseText);
    _response = response.responseText;
  }); */




}