from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import get_html_content
import get_links
import get_description
import pandas as pd
import job_scores
from datetime import datetime
if __name__ == "__main__":

    base_url = 'https://www.naukri.com/react-dot-js-python-azure-devops-jobs-in-bengaluru?experience=3&cityTypeGid=97&ctcFilter=15to25&jobAge=1'
    html_content = get_html_content.get_url_data(base_url)
    pages = get_links.get_pages(html_content,base_url) #this will return the pages
    job_listing = []
    # job_listing_page1 = get_links.get_job_links(html_content) #this will contains links of all jobs
    # job_listing.extend(job_listing_page1)
    if len(pages)>=1:  #getting the job listings of other pages
        for url in pages:
            html_content = get_html_content.get_url_data(url)
            job_listing_page1 = get_links.get_job_links(html_content) #this will contains links of all jobs
            job_listing.extend(job_listing_page1)
    job_description = []
    print("totol number of jobs", len(job_listing))
    if len(job_listing) >=50:
        job_listing = job_listing[:50]


    for url in job_listing:
        details = {}
        details['url'] = url
        html_content = get_html_content.get_url_data(url)
        description_json = get_description.extract_flexible_job_description(html_content)
        details['desc'] = description_json
        if description_json!={}:
            job_description.append(details)
    # print(job_description)
    jobs = pd.DataFrame(job_description)
    jobs.to_csv(f'jobs.csv', index = False)
    df = job_scores.get_job_match_score(jobs)
    today = datetime.now().strftime('%Y-%m-%d')
    df.to_csv(f'jobs_{today}.csv', index = False)






