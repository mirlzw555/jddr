#  coding: utf-8
 
import win32api
import pyDes
from binascii import b2a_hex, a2b_hex
import base64,pyperclip
import os, random,time
import datetime,http.client
def getCVolumeSerialNumber():
    CVolumeSerialNumber=win32api.GetVolumeInformation("C:\\")[1]
    # print(CVolumeSerialNumber)
    if CVolumeSerialNumber:
        return str(CVolumeSerialNumber)
    else:
        return 0
 
def DesEncrypt(string):
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None, padmode=pyDes.PAD_PKCS5)
    encryptStr = k.encrypt(string)
    string = base64.b64encode(encryptStr)
    # print(string)
    return string  # 转base64编码返回
 
def DesDecrypt(string):
    string = base64.b64decode(string)
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None, padmode=pyDes.PAD_PKCS5)
    decryptStr = k.decrypt(string)
    # print(decryptStr)
    return decryptStr

def getLastTime(dayCount,hour=2):
    '''
    获取试用版最后的时间
    '''
    try:
        bjTime = datetime.datetime.strptime(getBeijinTime(),"%d %b %Y %H:%M:%S")
        #bjDatetime=datetime.datetime.strptime(bjTime, "%d %b %Y %H:%M:%S")
        lastTime=bjTime+datetime.timedelta(days=dayCount,hours=hour+1)
        #datetime 转string--->strftime
        return lastTime.strftime('%d %b %Y %H:%M:%S').strip()
    except Exception as e:
        print("获取网络时间异常，请检查网络是否正确：{}".format(e))
        return None    

def getBeijinTime():
    try:
        conn=http.client.HTTPConnection("www.jd.com")
        conn.request("GET", "/")
        r=conn.getresponse()
        ts=  r.getheader('date') #获取http头date部分
        #将 转换成北京时间

        #string转datetime--->strptime
        ltimeDTime=datetime.datetime.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
        #gmt转成北京时间
        bjTime=ltimeDTime+datetime.timedelta(hours=8) 
        #datetime 转string--->strftime
        return bjTime.strftime('%d %b %Y %H:%M:%S').strip()
    except Exception as e:
        print("获取网络时间异常，请检查网络是否正确：{}".format(e))
        return None

def daysRemaining():
    try:
        pass 
    except Exception as e:
        print("获取网络时间异常，请检查网络是否正确：{}".format(e))
        pass
 
Des_Key = "jddr8888"  # Key
Des_IV = "jddr8888"  # 自定IV向量
if __name__ == "__main__":
    key1=input('请输入版本信息，注册版请输入b,试用版请输入t :')
    key3 = input('请输入天数:')
    key2 = input(">> 序列号:")
    try:
        if key1=='b':
            decryptstr = DesDecrypt(key2.encode('utf8')).decode('utf8') + 'Buy,' + getLastTime(int(key3),24)  
        #elif key1=='t':
            #decryptstr = DesDecrypt(key2.encode('utf8')).decode('utf8') + 'Trial,' + getLastTime(0)   
        else:
            decryptstr = DesDecrypt(key2.encode('utf8')).decode('utf8') + 'Trial,' + getLastTime(int(key3))   
        #decryptstr = DesDecrypt(key2.encode('utf8')).decode('utf8') + 'Buy123456'
        serialnumber = DesEncrypt(decryptstr)
        #print(decryptstr)
        if 'Buy' in decryptstr:
            print("注册终身版验证通过，验证码是：{}".format(str(serialnumber, encoding = "utf-8")))
            pyperclip.copy(str(serialnumber, encoding = "utf-8"))
        elif 'Trial' in decryptstr:    
            print("试用版本验证通过，验证码是：{}".format(str(serialnumber, encoding = "utf-8")))
            pyperclip.copy(str(serialnumber, encoding = "utf-8"))
        else:
            print('验证不通过')
    except Exception as e:
        print(">> 输入错误:{}".format(e))
    time.sleep(30)
