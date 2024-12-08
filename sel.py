from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome driver uchun brauzer instance yaratamiz
driver = webdriver.Chrome()

try:
    # TON Keeper saytiga kiramiz
    driver.get("https://wallet.tonkeeper.com/")

    # Sahifa to'liq yuklanishini kutamiz
    wait = WebDriverWait(driver, 20)

    # "Get started" tugmasini topamiz va bosamiz
    get_started_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get started')]")))
    get_started_button.click()

    # "Existing Wallet" tugmasini kutamiz va bosamiz
    existing_wallet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Existing Wallet']/ancestor::button")))
    existing_wallet_button.click()

    # Inputlarni kutamiz (XPath yordamida)
    inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[contains(@class, 'sc-leCVXs') and contains(@class, 'livCdq')]")))

    # Har bir mnemonik so'zni inputlarga ketma-ket kiritamiz
    mnemonic_words = [
        "vacant", "piece", "tell", "size", "fantasy", "book", "clean", 
        "casino", "general", "inmate", "erosion", "never", "truth", 
        "outer", "nest", "quantum", "crazy", "crush", "side", "convince", 
        "lunch", "park", "fruit", "turkey"
    ]
    
    for i in range(min(len(inputs), len(mnemonic_words))):
        inputs[i].send_keys(mnemonic_words[i])
        time.sleep(0.2)

    print("Mnemonik so'zlar muvaffaqiyatli kiritildi!")

    # Birinchi "Continue" tugmasini kutamiz va bosamiz
    continue_button_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button_1.click()

    # Ikkinchi "Continue" tugmasini kutamiz va bosamiz
    continue_button_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button_2.click()

    # Parolni kiritish
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='create-password']")))
    password_input.send_keys("Lalaku007")
    time.sleep(0.2)
    password2_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='create-password-confirm']")))
    password2_input.send_keys("Lalaku007")

    continue_button_3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button_3.click()

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]")))
    save_button.click()

    print("Ikkita 'Continue' tugmasi bosildi!")

    # Davom etish uchun Enter tugmasini kutmasdan doimiy ishlashga o'tamiz
    while True:
        try:
            print("Tekshirish boshlanmoqda...")
            ton_value_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sc-PfnDg')]/span[contains(text(), 'TON')]/following-sibling::span[@class='sc-jSguLX egBbuV']")))

            ton_value = ton_value_element.text.strip()

            # Agar qiymat bo'sh bo'lsa, uni 0 deb belgilaymiz
            if not ton_value:
                ton_value = "0"

            # Vergulni nuqtaga o'zgartiramiz
            ton_value = ton_value.replace(",", ".")

            # Faqat raqamlarni tekshirish
            try:
                ton_value_float = float(ton_value)
            except ValueError:
                print(f"Xatolik: {ton_value} raqam emas!")
                time.sleep(5)
                continue

            # Check if value is greater than 0.0001
            if ton_value_float > 0.0001:
                print(f"TON qiymati: {ton_value_float} - Send tugmasi bosildi!")
                send_button = wait.until(EC.element_to_be_clickable((
                    By.XPATH, 
                    "//div[@class='sc-boeIrO cdFSoc']//span[contains(text(), 'Send')]"
                )))
                send_button.click()
                break  # Exit loop after clicking the send button
            else:
                print(f"TON qiymati: {ton_value_float} kutish...")  # Value is too small
                time.sleep(5)  # Wait before checking again
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(5)  # Wait before retrying

finally:
    # Bu joyda brauzer doimiy ochiq turadi, hech qachon yopilmaydi
    print("Brauzer doimiy ochiq turadi!")
