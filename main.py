from datetime import date
from datetime import datetime as dt , timedelta
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import csv

url = "https://sharavoz.ru"
today = date.today()
now_is = today.strftime("%d.%m.%Y")
year_ago = dt.now()-timedelta(366)
# year_ago = year_ago.strftime("%d.%m.%Y")
print(now_is)
print("year ago is: ",year_ago.strftime("%d.%m.%Y"))
user_name = input("Логин для входа на сайт: ")
pass_word = input("Password:  ")
#
# # Selenium login
def shara_record_file():
    """records the html page into  a file for further parsing without bombing a server with multiple requests"""
    # url = "https://sharavoz.ru"

    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0")

    driver = webdriver.Firefox(executable_path=r"C:\Users\Uber\PycharmProjects\SHARAVOZ\geckodriver.exe", options=options)

    try:
        driver.get(url)
        enter_button = driver.find_element_by_css_selector("button.nav__button:nth-child(2)").click()
        login = driver.find_element_by_id('log-username')
        login.clear()
        login.send_keys(user_name)

        password = driver.find_element_by_id('log-password')
        password.send_keys(pass_word)

        confirm = driver.find_element_by_xpath("/html/body/div[3]/div/form/button").click()
        time.sleep(3)#4

        dealer_menu = driver.find_element_by_css_selector("li.treeview:nth-child(6) > a:nth-child(1)")
        time.sleep(2)#4
        dealer_menu.click()
        time.sleep(2)#4

        hundred_clients = driver.find_element_by_css_selector("#users-table_length > label:nth-child(1) > select:nth-child(1) > option:nth-child(4)")
        hundred_clients.click()
        time.sleep(2)#3


        index_page = driver.page_source
        time.sleep(2)#3

        with open("index.html", "w", encoding="utf-8") as file:
            file.write(index_page)
    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

def open_recorded_file():
    """opens previously saved html document and creates a soup object of it"""
    with open("index.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = bs(src,"lxml")

    client_cards_even = soup.find_all("tr", class_="even")
    client_cards_odd = soup.find_all("tr", class_="odd")
    client_cards = client_cards_odd + client_cards_even

    with open(f"{user_name}_{now_is}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(

            ["Номер","Имя клиента","Остаток  дней", "Баланс","Пакет","Дата окончания","Статус"]

                      )

    client_count = 1
    for cc in client_cards[1:]:
        client_name = cc.find("a", title="Просмотреть логи").text
        days_left = cc.find("span", class_="packet-count-left days-left") or cc.find("span", class_= "packet-count-left days-left three-or-less") or cc.find("span", class_="packet-count-left hours-left")
        ballance = cc.find("div", class_="info-tool pull-left").text
        packet_name = cc.find("span",class_="packet-name").text
        last_time_used = cc.find("span", class_="packet-dates").text.split()[-1]

        last_day = int(last_time_used.split(".")[0])
        last_month = int(last_time_used.split(".")[1])
        last_year = int(last_time_used.split(".")[2])
        last_time_used = dt(last_year, last_month, last_day)
        soon_end_marker = ""


        if days_left is not None:
            days_left = days_left.text.strip("(").strip(")")
            soon_end = int(days_left.split()[0])

            if soon_end <= 5 or "час" in days_left:
                soon_end_marker = "Внимание ! ! !"
            else:
                soon_end_marker = "Норма"

        else:
            days_left = "[INFO] пакет неактивен"
            if last_time_used < year_ago:
                soon_end_marker = "Кандидат на удаление"

        user_data = [
            client_count,client_name,days_left, ballance,packet_name,last_time_used.strftime("%d.%m.%Y"),soon_end_marker
        ]


        with open(f"{user_name}_{now_is}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(user_data)

        client_count +=1

def main():
    shara_record_file()
    open_recorded_file()

if __name__ == '__main__':
    main()

