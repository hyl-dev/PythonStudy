import urllib.request
import re

def getPriceAndScores(url):
    url=url.replace('www.','m.')
    opener = urllib.request.build_opener()
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
    opener.addheaders = [headers]
    data=opener.open(url).read()
    data= data.decode('utf-8')
    scores=re.compile(r'<span class="star star-(.*?)"></span>',re.DOTALL).findall(data)
    scores = int(scores[0])/10
    price =re.compile(r'<span class="price">(.*?)</span>',re.DOTALL).findall(data)
    price = int(''.join(price ))
    return price,scores

if __name__ == "__main__":
    url="http://www.dianping.com/shop/5159161"
    (price,scores)=getPriceAndScores(url)
    print(price)
    print(scores)