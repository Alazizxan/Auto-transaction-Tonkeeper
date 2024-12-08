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

    # Qiymatni tekshiradigan loop
    while True:
        # Elementni topamiz
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='sc-PfnDg fcSjsb']//span[3]")))
        value_text = element.text.replace(",", ".")  # Qiymatni float formatiga moslashtiramiz
        try:
            value = float(value_text)
            if value > 0.0001:
                print(f"Qiymat: {value} - Katta")
            else:
                print(f"Qiymat: {value} - Kichik")
        except ValueError:
            print("Qiymatni floatga o'tkazib bo'lmadi.")

        time.sleep(2)  # Har 2 soniyada tekshiruvni takrorlaymiz

except Exception as e:
    print(f"Xatolik: {e}")

finally:
    driver.quit()
