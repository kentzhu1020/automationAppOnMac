# coding: utf-8
import os
import atomac
from atomac.AXKeyCodeConstants import *
import time
import commands
import math
import keys_event
from atomac import AXKeyCodeConstants
from object_repository import object_repo

global log_file
global log_dir
global log_file

def logger(msg=' '):
    ''' To log the activities of the program '''
    try:
        if os.path.isfile(log_file):
            log_fp.write("\n")
            print msg
            log_fp.write(msg)
        else:
            print "[+] Looks like the Log Directory or Log File is not found"
            print "[+] Creating log file and directory for the first time"
            os.system("mkdir -p "+log_dir)
            os.system("touch"+log_file)
            log_fp =open(log_file,'a')
            log_fp.write("\n")
            print msg
            log_fp.write(msg)
    except Exception as er:
        print "[-] Exception occurred while calling the logger "
        print "[-] Error is "+str(er)

def open_app(cbundID):
    ''' To open the App '''
    try:
        logger("[+] Opening the "+cbundID+"app")
        atomac.launchAppByBundleId(cbundleID)
        time.sleep(3)
        app = atomac.getAppRefByBundleId(cbundleID)
        app.activate()
    except Exception as er:
        logger("[-] Exception while opening the app")
        logger("[-] Error @open_app is "+str(er))

def close_app(cbundleID):
    '''To close the app and kill the process '''
    try:
        logger("[+] Closing the "+cbundID+"app")
        atomac.terminateAppByBundleId(cbundleID)
        logger("Force killing  the process with signal")
        os.system("ps -eaf|grep -i 'Notes'|grep -v grep|awk '{print $2}'|xargs kill ")
        time.sleep(3)
    except Exception as er:
        logger("[-] Exception while opening the app")
        logger("[-] Error @open_app is "+str(er))

def  click_left(obj):
    '''Mouse left click action on object '''
    position = obj.AXPosition 
    size = obj.AXSize
    clickpoint = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
    try:
        obj.clickMouseButtonLeft(clickpoint)
    except Exception as er:
        # logger("[-] Error @click_left")
        # logger("[-] Error is " + str(er))
        print "[-] Error occur @click_left"

def click_right(obj):
    '''Mouse right click action on object '''
    position = obj.AXPosition
    size = obj.AXSize
    clickpoint = ((position[0] + size[0] / 2), (position[1] + size[1] / 2))
    try:
        obj.clickMouseButtonRight(clickpoint)
    except Exception as er:
        logger("[-] Error @click_right")
        logger("[-] Error is " + str(er))

def select_right_click_menu(app,obj,index):
    '''select the menu item after right click the object'''
  
    try:
        if index <= 0:
            print "[-] Exception occurred @select_right_click_menu "
            print "[-] Exception is: index is less than 0 "
        else:
            click_right(obj)
            for i in range(1,index+1):
                app.sendKey(DOWN)
            app.sendKey(RETURN)
    except Exception as er:
        logger("[-] Error @select_right_click_menu")
        logger("[-] Error is "+str(er))

def fill_text(text_field,text=''):
    try:
        click_left(text_field)
        text_field.sendKeys(text)
        text_field.sendKey(RETURN)
    except Exception as er:
        logger("[-] Error @fill_text")
        logger("[-] Error is"+str(er))

def validate_message(msg_validate= ''):
    '''Validation of the message '''
    pass

def view_profile(cbundleID,index,remark=''):
    ''' View the profile and change the remark '''
    try:
        app = atomac.getAppRefByBundleId(cbundleID)
        chat_window = app.findFirst(AXRole=object_repo['unknown_window']['AXRole'],AXSubrole=object_repo['unknown_window']['AXSubrole'])
        time.sleep(2)
        panel = chat_window.findFirst(AXRole=object_repo['split_panel']['AXRole'])
        time.sleep(2)
        name_list_panel = panel.findFirst(AXRole=object_repo['scroll_area']['AXRole'])
        time.sleep(2)
        row_item = name_list_panel.findAll(AXRole=object_repo['row_item']['AXRole'])
        for item in row_item:
            if item.AXIndex == index -1:
                select_right_click_menu(app,item,1)
                break
        time.sleep(3)
        profile_window =app.windows()[1]
        profile_detail_panel = profile_window.findFirst(AXRole=object_repo['scroll_area']['AXRole'])
        time.sleep(2)
        remark_button = profile_detail_panel.findFirst(AXRole=object_repo['remark_button']['AXRole'])
        time.sleep(2)
        remark_button.Press()
        time.sleep(1)
        remark_field = profile_detail_panel.textFileds()[0]
        fill_text(remark_field,remark)
        close_profile_checkbox =profile_window.findFirst(AXRole=object_repo['remark_button']['AXRole'],AXIdentifier=object_repo['remark_button']['AXIdentifier'])
        time.sleep(2)
        close_profile_checkbox.Press()
    except Exception as er :
        logger("[-] Error @view_profile")
        logger("[-] Error is "+str(er))

def send_message(cbundleID,name='',msg=''):
    '''serach the name whom is trying to start a chat with '''
    '''send message to the guy whom you are chatting with'''
    try:
        app = atomac.getAppRefByBundleId(cbundleID)
        chat_window = app.windows()[0]
        time.sleep(2)
        panel = chat_window.findFirst(AXRole=object_repo['split_panel']['AXRole'])
        time.sleep(2)
        serach_field = panel.textFileds()[0]
        fill_text(serach_field,name)
        chat_panel=panel.findFirst(AXRole=object_repo['split_panel']['AXRole'])
        time.sleep(2)
        emotion_button = chat_panel.findFirst()
        input_srcoll_area = chat_panel.findAll(AXRole=object_repo['scroll_area']['AXRole'])[1]
        time.sleep(2)
        input_area =input_srcoll_area.textAreas()[0]
        fill_text(input_area,msg)
    except Exception as er :
        logger("[-] Error @view_profile")
        logger("[-] Error is "+str(er))

def cut_screen_shot(app,obj):
    try:
        position = obj.AXPosition
        size = obj.AXSize
        start_posx = position[0]
        start_posy = position[1]
        dest_posx = position[0]+size[0]
        dest_posy = position[1]+size[1]
        double_click_posx = position[0]+size[0]/2
        double_click_posy = position[1]+size[1]/2
        double_click_coord = (double_click_posx,double_click_posy)
        time.sleep(1)
        key_event.mousemove(start_posx,start_posy)
        key_event.mouseclickdn(start_posx,start_posy)
        key_event.mousedrag(dest_posx,dest_posy)
        key_event.mouseclickup(dest_posx,dest_posy)
        time.sleep(2)
        app.doubleClickMouse(double_click_coord)
    except Exception as er:
        logger("[-] Error @cut_screen_shot") 
        logger("[-] Error is "+str(er)) 


def check_button_functionality(cbundleID,obj_to_screenshot_cut,matrix_x=0,matrix_y=0):
    '''Check the functionality on the split panel:
       --send emotion icons
       --send nudge
       --cut sreenshot
       --send picture
       --message mamagement
    '''
    try:
        app = atomac.getAppRefByBundleId(cbundleID)
        chat_window = app.windows()[0]
        time.sleep(2)
        panel = chat_window.findFirst(AXRole=object_repo['split_panel']['AXRole'])
        time.sleep(2)
        chat_panel=panel.findFirst(AXRole=object_repo['split_panel']['AXRole'])
        time.sleep(2)
        buttons = chat_panel.findAll(AXRole=object_repo['button']['AXRole'])
        time.sleep(2)
        # send a nudge
        # nudge_button = buttons[2]
        # nudge_button.Press()
        # # send a emotion icon
        # time.sleep(2)
        # emotion_button = buttons[0]
        # click_left(emotion_button)
        # emotion_window = app.findFirst(AXRole=object_repo['unknown_window']['AXRole'],AXSubrole=object_repo['unknown_window']['AXSubrole'])
        # time.sleep(2)
        # emotion_panel =emotion_window.findFirst(AXRole=object_repo['scroll_area']['AXRole'])
        # time.sleep(2)
        # position = emotion_panel.AXPosition
        # size = emotion_panel.AXSize
        # clickpoint = ((position[0] + math.floor(size[0] / 11) * matrix_x), (position[1] + math.floor(size[1] / 5) * matrix_y))
        # emotion_panel.clickMouseButtonLeft(clickpoint)
        # app.sendKey(RETURN)
        # send a sreen shot
        screen_shot_button = buttons[1]
        # screen_shot_button_position = screen_shot_button.AXPosition
        # screen_shot_button_size =screen_shot_button.AXSize
        # start_posx = screen_shot_button_position[0]
        # start_posy = screen_shot_button_position[1]
        # dest_posx = screen_shot_button_position[0]+screen_shot_button_size[0]
        # dest_posy = screen_shot_button_position[1]+screen_shot_button_size[1]
        # double_click_posx = screen_shot_button_position[0]+screen_shot_button_size[0]/2
        # double_click_posy = screen_shot_button_position[1]+screen_shot_button_size[1]/2
        # double_click_coord = (double_click_posx,double_click_posy)

        # key_event.mousemove(start_posx,start_posy)
        # key_event.mouseclickdn(start_posx,start_posy)
        # key_event.mousedrag(dest_posx,dest_posy)
        # key_event.mouseclickup(dest_posx,dest_posy)
        # app.doubleClickMouse(double_click_coord)
        # time.sleep(1)
        click_left(screen_shot_button)
        time.sleep(2)
        cut_screen_shot(app,obj_to_screenshot_cut)
        app.sendKey(RETURN)

        # upload picture(s)
        upload_pic_button = buttons[3]
        upload_pic_button.Press()


    except Exception as er:
        print "[-] Error @check_button_functionality"
        print "[-] Error is "+str(er)



def login_app(cbundleID):
    '''login application with username and password'''
    try:
        atomac.launchAppByBundleId(cbundleID)
        app = atomac.getAppRefByBundleId(cbundleID)
        login_window = app.windows()[0]
        time.sleep(2)
        username  = login_window.textFields()[0]
        click_left(username)
        username.sendKeys("YOUR-USERNAME")
        time.sleep(2)
        password = login_window.textFields()[1]
        click_left(password)
        password.sendKeys("YOUR-PASSWORD")
        login_checkbox = login_window.findFirst(AXRole=object_repo['login_checkbox']['AXRole'],AXIdentifier=object_repo['login_checkbox']['AXIdentifier'])
        login_checkbox.Press()
    except Exception as er:
        print "[-] Error @login_app"
        print "[-] Error is "+str(er)

cbundleID = 'com.tencent.qq'

login_app(cbundleID)











