# -*- coding: utf-8 -*-
import urllib.request # встроеная
from bs4 import BeautifulSoup
import csv
import codecs

BASE_URL = 'http://weblancer.net/jobs/'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html)#.encode("ascii") # интерфейс страницы, позволяющий искать теги, просматривать их содержимое
    table = soup.find('div', {'class': 'container-fluid cols_table show_visited'})
    rows = table.find_all('div' , {'class' : 'row'})#[1:]
    #print(rows)

    projects = []

    for row in rows:
        cols = row.find_all('div')
        categories = row.find_all('a', {'class': 'text-muted'})
        #print(categories)
        projects.append({'title': cols[0].a.text,
                         'categories': [category.text for category in categories],
                         'price': cols[1].text.strip(), 'application': cols[2].text.strip()})# strip() удаляет все whitespace
    return projects

def get_page_count(html):#ф-я, возвращающая количество страниц
    soup = BeautifulSoup(html)
    paggination = soup.find('ul', {'class': 'pagination'})
   # print(paggination)
    return int(paggination.find_all('a')[-3].text)

def save(projects, path): # cохраняем распарсенные данные в csv файл
    with codecs.open(path, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile) # объект который будет записывать данные и передадим ему объект файла
        writer.writerow(('Project','Categories', 'Price', 'Applications'))# шапка таблицы

        for project in projects: # каждый проект будем записывать в отдельном ряду
            writer.writerow((project['title'], project['categories'], project['price'], project['application']))

def main():
    page_count = get_page_count(get_html(BASE_URL))
    print('Всего найдено страниц: %d' % page_count)
    projects = []
    for page in range(1, page_count):
        print('Текущий статус парсинга %d%%' % (page / page_count * 100))
        projects.extend(parse(get_html(BASE_URL + '?page = %d' % page)))# расшираем актуалнный список элементами из другого списка

    for project in projects:
        print(project)

    save(projects, 'projects.csv')
if __name__=='__main__':
    main()