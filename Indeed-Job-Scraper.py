import csv 
from datetime import date
import requests
from bs4 import BeautifulSoup
import os



def get_url(position, location):
	template = 'https://in.indeed.com/jobs?q={}&l={}'
	url = template.format(position, location)
	return url



def get_record(card):

	atag = card.h2.a

	job_title = atag['title']

	job_url = 'https://www.indeed.com' + atag.get('href')

	job_company = card.find('span', {'class':'company'}).text.strip()

	try:
		job_location = card.find('div', {'class': 'location'}).text.strip()
	except AttributeError:
		job_location = ''

	job_summary = card.find('div', {'class': 'summary'}).text.strip()

	try:
		job_salary = str(card.find('span', {'class': 'salaryText'}).text.strip())
	except AttributeError:
		job_salary = ''

	post_date = card.find('span', {'class': 'date'}).text.strip()

	today = str(date.today())

	return (job_title, job_company, job_salary, job_location, job_summary, post_date, today, job_url)



def main():

	position = input('Enter the position of the job - ')

	location = input('Enter the location of the job - ')

	records = []

	url = get_url(position, location)

	while(url):

		response = requests.get(url)

		soup = BeautifulSoup(response.text, 'html.parser')

		cards = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})

		for card in cards:
			records.append(get_record(card))

		try:
			url = url = 'https://in.indeed.com/' + soup.find('a', {'aria-label': 'Next'}).get('href')
		except AttributeError:
			url = ""

	if len(records)==0:
		print("NO MATCHING FOUND!")
		return

	with open('Indeed-jobs-scrape.csv', 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(['JOB TITLE', 'COMPANY', 'SALARY', 'LOCATION', 'SUMMARY', 'POST DATE', 'EXTRACT DATE', 'JOB URL'])
		writer.writerows(records) 

	os.startfile('Indeed-jobs-scrape.csv')


main()

