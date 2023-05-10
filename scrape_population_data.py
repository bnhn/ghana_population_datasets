from bs4 import BeautifulSoup
import requests
import json

base_url = "https://statsghana.gov.gh/" 
ini_url = "https://statsghana.gov.gh/regionalpopulation.php?population=MTUwNDMxMDk2MS40NjA1&&UpperWest&regid=9"
def get_links(url):
    """
    Filters specific <a> tags from a webpage

    Args:
        url: Webpage to filter (string)

    Returns:
        list: of <a> text

    Dependencies:
        requests: pip install requests
        bs4: pip install beautifulsoup4
    """

    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    a_tag = soup.find_all("ul")

    return a_tag[10].find_all("a", href=True)

region_links = get_links(ini_url)


def get_population_data(url):
    """Scrapes Population data from statsghana.gov.gh

    Args:
        url (str): target website

    Returns:
        dict: {region_name: population}
    """
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    div = soup.find(attrs={"name":"statsDocFile"}).find_all("td")[3].text
    region_name = soup.find("h1", class_="pageTitle").span.text
    return {"region":region_name,"population":div}

population_data = []
for link in region_links:
    url = base_url+link["href"]
    data = get_population_data(url)
    population_data.append(data)

# Save to file
with open("population2021.json","w") as file:
    json.dump(population_data,file)