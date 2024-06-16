import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def get_faculty_info(url):
    emails = {}
    names = []

    # Send a GET request to the webpage with SSL verification disabled
    response = requests.get(url, verify=False)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return emails

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all email addresses from the main page
    email_pattern = re.compile(r'[a-zA-Z]+\.[a-zA-Z]+@northeastern\.edu')
    email_matches = re.findall(email_pattern, soup.get_text())
    for email in email_matches:
        emails[email] = None

    # Extract professor names and map with emails from the page
    name_tags = soup.find_all('h2', class_='list__contact__headline')
    for tag in name_tags:
        name_link = tag.find('a', class_='contact__name add__decoration')
        if name_link:
            name = name_link.text.strip()
            names.append(name)
            # Find corresponding email for the name
            for email in email_matches:
                if name.lower() in email.lower():  # Matching emails by name (case insensitive)
                    emails[email] = name
                    break
    
    print(f"Emails found on main page: {emails}")
    print(f"Names found on main page: {names}")

    # Find all internal links
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Construct full URL for the link
        full_url = urljoin(url, href)
        
        # Ensure we only follow links within the same domain
        if url in full_url:
            try:
                print(f"Following link: {full_url}")
                # Send a GET request to the linked page with SSL verification disabled
                linked_response = requests.get(full_url, verify=False)
                
                if linked_response.status_code == 200:
                    linked_soup = BeautifulSoup(linked_response.content, 'html.parser')
                    
                    # Extract emails from the linked page
                    found_emails = re.findall(email_pattern, linked_soup.get_text())
                    for email in found_emails:
                        emails[email] = None  # Initialize with None

                    # Extract professor names and map with emails from the linked page
                    linked_name_tags = linked_soup.find_all('h2', class_='list__contact__headline')
                    for tag in linked_name_tags:
                        name_link = tag.find('a', class_='contact__name add__decoration')
                        if name_link:
                            name = name_link.text.strip()
                            names.append(name)
                            # Find corresponding email for the name
                            for email in found_emails:
                                if name.lower() in email.lower():  # Matching emails by name (case insensitive)
                                    emails[email] = name
                                    break

                    print(f"Emails found on {full_url}: {found_emails}")
                    print(f"Names found on {full_url}: {[name.text.strip() for name in linked_name_tags if name.find('a', class_='contact__name add__decoration')]}")
                    
                else:
                    print(f"Failed to retrieve the linked webpage {full_url}. Status code: {linked_response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve the linked webpage {full_url}. Error: {e}")

    return emails

if __name__ == "__main__":
    # URL of the university's faculty page
    url = 'https://coe.northeastern.edu/faculty-staff-directory/?pt&dept=8&type=Faculty'
    faculty_info = get_faculty_info(url)
    
    # Print the extracted email addresses and names
    print("Faculty Information:")
    for email, name in faculty_info.items():
        print(f"Name: {name}, Email: {email}")
