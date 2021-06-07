import csv

def save_to_file(jobs):
  # mode = w(write) / csv file을 오픈해준다.
  file = open("jobs.csv", mode="w")
  # 오픈한 csv 파일에 데이터를 삽입한다.
  writer = csv.writer(file)
  writer.writerow(["title, company, location, link"])
  for job in jobs:
    # job.values() == go lang's content
    writer.writerow(list(job.values()))
  return 