#  coding: utf-8
import win32api
import pyDes
from binascii import b2a_hex, a2b_hex
import base64
import http.client,datetime
import os, random, pyperclip
def getCVolumeSerialNumber():
    CVolumeSerialNumber=win32api.GetVolumeInformation("C:\\")[1]
    # print(CVolumeSerialNumber)
    if CVolumeSerialNumber:
        return str(CVolumeSerialNumber)
    else:
        return 0

def getLastTime():
    '''
    获取试用版最后的时间
    '''
    try:
        bjTime = datetime.datetime.strptime(getBeijinTime(),"%d %b %Y %H:%M:%S")
        #bjDatetime=datetime.datetime.strptime(bjTime, "%d %b %Y %H:%M:%S")
        lastTime=bjTime+datetime.timedelta(days=30)
        #datetime 转string--->strftime
        return lastTime.strftime('%d %b %Y %H:%M:%S').strip()
    except Exception as e:
        print("获取网络时间异常，请检查网络是否正确：{}".format(e))
        return None    

def getBeijinTime():
    try:
        conn=http.client.HTTPConnection("www.baidu.com")
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
    if os.path.isfile('conf.bin'):
        with open('conf.bin', 'rb') as fp:
            key = a2b_hex(fp.readline().strip())
            #print(key)
        serialnumber = getCVolumeSerialNumber()
        decryptstr = DesDecrypt(key).decode('utf8')
        #print(decryptstr)
        if serialnumber in decryptstr:
            if 'Buy' in decryptstr:
                #print('>> Buy')
                print(">> 注册版验证完成")
                return 1
            elif 'Trial' in decryptstr:
                if daysRemaining():
                    print('>> 30天试用版验证通过')
                    return 1
                else:
                    
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
                if 'Buy' in decryptstr:
                    #print('>> Buy')
                    with open('conf.bin', 'wb') as fp:
                        fp.write(b2a_hex(key.encode('utf8'))+b'\r\n')
                        fp.write(b2a_hex('0'.encode('utf8'))+b'\r\n')
                        print(">> 验证完成")
                    return 1
                elif 'Trial' in decryptstr:
                    with open('conf.bin', 'wb') as fp:
                        fp.write(b2a_hex(key.encode('utf8'))+b'\r\n')
                        fp.write(b2a_hex(getLastTime().encode('utf8'))+b'\r\n')                        print(">> 验证完成")
                    return 1
        except Exception as e:
            print(e)
            print(">> 输入错误")
            continue
if __name__ == "__main__":
    Register()