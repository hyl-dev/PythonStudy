import urllib.request
import re
import os

def getHotelUrl(count):
    filename ='HotelUrl.txt'
    if os.path.exists(filename):
        os.remove(filename)  
    print("get the hotel URL of Haidian Beijing，and save to HotelUrl.txt")
    for page in range(1,51):  
        tempurl = "http://www.dianping.com/beijing/hotel/r17c274"+str(page)+"o10" 
        headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]  
        openurl = opener.open(tempurl)  
        data= openurl.read().decode(encoding='UTF-8')  
        linkre = re.compile(r'data-shop-url="(.*?)"\r\n   data-hippo', re.DOTALL).findall(data) 
       
        for url_shop in range(0, len(linkre)):  
            tempurlhotel = "http://www.dianping.com/shop/" + linkre[url_shop]   
            fileOp = open(filename, 'a', encoding="utf-8") 
            fileOp.write(str(count)+"\t"+tempurlhotel+'\n')  
            fileOp.close()
            count+=1
        print('the:  %d  page have completed！'%page) 
    
if __name__ == "__main__":
    count=1
    getHotelUrl(count)