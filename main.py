import time 
import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic 
from PyQt5.QtCore import *
import ctypes
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog,QInputDialog
from PyQt5.QtGui import QIcon,QFont
import os
from math import gcd
import numpy as np
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    app_path = "\\".join(base_path.split("\\")[0:5])+"\\LHENDE"
    return os.path.join(app_path,relative_path)
class Encrypt(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent
    def run(self):
        self.en_File_Folder()
    def encrypt_files(self,files,mpath,key,mode,origin_path):
        for ind,i in enumerate(files):
            if os.path.getsize(i) < 2000000000:
                di = self.getdi(i)
                if origin_path=="":
                    self.parent.label.setText("암호화중... : "+str(self.parent.fcnt)+"/"+str(len(files)))
                    self.parent.fcnt+=1
                else:
                    self.parent.label.setText("분산파일 암호화중... : "+str(ind)+"/"+str(len(files)))
                if not(di==0) and os.path.getsize(i)>di and os.path.getsize(i)>self.parent.cutsize:
                    try:
                        self.parent.md['encrypting'](i,key,os.path.getsize(i)//di)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
                else:
                    try:
                        self.parent.md['encrypting'](i,key,1)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
            else:
                t = self.divide_file(i, 8, "b")
                self.encrypt_files(t,mpath,key,mode,i)
        if origin_path!="":
            self.combine_file(origin_path)
            self.parent.fcnt+=1
    def encrypt_folder(self,path,mpath,key,mode):
        for ind,i in enumerate(os.listdir(path)):
            rpath = path+"/"+i
            if os.path.isdir(rpath):
                self.encrypt_folder(rpath,mpath,key,mode)
            elif os.path.getsize(rpath) < 2000000000:
                try:
                    tempo = os.path.getsize(rpath)
                except:
                    time.sleep(1)
                    tempo = os.path.getsize(rpath)
                di = self.getdi(rpath)
                
                if not(di==0) and os.path.getsize(rpath)>di and os.path.getsize(rpath)>self.parent.cutsize:
                    self.parent.label.setText("암호화중... : "+str(self.parent.fcnt)+"/"+str(self.parent.rallfile))
                    try:
                        self.parent.md['encrypting'](rpath,key,os.path.getsize(rpath)//di)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
                else:
                    self.parent.label.setText("암호화중... : "+str(self.parent.fcnt)+"/"+str(self.parent.rallfile))
                    try:
                        self.parent.md['encrypting'](rpath,key,1)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
                self.parent.fcnt+=1
            else:
                self.parent.label.setText("파일의 크기가 크므로 분할 암호화를 진행합니다.")
                files = self.divide_file(rpath, 8, "b")
                self.encrypt_files(files,mpath,key,mode,rpath)
                self.parent.fcnt+=1
    def en(self,path, mpath, key, mode):
        self.parent.fcnt = 0
        now = time.time()
        self.parent.allfile = 0
        self.parent.getallfile(path)
        self.parent.rallfile = self.parent.allfile
        self.encrypt_folder(path, mpath, key, mode)
        entime = time.time()-now
        self.parent.label.setText("암호화가 완료되었습니다.")
    def en_File_Folder(self):
        self.parent.fcnt = 0
        if self.parent.selectedfolder==True:
            self.parent.allfile = 0
            self.parent.getallfile(self.parent.nowfolder)
            self.parent.rallfile = self.parent.allfile
            self.en(self.parent.nowfolder,self.parent.mpath,self.parent.key,self.parent.mode)
        else:
            self.parent.allfile = len(self.parent.files)
            self.encrypt_files(self.parent.files, self.parent.mpath, self.parent.key, self.parent.mode, "")
        self.parent.label.setText("암호화가 완료되었습니다.")
    def divide_file(self,path,size,bkmg):
        divided_file = []
        MINDIV = 2
        MAXDIV = 30
        byte = 1
        kilobyte = byte*1024
        megabyte = kilobyte*1024
        gigabyte = megabyte*1024
        
        
        filename = path.split("/")[len(path.split("/"))-1]
        filename2 = "_"+filename
        path = "/".join(path.split("/")[0:len(path.split("/"))-1])+"/"

        filesize = os.path.getsize(path+filename)
        if bkmg=='b' or bkmg==0:
            divide_filesize = size*byte
        elif bkmg=='k' or bkmg==1:
            divide_filesize = size*kilobyte
        elif bkmg=='m' or bkmg==2:
            divide_filesize = size*megabyte
        elif bkmg=='g' or bkmg==3:
            divide_filesize = size*gigabyte
        else:
            divide_filesize = size
        
        if filesize%divide_filesize==0:
            filecount = filesize//divide_filesize
        else:
            filecount = (filesize//divide_filesize)+1
        if filecount > MAXDIV:
            filecount = MAXDIV+1
            divide_filesize = filesize//filecount
            alpha = 0
            while divide_filesize > 2*gigabyte:
                divide_filesize = filesize//(MAXDIV+alpha)
                filecount = MAXDIV+alpha
                alpah += 1
        cnt = 0
        with open(path+filename,'rb') as f:
            while True:
                self.parent.label.setText("파일 분산중... : "+str(cnt)+"/"+str(filecount))
                divided_file.append(os.path.abspath(path+str(cnt)+filename2).replace("\\", "/"))
                with open(path+str(cnt)+filename2,'wb') as f2:
                    f2.write(f.read(divide_filesize))
                cnt+=1
                if cnt>filecount:
                    break
        os.remove(path+filename)
        self.parent.allfile = len(divided_file)
        return divided_file
    def getdi(self,path):
        num = os.path.getsize(path)
        m = 0
        if num%2==1:
            for i in range(int(num**0.5),2,-2):
                if gcd(num,i)>m:
                    m = gcd(num, i)
        else:
            for i in range(int(num**0.5)-1,2,-2):
                if gcd(num,i)>m:
                    m = gcd(num, i)
        return m
    def combine_file(self,path):
        filename = path.split("/")[len(path.split("/"))-1]
        path = "/".join(path.split("/")[0:len(path.split("/"))-1])+"/"
        files = []
        filename_list = []
        for i in os.listdir(path):
            if filename in i and not(filename==i) and i.replace("_"+filename, "").isdigit():#숫자여야함, 대상파일과 이름이 달라야함, 이름 안에 대상 파일의 이름이 있어야함,
                t = int(str(i.split("_")[0]))
                files.append(t)
        files.sort()
        
        for ind,i in enumerate(files):#숫자의 연속성 검사
            if i == ind:
                pass
            else:
                files.remove(i)
        with open(path+filename,"wb") as nf:
            for ind,i in enumerate(files):
                self.parent.label.setText("파일 결합중... : "+str(ind)+"/"+str(len(files)))
                with open(path+str(i)+"_"+filename,"rb") as f:
                    nf.write(f.read())
                os.remove(path+str(i)+"_"+filename)
class Decrypt(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent 
    def run(self):
        self.de_File_Folder()
    def decrypt_files(self,files,mpath,key,mode,origin_path):
        for ind,i in enumerate(files):
            if os.path.getsize(i) < 2000000000:
                di = self.getdi(i)
                if origin_path=="":
                    self.parent.label.setText("파일 복호화중... : "+str(self.parent.fcnt)+"/"+str(len(files)))
                    self.parent.fcnt += 1
                else:
                    self.parent.label.setText("분산파일 복호화중... : "+str(ind)+"/"+str(len(files)))
                if not(di==0) and os.path.getsize(i)>di and os.path.getsize(i)>self.parent.cutsize:
                    try:
                        self.parent.md['decrypting'](i,key,os.path.getsize(i)//di)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
                else:
                    try:
                        self.parent.md['decrypting'](i,key,1)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
            else:
                t = self.divide_file(i, 8, "b")
                self.decrypt_files(t,mpath,key,mode,i)
        if origin_path!="":
            self.combine_file(origin_path)
            self.parent.fcnt+=1
    def decrypt_folder(self,path,mpath,key,mode):
        for ind,i in enumerate(os.listdir(path)):
            rpath = path+"/"+i
            if os.path.isdir(rpath):
                self.decrypt_folder(rpath,mpath,key,mode)
            elif os.path.getsize(rpath) < 2000000000:
                try:
                    tempo = os.path.getsize(rpath)
                except:
                    time.sleep(1)
                    tempo = os.path.getsize(rpath)
                di = self.getdi(rpath)
                
                if not(di==0) and os.path.getsize(rpath)>di and os.path.getsize(rpath)>self.parent.cutsize:
                    self.parent.label.setText("복호화중... : "+str(self.parent.fcnt)+"/"+str(self.parent.rallfile))
                    try:
                        self.parent.md['decrypting'](rpath,key,os.path.getsize(rpath)//di)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
                else:
                    self.parent.label.setText("복호화중... : "+str(self.parent.fcnt)+"/"+str(self.parent.rallfile))
                    try:
                        self.parent.md['decrypting'](rpath,key,1)
                    except:
                        self.parent.label.setText("비정상적인 소스파일입니다.")
                        return -1
                self.parent.fcnt+=1
            else:
                files = self.divide_file(rpath, 8, "b")
                self.decrypt_files(files,mpath,key,mode,rpath)
                self.parent.fcnt+=1
    def de(self,path, mpath, key, mode):
        self.parent.fcnt = 0
        now = time.time()
        self.parent.allfile = 0
        self.parent.getallfile(path)
        self.parent.rallfile = self.parent.allfile
        self.decrypt_folder(path, mpath, key, mode)
        detime = time.time()-now
        self.parent.label.setText("복호화가 완료되었습니다.")
    def de_File_Folder(self):
        self.parent.fcnt = 0
        if self.parent.selectedfolder==True:
            self.parent.allfile = 0
            self.parent.getallfile(self.parent.nowfolder)
            self.parent.rallfile = self.parent.allfile
            self.de(self.parent.nowfolder,self.parent.mpath,self.parent.key,self.parent.mode)
        else:
            self.parent.allfile = len(self.parent.files)
            self.decrypt_files(self.parent.files, self.parent.mpath, self.parent.key, self.parent.mode, "")
        self.parent.label.setText("복호화가 완료되었습니다.")
    def divide_file(self,path,size,bkmg):
        divided_file = []
        MINDIV = 2
        MAXDIV = 30
        byte = 1
        kilobyte = byte*1024
        megabyte = kilobyte*1024
        gigabyte = megabyte*1024
        
        
        filename = path.split("/")[len(path.split("/"))-1]
        filename2 = "_"+filename
        path = "/".join(path.split("/")[0:len(path.split("/"))-1])+"/"

        filesize = os.path.getsize(path+filename)
        if bkmg=='b' or bkmg==0:
            divide_filesize = size*byte
        elif bkmg=='k' or bkmg==1:
            divide_filesize = size*kilobyte
        elif bkmg=='m' or bkmg==2:
            divide_filesize = size*megabyte
        elif bkmg=='g' or bkmg==3:
            divide_filesize = size*gigabyte
        else:
            divide_filesize = size
        
        if filesize%divide_filesize==0:
            filecount = filesize//divide_filesize
        else:
            filecount = (filesize//divide_filesize)+1
        if filecount > MAXDIV:
            filecount = MAXDIV+1
            divide_filesize = filesize//filecount
            alpha = 0
            while divide_filesize > 2*gigabyte:
                divide_filesize = filesize//(MAXDIV+alpha)
                filecount = MAXDIV+alpha
                alpah += 1
        
        cnt = 0
        with open(path+filename,'rb') as f:
            while True:
                self.parent.label.setText("파일 분산중... : "+str(cnt)+"/"+str(filecount))
                divided_file.append(os.path.abspath(path+str(cnt)+filename2).replace("\\", "/"))
                with open(path+str(cnt)+filename2,'wb') as f2:
                    f2.write(f.read(divide_filesize))
                cnt+=1
                if cnt>filecount:
                    break
        os.remove(path+filename)
        self.parent.allfile = len(divided_file)
        return divided_file
    def getdi(self,path):
        num = os.path.getsize(path)
        m = 0
        if num%2==1:
            for i in range(int(num**0.5),2,-2):
                if gcd(num,i)>m:
                    m = gcd(num, i)
        else:
            for i in range(int(num**0.5)-1,2,-2):
                if gcd(num,i)>m:
                    m = gcd(num, i)
        return m
    def combine_file(self,path):
        filename = path.split("/")[len(path.split("/"))-1]
        path = "/".join(path.split("/")[0:len(path.split("/"))-1])+"/"
        files = []
        filename_list = []
        for i in os.listdir(path):
            if filename in i and not(filename==i) and i.replace("_"+filename, "").isdigit():#숫자여야함, 대상파일과 이름이 달라야함, 이름 안에 대상 파일의 이름이 있어야함,
                t = int(str(i.split("_")[0]))
                files.append(t)
        files.sort()
        
        for ind,i in enumerate(files):#숫자의 연속성 검사
            if i == ind:
                pass
            else:
                files.remove(i)
        with open(path+filename,"wb") as nf:
            for ind,i in enumerate(files):
                self.parent.label.setText("파일 결합중... : "+str(ind)+"/"+str(len(files)))
                with open(path+str(i)+"_"+filename,"rb") as f:
                    nf.write(f.read())
                os.remove(path+str(i)+"_"+filename)
                
class EncryptName(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent 
    def run(self):
        self.en_names()
    def crypt(self,filename,seed_key):
        lenth = len(filename)
        temp = np.array([])
        for i in filename:
            temp = np.append(temp, i)
        filename = temp
        
        ufilename = np.zeros(lenth,dtype=np.int32)

        for i in range(lenth):
            ufilename[i] += ord(filename[i])

        np.random.seed(seed_key)
        key = np.array(np.random.rand(lenth)*np.full(lenth,256),dtype=int)
        newfilename = np.bitwise_xor(key,ufilename)

        temp = ""
        for ind,i in enumerate(newfilename):
            temp += str(hex(i)).replace("0x", "")
            if not(ind==len(newfilename)-1):
                temp += ","
        return temp
    def en_names(self):
        if self.parent.selectedfolder==True:
            self.en_names_folder(self.parent.nowfolder, self.parent.key)
        else:
            self.en_names_files(self.parent.files, self.parent.key)
        self.parent.label.setText("이름 암호화 완료")
    def en_names_files(self,files,key):
        files.sort()
        for ind,i in enumerate(files):
            filename = i.split("/")[len(i.split("/"))-1]
            self.parent.files[ind] = "/".join(i.split("/")[0:len(i.split("/"))-1])+"/"+self.crypt(filename,key)
            os.rename("/".join(i.split("/")[0:len(i.split("/"))-1])+"/"+filename, "/".join(i.split("/")[0:len(i.split("/"))-1])+"/"+self.crypt(filename,key))
    def en_names_folder(self,path,seed_key):
        filelist = os.listdir(path)
        filelist.sort()
        for i in filelist:
            if os.path.isdir(path+"/"+i):
                os.rename(path+"/"+i, path+"/"+self.crypt(i, seed_key))
                self.en_names_folder(path+"/"+self.crypt(i, seed_key), seed_key)
            else:
                try:
                    os.rename(path+"/"+i, path+"/"+self.crypt(i, seed_key))
                except:
                    pass
class DecryptName(QThread): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent 
    def run(self):
        self.de_names()
    def decrypt(self,cryptedfilename,seed_key):
        try:
            filename = cryptedfilename.split(",")
        except:
            self.parent.label.setText("복호화할 이름이 부적절합니다.")
        lenth = len(filename)
        temp = np.array([],dtype=np.uint32)
        for i in filename:
            try:
                temp = np.append(temp,int(i, 16))
            except:
                self.parent.label.setText("복호화할 이름이 부적절합니다.")
                return -1
        np.random.seed(seed_key)
        key = np.array(np.random.rand(lenth)*np.full(lenth,256),dtype=int)
        val = np.bitwise_xor(key,temp)

        result = ""
        for i in range(lenth):
            result += chr(val[i])
        return result
    def de_names(self):
        t = 0
        if self.parent.selectedfolder==True:
            t = self.de_names_folder(self.parent.nowfolder, self.parent.key)
        else:
            t = self.de_names_files(self.parent.files, self.parent.key)
        if not(t==-1):
            self.parent.label.setText("이름 복호화 완료")
    def de_names_files(self,files,key):
        files.sort()
        for ind,i in enumerate(files):
            filename = i.split("/")[len(i.split("/"))-1]
            try:
                self.parent.files[ind] = "/".join(i.split("/")[0:len(i.split("/"))-1])+"/"+self.decrypt(filename,key)
            except:
                self.parent.label.setText("복호화할 이름이 부적절합니다.")
                return -1
            os.rename("/".join(i.split("/")[0:len(i.split("/"))-1])+"/"+filename, "/".join(i.split("/")[0:len(i.split("/"))-1])+"/"+self.decrypt(filename,key))
    def de_names_folder(self,path,seed_key):
        filelist = os.listdir(path)
        filelist.sort()
        for i in filelist:
            if os.path.isdir(path+"/"+i):
                os.rename(path+"/"+i, path+"/"+self.decrypt(i, seed_key))
                self.de_names_folder(path+"/"+self.decrypt(i, seed_key), seed_key)
            else:
                try:
                    os.rename(path+"/"+i, path+"/"+self.decrypt(i, seed_key))
                except:
                    return -1
        
class MyApp(QWidget):
    def __init__(self): 
        super().__init__()
        super().__init__()
        self.mpath = resource0
        self.icon = resource1
        self.allfile = 0
        self.rallfile = 0
        self.nowfolder = ""
        self.files = None
        self.folder_or_file = None
        self.key = -10
        self.cutsize = 1000
        self.cnt = 0     
        self.md = ctypes.WinDLL(self.mpath)
        self.selectedfolder = False
        self.mode = 0
        self.fcnt = 0
        self.showingkey = False
        self.isshowkey = False
        self.setAcceptDrops(True)
        self.initUI()
        
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.label = QLabel('                                                                                           ', self)
        self.label.setFixedWidth(300)
        self.label.move(0,180)
        self.label.setAlignment(Qt.AlignCenter)
        
        setkey_btn = QPushButton('key 설정', self)
        setkey_btn.setToolTip('<b>key값을 설정합니다.</b>')
        setkey_btn.clicked.connect(lambda:self.setkey())
        setkey_btn.move(45,20)
        setkey_btn.setFixedSize(100, 25)
        
        path_setting_btn = QPushButton("dll path 설정", self)
        path_setting_btn.setToolTip("<b>암/복호화 dll 파일의 위치를 설정합니다.</b>")
        path_setting_btn.clicked.connect(lambda: self.setpath())
        path_setting_btn.move(155, 20)
        path_setting_btn.setFixedSize(100, 25)
        
        getfolder_btn = QPushButton('폴더 선택', self)
        getfolder_btn.setToolTip('<b>대상 폴더를 선택합니다.</b>')
        getfolder_btn.clicked.connect(lambda: self.selectfolder())
        getfolder_btn.move(45, 60)
        getfolder_btn.setFixedSize(100, 25)
        
        
        
        getfile_btn = QPushButton('파일 선택', self)
        getfile_btn.setToolTip('<b>대상 파일을 선택합니다.</b>')
        getfile_btn.clicked.connect(lambda: self.selectfiles())
        getfile_btn.move(155, 60)
        getfile_btn.setFixedSize(100, 25)
        
        en_btn = QPushButton("암호화", self)
        en_btn.setToolTip('<b>선택된 폴더/파일을 암호화 합니다.</b>')
        en_btn.clicked.connect(self.EnFunction)
        en_btn.move(45,100)
        en_btn.setFixedSize(100, 25)
        
        de_btn = QPushButton("복호화", self)
        de_btn.setToolTip('<b>선택된 폴더/파일을 복호화 합니다.</b>')
        de_btn.clicked.connect(self.DeFunction)
        de_btn.move(155,100)
        de_btn.setFixedSize(100, 25)
        
        en_name_btn = QPushButton("이름 암호화", self)
        en_name_btn.setToolTip('<b>선택된 폴더/파일 이름을 암호화 합니다.</b>')
        en_name_btn.clicked.connect(self.EnName)
        en_name_btn.move(45,140)
        en_name_btn.setFixedSize(100, 25)
        
        de_name_btn = QPushButton("이름 복호화", self)
        de_name_btn.setToolTip('<b>선택된 폴더/파일 이름을 복호화 합니다.</b>')
        de_name_btn.clicked.connect(self.DeName)
        de_name_btn.move(155,140)
        de_name_btn.setFixedSize(100, 25)
        
        cb = QCheckBox('Key값 보기', self)
        cb.move(100, 210)
        cb.stateChanged.connect(self.change)
        
        self.setWindowTitle('En-Decrypter By LH')
        self.setWindowIcon(QIcon(self.icon))
        self.setFixedSize(300, 250)
        self.show()
    
    def change(self):
        self.isshowkey = not(self.isshowkey)
        if self.isshowkey == True:
            if self.key < 0:
                self.label.setText("None")
                self.label.setAlignment(Qt.AlignCenter)
            else:
                if str(self.key)[len(str(self.key))-1] == '0' or str(self.key)[len(str(self.key))-1] == '3' or str(self.key)[len(str(self.key))-1] == '6':
                    self.label.setText("key값이 "+str(self.key)+"으로 설정되었습니다.")
                else:
                    self.label.setText("key값이 "+str(self.key)+"로 설정되었습니다.")
                self.label.setAlignment(Qt.AlignCenter)
        else:
            if self.key < 0:
                self.label.setText("")
                self.label.setAlignment(Qt.AlignCenter)
            else:
                self.label.setText("key값이 "+''.join("●"*len(str(self.key)))+"(으)로 설정되었습니다.")
                self.label.setAlignment(Qt.AlignCenter)
    def EnFunction(self):
        if self.key < 0:
            self.label.setText("key값을 입력해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        elif self.folder_or_file == None:
            self.label.setText("폴더 또는 파일을 선택해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        else:
            self.cnt = 0
            h1 = Encrypt(self) 
            h1.start()
    def DeFunction(self): 
        if self.key < 0:
            self.label.setText("key값을 입력해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        elif self.folder_or_file == None:
            self.label.setText("폴더 또는 파일을 선택해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        else:
            self.cnt = 0
            h1 = Decrypt(self)
            h1.start()
    def EnName(self):
        if self.key < 0:
            self.label.setText("key값을 입력해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        elif self.folder_or_file == None:
            self.label.setText("폴더 또는 파일을 선택해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        else:
            h1 = EncryptName(self) 
            h1.start()
    def DeName(self): 
        if self.key < 0:
            self.label.setText("key값을 입력해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        elif self.folder_or_file == None:
            self.label.setText("폴더 또는 파일을 선택해주세요.")
            self.label.setAlignment(Qt.AlignCenter)
        else:
            h1 = DecryptName(self)
            h1.start()
    def setpath(self):
        t1 = QFileDialog.getOpenFileNames(self, '소스 파일을 선택하세요', self.nowfolder, filter='*.dll')[0]
        if not(t1==[]):
            self.mpath = str(t1[0])
            self.md = ctypes.WinDLL(self.mpath)
            self.label.setText("소스 파일 경로가 수정되었습니다.")
    def setkey(self):
        if self.isshowkey == True:
            text, ok = QInputDialog.getText(self, 'Key값 설정', 'Key값을 입력하세요:')
        else:
            text, ok = QInputDialog.getText(self, 'Key값 설정', 'Key값을 입력하세요:',QLineEdit.Password)
        if ok and text.isdigit() and not(len(text) != len(str(int(text)))):
            self.key = int(text)
            if self.isshowkey == True:
                if text[len(text)-1] == '0' or text[len(text)-1] == '3' or text[len(text)-1] == '6':
                    self.label.setText("key값이 "+text+"으로 설정되었습니다.")
                else:
                    self.label.setText("key값이 "+text+"로 설정되었습니다.")
            else:
                self.label.setText("key값이 "+''.join("●"*len(str(self.key)))+"(으)로 설정되었습니다.")
            
            self.label.setAlignment(Qt.AlignCenter)
        elif text.isdigit() and len(text) != len(str(int(text))):
            self.label.setText("key값은 0으로 시작할 수 없습니다.")
            self.setkey()
        elif text.isdigit() or ok:
            self.label.setText("key값은 0 이상의 숫자값을 입력하여야 합니다.")
            self.label.setAlignment(Qt.AlignCenter)
            self.setkey()
        

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def selectfolder(self):
        self.folder_or_file = True
        self.nowfolder = os.path.abspath(os.getcwd())
        folder = QFileDialog.getExistingDirectory(self, "폴더 선택")
        if not(folder==''):
            self.nowfolder = folder
            self.allfile = 0
            self.getallfile(self.nowfolder)
            self.rallfile = self.allfile
            self.selectedfolder = True
        self.label.setText('0/'+str(self.allfile))
        
    def selectfiles(self):
        self.folder_or_file = False
        self.files = []
        if self.nowfolder == "":
            self.nowfolder = os.path.abspath(os.getcwd())
        self.files = QFileDialog.getOpenFileNames(self, '파일 선택', self.nowfolder, filter='')[0]
        self.selectedfolder = False
        
        self.label.setText("0/"+str(len(self.files)))
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        self.folder_or_file = False
        self.files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.label.setText("0/"+str(len(self.files)))
    def getallfile(self,path):
        for i in os.listdir(path):
            if os.path.isdir(path+"/"+i):
                self.getallfile(path+"/"+i)
            elif self.rallfile==0:
                self.label.setText("파일의 개수 세는중")
                self.allfile += 1
if __name__ == "__main__" :
    base_path = getattr(sys, '_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    app_path = "\\".join(base_path.split("\\")[0:5])+"\\LHENDE"
    if not(os.path.isdir(app_path)):
        os.rename(base_path, app_path)
    sys.path[0] = app_path+"base_library.zip"
    sys.path[1] = app_path
    try:
        resource0 = resource_path("ENDE.dll")
        resource1 = resource_path("LHENDE.ico")
    except:
        pass
    app = QApplication(sys.argv)
    myWindow = MyApp() 
    myWindow.show() 
    app.exec_()