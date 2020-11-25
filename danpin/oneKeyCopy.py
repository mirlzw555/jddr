# -*- coding: utf8 -*-  
import configparser
import datetime
import hashlib
import logging
import register
import os, re
import random
import sys,chardet
import time
import urllib.request
from PIL import Image
#from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By  
from  selenium.common.exceptions import NoSuchElementException
#达人首页id号
#小baby(522915)
#改革春风吹满地(511254)
#家电大大咖(528614)
#ua = UserAgent()
appName='oneKeyCopy'
ver = 'V1.0.1.1'
#OUT_PATH= os.path.dirname(os.path.dirname(__file__)) +'/config.txt'
confPath = os.path.dirname(os.path.realpath(sys.argv[0]))

def get_logger():
    logPath=confPath+'\\log\\'
    logFileName=logPath+"%s_%s.log"%(appName,(datetime.datetime.today()).strftime('%Y-%m-%d'))
    if not os.path.exists(logPath):
        os.mkdir(logPath) 
    loggers = logging.getLogger()    
    fh=logging.FileHandler(logFileName)
    ch=logging.StreamHandler()
    loggers.addHandler(fh)
    loggers.addHandler(ch)
    logformat=logging.Formatter('%(asctime)s -> : %(message)s')
    fh.setFormatter(logformat)
    ch.setFormatter(logformat)
    loggers.setLevel(logging.INFO)
    return loggers
log = get_logger()

#OUT_PATH + "/rfcode/配置信息/key.txt".decode("utf-8")
danpinUrl = 'https://h5.m.jd.com/active/jmp/zhidemai/index.html?ad_od=1&id='
wenzhangUrl='https://h5.m.jd.com/active/faxian/html/innerpage.html?id='
qingdanUrl='https://h5.m.jd.com/active/youpin/qingdan/index.html?id='
#qingdanUrl='https://h5.m.jd.com/active/youpin/qingdan/index.html?id=221219392&style=50&ad_od=1&type=code'
productUrl = 'https://item.jd.com/'
        
class copyContents(object):
    def __init__(self):
        self.config=self.readfile(confPath + '\config.txt')
        self.webSetOptions()
        #self.driver = webdriver.Chrome()
        # print(self.get_data('homeId').strip(',').split(','))
        self.homeIdList=list(self.get_data('homeId').strip(',').split(','))
        self.cf = configparser.ConfigParser()
        self.homeId = ''
        self.homeUrl = ''
        self.scrollValue = int(self.get_data('scrollValue'))  #下拉滚动条滚动的基数
        self.dataSubposition = list(self.get_data('dataSubposition').strip(',').split(',')) 
        self.dataStyle = self.get_data('dataStyle')     #文章的类型，比如单品、视频、专辑、清单等等
        #self.dataSubposition=self.get_data('dataSubposition')  #渠道类型
        # self.contentCount = int(self.get_data('getArCount'))
        # self.quickBrowsing = self.get_data('quickBrowsing')
        self.idAndDataStyle={}
        self.picDicts={}
        self.danpinIdList = []
        self.wenzhangIdList = []
        self.qingdanIdList = []
        #print(self.homeHtml)
    def readfile(self, file_path):
        config = configparser.ConfigParser()
        try:
            with open(file_path, 'rb') as f:
                cur_encoding = chardet.detect(f.read())['encoding']
                print (cur_encoding)    
                config.read(file_path,encoding=cur_encoding)
            return config    
        #config = codecs.open(confPath,'r','utf-8').read()
        except Exception as e:
            logging.error("读取配置失败 %s" % e)
            sys.exit(1)

    def webSetOptions(self):
        #userA = ua.random
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        self.option.add_experimental_option("prefs", prefs)
        self.option.add_argument('--log-level=3')
        self.option.add_argument('--disable-infobars')
        #self.option.add_argument('--user-agent=%s'%userA)
        self.driver = webdriver.Chrome(options=self.option)
        
    def scroll(self, pagetype='subpage'):
        time.sleep(1)
        log.info(u"首页模拟滚动生成内容，生成完毕后才能获取内容ID进行分析")
        for i in range(100,self.scrollValue,500):
            self.driver.execute_script("window.scrollBy(0, {})".format(i))
            time.sleep(0.5)
            log.info("滚动条滚动基数：{0}".format(i))
        #浏览完随机(10-50秒)停 顿
        #time.sleep(random.randint(1,self.showDuration))
    #----------------------------------------------------------------------
    def get_data(self,key,title='KEY'):
        """
        参数配置
        :param title: 配置文件的头信息
        :param key: 配置文件的key值
        :return: 配置文件的value
        """
        try:
            value = self.config.get(title, key)
            return value
        except Exception as e:
            logging.error(r"获取参数失败 %s" % e)
    
    def picDownload(self, item, contentId, dstyle='100'):
        picList=[]
        tempPath=confPath+'\\'+self.homeId
        if not os.path.exists(tempPath):
            os.makedirs(confPath+'\\'+self.homeId) #如果没有这个path则直接创建
        if dstyle=='100':   # 单品时保存方式
            for i in range(1,4):
                try:
                    img = item.find_element_by_xpath('//*[@data-id='+contentId+']/div/div/div/img['+str(i)+']').get_attribute('data-src')
                    file_suffix = os.path.splitext(img)[1]
                    if file_suffix.lower() == '.png':
                        file_suffix = '.jpg'
                    #print(file_suffix)
                    filename = '{}{}'.format(tempPath+'\\' + contentId + '_'+str(i), file_suffix)   #拼接文件名。
                    #print(filename)
                    data=urllib.request.urlopen(img,timeout=5).read()
                    with open(filename, 'wb') as f:
                        f.write(data) 
                    #urllib.request.urlretrieve(img, filename=filename) #利用urllib.request.urltrieve方法下载图片
                    #大于1M的图片需要重新修改成小于1M，才能上传成功
                    size = os.path.getsize(filename)
                    with Image.open(filename) as imgLocal:
                        imgLocal = imgLocal.convert('RGB')
                        x,y = imgLocal.size
                        if (size > 1000000) or (x<800 or y<800):    
                            imgLocal = imgLocal.resize((800,800))
                            imgLocal.save(filename,"JPEG")   
                        #else:
                            #imgLocal.save(filename,"JPEG")  

                    picList.append('{0}{1}'.format(contentId + '_'+str(i),file_suffix))
                    #log.info('下载图片{0}成功'.format(contentId + '_'+str(i)+file_suffix))
                    log.info('下载图片{0}成功'.format(picList[i-1]))
                except IOError as e:
                    log.info('IOError图片下载异常:{0}'.format(e))
                    break
                except TimeoutError as e:
                    log.info('TimeoutError图片下载超时异常:{0}'.format(e))
                    break
                except Exception as e:
                    log.info('Exception图片下载异常:{0}'.format(e))  
                    break
            return picList
        # 文章：dstyle=='0'
        elif dstyle=='0':
            pass
        

    def set_data(self,contentId,dataStyle='100'):
        sec = '100'
        if dataStyle == '100':
            sec = contentId + '_100'
            time.sleep(0.5)
            self.driver.get(danpinUrl+contentId)
            #self.driver.implicitly_wait(20)
        elif dataStyle == '0':
            sec = contentId + '_0'
            self.driver.get(wenzhangUrl+contentId)
        elif dataStyle == '50':    
            sec = contentId + '_50'
            self.driver.get(qingdanUrl+contentId)
        try:    
            #WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//a[text()="去购买"]')))    
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="recommend-gobuy"]')))    
            title = self.driver.find_element_by_css_selector('.recommend-pro-title').text
            if title.find('%'):
                title=title.replace('%','%%')
            if len(title)<=0:
                logging.error('由于获取到的标题为空，可能是京东的bug或被京东发现爬虫正在爬取，请在浏览器输入： {0} 检查是否有内容'.format(danpinUrl+contentId))
                #continue
                return
            description = self.driver.find_element_by_css_selector('.recommend-pro-info').text
            if description.find('%'):
                description=description.replace('%','%%')
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="gobuy_right goJdMInfo"]'))) 
            #WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="recommend-pro-anchor goJdMInfo"]'))) 
        except NoSuchElementException as e:
            logging.error("出错ID:{0} 信息：找不到该页面元素。请在浏览器输入链接 {1} 看是否正常显示,错误信息:{2}".format(sec, self.driver.current_url,e))
            self.saveConfig()
            #continue
        
        #dataSkuId = self.driver.find_element_by_xpath('//*[@class="recommend-pro-anchor goJdMInfo"]').get_attribute('data-sku-id')
        dataSkuId = self.driver.find_element_by_xpath('//*[@class="gobuy_right goJdMInfo"]').get_attribute('data-sku-id')
        prUrl = productUrl + dataSkuId + '.html'
        pic=self.picDicts[contentId]
        if not self.cf.has_section(sec): #判断是否含有商品id这个section
            #self.cf.add_section(sec)#设置商品ID,即section
            self.cf[sec] = {
                "title": title,
                "description": description,
                "url": prUrl,
                "pic": pic
            }
            log.info("section为{0}的内容写入成功".format(sec))
            #self.cf.set(sec,"title",title) #设置商品标题
            #self.cf.set(sec,"description",description) #设置商品描述
            #self.cf.set(sec,"url",prUrl) #设置商品链接
            #self.cf.set(sec, "pic", contentId)  #设置图片存放地址
    # 拉单品
    def getDanpin_100(self,dataId):
        if len(dataId) > 0:
            return self.danpinIdList.append(dataId)
        else:
            return ""
        
    
    # 拉文章
    def getWenzhang_0(self,dataId):
        if len(dataId) > 0:
            return self.wenzhangIdList.append(dataId)
        else:
            return ""
    
    # 拉清单
    def getQingdan_50(self,dataId):
        if len(dataId) > 0:
            return self.qingdanIdList.append(dataId)
        else:
            return ""
    
    # 拉所有能识别的产品
    def getAllContents(self,dataId):
        pass
    
    def saveConfig(self):
        tempPath = confPath+'\\'+self.homeId
        if not os.path.exists(tempPath):
            os.mkdir(tempPath)        
        if len(self.cf.sections())>0:
            with open(tempPath+'\\'+self.homeId+'.ini', 'w', encoding='utf-8-sig') as configfile:
                self.cf.write(configfile)
            log.info('保存{0}文件成功，包含{1}个产品'.format(self.homeId+'.ini',len(self.cf.sections())))
        
    def startRun(self):
        try:
            log.info('本次分析获取的达人ID为：{0}'.format(','.join(self.homeIdList)))
            for homeid in self.homeIdList:
                self.homeId=homeid
                if self.homeId in ('522915','511254','528614','548782'):
                    log.info('八戒你又调皮了，怎能盗采你师傅的菜呢，小心师傅让大师兄揍你')
                    continue
                self.danpinIdList.clear()
                self.idAndDataStyle.clear()
                self.cf.clear()
                self.picDicts.clear()
                self.homeUrl='https://eco.m.jd.com/content/dr_home/index.html?authorId=' + self.homeId      #random.choice(self.darenId)
                self.driver.get(self.homeUrl)
                self.driver.implicitly_wait(10)
                log.info ("开始读取[%s]首页内容并分析" % self.driver.title)
                self.scroll('home')
                self.contentItems = self.driver.find_elements_by_xpath('//div[@id="container"]/div[2]/div[3]/div/ul/li')
                time.sleep(1)
                for item in self.contentItems:
                    lsId = item.get_attribute('data-id')
                    dataStyle = item.get_attribute('data-style')
                    dataSubPos =  item.get_attribute('data-subposition')
                    pics=[]
                    #if not self.dataSubposition[0] and dataSubPos.strip() !='-1' and dataStyle == '100':
                    if not self.dataSubposition[0] and dataStyle == '100':
                        pics=self.picDownload(item,lsId)
                        if len(pics)>=3:
                            self.picDicts[lsId]=pics
                            self.idAndDataStyle[lsId] = dataStyle
                    elif dataStyle == self.dataStyle and dataSubPos in self.dataSubposition:
                        pics=self.picDownload(item,lsId, dataStyle)
                        if len(pics)>=3:
                            self.picDicts[lsId]=pics
                            self.idAndDataStyle[lsId] = dataStyle
                    else:
                        logging.error('{0}的内容不是单品，放弃抓取，跳到下一个'.format(lsId))
                        
                        #保存图片信息
                        #self.imgFlag=True   #找不到三张图片，则不保存
                        #self.picDicts[lsId]=self.picDownload(item,lsId, '100')
                        #if self.imgFlag:
                            #self.idAndDataStyle[lsId] = dataStyle                        
                    #elif dataStyle == self.dataStyle and dataSubPos in self.dataSubposition:
                        # #保存图片信息
                        #self.imgFlag=True   #找不到三张图片，则不保存
                        #self.picDicts[lsId]=self.picDownload(item,lsId,dataStyle)
                        #if self.imgFlag:
                            #self.idAndDataStyle[lsId] = dataStyle
                        
                log.info("开始写入ini文件......")
                log.info("self.idAndDataStyle.keys包含的值：{}".format(self.idAndDataStyle.keys()))
                for k in self.idAndDataStyle.keys():
                    try:
                        self.set_data(k,self.idAndDataStyle[k])
                    except Exception as e:
                        log.info("写入{0}异常,跳转下一个循环：{1}".format(k,e))
                        self.saveConfig()
                        continue
                    #做判断
                self.saveConfig()
            self.tearDown()
        except Exception as e:
            logging.error('运行异常，异常信息：{}'.format(e))
            self.saveConfig()
            self.tearDown()
            
    def tearDown(self):
        # 退出Chrome浏览器
        self.driver.quit()
        #os.system('taskkill /im chromedriver.exe /F')

if __name__ == '__main__':
    #print(u"请输入首页ID号：")
    #homeId = input(u"请输入首页ID号，然后回车：")
    log.info("********启动京东达人[%s],版本号:%s********"% (appName,ver))
    if register.Register() == 1:
        cp=copyContents()
        cp.startRun()
    else:
        logging.error('程序注册失败')
        time.sleep(2)
        sys.exit()    