# pythonstudy
the process of studying python
#1 spider study
 it will record my spider studying.
  
 simplespider_1 using Python3.5 ,and spider the movie data of douban,then using xltw3 so that save the data to excel. when install
 
 xltw3 packets, it will occur the errors:ValueError: '__init__' in __slots__ conflicts with class variable ,you just modify as follows:
open Python33\Lib\site-packages\xlwt3\formula.py file ，and find the line

__slots__ = ["__init__",  "__s", "__parser", "__sheet_refs", "__xcall_refs"]

modify to 

__slots__ = [ "__s", "__parser", "__sheet_refs", "__xcall_refs"]
