import os
from time import sleep
from decouple import config
import subprocess
import json
import urllib.parse

os.system("tput reset")
print("Listening...")

profile = json.loads(subprocess.check_output("curl -s https://"+config("INSTANCE")+"/api/v1/accounts/verify_credentials -H \"Authorization: Bearer "+config("TOKEN")+"\"", shell=True).decode("utf-8"))
fields = profile["source"]["fields"]
data = ""
i = 0
for item in fields:
    if str(i) == config("FIELDID"):
        data = data+"fields_attributes["+str(i)+"][name]="+urllib.parse.quote_plus(config("NAME"))+"&"
    else:
        data = data+"fields_attributes["+str(i)+"][name]="+urllib.parse.quote_plus(item["name"])+"&"
        data = data+"fields_attributes["+str(i)+"][value]="+urllib.parse.quote_plus(item["value"])+"&"
    i = i+1
data = data[:-1]

while True:
    np = subprocess.check_output("echo $(playerctl metadata -p "+config("PLAYER")+" xesam:artist) - $(playerctl metadata -p "+config("PLAYER")+" xesam:title)", shell=True).decode("utf-8")
    os.system("curl -sSL \"https://"+config("INSTANCE")+"/api/v1/accounts/update_credentials\" -H \"Authorization: Bearer "+config("TOKEN")+"\" -X PATCH -d \""+data+"\" --data-urlencode \"fields_attributes["+config("FIELDID")+"][value]="+np+"\" > /dev/null")
    sleep (5)
