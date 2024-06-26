from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

def home(request):
    return render(request, 'home.html')

def truncate_words(text, num_words):
    words = text.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return text

def scrape_job_details(keyword):
    base_url = 'https://www.shine.com/job-search/'
    search_url = f'{base_url}{keyword}'

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', {"class": "jobCard_jobCard__jjUmu"})
        
        job_list = []
        
        for job_card in job_cards:
            job_details = {}
        
            # Extract the job title
            title_tag = job_card.find('strong', class_='jobCard_pReplaceH2__xWmHg')
            job_details['title'] = title_tag.get_text(strip=True) if title_tag else None
            
            posted_on_div = job_card.find('div', class_='jobCard_jobCard_features__wJid6')
            posted_on_spans = posted_on_div.find_all('span') if posted_on_div else []
            job_details['posted_on'] = posted_on_spans[1].get_text(strip=True) if len(posted_on_spans) > 1 else None
        
            # Extract the company name
            company_tag = job_card.find('div', class_='jobCard_jobCard_cName__mYnow')
            job_details['company'] = company_tag.get_text(strip=True) if company_tag else None
        
            # Extract the link
            link_tag = job_card.find('a', href=True)
            job_details['link'] = 'https://www.shine.com'+link_tag['href'] if link_tag else None
        
            # Extract the job description (assuming it's within a <p> tag or similar identifiable tag)
            description_tag = job_card.find('div', class_='jobCard_skillList__KKExE')
            description = description_tag.get_text(strip=True) if description_tag else None
            truncated_description = truncate_words(description, 30)
            job_details['description']=truncated_description
        
            # Add job_details to job_list if it contains any information
            if job_details['title'] or job_details['company']:
                job_list.append(job_details)
        
        return job_list
    else:
        return None

def get_job_details(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        job_details = scrape_job_details(keyword)
        return render(request, 'home.html', {'job_details': job_details})
    return render(request, 'home.html')
