from datetime import date
from bs4 import BeautifulSoup as bs
from selenium import webdriver
# import lxml
import time
import csv

today = date.today()
now_is = today.strftime("%A_%d_%B_%Y")
print(now_is)
#
# # Selenium login
def shara_parse():
    url = "https://sharavoz.ru"
    # user_name = input("Username:  ")
    user_name = "uberalles"
    # pass_word = input("Password:  ")
    pass_word = "remedyshara1"

    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0")

    driver = webdriver.Firefox(executable_path=r"C:\Users\Uber\PycharmProjects\SHARAVOZ\geckodriver.exe", options=options)

    try:
        driver.get(url)
        # time.sleep(2)

        enter_button = driver.find_element_by_css_selector("button.nav__button:nth-child(2)").click()
        login = driver.find_element_by_id('log-username')
        login.clear()
        login.send_keys(user_name)
        time.sleep(2)

        password = driver.find_element_by_id('log-password')
        password.send_keys(pass_word)
        time.sleep(1)
        confirm = driver.find_element_by_xpath("/html/body/div[3]/div/form/button").click()
        time.sleep(3)

        dealer_menu = driver.find_element_by_css_selector("li.treeview:nth-child(6) > a:nth-child(1)")
        time.sleep(3)
        dealer_menu.click()
        time.sleep(3)

        hundred_clients = driver.find_element_by_css_selector("#users-table_length > label:nth-child(1) > select:nth-child(1) > option:nth-child(4)")
        hundred_clients.click()
        time.sleep(3)

        index_page = driver.page_source
        time.sleep(3)


        with open("index.html", "w", encoding="utf-8") as file:
            file.write(index_page)


#РАБОТА БЕЗ ЗАПРОСОВ 2 tabs


        with open("index.html", "r", encoding="utf-8") as file:
            src = file.read()
        # try:
        soup = bs(src,"lxml")

        client_cards_even = soup.find_all("tr", class_="even")
        client_cards_odd = soup.find_all("tr", class_="odd")
        client_cards = client_cards_odd + client_cards_even



        with open(f"{now_is}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(

                ["Номер","Имя клиента","Остаток  дней", "Баланс","Пакет","Скоро закончится"]

                          )


        client_count = 1
        for cc in client_cards[1:]:

            # print(client_count,cc)
            client_name = cc.find("a", title="Просмотреть логи").text
            days_left = cc.find("span", class_="packet-count-left days-left") or cc.find("span", class_= "packet-count-left days-left three-or-less")
            ballance = cc.find("div", class_="info-tool pull-left").text

            packet_name = cc.find("span",class_="packet-name").text
            soon_end_marker = None

            if days_left is not None:
                days_left = days_left.text.strip("(").strip(")")
                soon_end = int(days_left.split()[0])
                print(soon_end)
                if soon_end < 5:
                    soon_end_marker = "Внимание!!"
                    print("скоро",soon_end_marker)
                else:
                    soon_end_marker = ""
                    print("скоро",soon_end_marker)


        else:
            days_left = "[INFO] Подписка не активна!"


        user_data = [
            client_count,client_name,days_left, ballance,packet_name,soon_end_marker
        ]


        with open(f"{now_is}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(user_data)

            client_count +=1

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

# def main():
#     shara_parse()
#
# if __name__ == '__main__':
#     main()

