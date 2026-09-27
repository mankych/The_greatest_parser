import sqlite3
import logging
import os
from playwright.sync_api import sync_playwright
logging.basicConfig(level=logging.INFO,filename='parser.log',format='%(asctime)s - %(levelname)s - %(message)s')
def view():
    print('1.Просмотреть базу данных\n2.Очистить базу данных')
    choose = input()
    if choose == '1':
         print('Какую базу данных открыть?\n1.Wildberries\n2.Ozon\n3.Yandex')
         choose_bd = input()
         if choose_bd == '1':
              conn = sqlite3.connect('Wildberries.db')
              cursor = conn.cursor()
              try:
                cursor.execute('SELECT * FROM wb')
              except:
                   logging.warning('Таблица wb не найдена')
                   print('Вероятно такой таблицы нет. Попробуйте что то спарсить')
              rows = cursor.fetchall()
              if rows:
                for row in rows:
                     print(f'ID: {row[0]}')
                     print(f'Название: {row[1]}')
                     print(f'Цена: {row[2]}')
                     print(f'Ссылка: {row[3]}')
                     print('---')
                print('Если бд вдруг большая то для полного просмотра понадобится db browser')
                logging.info('Просмотрено бд Wildberries')
                conn.close()
              else:
                   logging.info('Открыта пустая бд')
                   print('Тут пусто')
         elif choose_bd == '2':
            conn = sqlite3.connect('Ozon.db')
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM ozon')
            except:
                 print('Вероятно такой таблицы нет. Попробуйте что то спарсить')
                 logging.warning('Таблина ozon не найдена')
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f'ID: {row[0]}')
                    print(f'Название: {row[1]}')
                    print(f'Цена: {row[2]}')
                    print(f'Ссылка: {row[3]}')
                    print('---')
                print('Если бд вдруг большая то для полного просмотра понадобится db browser')
                logging.info('Просмотрено бд Ozon')
                conn.close()
            else:
                logging.info('Открыта пустая бд')
                print('Тут пусто')
         elif choose_bd == '3':
            conn = sqlite3.connect('Yandex.db')
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM yandex')
            except:
                print('Вероятно такой таблицы нет. Попробуйте что то спарсить')
                logging.warning('Таблина yandex не найдена')
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f'ID: {row[0]}')
                    print(f'Название: {row[1]}')
                    print(f'Цена: {row[2]}')
                    print(f'Ссылка: {row[3]}')
                    print('---')
                print('Если бд вдруг большая то для полного просмотра понадобится db browser')
                logging.info('Просмотрено бд Yandex')
                conn.close()
            else:
                logging.info('Открыта пустая бд')
                print('Тут пусто')
         else:
             print('Ошибка вводите только доступные варианты')
    elif choose == '2':
        print('Какую базу очистить?\n1.Wildberries\n2.Ozon\n3.Yandex')
        which_bd = input()
        if which_bd == '1':
            you_sure = input('Вы действительно хотите удалить все записи?(д/н) ').lower()
            if you_sure == 'д':
                conn = sqlite3.connect('Wildberries.db')
                cursor = conn.cursor()
                try:
                    cursor.execute('DELETE FROM wb')
                    print('Бд очищено')
                    logging.info('Бд Wildberries очищено')
                except:
                    print('Нечего удалять')
                    logging.warning('Нечего удалять из таблицы wb')
                conn.commit()
            else:
                return
        elif which_bd == '2':
                you_sure = input('Вы действительно хотите удалить все записи?(д/н) ').lower()
                if you_sure == 'д':
                    conn = sqlite3.connect('Ozon.db')
                    cursor = conn.cursor()
                    try:
                        cursor.execute('DELETE FROM ozon')
                        print('Бд очищено')
                        logging.info('Бд ozon очищен')
                    except:
                        print('Нечего удалять')
                        logging.warning('Нечего удалять из таблицы ozon')
                    conn.commit()
                else:
                    return
        elif which_bd == '3':
            you_sure = input('Вы действительно хотите удалить все записи?(д/н) ').lower()
            if you_sure == 'д':
                conn = sqlite3.connect('Yandex.db')
                cursor = conn.cursor()
                try:
                    cursor.execute('DELETE FROM yandex')
                    print('Бд очищено')
                    logging.info('Бд yandex очищена')
                except:
                    print('Нечего удалять')
                    logging.warning('Нечего удалять из таблицы yandex')
                conn.commit()
            else:
                return


                     
                        
         
            
                    
#Функция парсинга вб
def wb():
    conn = sqlite3.connect('Wildberries.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS wb(
    id INTEGER PRIMARY KEY ,
    name TEXT,
    cost TEXT,
    link TEXT)''')
    conn.commit()
    name = input('Введите название товара: ')
    with sync_playwright() as f:
        browser = f.chromium.launch(headless = False,args=[
        '--disable-blink-features=AutomationControlled',  
    ])
        page = browser.new_page()
        page.goto('https://www.wildberries.ru/?ysclid=mtzpjrlqqy865446164')
        page.wait_for_selector('.main-page__content.main-page__content-wrapper--snippet-rate-wallet')
        product = page.get_by_placeholder('Найти на Wildberries')
        product.fill(name)
        product.press('Enter')
        logging.info(f'Запустился парсер Wildberries по запросу:{name}')
        page.wait_for_selector('.catalogCardLink--CgiYl.j-card-link.j-open-full-product-card')
        for _ in range(15):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(2000)
        all_product = page.locator('.catalogCardLink--CgiYl.j-card-link.j-open-full-product-card').count()
        for i in range(all_product):
            try:
                product_name = page.locator('[class*="productLabelWrap"]').nth(i).inner_text()
                product_cost = page.locator('[class*="product-card__price"]').nth(i).inner_text()
                product_href = page.locator('[class*="catalogCardLink"]').nth(i).get_attribute('href')
                new_name = product_name.replace('\n', ' ')
                new_cost = product_cost.replace('\n', ' ')
                
                try:
                    cursor.execute('INSERT INTO wb(name,cost,link)VALUES(?,?,?)',(new_name,new_cost,product_href))
                    
                except Exception as e:
                     logging.error(f'Данные не сохранились по причине: {e}')
            
                     
            except:
                
                 continue
        
        conn.commit()
        logging.info('Данные сохранены в бд')  
        conn.close()
        
def ozon():
    with sync_playwright() as f:
        conn = sqlite3.connect('Ozon.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ozon(
        id INTEGER PRIMARY KEY ,
        name TEXT,
        cost TEXT,
        link TEXT)''')
        conn.commit()
        choose = input('Введите название товара: ')
        browser = f.chromium.launch(headless=False,args=[
        '--disable-blink-features=AutomationControlled',  
    ])
        page = browser.new_page()
        page.goto('https://www.ozon.ru/?__rr=1&abt_att=1&origin_referer=yandex.ru')
        product = page.get_by_placeholder('Искать на Ozon')
        product.fill(choose)
        product.press('Enter')
        logging.info(f'Запустился парсер Ozon по запросу:{choose}')
        page.wait_for_timeout(10000)
        for _ in range(15):
                    page.mouse.wheel(0, 1500)
                    page.wait_for_timeout(2000)
        cards = page.locator('[class*="tile-root"]').count()
        for i in range(cards):
            try:    
                card = page.locator('[class*="tile-root"]').nth(i)
                name = card.locator('span.tsBody500Medium').inner_text()
                cost = card.locator('.tsHeadline500Medium').inner_text()
                href = card.locator('a[href*="/product/"]').first.get_attribute('href')
                full_link = f"https://www.ozon.ru{href}"
                cursor.execute('INSERT INTO ozon(name,cost,link)VALUES(?,?,?)',(name,cost,full_link))
            except:   
                 
                 continue
        logging.info('Данные спаршены')
        conn.commit()
        logging.info('Данные сохранены в бд')
        conn.close()
def yan():
    conn = sqlite3.connect('Yandex.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS yandex(
    id INTEGER PRIMARY KEY,
    name TEXT,
    cost TEXT,
    link TEXT)''')
    conn.commit()
    choose = input('Введите название товара: ')
    with sync_playwright() as f:
        browser = f.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="ru-RU"
        )
        page = context.new_page()
        page.goto('https://market.yandex.ru/')
        page.set_default_timeout(4000)
        product_input = page.get_by_placeholder('Найти товары')
        product_input.fill(choose)
        product_input.press('Enter')
        logging.info(f'Запустился парсер YandexMarket по запросу:{choose}')
        page.wait_for_timeout(10000)
        for _ in range(15):
                      page.mouse.wheel(0, 1500)
                      page.wait_for_timeout(2000)
        page.wait_for_timeout(3000)
        product_count = page.locator('[data-data-source="ss-product"]').count()
        for i in range(product_count):
            try:
                product = page.locator('[data-data-source="ss-product"]').nth(i)
                product_name = product.locator('[itemprop="name"]').get_attribute('title')
                product_cost = product.locator('[class *= "ds-valueLine"]').first.inner_text()
                new_cost = product_cost.replace('\n', '')
                product_href = product.locator('[href *= "/card/"]').first.get_attribute('href')
                clean_link = f"https://market.yandex.ru{product_href.split('?')[0]}"
                cursor.execute('INSERT INTO yandex(name,cost,link)VALUES(?,?,?)',(product_name,new_cost,clean_link))
                
            except Exception as e:
                continue
        conn.commit()
        logging.info('Данные сохранены в бд')
        conn.close()
            
                
                
        print('Данные спаршены')
def allparser():
    print(' Выберите вариант:\n1. Спарсить Wildberries\n2. Спарсить Ozon\n3. Спарсить YandexMarket'
    )
    choose_parser = input()
    if choose_parser == '1':
         logging.info('Был выбран парсер Wildberries')
         print('Вы выбрали Wildberries')
         wb()
    elif choose_parser == '2':
        logging.info('Был выбран парсер Ozon')
        print('Вы выбрали Ozon')
        ozon()
    elif choose_parser == '3':
         logging.info('Был выбран парсер YandexMarket')
         print('Вы выбрали YandexMarket')
         yan()
    else:
         logging.warning('Ошибка, вы выбрали недоступный парсер')
         print('Ошибка, вводите только доступные числа')
def clear_logs():
    what_do = input('Выберите число\n1.Просмотреть логи\n2.Очистить логи\n')
    if what_do == '2':
        if os.path.exists('parser.log'):
            with open('parser.log', 'w', encoding='utf-8') as f:
                f.write('')  
            print('Логи очищены')
        else:
            print('Файл логов не найден')
    elif what_do =='1':
        with open('parser.log','r') as logs:
            for log in logs:
                print(log.strip())
    else:
        print('Введите только доступный вариант')
            

#Основной интерфейс
while True:
    print('Выберите один из вариантов\n' \
    '1. Cпарсить маркетплейс(wb,ozon,yandex market)\n' \
    '2. Взаимодействие с логами\n'
    '3. Взаимодействие с базой данных\n'
    '4. Закрыть программу')
    choose = input()
    if choose == '1':
        logging.info('Выбран вариант "Спарсить маркетплейс"')
        allparser()
    elif choose == '2':
        clear_logs()
    elif choose == '3':
         view()
         
    elif choose == '4':
        logging.info('Программа была закрыта')
        break
    else:
        logging.warning('Выбрали недоступный вариант')
        print('Ошибка введите одну из доступных команд')
