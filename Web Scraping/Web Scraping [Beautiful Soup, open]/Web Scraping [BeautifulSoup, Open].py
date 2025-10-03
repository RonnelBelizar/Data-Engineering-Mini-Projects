# 🕸️ Exercise: Web Scraping with BeautifulSoup
# ====================================================
# 📌 Problem Description
# You are tasked with scraping a simple web page to extract and process information using BeautifulSoup.
#
# ✅ Requirements
# 1. Use the `requests` library to fetch the HTML content from a given URL.
# 2. Parse the content using `BeautifulSoup`.
# 3. Extract the following from the page:
#    - The <title> of the page.
#    - All the <h2> headings.
#    - All the hyperlinks (<a> tags) and their text.
# 4. Store all extracted hyperlinks in a list.
# 5. Print the number of links you found.
#
# 🧩 Challenge
# - Filter the extracted links:
#   - Only keep links that start with "https".
#   - Save them into a text file called "links.txt" using Python's open() function.

from bs4 import BeautifulSoup
import requests

url = "https://www.python.org"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

title = soup.title.string
h2 = soup.find_all("h2")
a = soup.find_all("a")

hyp = []
for link in soup.find_all("a", href=True):
    hyp.append(link["href"])

# print(hyp)

text = []
for link in hyp:
    if "https" in link:
        text.append(link)
    else:
        continue
text_str = ""

for line in text:
    text_str += line + '\n'

print(text_str)

directory = r"C:\Users\Ronnel\Desktop\IBM Data Engineering\exercises\Python\Python for Data Science, AI, & Devvelopment\Mod_5_Web Scraping with BeautifulSoup [BeautifulSoup, open]"

with open(fr"{directory}\links.txt", "w", encoding="utf-8") as file:
    file.write(text_str)
