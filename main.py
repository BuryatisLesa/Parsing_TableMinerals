from typing import Any
import requests
import time
from bs4 import BeautifulSoup
import sqlite3

st_accept = "text/html"

st_useragent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0.5993.731 YaBrowser/23.11.1.731 Yowser/2.5 Safari/537.36"
                )
headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent
}

main_url = 'https://catalogmineralov.ru'

req = requests.get(f"{main_url}/mineral/", headers)
src = req.text
soup = BeautifulSoup(req.text, 'html.parser')


def test_request(url, retry=5):
    try:
        response = requests.get(f'{url}', headers)
        print(f"[+] {url} {response.status_code}")
    except Exception:
        time.sleep(3)
        if retry:
            print(f"[INFO] retry =>{retry} => {url}")
            return test_request(url, retry=(retry - 1))
        else:
            raise
    else:
        return response


# def exception(var):
#     try:
#         var
#     except Exception:
#         exception("['None']")
#     return var


def url_href(var_process) -> list[str | Any]:
    save_container = []
    for var in var_process:
        save_cont = var.get('href')
        save_container.append(main_url + save_cont)
    return save_container


def req_paste(url) -> Any:
    req_p = requests.get(f'{url}', headers)
    return req_p


def soup_paste(var) -> Any:
    var = BeautifulSoup(var.text, 'lxml')
    return var


def replace(var):
    var_1 = var.replace("['", '')
    var_2 = var_1.replace("']", '')
    var_3 = var_2.replace("\\n", '')
    var_4 = var_3.replace("\n", '')
    return var_4


def insert_data_to_db(name_db, data):
    connect = sqlite3.connect(name_db)
    cursor = connect.cursor()
    cursor.executemany("INSERT INTO MINERALS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    connect.commit()
    print(f'Получены новые данные ==> внесены {db}')
    connect.close()


container = soup.select_one('h3').find_next('p')
teg_urls = container.find_all('a')
alf_urls = url_href(teg_urls)
alf_urls = alf_urls[0:-1]
alf_urls = alf_urls[10:-8]

for el_alf in alf_urls:
    req_alf = req_paste(el_alf)
    test_request(el_alf)
    scr_alf = req_alf.text
    soup_alf = soup_paste(req_alf)
    var_alf = soup_alf.select_one('div.ul_mineral')
    product_alf = var_alf.find_all('a')
    urls_min = url_href(product_alf)
    args = []
    for count, process in enumerate(urls_min):
        count += 1
        req_process = req_paste(process)
        test_request(process)
        scr_process = req_process.text
        soup_process = soup_paste(req_process)
        teg_soup = soup_process.find_all('tr', class_='tbl2')
        try:
            name_mineral = soup_process.select_one('h1').text
        except Exception:
            name_mineral = "['None']"
        formula = "['None']"
        syngony = "['None']"
        unit = "['None']"
        color = "['None']"
        color_trait = "['None']"
        shine = "['None']"
        cleavage = "['None']"
        hard = "['None']"
        density = "['None']"
        try:
            diagnostics = soup_process.find('span').text
        except Exception:
            diagnostics = "['None']"
        try:
            pair = soup_process.find('div', {'class': 'pre'}).text
        except Exception:
            pair = "['None']"
        for select_process in teg_soup:
            select_data = select_process.find_all('td')
            row = [attribut.text for attribut in select_data]
            if row[0] == 'Химическая формула':
                formula = str(row[1:])
            if row[0] == 'Сингония':
                syngony = str(row[1:])
            if row[0] == 'Форма выделения':
                unit = str(row[1:])
            if row[0] == 'Цвет':
                color = str(row[1:])
            if row[0] == 'Цвет черты':
                color_trait = str(row[1:])
            if row[0] == 'Блеск':
                shine = str(row[1:])
            if row[0] == 'Спайность':
                cleavage = str(row[1:])
            if row[0] == 'Твердость':
                hard = str(row[1:])
            if row[0] == 'Удельный вес':
                density = str(row[1:])
        formula = replace(formula)
        syngony = replace(syngony)
        unit = replace(unit)
        color = replace(color)
        color_trait = replace(color_trait)
        shine = replace(shine)
        cleavage = replace(cleavage)
        hard = replace(hard)
        density = replace(density)
        diagnostics = replace(diagnostics)
        pair = replace(pair)
        print(f'{count}.{name_mineral}. Minerals save in variable -> args')
        args.append((name_mineral, formula, syngony, unit, color, color_trait, shine, cleavage, hard, density,
                     diagnostics, pair))
    db = "db_minerals.db"
    insert_data_to_db(db, args)

