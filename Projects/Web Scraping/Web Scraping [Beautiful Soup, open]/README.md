# Web Scraping with BeautifulSoup

A hands-on mini project demonstrating how to extract structured information from a webpage using **BeautifulSoup** and **Requests** in Python.

---

## 📌 Problem Description
You are tasked with scraping a simple web page to extract and process information such as page titles, headings, and hyperlinks.  
This exercise introduces how web scraping can be used to collect and clean publicly available data.

---

## 🧠 Learning Objectives
- Understand how to send HTTP requests and retrieve web content using `requests`.
- Parse HTML documents with `BeautifulSoup`.
- Extract specific elements like `<title>`, `<h2>`, and `<a>` tags.
- Filter and store hyperlinks programmatically.
- Save processed data into a local file using Python’s built-in `open()` function.

---

## ⚙️ Requirements
1. Use the `requests` library to fetch HTML content from a given URL.  
2. Parse the page using `BeautifulSoup`.  
3. Extract the following:
   - The `<title>` of the page.  
   - All `<h2>` headings.  
   - All hyperlinks (`<a>` tags) and their text.  
4. Store all extracted hyperlinks in a list.  
5. Print the total number of links found.

---

## 🧩 Challenge
Add a filter for the extracted links:
- Keep only those that start with `"https"`.
- Save the filtered links to a file named `links.txt`.

---

## 🧰 Libraries Used
- `requests` — to fetch web content.  
- `BeautifulSoup` (from `bs4`) — to parse and extract data from HTML.  
