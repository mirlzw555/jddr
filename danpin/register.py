#  coding: utf-8
#import win32api
#from win32ctypes.pywin32 import win32api as win32api
import win32api
import win32con 
import pyDes
from binascii import b2a_hex, a2b_hex
import base64
import http.client,datetime,socket
import os, random, pyperclip
def getCVolumeSerialNumber():
    CVolumeSerialNumber=win32api.GetVolumeInformation("C:\\")[1]
    # print(CVolumeSerialNumber)
    if CVolumeSerialNumber:
        return str(CVolumeSerialNumber)
    else:
        return 0

def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'http')
    print(myaddr[0][4][0])

def getBeijinTime():
    try:
        #getIP('www.jd.com')
        conn=http.client.HTTPConnection("www.jd.com")
        conn.request("GET", "/")
        r=conn.getresponse()
        ts=  r.getheader('date') #获取http头date部分
        #将 转换成北京时间

        #string转datetime--->strptime
        ltimeDTime=datetime.datetime.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
        #gmt转成北京时间
        bjTime=ltimeDTime+datetime.timedelta(hours=8)
        #bjTime=bjTime-datetime.timedelta(days=-1)
        
        #datetime 转string--->strftime
        return bjTime.strftime('%d %b %Y %H:%M:%S').strip()
    except Exception as e:
        print("网络异常，请检查网络是否能正常联网：{}".format(e))
        return None
#types等于d表示天数，否正表示小时
def daysRemaining(timeStr,types="d"):
    try:
        bjTime=datetime.datetime.strptime(getBeijinTime(), "%d %b %Y %H:%M:%S")
        lastTime=datetime.datetime.strptime(timeStr, "%d %b %Y %H:%M:%S")
        #return (lastTime-bjTime).days+1
        #return ((lastTime-bjTime).days+1)*24
        if types=='d':
            return (lastTime-bjTime).days-1
        else:
            return (lastTime-bjTime).days*24+(lastTime-bjTime).seconds // 3600
    except Exception as e:
        print("获取网络时间异常，请检查网络是否正确：{}".format(e))
        pass
 
def DesEncrypt(str):
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None, padmode=pyDes.PAD_PKCS5)
    encryptStr = k.encrypt(str)
    string = base64.b64encode(encryptStr)
    # print(string)
    return string  # 转base64编码返回
 
def DesDecrypt(string):
    string = base64.b64decode(string)
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None, padmode=pyDes.PAD_PKCS5)
    decryptStr = k.decrypt(string)
    # print(decryptStr)
    return decryptStr
 
Des_Key = "jddr8888"  # Key
Des_IV = "jddr8888"  # 自定IV向量
def Register():
    if os.path.isfile('reg'):
        with open('reg', 'rb') as fp:
            key = a2b_hex(fp.read())
            #print(key)
        serialnumber = getCVolumeSerialNumber()
        deStrList = list(DesDecrypt(key).decode('utf8').strip(',').split(','))
        decryptstr = deStrList[0]
        lastTime=deStrList[1]
        #print(decryptstr)
        if serialnumber in decryptstr:            if 'Buy' in decryptstr:
                syTime=daysRemaining(lastTime)
                if syTime>0:
                    #print('月度版还剩{}天使用时间'.format(daysRemaining(lastTime)))
                    print(">> 程序还剩{0}天使用时间".format(syTime))
                    return 1
                else:
                    print('程序用时间已到期,请联系作者(微信:boss645)购买续费')
                    os.remove('reg')
                    return 2
            if 'Trial' in decryptstr:
                syTime=daysRemaining(lastTime,"h")
                if syTime>0:
                    #print('月度版还剩{}天使用时间'.format(daysRemaining(lastTime)))
                    print('试用版还剩{0}小时使用时间'.format(syTime))
                    return 1
                else:
                    print('试用版使用时间已到期,请联系作者购买续费')
                    os.remove('reg')
                    return 2
        else:
            print("找不到版本注册信息，验证不通过")
            return 2
        
        
        if serialnumber in decryptstr:
            if 'Buy' in decryptstr:
                syTime=daysRemaining(lastTime)
                #print('>> Buy')
                print(">> 计费版还剩{0}天使用时间".format(syTime))
                return 1
            elif 'Trial' in decryptstr:
                syTime=daysRemaining(lastTime)
                if syTime>0:
                    #print('月度版还剩{}天使用时间'.format(daysRemaining(lastTime)))
                    print('试用版还剩{0}小时使用时间'.format(syTime))
                    return 1
                else:
                    print('试用版使用时间已到期,请联系作者购买永久使用版')
                    os.remove('reg')
                    return 2
    rand = str(random.randrange(1, 1000))
    #获取系统C盘序列号作为识别ID，并添加随机数作为混淆，生成最终机器码。
    serialnumber = getCVolumeSerialNumber() + rand
    #print(serialnumber)
    encryptstr = DesEncrypt(serialnumber).decode('utf8')
    pyperclip.copy(encryptstr)
    print(">> 已经将序列号复制到剪贴板，把此序列号发给作者获取验证码填入以下验证码信息:", encryptstr)
    while True:
        key = input(">> 验证码:")
        try:
            decryptstr = DesDecrypt(key.encode('utf8')).decode('utf8')
            #print(decryptstr)
            if serialnumber in decryptstr:
                with open('reg', 'wb') as fp:
                    fp.write(b2a_hex(key.encode('utf8')))
                    win32api.SetFileAttributes('reg', win32con.FILE_ATTRIBUTE_HIDDEN)
                    print(">> 注册成功")
                return 1
            else:
                print(">> 注册失败")
                return 2
                #if 'Buy' in decryptstr:
                    # #print('>> Buy')
                    #with open('reg', 'wb') as fp:
                        #fp.write(b2a_hex(key.encode('utf8')))
                        #print(">> 注册成功")
                    #return 1
                #elif 'Trial' in decryptstr:
                    #with open('reg', 'wb') as fp:
                        #fp.write(b2a_hex(key.encode('utf8')))
                        #print(">> 注册成功")
                    #return 1
        except Exception as e:
            print(e)
            print(">> 输入错误")
            continue
if __name__ == "__main__":
    Register()