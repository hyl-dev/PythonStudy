import urllib.request
import re

def getPicture(url,FileOut):
    webPage=urllib.request.urlopen(url)
    data = webPage.read()
    data = data.decode('UTF-8')
    
    picture_temp=re.compile(r'<img src="(.*?)%',re.DOTALL).findall(data)
    picture_url=picture_temp[0:3]
    for i in range(0,3):
        web = urllib.request.urlopen(picture_url[i])
        #print(web)
        itdata = web.read()
        f = open(FileOut+str(i+1)+'.jpg',"wb")
        f.write(itdata)
        f.close()
        
if __name__ == "__main__":
    url = "http://www.dianping.com/shop/5159161"
    
    HotelName=u"如家快捷酒店"
    FileOut ='.\\image\\'+HotelName
    getPicture(url,FileOut)