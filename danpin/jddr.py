#coding:utf-8
import re
import os
import wx
import subprocess
import shutil
import register
import oneKeyCopy

class MainWindow(wx.Frame):
    def __init__(self, parent, title, pos, size):
        super(MainWindow, self).__init__(parent, title=title, pos=pos, size=size, style=wx.DEFAULT_FRAME_STYLE)

        self.__comList = []     # combox下拉列表

        # 获取Python路径
        self.GetDefaultPath()

        # 初始化界面
        self.InitUI()
# ------------------------------------------------------------------------------------------------------        
        self.okCopy = oneKeyCopy.copyContents()
        print(self.okCopy.homeIdList)
# ------------------------------------------------------------------------------------------------------        
        # 事件绑定
        self.BindEvent()

    def InitUI(self):
        """
        初始化界面
        """
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(0, 0)
    
        self.st_user = wx.StaticText(self.panel, wx.ID_ANY, u'达人登录账号:')
        self.tc_user = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_NO_VSCROLL)
        self.sizer.Add(self.st_user, pos=(0, 0), span=(1, 1), flag=wx.ALL, border=5)
        self.sizer.Add(self.tc_user, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        self.st_pwd = wx.StaticText(self.panel, wx.ID_ANY, u'达人登录密码:')
        self.tc_pwd = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_NO_VSCROLL)
        self.sizer.Add(self.st_pwd, pos=(0, 3), span=(1, 1), flag=wx.ALL, border=5)
        self.sizer.Add(self.tc_pwd, pos=(0, 4), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        
        #wx.CheckBox(self.panel)



        self.combox = wx.ComboBox(self.panel, wx.ID_ANY, choices=self.__comList, style=wx.CB_READONLY)
        #self.m_btnAdd1 = wx.Button(self.panel, wx.ID_ANY, u"添  加")
        self.sizer.Add(self.combox, pos=(2, 6), span=(1, 8), flag=wx.EXPAND | wx.ALL, border=5)
        #self.sizer.Add(self.m_btnAdd1, pos=(1, 8), span=(1, 1), flag=wx.ALL, border=5)

        #self.sbox2 = wx.StaticText(self.panel, wx.ID_ANY, u'需要打包exe的py文件:')
        #self.sizer.Add(self.sbox2, pos=(2, 0), span=(1, 1), flag=wx.ALL, border=5)
        #self.m_btnAdd2 = wx.Button(self.panel, wx.ID_ANY, u"添  加")
        #self.m_txtCtrl2 = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_READONLY)
        #self.sizer.Add(self.m_txtCtrl2, pos=(3, 0), span=(1, 8), flag=wx.EXPAND | wx.ALL, border=5)
        #self.sizer.Add(self.m_btnAdd2, pos=(3, 8), span=(1, 1), flag=wx.ALL, border=5)

        #self.sbox4 = wx.StaticText(self.panel, wx.ID_ANY, u'需要打包pyd的py文件:')
        #self.sizer.Add(self.sbox4, pos=(4, 0), span=(1, 1), flag=wx.ALL, border=5)
        #self.m_listBox = wx.ListBox(self.panel, wx.ID_ANY, style=wx.LB_EXTENDED)
        #self.sizer.Add(self.m_listBox, pos=(5, 0), span=(0, 9), flag=wx.EXPAND | wx.ALL, border=5)
        self.log = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.sizer.Add(self.log, pos=(5, 0), span=(0, 9), flag=wx.EXPAND | wx.ALL, border=5)
        #self.m_btnImport = wx.Button(self.panel, label=u"添  加")
        #self.m_btnDelete = wx.Button(self.panel, label=u"删  除")
        #self.m_btnPack = wx.Button(self.panel, label=u"打  包")
        self.m_btnImport = wx.Button(self.panel, label=u"开始下载单品")
        self.m_btnDelete = wx.Button(self.panel, label=u"开始上传单品")
        self.m_btnPack = wx.Button(self.panel, label=u"打  包")
        self.sizer.Add(self.m_btnImport, pos=(6, 6), flag=wx.ALL, border=5)
        self.sizer.Add(self.m_btnDelete, pos=(6, 7), flag=wx.ALL, border=5)
        self.sizer.Add(self.m_btnPack, pos=(6, 8), flag=wx.ALL, border=5)

        self.sizer.AddGrowableRow(5)
        self.sizer.AddGrowableCol(2)

        #状态栏
        self.CreateStatusBar()
        if len(self.__comList) > 0:
            self.getSysInfo(self.__comList[0])
            self.combox.SetValue(self.__comList[0])
            self.SetStatusText(self.sysName + "  python:" + self.pyVersion + "_" + self.pyBit)
        else:
            self.SetStatusText("Welcome...")

        self.panel.SetBackgroundColour(wx.Colour(240, 255, 255))
        self.panel.SetSizerAndFit(self.sizer)
        self.Centre()
        self.Raise()

    def BindEvent(self):
        """
        绑定事件
        """
        #self.Bind(wx.EVT_BUTTON, self.onAdd1, self.m_btnAdd1)
        #self.Bind(wx.EVT_BUTTON, self.onAdd2, self.m_btnAdd2)
        #self.Bind(wx.EVT_BUTTON, self.onImport, self.m_btnImport)
        #self.Bind(wx.EVT_BUTTON, self.onDelete, self.m_btnDelete)
        #self.Bind(wx.EVT_BUTTON, self.onPack, self.m_btnPack)
        #self.Bind(wx.EVT_LISTBOX_DCLICK, self.onListboxDoubleClick, self.m_listBox)
        #self.Bind(wx.EVT_COMBOBOX, self.comboxSelcet, self.combox)

    def GetDefaultPath(self):
        """
        获取默认的python路径，目前只使用与windows
        """
        path = os.environ['path']
        lst = path.split(';')
        for dir in lst:
            try:
                files = os.listdir(dir)
                for file in files:
                    if file == "python.exe":
                        self.__comList.append(dir)
            except:
                pass

    def getSysInfo(self, pythonPath):
        """
        指定python路径时收集系统信息
        """
        cmd = pythonPath + "\python.exe -c "
        cmd += "\"import platform; print(platform.architecture())\""
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        rtn = p.stdout.read()
        strtn = bytes.decode(rtn,encoding="utf-8")
        if '32' in strtn:
            self.pyBit = "32"
        elif "64" in strtn:
            self.pyBit = "64"
        else:
            self.pyBit =""

        cmd = pythonPath + "\python.exe -c "
        cmd += "\"import platform; print(platform.system())\""
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        rtn = p.stdout.read()
        strtn = bytes.decode(rtn, encoding="utf-8")
        if "Windows" in strtn:
            self.sysName = "Windows"
        elif "Linux" in strtn:
            self.sysName = "Linux"
        else:
            self.sysName = ""

        cmd = pythonPath + "\python.exe -c "
        cmd += "\"import platform; print(platform.python_version())\""
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        rtn = p.stdout.read()
        strtn = bytes.decode(rtn, encoding="utf-8")
        if strtn is not None:
            self.pyVersion = strtn[:3]
        else:
            self.pyVersion = ""

    def chkCython(self, path):
        '''
        检查是否安装了cython
        '''
        path += "\Scripts"
        files = os.listdir(path)
        for file in files:
            if file == "cython.exe":
                return True
        return False

    def addComboxList(self, path):
        '''
        增加combox的list选项
        '''
        for str in self.__comList:
            if str == path:
                self.combox.SetValue(str)
                return

        self.__comList.append(path)
        self.combox.Append(path)
        self.combox.SetValue(path)

    def comboxSelcet(self, event):
        """
        combox的选择事件
        """
        path = self.combox.GetStringSelection()
        self.getSysInfo(path)
        self.SetStatusText(self.sysName + "  python:" + self.pyVersion + "_" + self.pyBit)

    def onAdd1(self, event):
        """
        添加python.exe路径
        """
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pythonPath = dlg.GetPath()
            if pythonPath is not None:
                if self.checkPythonPath(pythonPath):
                    self.addComboxList(pythonPath)
                else:
                    self.SetStatusText(u"添加python.exe目录错误，请重新选择...")
                    dlg.Destroy()
                    return
        dlg.Destroy()
        self.getSysInfo(pythonPath)
        self.SetStatusText(self.sysName + "  python:" + self.pyVersion + "_" + self.pyBit)

    def checkPythonPath(self, pythonPath):
        """
        检查添加的python路径是否正确
        """
        for fp in os.listdir(pythonPath):
            if fp == "python.exe":
                return True
        return False

    def onAdd2(self, event):
        """
        添加打包exe的py文件
        """
        file_wildcard = "python files(*.py)|*.py"
        dlg = wx.FileDialog(self, "", os.getcwd(), wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if filename is not None:
                self.m_txtCtrl2.SetValue(filename)
                self.SetStatusText(u"添加打包exe的python文件")
        dlg.Destroy()

    def onImport(self, event):
        """
        导入需要打包pyd的py文件
        """
        file_wildcard = "python files(*.py)|*.py"
        dlg = wx.FileDialog(self, "", os.getcwd(), wildcard=file_wildcard, style=wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPaths()
            num = self.m_listBox.GetCount()
            tmp = filename.copy()
            for name in tmp:
                if self.m_listBox.FindString(name) != wx.NOT_FOUND:
                    filename.remove(name)

            if len(filename):
                self.m_listBox.InsertItems(filename, num)
                self.SetStatusText(u"添加打包pyd的python文件")
        dlg.Destroy()

    def onListboxDoubleClick(self, event):
        """
        双击Listbox元素删除
        """
        listItems = self.m_listBox.GetSelections()
        self.m_listBox.Delete(listItems[0])
        self.SetStatusText(u"删除打包pyd的python文件")

    def onDelete(self, event):
        """
        删除listbox中选中的item
        """
        allItem = self.m_listBox.GetItems()
        listItems = self.m_listBox.GetSelections()
        for i in listItems:
            allItem.remove(self.m_listBox.GetString(i))

        if len(listItems):
            self.m_listBox.Clear()
            self.m_listBox.InsertItems(allItem, 0)
            self.SetStatusText(u"删除打包pyd的python文件")

    def getLibName(self, path):
        """
        得到python的库名（如 python36）
        """
        path += '\libs'
        for fp in os.listdir(path):
            rtn = re.match(r'python...lib',  fp)
            if rtn is not None:
                return fp[:len(fp)-4]

    def modifyWmain(self, filePath):
        """
        修改*.c文件中的wmain-->main
        32位gcc并没有 -municode 选项，不能识别 wmain
        """
        fopen = open(filePath, "r")
        str = ""
        for line in fopen:
            if re.search("wmain\(int", line):
                line = re.sub("wmain", "main", line)
                str += line
            else:
                str += line

        wopen=open(filePath, "w")
        wopen.write(str)
        fopen.close()
        wopen.close()

    def chkMingwDirectory(self, mingw):
        """
        检查是否存在对应的mingw目录
        """
        flag = False
        path = os.getcwd()
        for fp in os.listdir(path):
            if os.path.isdir(fp) and fp == mingw:
                flag = True
                path += "\\" + mingw + "\\bin"
                break

        if not flag:
            self.SetStatusText(path + "下不存在" + mingw + "目录")
            return False

        flag = False
        for exe in os.listdir(path):
            if exe == "gcc.exe":
                return True

        if not flag:
            self.SetStatusText("不存在 " + path + "\\gcc.exe")
            return False

    def onPack(self, event):
        """
        打包
        """
        self.SetStatusText(u"开始打包...")
        pythonPath = self.combox.GetStringSelection()
        if pythonPath == "":
            self.SetStatusText(u"未添加python执行路径")
            return

        #打包exe
        if not self.packEXE(pythonPath):
            return

        #打包pyd
        if not self.packPydFiles(pythonPath):
            return

        #复制dll
        if not self.copyDLL():
            return

        self.SetStatusText(u"打包完成...")

    def packEXE(self, pythonPath):
        """
        打包exe
        """
        packFile = self.m_txtCtrl2.GetLineText(0)
        if packFile == "":
            self.SetStatusText(u"未添加打包exe的python文件，跳过exe打包...")
            return False

        mingw = ""
        if self.sysName == "Windows":
            mingw = "mingw"
        else:
            pass    #linux暂时没有实现

        if not self.chkMingwDirectory(mingw):
            return False

        strPath = self.combox.GetStringSelection()
        if not self.chkCython(strPath):
            self.SetStatusText(u"没有安装cython，请安装...")
            return False

        # 生成*.c文件
        pos1 = packFile.rfind('\\')
        pos2 = packFile.rfind(".")
        filePath = packFile[:pos1]
        str = packFile[pos1+1:pos2]
        str_c = str + ".c"
        str_exe = str + ".exe"

        cmd = pythonPath;
        cmd += "\Scripts\cython --embed "
        cmd += '"{0}"'.format(packFile)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rtn = p.wait()
        if rtn == 0:
            self.SetStatusText(u"成功生成文件：" + str_c)
        else:
            self.SetStatusText(u"未能生成文件：" + str_c)
            return False

        #生成exe文件
        curPath = os.getcwd()
        os.chdir(filePath)
        if self.pyBit == "64":
            cmd = curPath + "\\" + mingw + "\\bin\gcc " + str_c + " -o " + str + " -municode -DMS_WIN64 " + \
                "-I" + pythonPath + "\include" + " -L" + pythonPath + \
                  "\\libs" + " -l" + self.getLibName(pythonPath)
        elif self.pyBit == "32":
            if self.pyVersion[0] == "3":
                self.modifyWmain(filePath + "\\" + str_c)  # 修改wmain
            cmd = curPath + "\\" + mingw + "\\bin\gcc " + str_c + " -m32 -o " + \
                str + " -I" + pythonPath + "\include" + \
                   " -L" + pythonPath + "\\libs" + " -l" + self.getLibName(pythonPath)

        rtn = os.system(cmd)
        cmd = "del " + str_c
        rtn2 = os.system(cmd)
        if rtn2 == 0:
            self.SetStatusText(u"成功删除文件：" + str_c)
        else:
            self.SetStatusText(u"未能删除文件：" + str_c)
            os.chdir(curPath)
            return False

        if rtn == 0:
            self.SetStatusText(u"成功生成文件：" + str_exe)
        else:
            self.SetStatusText(u"未能生成文件：" + str_exe)
            os.chdir(curPath)
            return False

        os.chdir(curPath)
        return True

    def packPydFiles(self, pythonPath):
        """
        打包pyd文件
        """
        curPath = os.getcwd()
        nItem = self.m_listBox.GetCount()
        for i in range(nItem):
            str = self.m_listBox.GetString(i)
            pos1 = str.rfind('\\')
            pos2 = str.rfind(".")
            filePath = str[:pos1]
            fileName = str[pos1+1:pos2]

            #生成*.c文件
            cmd = pythonPath;
            cmd += "\Scripts\cython "
            cmd += '"{0}"'.format(str)
            rtn = os.system(cmd)
            str_c = fileName + ".c"
            if rtn == 0:
                self.SetStatusText(u"成功生成文件：" + str_c)
            else:
                self.SetStatusText(u"未能生成文件：" + str_c)

            #生成*.pyd文件
            mingw = ""
            if self.sysName == "Windows":
                mingw = "mingw"
            elif self.sysName == "Linux":
                pass  # linux暂时没有实现

            str_pyd = fileName + ".pyd"
            os.chdir(filePath)
            if self.pyBit == "64":
                cmd = curPath + "\\" + mingw + "\\bin\gcc " + str_c + " -o "  + str_pyd +  \
                    " -shared -DMS_WIN64 " + "-I" + pythonPath + "\include" + \
                      " -L" + pythonPath + "\\libs" + " -l" + self.getLibName(pythonPath)
            elif self.pyBit == "32":
                cmd = curPath + "\\" + mingw + "\\bin\gcc " + str_c + " -m32 -o " + str_pyd + \
                    " -shared " + "-I" + pythonPath + "\include" + \
                      " -L" + pythonPath + "\\libs" + " -l" + self.getLibName(pythonPath)
            else:
                cmd = ""

            rtn = os.system(cmd)
            cmd = "del " + str_c
            rtn2 = os.system(cmd)
            if rtn2 == 0:
                self.SetStatusText(u"成功删除文件：" + str_c)
            else:
                self.SetStatusText(u"未能删除文件：" + str_c)
                os.chdir(curPath)
                return False

            if rtn == 0:
                self.SetStatusText(u"成功生成文件：" + str_pyd)
            else:
                self.SetStatusText(u"未能生成文件：" + str_pyd)
                os.chdir(curPath)
                return False

        os.chdir(curPath)
        return True

    def copyDLL(self):
        """
        复制DLL到exe生成目录
        """
        fileName = self.m_txtCtrl2.GetLineText(0)
        pos = fileName.rfind('\\')
        filePath = fileName[:pos]

        pythonPath = self.combox.GetStringSelection()
        dllName = "python" + self.pyVersion[0] + self.pyVersion[2] + ".dll"
        flag = False
        for fp in os.listdir(pythonPath):
            if fp == dllName:
                flag = True
                break

        if not flag:
            self.SetStatusText(pythonPath + u"下不存在" + dllName)
            return False

        pythonPath += "\\" + dllName
        shutil.copy(pythonPath, filePath)
        return True

if __name__=="__main__":
    app=wx.App()
    frm=MainWindow(None, "京东达人创作工具", (300,200), (1000, 800))
    frm.Show()
    app.MainLoop()
