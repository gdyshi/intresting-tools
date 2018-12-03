# 相关工具库

## python2.7

[下载地址](https://www.python.org/downloads/)

## pyhook

安装`pip install pyHook-1.5.1-cp27-cp27m-win_amd64.whl` [下载地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)

## pywin32

安装`pip install xxx.whl` [下载地址](https://pypi.org/project/pypiwin32/219/)

# 配置开机启动
- 创建启动脚本的快捷方式
- 命令窗口输入`shell:startup`
- 移动快捷方式

# 调试中出现的问题

python3 会出现对中文字符的支持问题`TypeError: MouseSwitch() missing 8 required positional arguments: 'msg', 'x', 'y', 'data', 'flags', 'time', 'hwnd', and 'window_name'`
使用python2来解决

# 参考

- [用Python监听鼠标和键盘事件](https://www.cnblogs.com/qiernonstop/p/3654021.html)
