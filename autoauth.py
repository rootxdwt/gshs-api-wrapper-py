import requests

from jsbn import RSAKey
from bs4 import BeautifulSoup
import re
from getpass import getpass

id=input("id: ")
pw=getpass("password:")

loginPageResp = requests.get("https://student.gs.hs.kr/student/index.do?mode=manual&returnUrl=/index.do")

temporaryToken = re.findall(
    "JSESSIONID=(\\w+)", loginPageResp.headers['Set-Cookie'])[0]
bs4Finder = BeautifulSoup(loginPageResp.text, 'html.parser')
nVal = bs4Finder.find('input', {'id': 'm'})['value']
eVal = bs4Finder.find('input', {'id': 'e'})['value']
rsa = RSAKey()
rsa.setPublic(nVal, eVal)

id = rsa.encrypt(id)
pw = rsa.encrypt(pw)
try:
    getTkReq = requests.post("https://student.gs.hs.kr/student/requestAccessCode.do",
                            data={'type': 'STUD', 'userId': id, 'pwd': pw}, cookies={'JSESSIONID': temporaryToken, 'userId': id},
                            headers={
                                'Content-Type': 'application/x-www-form-urlencoded'},
                            allow_redirects=False
                            )
except:
    print("error")

if getTkReq.text == "FINE":
    code = input("code: ")
    try:
        logInReq = requests.post("https://student.gs.hs.kr/student/loginCommit.do",
                                data={'type': 'STUD', 'userId': id, 'pwd': pw, 'accessCode': code, "mode": "ONE", "guid": "MOZILLAMACINTOSHINTELMACOSXAPPLEWEBKITKHTMLLIKEGECKOCHROMESAFARI", "device": "chrome", "returnUrl": "/index.do"}, cookies={'JSESSIONID': temporaryToken, 'userId': id},
                                headers={
                                    'Content-Type': 'application/x-www-form-urlencoded'},
                                allow_redirects=False
                                )

        sessionKey = re.findall("JSESSIONID=(\\w+)",
                                logInReq.headers['Set-Cookie'])[0]
        f = open("sessionKey.txt", "w")
        f.write(sessionKey)
        f.close()
    except:
        print("err")
