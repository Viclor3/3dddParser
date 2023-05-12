import csv
from requests_html import HTMLSession

session = HTMLSession()


def parser_href(file_path):
    furniture = []
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
        for url in urls_list:
            r = session.get(url)
            r.html.render(sleep=3, keep_page=True, scrolldown=3)
            try:
                block = r.html.find('.model-title')
                for item in block[:5]:
                    hrefs = item.find('a')
                    for href in hrefs:
                        furniture.append(href.absolute_links)
                        print(href.absolute_links)
            except Exception as ex:
                print('Ошибка')
    with open('furniture_hrefs.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for row in furniture:
            writer.writerow(row)


def parser_furniture(file_path):
    furniture = []
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
        for url in urls_list:
            r = session.get(url)
            r.html.render(sleep=3)
            with open('item.csv', 'a', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)
                try:
                    table = r.html.find('.model-info-block', first=True)

                    title = r.html.find('.title', first=True).text

                    try:
                        type = r.html.find("[itemprop='name']")[0].text
                    except:
                        type = None

                    try:
                        subtype = r.html.find("[itemprop='name']")[1].text
                    except:
                        subtype = None

                    try:
                        div = r.html.xpath('//*[@id="info-desktop"]/div[4]/table/tbody/tr[4]/td[2]/div', first=True)
                        color = div.attrs['style'].split('background-color: ')[1].split(';')[0]
                    except:
                        color = None

                    try:
                        style = table.find('tr', containing='Стиль:')[0].text.split('\n')[1]
                    except:
                        style = None

                    try:
                        length = table.find('tr', containing='Длина:')[0].text.split('\n')[1]
                    except:
                        length = None

                    try:
                        width = table.find('tr', containing='Ширина:')[0].text.split('\n')[1]
                    except:
                        width = None

                    try:
                        height = table.find('tr', containing='Высота:')[0].text.split('\n')[1]
                    except:
                        height = None

                    try:
                        materials = table.find('tr', containing='Материалы:')[0].text.split('\n')[1]
                    except:
                        materials = None
                    href = url
                    result = [title, type, subtype, materials, style, length, width, height, color, url]
                    writer.writerow(result)
                    print(result)
                except:
                    raise


def main():
    parser_furniture('result.csv')


if __name__ == "__main__":
    main()

