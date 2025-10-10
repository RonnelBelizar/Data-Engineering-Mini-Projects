# 🏦 ETL Project: Largest Banks Data Pipeline

### 📘 Project Overview
This project demonstrates a simple **ETL (Extract, Transform, Load)** workflow using Python.  
It collects data from a public web source — *Wikipedia’s List of Largest Banks* — and transforms it into a clean, structured format for analysis and storage.

The goal of this project is to show how automated data collection and transformation can make large financial datasets easier to analyze and integrate into a database system.

---

### 🧩 What This Project Does
1. **Extract:**  
   - Scrapes the “List of Largest Banks” table from Wikipedia using `requests` and `BeautifulSoup`.

2. **Transform:**  
   - Cleans and standardizes column names.  
   - Converts USD-based market capitalization values into other currencies (GBP, EUR, INR) using exchange rates from a CSV file.  
   - Rounds results for easier readability and consistency.

3. **Load:**  
   - Exports the processed dataset into a CSV file for local storage.  
   - Loads the same dataset into a SQLite database (`Banks.db`) for easy querying and reporting.  
   - Runs basic SQL queries to verify data integrity.

---

### 🛠️ Tools & Libraries Used
- **Python 3**  
- **pandas** – for data manipulation  
- **BeautifulSoup (bs4)** – for web scraping  
- **requests** – for fetching web data  
- **SQLite3** – for lightweight database operations  
- **NumPy** – for numerical operations  
- **datetime** – for logging process stages  

---

### 📄 Output Files
- `Largest_banks_data.csv` – final cleaned dataset  
- `Banks.db` – database containing the transformed table  
- `code_log.txt` – process log with timestamps  

---

### 🧠 Key Takeaways
This project highlights:
- End-to-end data automation from extraction to database loading  
- Practical use of Python libraries for real-world ETL tasks  
- Data transformation with currency conversions  
- Process logging and error handling for maintainability  

---

### 💼 Why It Matters
Automating data pipelines like this reduces manual effort, ensures data consistency, and prepares information for further analysis — valuable skills for roles in **data engineering, analytics, and automation**.

---

### 👨‍💻 Author
**Ronnel Belizar**  
Electronics & Biomedical Engineer transitioning into Data Engineering  
📍 Passionate about healthcare data, analytics, and automation  

---

