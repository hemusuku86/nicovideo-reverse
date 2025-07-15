import datetime
import hashlib
import hmac
import requests

Resource = {
  "8.17.1": {
    "account_api_key": "A1jjnnqfvt7r5vdzhben",
    "account_api_secret": "n27s7v7ih654i2uqtehgipv2qfb2b8kb8jvgy9fv"
  },
  "8.29.1": {
    "account_api_key": "A1jjnnqfvt7r5vdzhben",
    "account_api_secret": "n27s7v7ih654i2uqtehgipv2qfb2b8kb8jvgy9fv"
  }
}

class uri:
  def __init__(self, s):
    self.url = s
  def getPath(self):
    return "/" + "/".join(self.url.split("/")[3:]) + "/"
  def getHost(self):
    return self.url.split("/")[2]

def oh_m_d(_str, str2):
  sb2 = []
  sb2.append(_str)
  sb2.append("" if _str.endswith("/") else "/")
  sb2.append(str2[(1 if str2.startswith("/") else 0):])
  return "".join(sb2)

def c(bArr, _str):
  mac = hmac.new(bArr, _str.encode('utf-8'), hashlib.sha256)
  return mac.digest()

def e(_str):
  return hashlib.sha256(_str.encode()).digest()

def f(bArr):
  sb2 = []
  for b10 in bArr:
    sb2.append(hex(b10 & 255).replace("0x","").rjust(2,"0"))
  return "".join(sb2)

def nicoaccount_signature(_str, str2, uri, h0, str3, str4, str5):
  return f(c(c(c(("nicoaccount1" + _str).encode(), str4[0:8]), "nicoaccount1_request"), "NICOACCOUNT1-HMAC-SHA256\n" + str4 + "\n" + f(e(str2 + "\n" + uri.getPath() + "\n" + "" + "\n" + ("host:" + uri.getHost() + "\n" + str5.lower() + ":" + str4 + "\n") + "\n" + f(e(str3))))))

def register_test():
  global Resource
  now = datetime.datetime.now(datetime.UTC)
  m = now.month
  if len(str(m)) == 1:
    m = f"0{m}"
  d = now.day
  if len(str(d)) == 1:
    d = f"0{d}"
  h = now.hour
  if len(str(h)) == 1:
    h = f"0{h}"
  mm = now.minute
  if len(str(mm)) == 1:
    mm = f"0{mm}"
  s = now.second
  if len(str(s)) == 1:
    s = f"0{s}"
  frontend_version = "8.17.1"
  date = f"{now.year}{m}{d}T{h}{mm}{s}Z"
  signature = nicoaccount_signature(Resource[frontend_version]["account_api_secret"], "POST", uri(oh_m_d("https://account.nicovideo.jp/", "/api/v1/register/account_passport")), None, "", date, "X-Nicoaccount-Date")
  print(f"Generated X-Nicoaccount-Signature -> {signature}")
  headers = {
    "accept": "application/json",
    "accept-language": "ja",
    "accept-encoding": "gzip, deflate, br",
    "content-type": "application/json",
    "Host": uri(oh_m_d("https://account.nicovideo.jp/", "/api/v1/register/account_passport")).getHost(),
    "X-Nicoaccount-Date": date,
    "X-Nicoaccount-Signature": signature,
    "X-Nicoaccount-Api-Key": Resource[frontend_version]["account_api_key"],
    "x-frontend-id": "1",
    "x-frontend-version": frontend_version,
    "x-request-with": "nicoandroid",
    "X-OS-Version": "15", # android.os.Build.VERSION.RELEASE
    "X-Model-Name": "panther" # android.os.Build.DEVICE
  }
  print(requests.post("https://account.nicovideo.jp/api/v1/register/account_passport", headers=headers, data="{}").text)

register_test()
