# -*- coding: utf-8 -*-
#
# by oldj
# http://oldj.net/
#

import pythoncom
import pyHook
import time

last_position = (0, 0)
fo=None

def logMouse(event):
    global fo
    if fo is None:
        print("MessageName:", event.MessageName)
        print("Message:", event.Message)
        print("Time:", time.ctime(time.time()))
        print("Window:", event.Window)
        print("WindowName:", event.WindowName)
        print("Position:", event.Position)
        print("Wheel:", event.Wheel)
        print("Injected:", event.Injected)
        print("---")
    else:
        fo.write("MessageName:{}\n".format(event.MessageName))
        fo.write("Message:{}\n".format(event.Message))
        fo.write("Time:{}\n".format(time.ctime(time.time())))
        fo.write("Window:{}\n".format(event.Window))
        fo.write("WindowName:{}\n".format(event.WindowName))
        fo.write("Position:{}\n".format(event.Position))
        fo.write("Wheel:{}\n".format(event.Wheel))
        fo.write("Injected:{}\n".format(event.Injected))
        fo.write("---\n")
        fo.flush()


def onMouseEvent(event):
    global last_position
    distance = 400
    if ('mouse move' == event.MessageName):
        # print('move')
        # todo 到任务栏时 TypeError: MouseSwitch() missing 8 required positional arguments: 'msg', 'x', 'y', 'data', 'flags', 'time', 'hwnd', and 'window_name'
        cur_position = event.Position
        if (distance < abs(last_position[0] - cur_position[0])) or (distance < abs(last_position[1] - cur_position[1])):
            last_position = cur_position
            logMouse(event)
    else:
        logMouse(event)
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


def logKeyboard(event):
    global fo
    if fo is None:
        print("MessageName:", event.MessageName)
        print("Message:", event.Message)
        print("Time:", time.ctime(time.time()))
        print("Window:", event.Window)
        print("WindowName:", event.WindowName)
        print("Ascii:", event.Ascii, chr(event.Ascii))
        print("Key:", event.Key)
        print("KeyID:", event.KeyID)
        print("ScanCode:", event.ScanCode)
        print("Extended:", event.Extended)
        print("Injected:", event.Injected)
        print("Alt", event.Alt)
        print("Transition", event.Transition)
        print("---")
    else:
        fo.write("MessageName:{}\n".format(event.MessageName))
        fo.write("Message:{}\n".format(event.Message))
        fo.write("Time:{}\n".format(time.ctime(time.time())))
        fo.write("Window:{}\n".format(event.Window))
        fo.write("WindowName:{}\n".format(event.WindowName))
        fo.write("Ascii:{}\n".format(event.Ascii, chr(event.Ascii)))
        fo.write("Key:{}\n".format(event.Key))
        fo.write("KeyID:{}\n".format(event.KeyID))
        fo.write("ScanCode:{}\n".format(event.ScanCode))
        fo.write("Extended:{}\n".format(event.Extended))
        fo.write("Injected:{}\n".format(event.Injected))
        fo.write("Alt{}\n".format(event.Alt))
        fo.write("Transition{}\n".format(event.Transition))
        fo.write("---\n")
        fo.flush()


def onKeyboardEvent(event):
    logKeyboard(event)
    # 同鼠标事件监听函数的返回值
    return True


def main():
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    global fo
    fo = open("foo_{}.ddt".format(time.time()), "w")

    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()

    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    hm.HookMouse()

    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()
    if fo is not None:
        fo.close()


if __name__ == "__main__":
    main()
