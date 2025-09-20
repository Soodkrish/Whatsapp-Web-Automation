from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


CONTACTS = [""] # write the names of your contacts here  
NORMAL_MESSAGES = [
    "All secrets vanish, Reality bends beneath shadows, Sudden storms rise",
    "Know fear before it finds you."
]


driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

print("WhatsApp Web opened")
input("Press ENTER after logged in and chats are visible...")

for CONTACT_NAME in CONTACTS:
    print(f"\n📌 Processing contact: {CONTACT_NAME}")

    # -------- Search Contact --------
    search_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true" and @data-tab="3"]'))
    )
    search_box.click()
    search_box.clear()
    search_box.send_keys(CONTACT_NAME)
    time.sleep(2)  # wait for search results

    # -------- Locate visible contact span --------
    contact_span = None
    for el in driver.find_elements(By.XPATH, f'//span[@title="{CONTACT_NAME}"]'):
        if el.is_displayed():
            contact_span = el
            break

    if contact_span is None:
        print(f"❌ Could not find contact '{CONTACT_NAME}'. Skipping...")
        continue

    # -------- Try clicking the span first --------
    try:
        driver.execute_script("""
            var el = arguments[0];
            el.click();
            el.dispatchEvent(new MouseEvent('mousedown', {bubbles:true}));
            el.dispatchEvent(new MouseEvent('mouseup', {bubbles:true}));
        """, contact_span)
        print(f"✅ Clicked on '{CONTACT_NAME}' span.")
        time.sleep(2)  # wait for chat to load
    except:
        print("⚠️ Span click failed, falling back to container div...")
        contact_div = contact_span
        while contact_div.tag_name != 'div' or not contact_div.is_displayed():
            try:
                contact_div = contact_div.find_element(By.XPATH, "..")
            except:
                contact_div = None
                break
        if contact_div:
            driver.execute_script("arguments[0].scrollIntoView(true);", contact_div)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", contact_div)
            print(f"✅ Failsafe click on '{CONTACT_NAME}' container div done.")
            time.sleep(2)
        else:
            print(f"❌ Could not click contact '{CONTACT_NAME}'. Skipping...")
            continue

    # -------- Wait for message box --------
    msg_box = None
    try:
        chat_panel = driver.find_element(By.XPATH, '//div[@id="main"]')
        for el in chat_panel.find_elements(By.XPATH, './/div[@contenteditable="true"]'):
            if el.is_displayed():
                msg_box = el
                break
    except:
        msg_box = None

    if msg_box is None:
        print(f"❌ Could not locate message box for '{CONTACT_NAME}'. Skipping...")
        continue

    # -------- Send NORMAL messages --------
    for msg in NORMAL_MESSAGES:
        msg_box.send_keys(msg)
        msg_box.send_keys(Keys.ENTER)
        time.sleep(0.5)  # small delay
    print(f"✅ Sent {len(NORMAL_MESSAGES)} message(s) to '{CONTACT_NAME}' successfully!")

print("\n🌙 Finished sending messages to all contacts. Browser remains open.")
input()
