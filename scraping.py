import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def scrape_content(url, element_ids):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_dict = {}
        for element_id in element_ids:
            element = soup.find(id=element_id)
            if element:
                content_dict[element_id] = element.get_text(strip=True)
            else:
                print(f"Element with id '{element_id}' not found.")
                content_dict[element_id] = None
        return content_dict
    else:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")
        return None

url = 'https://www.promtior.ai/service'
element_ids = [ "comp-ly0nzysz", "comp-lyarslb1", 'tab-comp-ly34jriv', 'comp-ly34jrix', 'tab-comp-lyaruxg2',"comp-lyaruxgh1", 'tab-comp-lyaruxg2', 'tab-comp-lyarx6ta',"comp-lyarx6uq", 'tab-comp-lyp0hhv4',"comp-lyp0hhve" ]
content_dict = scrape_content(url, element_ids)

if content_dict:
    for element_id, content in content_dict.items():
        if content:
            print(f"{content}\n")
        else:
            print(f"No content found for element with id '{element_id}'.")

documents = [Document(page_content=content) for content in content_dict.values() if content]
