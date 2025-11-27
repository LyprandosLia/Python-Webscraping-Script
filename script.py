from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time



# 1. ΤΙΜΕΣ ΦΙΛΤΡΩΝ (ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΑΚΡΙΒΩΣ ΟΠΩΣ ΕΜΦΑΝΙΖΟΝΤΑΙ ΣΤΟ DROPDOWN)
FILTER_VALUES = {
    "ΧΩΡΑ": "Επιλογή όλων των χωρών",  
    "ΕΘΝΙΚΑ ΜΗΤΡΩΑ": "ΙΔΡΥΜΑΤΑ", 
    "ΔΙΚΑΙΟΧΡΗΣΗ": "Ναι (με σύμβαση δικαιόχρησης)"   # Π.χ. "Ναι (με σύμβαση δικαιοχρήσης)"
}

# 2. SELECTORS ΤΟΥ ΚΥΡΙΩΣ ΠΕΔΙΟΥ (ΒΡΕΘΗΚΑΝ ΑΠΟ ΤΟ INSPECT ELEMENT ΤΟΥ BROWSER)
FILTER_SELECTORS = {
    "ΧΩΡΑ": "search_country_name",
    "ΕΘΝΙΚΑ ΜΗΤΡΩΑ": "instituteTitleOptionsId",
    # "ΙΔΡΥΜΑ": "instituteTitleOptionsId",
    "ΔΙΚΑΙΟΧΡΗΣΗ": "franchise"
}

# 3. SELECTOR ΣΕΛΙΔΟΠΟΙΗΣΗΣ & ΚΟΥΜΠΙΟΥ ΑΝΑΖΗΤΗΣΗΣ

TABLE_ROW_SELECTOR = "table.min-w-full tbody tr" 
NEXT_BUTTON_ICON_SELECTOR = "button i.fa-solid.fa-angle-right" # Στόχευση του βέλους >
# SEARCH_BUTTON_XPATH = "//button[contains(text(), 'Νέα Αναζήτηση')]"  -> ΑΝ ΥΠΑΡΧΕΙ ΚΟΥΜΠΙ ΑΝΑΖΗΤΗΣΗΣ, ΕΙΣΑΓΕΤΑΙ ΕΔΩ. ΔΙΑΦΟΡΕΤΙΚΑ ΥΠΑΡΧΕΙ EXCEPT ΠΑΡΑΚΑΤΩ ΚΑΙ ΤΟ ΠΡΟΓΡΑΜΜΑ ΤΟ ΠΑΡΑΚΑΜΠΤΕΙ



# ==============================================================================

def select_custom_dropdown(driver, element_id, value):
    """Επιλέγει μια τιμή από ένα προσαρμοσμένο dropdown (Custom Component)."""
    
    # 1. Κλικ για Άνοιγμα του Dropdown
    try:
        dropdown_display_selector = f"div#{element_id} .cursor-pointer"
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_display_selector))
        )
        dropdown_element.click()
        time.sleep(1) # Χρονος για load της λιστας
    except Exception as e:
        print(f"Δεν βρέθηκε το dropdown με ID '{element_id}'. Παράκαμψη. Σφάλμα: {e}")
        return
        
    # 2. Κλικ στην Επιλογή (Χρησιμοποιούμε XPath με βάση το κείμενο)
    try:
        # Ψάχνουμε για οποιοδήποτε div ή li που περιέχει ακριβώς το ζητούμενο κείμενο
        option_xpath = f"//div[normalize-space(text())='{value}'] | //li[normalize-space(text())='{value}']"
        option_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        
        # Κλικ στην επιλογή
        option_element.click()
        print(f"Επιλογή '{value}' έγινε για το φίλτρο '{element_id}'.")
        time.sleep(1) # Σύντομη αναμονή μετά την επιλογή
        
    except Exception as e:
        print(f"Δεν βρέθηκε η επιλογή '{value}' για το φίλτρο '{element_id}'. Σφάλμα: {e}")



def scrape_page_data(driver):
    """Εξάγει τα δεδομένα από την τρέχουσα σελίδα του πίνακα."""
    entries = []
    
    # *** ΔΙΟΡΘΩΣΗ: Χρήση της κλάσης αντί του ID ***
    TABLE_ROW_SELECTOR = "table.min-w-full tbody tr" 
    
    try:
        # Περιμένουμε μέχρι να γίνουν ΟΡΑΤΕΣ όλες οι γραμμές του πίνακα (timeout 20s)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, TABLE_ROW_SELECTOR))
        )
        
        current_entries = driver.find_elements(By.CSS_SELECTOR, TABLE_ROW_SELECTOR)
        
        for entry in current_entries:
            # Οι στήλες είναι: 0:ID (αριθμός), 1:ΧΩΡΑ, 2:ΙΔΡΥΜΑ
            cols = entry.find_elements(By.TAG_NAME, "td")
            
            # Ελέγχουμε ότι έχουμε τουλάχιστον 6 στήλες (ID + 5 στήλες δεδομένων)
            if len(cols) >= 6:
                entries.append([
                    cols[1].text.strip(), # ΧΩΡΑ
                    cols[2].text.strip(), # ΙΔΡΥΜΑ
                    # cols[3].text.strip(), # ΠΛΗΡΟΦΟΡΙΕΣ -> παραλείπεται στην εξαγωγή
                    # cols[4].text.strip()  # ΔΙΚΑΙΟΧΡΗΣΗ
                ])
    except Exception as e:
        # Το σφάλμα οφειλόταν πιθανότατα σε λάθος selector/timeout
        print(f"Σφάλμα κατά την εξαγωγή δεδομένων σελίδας: {e}")
        
    return entries


# ==============================================================================
#                           MAIN SCRIPT
# ==============================================================================

driver = webdriver.Chrome()
driver.get("https://mitroa.doatap.gr/")
all_scraped_entries = []

# --- 1. Εφαρμογή Φίλτρων ---

print("--- Εφαρμογή Φίλτρων ---")
for filter_name, element_id in FILTER_SELECTORS.items():
    value = FILTER_VALUES.get(filter_name)
    if value:
        select_custom_dropdown(driver, element_id, value)
    else:
        print(f"Παράλειψη φίλτρου {filter_name}, δεν δόθηκε τιμή.")

# --- 2. Κλικ στο Κουμπί Αναζήτησης (Αν δεν έγινε αυτόματα) ---
try:
    search_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, SEARCH_BUTTON_XPATH))
    )
    search_button.click()
    print("Κλικ στο κουμπί Νέα Αναζήτηση.")
    time.sleep(3) 
except: # Αν δεν βρεθεί το κουμπί, προχωράμε κανονικά
    print("Το κλικ στο κουμπί αναζήτησης απέτυχε ή δεν χρειάστηκε.")


# --- 3. Διαχείριση Σελιδοποίησης & Εξαγωγή Δεδομένων ---
print("\n--- Έναρξη Σελιδοποίησης ---")
page_number = 1
while True:
    print(f"Επεξεργασία σελίδας: {page_number}")
    
    # Εξαγωγή δεδομένων
    all_scraped_entries.extend(scrape_page_data(driver))
    
    # Εντοπισμός του κουμπιού 'Επόμενη' (>)
    try:
        # 1. Εντοπίζουμε το εικονίδιο 'Επόμενη' (>)
        next_icon = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, NEXT_BUTTON_ICON_SELECTOR))
        )
        
        # 2. Εντοπίζουμε το γονικό <button> για έλεγχο/κλικ
        next_button = next_icon.find_element(By.XPATH, '..')

        # 3. Έλεγχος αν το κουμπί είναι απενεργοποιημένο (Τελευταία Σελίδα)
        if not next_button.is_enabled():
            print("Τελευταία σελίδα, ολοκληρώθηκε η εξαγωγή.")
            break
            
        # 4. Κλικ στο κουμπί
        next_button.click()
        page_number += 1
        time.sleep(3) # Περιμένουμε να φορτώσει η επόμενη σελίδα
        
    except Exception as e:
        # Αν ούτε μετά τα 5 δευτερόλεπτα δεν βρεθεί το κουμπί, 
        # θεωρούμε ότι η σελιδοποίηση έχει τελειώσει (ή δεν υπάρχει).
        print(f"Δεν βρέθηκε κουμπί επόμενης σελίδας (ή σφάλμα: {e}), ολοκληρώθηκε η εξαγωγή.")
        break

# --- 4. Αποθήκευση Δεδομένων ---

filename = "university_list_filtered.csv"
with open(filename, mode="w", newline='', encoding='utf-8') as csvfile:     
    writer = csv.writer(csvfile)
    writer.writerow(["Country","University Name", "Info", "Franchise"])

    for entry in all_scraped_entries:
        writer.writerow(entry)

print(f"\n{len(all_scraped_entries)} entries were saved in {filename}")
driver.quit()