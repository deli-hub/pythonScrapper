import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():

  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  # find -> 첫 번째 해당 태그를 리턴
  pagination = soup.find("div", {"class":"pagination"})
  # find_all -> 해당하는 모든 태그를 리턴
  links = pagination.find_all("a")
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  #pages = pages[0:-1] #list의 0번째부터 마지막 -1번째까지 출력
  max_page = pages[-1] # 제일 마지막(큰) 수를 가져온다

  return max_page

def extract_job(html):
  title = html.find("h2", {"class":"title"}).find("a")["title"]
  company = html.find("span", {"class":"company"})
  co_anchor = company.find("a")
  if co_anchor is not None:
    company = str(co_anchor.string)
  else :
    company = str(company.string)
  #양 끝에 있는 문자를 제거해주는 라이브러리 함수 (괄호안에 있는 문자 - 공백포함)
  company = company.strip()
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
  # 내부에 있는 attr를 찾을 때는 대괄호를 사용
  job_id = html["data-jk"]
  
  return {'title': title, "company": company, "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    # print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(2)
  return jobs