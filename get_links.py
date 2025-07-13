from urllib.parse import urljoin, urlparse, parse_qs, urlencode
#each page has a job listing this return the links. 
def get_job_links(html_content):
    links = html_content.select('a.title')
    jobs_listing_links = [a.get("href") for a in links if a.get("href")]
    return jobs_listing_links

#return pagination links
def get_pages(html_content,base_url):
    pagination_links = html_content.select("div.styles_pages__v1rAK a[href]")
    parsed_url = urlparse(base_url)
    query_params = parse_qs(parsed_url.query)
    query_string = urlencode(query_params, doseq=True)
    base_domain = "https://www.naukri.com"
    page_urls = []
    for a_tag in pagination_links:
        href = a_tag.get("href")
        full_path = urljoin(base_domain, href)
        full_url_with_query = f"{full_path}?{query_string}"
        page_urls.append(full_url_with_query)
    return page_urls