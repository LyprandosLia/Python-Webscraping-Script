# DOATAP Public Register Web Scraper

A Python web scraper to extract data from the [DOATAP Register](https://mitroa.doatap.gr/).  
This script automates selection of custom JavaScript dropdown filters and handles pagination to extract **all filtered table results**.

---

## ✅ Features

- **Filtering**: Automatically applies predefined filters (Country, Institution, Register, etc.) by simulating user clicks on the webpage.
- **Full Extraction**: Iterates through all pages of filtered results.
- **Data Storage**: Saves extracted data (Country, Institution, Info, Franchise) into a CSV file (`university_list_filtered.csv`).

---

## ⚙️ System Requirements

- Python 3.x
- External Python libraries:
  - `selenium` – for browser automation
  - `webdriver-manager` – for automatic ChromeDriver management

---
## Installation & Running the Script

Follow these steps to install dependencies and run the scraper:

1. **Clone or Download the Repository**:

```bash
git clone https://github.com/your-username/doatap-scraper.git
cd doatap-scraper
```
2. **Install Dependenices**:
   
```bash
pip install selenium webdriver-manager
```
3. **Configure Filters**:
   
Open script.py and edit the FILTER_VALUES dictionary to match the filters you want to apply:
```bash
FILTER_VALUES = {
    "ΧΩΡΑ": "GREECE", 
    "ΕΘΝΙΚΗ ΜΗΤΡΩΑ": "REGISTER OPTION", 
    # ... add other filters as needed
}
```
Make sure the text matches exactly what appears in the dropdowns on the website.

4. **Run the script**:
```bash
python script.py
```

5. **Check the Output**:
After the script finishes, you will find university_list_filtered.csv in the project folder containing all the extracted data.

## 📁 Results
The CSV file includes columns for Country, Institution, Info, and Franchise.

Supports automatic pagination and full extraction for all filtered entries.

## ⚠️ Notes
1. Make sure Chrome is installed on your system.

2. The script may require updates if the DOATAP website structure changes.

3. Tested on Python 3.10+ and Chrome 115+.
