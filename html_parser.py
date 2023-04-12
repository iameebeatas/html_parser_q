
# -*- coding: utf-8 -*-

import time
# import common
import json
# import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
# from pandas.io.sql import execute
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
# from sqlalchemy import create_engine
# import lrb_user
# import lrb_board
# import get_note
# from sqlalchemy.orm import sessionmaker
import urllib.parse
# import optparse
import argparse
# import traceback
import traceback
from selenium.webdriver.common.action_chains  import ActionChains

import os
import sys
from os import listdir
from base64 import b64decode
from PIL import Image
# import pytesseract
import ddddocr
# ddddocr python开源免费的OCR文字识别库
# 下载：pip install ddddocr
# python3 -m pip uninstall ddddocr
# https://blog.csdn.net/weixin_55810728/article/details/125439425

import numpy as np


# html_parser.py
# https://github.com/cxy-csx/little_red_book/blob/main/get_user_fire.py

# openpyxl
# pandas
# bs4
# selenium
# pymysql
# sqlalchemy
# lxml
# isodate
# xmlwitch
# pywinrm

''' 解析html页面 '''
class html_parser:
    def __init__(self):
        """初始化"""
        # 这个小红书的地址 需要打开两次或者打开一次再刷新  才会有数据
        # self.url = "https://www.xiaohongshu.com/user/profile/562ef75ae00dd861d410784a"
        # self.url = "https://www.baidu.com/"
        self.url = "https://xkczb.jtw.beijing.gov.cn/"
        self.driver = ''
        self.user_html = ''
        self.user_html_bs = ''
        self.is_slide = False
        self.headless = 0

    def createNewBrowser(self):
        option = webdriver.ChromeOptions()
        # 无界面模式
        # if self.headless == 1 :
        if self.isHeadless() :
            option.add_argument('--headless')

        # prefs = {"download.default_directory" : defaultDirectory}
        # option.add_experimental_option("prefs",prefs)
        option.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/104.0.0.0 Safari/537.36")
        # 忽略SSL证书错误问题
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--ignore-ssl-errors')
        # 隐藏浏览器检测selenium
        option.add_argument("--disable-blink-features=AutomationControlled")
        # 忽略无用日志
        option.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        option.add_experimental_option("detach", True)
        

        # 设置下载路径
        path = self.get_path_parent_dir()
        # 每月一个
        dt = time.strftime("%Y-%m", time.localtime())
        # new_path = path + '/public/excel' + '/' + dt + '/1' + '/a'
        # defaultDirectory = path + '\public\excel' + '\\' + dt + '\\' + self.memo_type_obj[self.classTitle] + '\\' + self.account_item['filepath']
        # self.mkdirPath(path=defaultDirectory)
        # self.removeFiles(defaultDirectory + '\\')
        # self.download_path = defaultDirectory + '\\'



        # 禁用记住密码弹框
        # option.add_experimental_option("prefs",{"credentials_enable_service":False,"profile.password_manager_enabled":False,"download.default_directory" : defaultDirectory})
        option.add_experimental_option("prefs",{"credentials_enable_service":False,"profile.password_manager_enabled":False} )
        driver = webdriver.Chrome(chrome_options=option)
        
        
        # WebDriverWait(driver, 10)
        sleep(3)
        self.driver = driver
        # 窗口最大化
        self.setMaxImizeWindow()
        # return driver

    def isHeadless(self):
        ''' 是否是无界面模式'''
        if self.headless :
            ''' 是 '''
            return True
        return False

    def setMaxImizeWindow(self):
        ''' 设置窗口最大化 '''
        if self.isHeadless() :
            ''' '''
        else:
            self.driver.maximize_window()
            ''' '''

    def ocrImgUrl(self,img_url):
        ''' 识别图片验证码 '''
        ocr = ddddocr.DdddOcr()
        # img_url = self.img_url
        with open(img_url,'rb') as f :
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        return res

    def mkdirPath(self,path):
        ''' 创建目录 '''
        # 引入模块
        # import os
    
        # 去除首位空格
        path=path.strip()
        # 去除尾部 \ 符号
        path=path.rstrip("\\")
    
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
    
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            # print(path+' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(path+' 目录已存在')
            return False

    def get_path_parent_dir(self):
        ''' 获取当前文件的所在目录的上一级目录 '''
        # /Users/a123456/zwn/gs_gitee/jingtong-data-capture
        parent_directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return parent_directory_path
    
    def removeFiles(self,my_path):
        ''' 删除目录下的所有文件 '''
        for file_name in listdir(my_path):
            os.remove(my_path + file_name)
    
    def openUrl(self):
        ''' 在当前资源覆盖打开地址 '''
        self.driver.get(self.url)
        # WebDriverWait(self.driver, 10)
        sleep(3)

    def screenShotDriver(self,fileName):
        ''' 截图 '''
        defaultDirectory = './image_path/'
        png_path = defaultDirectory + '{}={}={}.png'.format(fileName,self.headless, '1-' +  '-截图-')
        self.driver.get_screenshot_as_file(png_path)
        # self.driver.save_screenshot(png_path)
        return png_path

    def getPageSource(self):
        ''' 获取页面源码解析 '''
        self.user_html = self.driver.page_source
        self.user_html_bs = BeautifulSoup(self.user_html, 'lxml')
        
    def refresh(self):
        ''' 刷新 '''
        self.driver.refresh()
        sleep(13)

    def setHeadles(self,headles):
        ''' 设置为无界面模式 '''
        # if headles == 1 :
        if headles :
            self.headless = headles
        else:
            self.headless = 0
        

    def getFirstNoticeTitle(self):
        ''' 获取第一个公告的标题 '''
        text = self.driver.find_element(By.XPATH, "//div[@class='jmtd-modal-tips-follow-text']").text
        textObj = {'title':text,'title_date':''}
        return textObj

    def saveBaseLsImg(self):
        ''' 保存 base64 数据图片'''
        hk_img = self.driver.find_element(By.XPATH, '//div[@class="JDJRV-smallimg"]/img').get_attribute('src')  # 滑块图
        hkdata = hk_img.split(',')[1]
        hk_b64 = b64decode(hkdata)
        # 缺口滑块
        with open(self.root + self.hk_img, 'wb') as f:
            f.write(hk_b64)
            f.close()

    # 小红书笔记爬虫
    # https://github.com/OrangeySeven/RedbookSpider
    # https://github.com/yuncaiji/API
    # https://github.com/cxy-csx/little_red_book/blob/main/get_user_fire.py
    # https://www.cnblogs.com/futurelifekin/p/17146473.html
    # http://zcykj.byethost5.com/zcykj.html
    # https://github.com/lixi5338619/lxSpider
    # https://github.com/Wahahaha0/xhs
    # https://github.com/KertinH/xiaohongshu_go
    # https://github.com/InJeCTrL/XHSPicExtractor
    # https://github.com/ReaJason/xhs
    # https://github.com/zsmhub/workweixin
    def orcImagePaser(self):
        ''' 循环识别验证码图片'''
        i = 0
        successBool = False
        while i < 10:
            try:
                imgOcrUrlMake = self.saveImgByUrl()
                imgCode = self.ocrImgUrl(imgOcrUrlMake)
                print('识别出来的验证码',imgCode,len(imgCode) )
                successBool = True
                i += 11
                # 验证码成功
                # <label id="checkResult" class="checkTrue"><img src="https://xkczb.jtw.beijing.gov.cn/templates/default/www/images/note_yes.gif"></label>
                # 验证码失败
                # <label id="checkResult" class="checkFalse"></label>
                # <label id="checkResult" class="checkFalse"><img src="https://xkczb.jtw.beijing.gov.cn/templates/default/www/images/note_no.gif"></label>
                # 验证码不足位数
                # <label id="checkResult"></label>

            except Exception as e:
                errInfo = traceback.format_exc()
                print('--errInfo--',errInfo)
                i += 11
        return successBool

    def scrollLeft(self,num):
        ''' 向右滑动-->>> 也就是距离左边多少距离 '''
        self.driver.execute_script("document.documentElement.scrollLeft=" + str(num) )
        time.sleep(1)

    def saveImgByUrl(self):
        ''' 通过URL地址保存图片'''
        # 这个地址每次请求的图片都不一样
        # https://apply.jtw.beijing.gov.cn/apply/app/common/validCodeImage?ee=2
        # <label id="getValidCode" class="validCodeImg" title="单击刷新验证码"><img src="https://apply.jtw.beijing.gov.cn/apply/app/common/validCodeImage?ee=1"></label>
        ''' 思路  保存验证码图片
        1 使用PIL裁切图片需使用PIL引用Image模块(pip install pillow直接安装)
        2 from PIL import Image  Image.open(file)方法可以返回打开的图片
        3 使用crop((x0,y0,x1,y1))方法可以对图片做裁切:依次为起始点的横坐标,起始点的纵坐标,距离原点的宽度,高度
        4 查找到元素,通过element.location可以得到x0,y0:通过element.size计算得到x1,y1即可
        https://www.lmlphp.com/user/59846/article/item/2368945/
        https://blog.csdn.net/qq_39620483/article/details/99842026
        https://blog.csdn.net/redrose2100/article/details/121144075
        https://www.dgrt.cn/a/2202464.html?action=onClick
        '''
        # 获取指定元素（验证码）
        # <img id="s_lg_img" class="s_lg_img_gold_show" src="//www.baidu.com/img/PCfb_5bf082d29588c07f842ccde3f97243ea.png" width="270" height="129" onerror="this.src='https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/logo_white-d0c9fe2af5.png';this.onerror=null;" usemap="#mp" title="" cursor="default">
        # captchaElem = self.driver.find_element(By.XPATH, "//img[@id='s_lg_img']")
        captchaElem = self.driver.find_element(By.XPATH, "//label[@id='getValidCode']/img")
        # 因为验证码在没有缩放，直接取验证码图片的绝对坐标;这个坐标是相对于它所属的div的，而不是整个可视区域
        # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标;  
        # location 拿到的是相对整个html页面的坐标

#         captchaX = int(captchaElem.location['x']) # x坐标
        captchaY = int(captchaElem.location['y']) # y坐标
#         captchaX = 283 # x坐标
#         captchaX = 366 # x坐标
        captchaX = 467 # x坐标
#         captchaY = 676 # y坐标
        print('元素左上角' , 'x坐标' , captchaX,'y坐标',captchaY)
        # 获取验证码宽高
        captchaWidth = captchaElem.size['width']
        captchaHeight = captchaElem.size['height']
#         captchaWidth = 540
#         captchaHeight = 182
        print('x坐标宽' , captchaWidth,'y坐标高',captchaHeight)
        captchaRight = captchaX + captchaWidth
        captchaBottom = captchaY + captchaHeight
        print('元素右下角' , 'x坐标宽' , captchaRight,'y坐标高',captchaBottom)
        
        # 声明一个方法获取验证码图片的四个坐标点
        # captchaX,captchaY,captchaRight,captchaBottom
        # captchaWidth,captchaHeight,
        # _file_url = './image_path/captcha_'  + '.png'
        _file_url = self.screenShotDriver(fileName='验证码截图')
        imgObject = Image.open(_file_url)  #获得截屏的图片

        imgCaptcha = imgObject.crop((captchaX, captchaY, captchaRight, captchaBottom))  # 裁剪
        # imgCaptcha=imgCaptcha.convert('RGB')
        imgCaptcha = imgCaptcha.convert('L')
        threshold = 50
        array = np.array(imgObject)
        array = np.where(array > threshold, 255, 0)
        imgCaptcha = imgCaptcha.fromarray(array.astype('uint8'))




        _file_name = 1222
        _save_url = './image_path/'
        yanzhengma_file_name = str(_file_name) + '-' + str(self.headless) + '-' + '验证码.png'
        imgCaptcha.save(_save_url + yanzhengma_file_name)
#         print('--展示验证码图片-')
#         imgCaptcha.show()
        return  _save_url + yanzhengma_file_name






def getInputParams():
    ''' 获取用户输入的参数 '''
    parser = argparse.ArgumentParser()
    parser.description='please enter two parameters a and b ...'
    parser.add_argument("-a", "--inputA", help="this is parameter a", dest="argA", type=int, default="0")
    parser.add_argument("-b", "--inputB", help="this is parameter b",  type=int, default="1")
    parser.add_argument("--filepath", help="this is parameter c",  type=str, default="")
    parser.add_argument("--headless", help="0有界面,1无界面模式",  type=int, default=0)

    args = parser.parse_args()
    '''
    https://www.cnblogs.com/wutou/p/16975731.html
    https://code84.com/759656.html
    https://www.cnblogs.com/wutou/p/16975731.html 
    '''
    print("parameter a is :",args.argA)
    print("parameter b is :",args.inputB)
    print("parameter c is :",args.filepath,len(args.filepath) )
    '''
    python slip_python\gylkcspmxr.py --filepath=22
    python slip_python\gylkcspmxr.py --filepath=i
    python slip_python\gylkcspmxr.py --filepath=
    '''
    return args

def exec_main_account(item,args):
    ''' 执行 '''
    htmlParser = html_parser()
    # 是否使用无界面模式
    htmlParser.setHeadles(args.headless)
    if not args.headless :
        print('--取反-传0-' ,args.headless)
    print('创建浏览器')
    htmlParser.createNewBrowser()
    print('打开地址')
    htmlParser.openUrl()
    print('刷新')
    htmlParser.refresh()
    htmlParser.scrollLeft(num=1000)
    print('保存截图')
    htmlParser.screenShotDriver(fileName='初始化')
    # print('获取第一个公告的标题')
    # noticeTitle = htmlParser.getFirstNoticeTitle()
    # print('-获取第一个公告的标题-',noticeTitle)
    # print('获取源码')
    # htmlParser.getPageSource()
    ocrImgBool = htmlParser.orcImagePaser()
    print('==ocrImgBool==',ocrImgBool)
    htmlParser.saveImgByUrl()
    # print(htmlParser.user_html)


if __name__ == '__main__':
    # 有界面模式
    # python3 html_parser.py  --headless=0
    # 无界面模式
    # python3 html_parser.py  --headless=1
    args = getInputParams()
    if args.filepath :
        print('--args.filepath=',args.filepath)

    item = {}
    exec_main_account(item=item,args=args)















