import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  # 마지막 페이지의 숫자를 가져옴 (strip = 공백 지워줌 / 1 = True, 0 = False)
  last_page = pages[-2].get_text(strip=1)
  return int(last_page)

def extract_job(html):
  title = html.find("h2", {"class":"mb4"}).find("a")["title"]
  # recursive -> span 안의 span까지 도달하지 않게 도와준다. get first level one
  company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span", recursive=0)
  company = company.get_text(strip=1)
  location = location.get_text(strip=1)
  job_id = html["data-jobid"]
  return {"title" : title, 'company': company, 'location': location, 'apply_link':f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page):
  jobs = []
  # range를 사용하려면 Integer를 사용해야한다.
  for page in range(last_page):
    # print(f"Scrapping SO: Page: {page}" )
    # 해당 URL의 상태코드가 정상적으로 출력되는지 확인한다.
    result = requests.get(f"{URL}&pg={page+1}")
    # BeautifulSoup는 function scope로 작동한다.
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div",{"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs
