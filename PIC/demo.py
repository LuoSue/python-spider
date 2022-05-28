import re

import requests
from bs4 import BeautifulSoup

path = "./results"
baseurl = 'https://wallpaperscraft.com'
url = 'https://wallpaperscraft.com/catalog/anime'

headers = {
    'Cookie': '_ga=GA1.2.576102800.1639831674; _gid=GA1.2.230985776.1653673358; '
              '__gads=ID=7466a7214cdd6a35-225079c777d30036:T=1653673358:RT=1653673358:S'
              '=ALNI_MYMyqEXiCb65RKFh4GldYMAnc-u_g; '
              '__gpi=UID=000005dbac29601c:T=1653673358:RT=1653673358:S=ALNI_MYasVPmA3BliQegajbwBbO27q9w_Q; '
              '_gat_gtag_UA_11053870_8=1',
    'Host': 'wallpaperscraft.com',
    'Refer': 'https://wallpaperscraft.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
}


def get_page(pageNum):
    if pageNum == 1:
        page_args = ''
    else:
        page_args = 'page' + pageNum
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    imglist = soup.find_all(name="a", attrs={'class': 'wallpapers__link'})
    for img in imglist:
        url_args = img.get('href')
        new_url = baseurl + url_args

        response = requests.get(new_url, headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        span = soup.find_all(name='span', attrs={'class': 'wallpaper-table__cell'})
        img_url_args = span[1]

        img_new_url = baseurl + img_url_args.a.get('href')
        response = requests.get(img_new_url, headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        img_holder = soup.find(name='div', attrs={'class': 'wallpaper__placeholder'})
        img_result = img_holder.a.get('href')

        real_response = requests.get(url=img_result, headers=headers)
        name = re.split('/', img_result)[-1].strip('.jpg')
        print(name)
        try:
            with open(path + '/' + name + '.jpg', mode='wb') as f:
                f.write(real_response.content)
            f.close()
            print(name + "----------------下载完毕！")
        except Exception as error:
            print(error)
    print("----------------------第{}页图片下载完毕！----------------------".format(pageNum), '\n')


if __name__ == '__main__':
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    last_item = soup.find(name="li", attrs={'class': 'pager__item pager__item_last-page'})
    reobj = re.findall(r'\d+', last_item.a.get('href'))
    maxNum = reobj[0]

    for i in range(0, maxNum):
        get_page(i)
