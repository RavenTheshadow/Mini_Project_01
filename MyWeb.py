from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import os
from getpass import getpass
def login(driver, login_url, username, password):
    driver.get(login_url)
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'password').submit()

def scrape_table(driver, source_url):
    driver.get(source_url)
    
    # Wait until the last updated date element in the table appears, indicating the page has fully loaded.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tfoot/tr/td[contains(text(), 'ĐTBTL chung')]"))
    )
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    all_data = []
    tables = soup.find('div', {'id': 'tblStudentGrade'}).find_all('table')
    
    for table in tables:
        header = [th.text.strip() for th in table.find_all('th')]
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = [td.text.strip() for td in row.find_all('td')]
            if len(cols) > 0:  # Ensure the row has data
                all_data.append(cols)
    
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(all_data, columns=['Mã Môn học', 'Tên môn học', 'Số tín chỉ', 'Điểm số', 'Điểm chữ', 'Ngày cập nhật'])
    return df

def main():
    login_url = "https://sso.hcmut.edu.vn/cas/login?service=https://mybk.hcmut.edu.vn/my/homeSSO.action"
    source_url = "https://mybk.hcmut.edu.vn/app/he-thong-quan-ly/sinh-vien/ket-qua-hoc-tap"
    
    input_file = "login_info.txt"
    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
        return
    # Read the login information from the file
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    driver = webdriver.Firefox()
    login(driver, login_url, username, password)
    sleep(5)
    df = scrape_table(driver, source_url)
    
    # Save the DataFrame to an Excel file
    output_file = "student_grades.xlsx"
    df.to_excel(output_file, index=False, engine='xlsxwriter')
    print(f"Data saved to {output_file}")

    driver.quit()
    print("End of program.")

if __name__ == "__main__":
    main()