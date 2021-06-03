import requests

indeed_result = requests.get("https://kr.indeed.com/jobs?q=python&limit=50")

#print(indeed_result) <Response [200]>
#print(indeed_result.text) // get HTML


