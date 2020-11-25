# -*- coding: utf8 -*-  
import configparser
import datetime
import logging
import register
import pickle,codecs
#import win32api,win32com
import os, ast,re,sys,time,chardet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from  selenium.common.exceptions import NoSuchElementException
from PIL import Image
#from fake_useragent import UserAgent
#达人首页id号
#小baby(522915)
#改革春风吹满地(511254)
#家电大大咖(528614)
#数码家电(516694)
#ua = UserAgent()
appName='oneKeyUpload'
ver = 'V1.0.0.0'
#OUT_PATH= os.path.dirname(os.path.dirname(__file__)) +'/config.txt'
confPath = os.path.dirname(os.path.realpath(sys.argv[0]))

dpHandle = None
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

def gettime():
    now=datetime.datetime.now()
    #log.info(now.strftime("%Y-%m-%d %H:%M:%S"))
    return now.strftime('<%Y-%m-%d %I:%M:%S>')

class uploadContents(object):
    def __init__(self):
        self.config=self.readfile(confPath + '\config.txt')
        self.option=self.webSetOptions(True)
        self.driver = webdriver.Chrome(options=self.option)
        
        # log.info(self.get_data('homeId').strip(',').split(','))
        self.homeIdList=list(self.get_data('homeId').strip(',').split(','))
        self.cf = configparser.ConfigParser()
        self.userName = self.get_data('userName')
        self.password = self.get_data('userPwd')
        self.ckFile=confPath+"\\"+self.userName+"_cookies"
        self.loginUrl = self.get_data('drHomeUrl')
        self.uploadCount =  int(self.get_data('uploadCount'))
        self.praiseRate = int(self.get_data('praiserate'))
        self.praiseNum = int(self.get_data('praisenum'))
        self.commission = float(self.get_data('commission'))
        self.curCount = 1
        self.curPath = confPath
        self.driver.get(self.loginUrl)
        self.driver.implicitly_wait(10)
        self.readCk()
        #self.driver.get('https://dr.jd.com')
        
        #self.loginDr()
        #cookiesList=self.driver.get_cookies()
        #print(cookiesList)
    def readfile(self, file_path):
        config = configparser.ConfigParser()
        try:
            with open(file_path, 'rb') as f:
                cur_encoding = chardet.detect(f.read())['encoding']
                #print (cur_encoding)    
                config.read(file_path,encoding=cur_encoding)
            return config    
        #config = codecs.open(confPath,'r','utf-8').read()
        except Exception as e:
            logging.error("读取配置失败 %s" % e)
            sys.exit(1)

    def getCkAndLogin(self):
        self.loginDr()
        cookies = {}
        #print(self.driver.get_cookies())
        for item in self.driver.get_cookies():
            cookies[item['name']] = item['value']
        #print(cookies)
            outputPath = open(self.ckFile,'wb')
        #win32api.SetFileAttributes(outputPath,win32con.FILE_ATTRIBUTE_HIDDEN)
        pickle.dump(cookies,outputPath)
        outputPath.close()
        return cookies
    def read_cookie(self):
        if os.path.exists(self.ckFile):
            ctime = os.path.getctime(self.ckFile)#获取文件创建时间
            create = datetime.datetime.fromtimestamp(ctime) + datetime.timedelta(days=+1)  #当前天加1
            nowdate = datetime.datetime.now()
            if(nowdate>create):
                os.remove(self.ckFile)
                return False
            else:
                try:
                    with open("cookies%s" % self.uid, "rb") as fs:
                        data = pickle.load(fs)
                    return data
                except:
                    get_logger().info("Cookies Not In Disk")
                    return False
                
    def readCk(self):
        if os.path.exists(self.ckFile):
            ctime = os.path.getctime(self.ckFile)#获取文件创建时间
            create = datetime.datetime.fromtimestamp(ctime) + datetime.timedelta(days=+1)  #当前天加1
            nowdate = datetime.datetime.now()
            if(nowdate>create):
                os.remove(self.ckFile)
                self.getCkAndLogin()
            else:
                with open(self.ckFile,'rb') as readPath:
                    cookies = pickle.load(readPath)
                    strdays=(datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                    ts = int(time.mktime(time.strptime(strdays, "%Y-%m-%d %H:%M:%S")))     #换成时间戳：当前时间+365天的cookies有效期   
                    for cookie in cookies:
                        self.driver.add_cookie({
                            "domain":".jd.com",
                            "name":cookie,
                            "value":cookies[cookie],
                            "path":'/',
                            "expires":ts
                        })    
                time.sleep(1)
                self.driver.get('https://dr.jd.com')
        else:
            self.getCkAndLogin()
            #readPath = open(self.ckFile,'rb')
            #cookies = pickle.load(readPath)
            #strdays=(datetime.datetime.now()+datetime.timedelta(days=360)).strftime("%Y-%m-%d %H:%M:%S")
            #ts = int(time.mktime(time.strptime(strdays, "%Y-%m-%d %H:%M:%S")))     #换成时间戳：当前时间+365天的cookies有效期   
            #for cookie in cookies:
                #self.driver.add_cookie({
                    #"domain":".jd.com",
                    #"name":cookie,
                    #"value":cookies[cookie],
                    #"path":'/',
                    #"expires":ts
                #})      
            #readPath.close()
            #self.driver.get('https://dr.jd.com')
            #try:
                #self.driver.find_element_by_xpath('//*[@class="main-nav"]')
            #except NoSuchElementException as e:
                #self.getCkAndLogin()
        #else:
            #cookies = self.getCkAndLogin()
        #return cookies        
    
    def webSetOptions(self,needOption=False):
        if needOption:
            #userA = ua.random
            options = webdriver.ChromeOptions()
            #self.option.add_argument('--headless')
            options.add_argument('disable-infobars')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--log-level=3')
            options.add_argument('--start-maximized')
            #prefs = {"profile.managed_default_content_settings.images":2}
            #options.add_experimental_option("prefs", prefs)
            #self.option.add_argument('--user-agent=%s'%userA)
            return options
        else:
            return None

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
            log.error(r"获取参数失败 %s" % e)
    
       
    # 拉所有能识别的产品
    def getAllContents(self,dataId):
        pass

    def isElementExist(self,element):
        flag=True
        try:
            self.driver.find_element_by_css_selector(element)
            return flag
        except:
            flag=False
            return flag
        
    def removeSecImgs(self,secId,pics='none'):
        self.cf.remove_section(secId)
        #for pig in pics:
            #os.remove(self.curPath+'\\'+pig)
        with open(self.curConfigFile, 'w+', encoding='utf-8-sig') as files:
            self.cf.write(files)
        #self.cf.write(open(self.curConfigFile,"w+"))     
        
    def checkFileExist(self, fName):
        pass
   
    def getDrIdList(self, dict_name):
        for root, dirs, files in os.walk(dict_name):  
            #log.info('root:{}'.format(root)) #当前目录路径
            if len(dirs) > 0:
                return dirs
            else:
                return []
            #log.info('dirs:{0},type:{1}'.format(dirs[1], type(dirs[1]))) #当前路径下所有子目录  
            #log.info('files:{}'.format(files)) #当前路径下所有非目录子文件
            
    def getIniConfig(self, drId):
        try:
            drPath='{}\\{}\\{}.ini'.format(confPath, drId, drId)
            with open(drPath, 'rb') as f:
                cur_encoding = chardet.detect(f.read())['encoding']
                self.cf.read(drPath,encoding=cur_encoding)
            
            #self.cf.read('{}\\{}\\{}.ini'.format(confPath, drId, drId),encoding='utf-8-sig')
            self.curPath = '{}\\{}'.format(confPath,drId)
            self.curConfigFile = '{}\\{}\\{}.ini'.format(confPath, drId, drId)
        #config = codecs.open(confPath,'r','utf-8').read()
        except Exception as e:
            log.error("读取配置{0}.ini失败;请检查是否存在该文件信息，失败日志:{1}".format(drId, e))
            self.tearDown()
            sys.exit(1)
    def createWenzhangContent(self,secId):
        pass
    def createDanpinContent(self,secId):
        #time.sleep(2)
        pics = (self.cf.get(secId,'pic'))
        pic = ast.literal_eval(pics)   # 将"['1234.jpg','2343.jpg','2234.jpg']"类型的字符串转换成列表
        img1 = self.curPath+'\\'+pic[0]
        #img2 = self.curPath+'\\'+pic[1]
        #img3 = self.curPath+'\\'+pic[2]
        #等待《添加商品》按钮可见
        try:
            WebDriverWait(self.driver,15).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="module-collection"]/div[1]/input'))).click()
            #self.driver.find_element_by_xpath('//*[@id="module-collection"]/div[1]/input').click()   #点击《添加商品》
        except:
            pass
        
        time.sleep(0.5)
        # 等待插入商品页面加载,直到"输入商品链接"输入框显示出来
        inputUrls=WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.XPATH,'//*[@class="jd-modal"]/div/div[3]/div/input')))
        #time.sleep(2)
        #inputUrls = self.driver.find_element_by_css_selector('.jd-modal-footer > #ui-input > input')  # 输入商品 URL
        time.sleep(0.1)  
        inputUrls.send_keys(self.cf.get(secId,'url'))
        inputUrls.send_keys(Keys.CONTROL,'a')
        time.sleep(0.2) 
        inputUrls.send_keys(Keys.CONTROL,'x')
        time.sleep(0.2) 
        inputUrls.send_keys(Keys.CONTROL,'v')
        actions = ActionChains(self.driver) 
        addBaby = self.driver.find_element_by_css_selector('.ui-btn-search:nth-child(4)')  #点击《添加宝贝》
        time.sleep(1)
        #actions = ActionChains(self.driver)     
        #actions.move_to_element(addBaby).click().perform()
        addBaby.click()
        time.sleep(2)
        try:
            # 判断是否添加了商品（商品是否已经添加过），找不到商品说明已经添加过,点取消返回
            self.driver.find_element_by_xpath('//*[@class="choose-list"]/li')
            #WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH, '//*[@class="choose-list"]/li')))   
            #WebDriverWait(self.driver, 3,1).until(lambda x:x.find_element_by_xpath('//*[@class="choose-list"]/li').is_displayed())
            #WebDriverWait(self.driver, 10, 0.5).until_not(ec.visibility_of_element_located((By.XPATH, '//*[@class="choose-list"]/li')),"2222")            
        except:
            #点击取消返回
            self.driver.find_element_by_xpath('//*[@class="jd-modal-footer choose-list-btns"]/input[2]').click()
            log.error("{}已经添加过啦！继续添加下一个".format(secId.split('_')[0]))
            self.removeSecImgs(secId,pic)
            return
        #判断做完,开始点击确定按钮添加商品
        self.driver.find_element_by_css_selector('.ui-btn-prev:nth-child(7)').click()
        '''判断某个元素在是否存在于dom或不可见,如果可见返回False,不可见返回这个元素'''
        #WebDriverWait(self.driver,10).until(ec.invisibility_of_element((By.XPATH,'//*[@class="jd-modal"]')))
        #点击《编辑商品》，对商品的2个附图进行编辑
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="module-collection"]/ul/li/div/div[1]').click()
        time.sleep(1)
        #WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.XPATH,'//*[@class="jd-modal"]')))
        #有时候点击没有上传的组件，所以多试几下
        for i in range(1,11):
            try:
                time.sleep(0.5)
                # 定位  //div[contains(text(),'上传照片')]
                self.driver.find_element_by_xpath('//div[contains(text(),"上传照片")]')
                break
            except:
                time.sleep(1)
                #self.driver.find_element_by_xpath('//*[@id="module-collection"]/ul/li/div/div[1]').click()
                self.driver.find_element_by_xpath('//*[@class="jd-modal"]/div/div[3]/input[1]').click()  #取消按钮
                time.sleep(0.5)
                self.driver.find_element_by_xpath('//*[@id="module-collection"]/ul/li/div/div[1]').click()
                time.sleep(1)
        time.sleep(1.5)
        #点击取消默认勾选的两幅图
        for clickItem in self.driver.find_elements_by_xpath('//*[@class="right-check select on"]'):
            time.sleep(1)
            clickItem.click()
            time.sleep(0.2)
        #添加2个附图
        try:
            for i in range(2, 0, -1):
                #time.sleep(2)
                ele=self.driver.find_element_by_xpath('//div[contains(text(),"上传照片")]/../div[2]/input')
                time.sleep(1)
                picId=self.curPath+'\\'+pic[i]
                #if not os.path.exists(picId):
                    #log.info('找不到[{0}]'.format(picId)) 
                
                ele.send_keys(picId)
                time.sleep(1)
                self.driver.find_element_by_xpath('(//input[@value="上传"])[1]').click()
                #log.info("点击了上传按钮")
                try:
                    #WebDriverWait(self.driver, 10).until_not(ec.presence_of_element_located((By.XPATH, '//*[@class="jd-modal-body cutupload-modal-body"]')))   #等到编辑附图上传页面消失
                    WebDriverWait(self.driver, 10).until(ec.invisibility_of_element((By.XPATH, '//*[@class="image-cut-upload"]/div/div')))                
                    #time.sleep(2)
                    pass
                except:
                    self.driver.find_element_by_xpath('//*[@class="jd-modal-body cutupload-modal-body"]/../div[3]/input[1]').click() # 取消回到编辑商品页面
                    #log.info("上传失败，点击了取消按钮")
                    time.sleep(1)
                    self.driver.find_element_by_xpath('//*[@class="jd-modal"]/div/div[3]/input[1]').click()  # 从编辑商品页面取消回到单品主页
                    #log.info("点击了取消回到单品主页")
                    time.sleep(1)
                    log.error("由于图片问题导致上传商品【{}】失败，放弃添加，继续下一个".format(self.cf.get(secId,'title')))
                    self.removeSecImgs(secId,pic)
                    return            
        except:
            log.info('找不到图片:{0} ,放弃添加，继续下一个'.format(picId)) 
            self.removeSecImgs(secId,pic)
            return
            
        #附图编辑完毕，点击《确定》返回
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@class="jd-modal"]/div/div[3]/input[2]').click()
        #WebDriverWait(self.driver, 10, 0.5).until_not(ec.invisibility_of_element((By.XPATH, '//*[@class="jd-modal"]/div/div[3]/input[2]')))   # 等待确定按钮消失
        time.sleep(1)
        # ------------------------------结束编辑商品----------------------------------
        self.driver.find_element_by_css_selector('#module-text>div>input').clear()  #清空单品标题(推荐主题)
        self.driver.find_element_by_css_selector('#ui-textarea>textarea').clear()   #清空单品描述(推荐理由)
        self.driver.find_element_by_css_selector('#module-text>div>input').send_keys(self.cf.get(secId,'title'))  #输入单品标题(推荐主题)
        time.sleep(0.5)
        self.driver.find_element_by_css_selector('#ui-textarea>textarea').send_keys(self.cf.get(secId,'description'))  #输入单品描述(推荐理由)
        time.sleep(1)
        #添加首页图
        self.driver.find_element_by_css_selector('.image-cut-upload>input').send_keys(img1)
        time.sleep(2)
        #jsEle = "var q=document.getElementsByClassName('cropper-crop-box')[0];q.style.transform = 'none';"
        #jsEle = "var q=document.getElementsByClassName('cropper-crop-box')[0];q.style.width = '300px';q.style.height = '300px';q.style.transform='none';"
        #self.driver.execute_script(jsEle)
        # -----------------------鼠标调整封面图适应操作---------------------------------
        try:
            source = self.driver.find_element_by_xpath('//*[@class="cropper-face cropper-move"]')
            source1 = self.driver.find_element_by_xpath('//*[@class="cropper-point point-se"]')
            im = Image.open(img1)
            w,h = im.size
            if w>=800:
                actions = ActionChains(self.driver) 
                actions.drag_and_drop_by_offset(source,-50,-50).perform()
                actions.drag_and_drop_by_offset(source1,100,100).perform()
        except:
            pass
        # ----------------------------------------------------------------
        time.sleep(1)
        self.driver.find_element_by_css_selector('.image-cut-upload>div>div>div:nth-child(3)>input:nth-child(2)').click()  # 点击上传
        #WebDriverWait(self.driver, 20, 0.5).until_not(
            #ec.visibility_of_element_located((By.XPATH, '//*[@class="jd-modal-body cutupload-modal-body"]')))     # 等待裁剪窗口消失
        time.sleep(3)
        # 点击<保存草稿>
        savebtn = self.driver.find_element_by_css_selector('.save-col>div:nth-child(2)>input:nth-child(1)')
        actions = ActionChains(self.driver) 
        actions.move_to_element(savebtn).click().perform()
        time.sleep(1)
        log.info("{0}:上传第【{1}】个单品【{2}】成功".format(secId.split('_')[0],str(self.curCount), self.cf.get(secId,'title')))
        self.curCount += 1
        self.removeSecImgs(secId,pic)
        time.sleep(2)
        #self.driver.find_element_by_link_text(u'预览后提交').click()
        
    def loginDr(self):
        try:
            self.driver.switch_to.frame('login_frame')
            WebDriverWait(self.driver, 20, 0.5).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="paipaiLoginSubmit"]')))
            self.driver.find_element_by_id('loginname').clear()
            self.driver.find_element_by_id('loginname').send_keys(self.userName)
            self.driver.find_element_by_xpath('//*[@id="nloginpwd"]').clear()
            self.driver.find_element_by_xpath('//*[@id="nloginpwd"]').send_keys(self.password)
            self.driver.find_element_by_xpath('//*[@id="paipaiLoginSubmit"]').click()
            time.sleep(2)
            while self.driver.current_url == self.loginUrl:
                continue
            log.info("登陆成功,开始操作创作")            
        except Exception as e:
            log.error('登录后台失败，请检查，失败原因:{}'.format(e))
            quit() 
            self.tearDown()
    def check(self,cstr,compareNum):
        digitList=list(map(float,re.findall(r"\d+\.?\d*",cstr)))
        if '万' in cstr:
            return (digitList[0]*10000)>=compareNum
        else:
            return digitList[0]>=compareNum
        
    def checkProduct(self,secId):
        # 点击<选品工具>
        WebDriverWait(self.driver,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'.main-nav>li:nth-child(3)>ul>li:nth-child(3)'))).click()
        #xp=WebDriverWait(self.driver,10).until(ec.element_to_be_clickable(By.CSS_SELECTOR,'.main-nav>li:nth-child(2)>ul>li:nth-child(3)'))
        #self.driver.find_element_by_css_selector('.main-nav>li:nth-child(2)>ul>li:nth-child(3)').click()  
        '''判断《选全站》元素中是否可见并且是enable的，代表可点击'''  
        time.sleep(1)
        WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="ui-search"]/button')))
        try:
            inputs=self.driver.find_element_by_xpath('//*[@class="ui-search-input"]')
            inputs.send_keys(Keys.CONTROL,'a')
            time.sleep(0.1) 
            inputs.send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath('//*[@id="ui-search"]/input').send_keys(self.cf.get(secId,'url'))
            #time.sleep(0.)
            #点击《选全站》
            self.driver.find_element_by_xpath('//*[@id="ui-search"]/button').click()
            #WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="ui-search"]/button'))).click()
            time.sleep(1)
            #如果搜索没有找到商品，则返回false
            try:
                self.driver.find_element_by_xpath('//*[@class="mate_search_item_img"]')
                time.sleep(1)
            except:
                log.info('没有搜到商品{0}，放弃上传并删除'.format(secId.split('_')[0]))
                self.removeSecImgs(secId)
                return False
            #获取佣金值
            yongjin=self.driver.find_element_by_xpath('//*[@class="cpsPrice"]/span').text
            yongjinOk=self.check(yongjin, self.commission)
            if not yongjinOk:
                log.info('{0}的佣金没有大于或等于{1}，放弃上传并删除'.format(secId.split('_')[0],self.commission))
                self.removeSecImgs(secId)
                return False            
            #获取好评数
            haopingStr=self.driver.find_element_by_xpath('//*[@class="mate_content"]/ul/li[1]/div[1]/p[4]').text
            haopingshu=(haopingStr.split('|'))[0]
            haopingshuOk=self.check(haopingshu, self.praiseNum)
            if not haopingshuOk:
                log.info('{0}的好评数没有大于或等于{1}，放弃上传并删除'.format(secId.split('_')[0],self.praiseNum))
                self.removeSecImgs(secId)
                return False           
            #获取好评率
            haopinglv=(haopingStr.split('|'))[1]
            haopinglvOk=self.check(haopinglv, self.praiseRate)
            if not haopinglvOk:
                log.info('{0}的好评率没有大于或等于{1}%，放弃上传并删除'.format(secId.split('_')[0],self.praiseRate))
                self.removeSecImgs(secId)
                return False
            log.info('{0}条件满足上传要求,准备上传'.format(secId.split('_')[0]))
            return (yongjinOk and haopingshuOk and haopinglvOk)
        except Exception as e:
            log.info('{0}的产品信息获取失败，默认满足上传条件，准备上传'.format(secId.split('_')[0]))
            return True            

    def uploadProduct(self,secId):
        #self.driver.find_element_by_css_selector('.main-nav>li:nth-child(2)>ul>li:nth-child(1)').click()
        self.driver.find_element_by_css_selector('.main-nav>li:nth-child(3)>ul>li:nth-child(1)').click()
        time.sleep(1)
        if secId.split('_')[1] == '100':    # 单品
            #if not danpinIsClick:
            time.sleep(1)
            self.driver.find_element_by_link_text(u'单品').click()  #点击《单品》
            h = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != self.driver.current_window_handle:
                    dpHandle = handle
            self.driver.switch_to.window(dpHandle)
            #danpinIsClick=True
            self.createDanpinContent(secId)
            self.driver.close()
            self.driver.switch_to.window(h)
        elif secId.split('_')[1] == '0':   # 文章
            self.createWenzhangContent(secId)
        elif secId.split('_')[1] == '50':  # 清单
            pass
        
    def startCreateContent(self, drId):
        
        #try:
        #WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="new-homepage"]/main/div[2]')))
        #self.driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/ul/li[2]/ul/li[1]').click()\
        for sc in self.cf.sections():       
            if self.curCount <= self.uploadCount:
                if self.checkProduct(sc):
                    self.uploadProduct(sc)
            else:
                break
          
    def startRun(self):
        try:
            drIdList = self.getDrIdList(confPath)
            if len(drIdList) > 0:
                for drId in drIdList:
                    if drId in self.homeIdList:
                        self.getIniConfig(drId)
                        self.startCreateContent(drId)
                        pass
                if self.curCount>=self.uploadCount:
                    log.info("上传完毕，本次上传{}个产品".format(self.uploadCount))  
            else:
                log.info("该目录下找到符合条件的文件夹或单品，请先运行onekeyCopy程序获取单品信息")
                self.tearDown()
        except Exception as e:
            log.error('在[startRun]函数运行异常，异常信息：{}'.format(e))
            self.tearDown()

    def tearDown(self):
        # 退出Chrome浏览器
        log.info("程序运行完成，5秒钟后自动关闭")
        time.sleep(5)
        self.driver.quit()
        #os.system('taskkill /im chromedriver.exe /F')

if __name__ == '__main__':
    #log.info(u"请输入首页ID号：")
    #homeId = input(u"请输入首页ID号，然后回车：")
    log.info("********启动京东达人[%s],版本号:%s********"% (appName,ver))
    if register.Register() == 1:
        cp=uploadContents()
        cp.startRun()
    else:
        log.error(gettime()+'程序注册失败')
        time.sleep(2)
        sys.exit()        