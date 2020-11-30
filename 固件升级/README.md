# 虚谷号版本升级记录

固件下载地址：http://www.vvboard.com.cn/plus/view.php?aid=6

版本号: Linux vvBoard OS 基础版V2.3.4 aarch64
发布时间：2020年7月20日

创客版（1+8）百度云固件下载地址
链接：https://pan.baidu.com/s/1N7uwrbW0ThYOVp2Yj7nU4w
提取码：gc7w

### 版本更新内容：

1.  加入支持快速部署模式，详见“虚谷U盘快速部署功能说明.pdf”
2.  新增SSH的链接策略
3.  关闭新增软件的自动更新功能，使其不会跳出自动更新窗口
4.  优化虚谷PC软件接口及启动的目录结构
5.  增加支持pymata4的arduino协议。
6.  增加pymata4 案例程序
7.  修改Jupyter权限组，由原来的root改为scope。
8.  改进蓝牙自动链接方式
9.  修正U盘模式下链接问题
10. 增加默认U盘开机/插入自动挂载功能
11. 更新芯片端串口驱动补丁

## 固件版本：9.20日固件
### 版本更新内容：
- 更新虚谷号使用说明书和虚谷号GPIO使用文档
- 更换Arduino IDE版本为1.6.10
- 集成siot，并且在vvBoard中可配置打开与关闭
- Python_log通过配置run_time打印，run_time值为多少，则打印多长时间内的log
- 删除ArduBlockTool
- 解决WiFi名称和密码有空格不能连接的问题
- 解决菜单人头打开出错的问题
- 屏蔽菜单里使用浏览器的选项
- 解决Jupyter不能使用虚谷库的问题和添加vvBoardBook，存放GPIO例程和在画布上画画的例程
- 解决虚谷库python运行串口打印程序后，再次运行不能使用的问题
- 解决python运行完analog的程序，再运行类似点阵的程序报错问题
- 去掉U盘中.ino代码里不必要的解释
- 在vvBoard/vvBoard/tools里放入文本编辑器
- 在vvBoard/Python/03.doc中放入python库说明
- 解决python使用虚谷库里面的pwm（analog_write）没有现象的问题
- 更改vvBoard/Python/01.example/11.vvBox里的Python示例文档并且更改部分代码的引脚
- 解决vvBoard/Python/01.example中两个文件夹命名错误的问题
- 当wifi和jupyter同时打开，生成一个jupyter的Windows网页快捷方式；当wifi和siot同时打开，生成一个siot的Windows网页快捷方式
- Python库增加了yeelight、paho-mqtt、pyflakes、ipyturtle
- 在/usr/share/fonts/Fonts中添加了Windows的几种常规字库


## 固件版本：xugu_xubuntu16.04_20190702(2019/07/02)
### 版本更新内容：
- 更新虚谷号使用说明书和虚谷号GPIO使用文档
- 解决Arduino闪退问题
- 关闭Arduino IDE的更新提示
- 隐藏chromium浏览器和网络浏览器
- 更改vvBoard目录结构
- 集成SAMBA和SSH的工作方式
- 修改了固件烧录工具，可单独烧录rootfs
- 添加arublock的方法：将home/scope/software目录下的ArduBlockTool文件放人Larduino_HSP_v3.6c/tool目录下，代开arduino ide便可在tool中看到ArduBlock(此功能会影响arduino ide打开的速度)
- 不带流水编码的板子不能使用此版本的vvBoard功能
- 更改桌面默认分辨率为800*600

## 固件版本：xugu_xubuntu16.04_20190320(2019/03/20)
###  版本更新内容：
- 添加S4A软件
- 添加ttyUSB-vvBoard节点，让S4A与scratch能够与arduino相连接
- 更新虚谷库
- 更新Python例程
- 添加python库pyfirmata
- 添加长按reset键10秒以上，恢复桌面部分图标
- 在vvBoard/tool中添加kitty_portable.exe
- 此版本python log不能使用
- 拥有USB转虚拟串口的功能，目前建议win10 、mac、 linux用户可以使用此功能
- 添加simsun.ttc在/usr/lib/目录下
- 在vvBoard:example/arduino下添加picoboard.ino 与 S4AFirmware16.ino


## 固件版本：xugu_xubuntu16.04_20190307(2019/03/07)
### 版本更新内容：
- 优化了arduino IDE打开速度
- 解决jupyter因权限问题无法打开ipynb文件
- 解决MAC系统使用vvBoard时config.txt文件为空


## 固件版本：xugu_xubuntu16.04_20190302(2019/03/02)
### 版本更新内容：
- 修改烧写arduino.ino文件后剪切到upload/Arduino_bak目录下
- U盘模式中配置config.txt文件打开Jupyter，配置方法：Jupyter=true
- U盘模式，默认烧写uploade下的Arduino.ino/arduino.ino命名的文件。
- U盘模式，默认执行uploade/python下的main.py/Main.py
- U盘模式中，config.txt有配置Arduino和python文件名时，先去搜索执行该文件，若未找到该文件，默认搜索以上两点的文件名
- 添加虚谷库示例程序
- 添加配置Jupyter可以使用默认浏览器打开
- 更新使用文档
- 更新版本查询uname命令输出内容格式


## 固件版本：xugu_xubuntu16.04_20190221(2019/02/21)
### 版本更新内容：
- 升级固件后不接显示器可以开机
- upyter提供网络连接，详情请见论坛http://www.vvboard.com.cn/bbs/forum.php?mod=viewthread&tid=29&extra=page%3D1
- 整理简化桌面图标
- 修复vvBoard分区锁死问题
- 添加config.txt文件恢复机制，禁止删除config.txt文件中配置信息
- 添加vvBoard恢复机制，禁止删除vvBoard下任何文件夹，否则会格式化vvBoard。
- 添加版本信息，查询命令：uname
- 添加烧写arduino.ino文件后拷贝到upload/Arduino_bak目录下


紧急说明：升级xugu_xubuntu16.04_20190112(2019/01/12)
固件时，请连接hdmi显示器

固件版本：xugu_xubuntu16.04_20190112(2019/01/12)
版本更新内容：
62.	添加hdmi热插拔功能
63.	添加U盘升级功能，需要sudo权限执行，令格式如下 sudo backuprootfs $1，$1是U盘的硬件节点，插上U盘后，输入ls /dev/sd*来查看硬件节点，例如，显示有sda sda1，那么命令就是sudo update_system /dev/sda1。
64.	修改vvBoard（U盘模式启动方式），使用硬件分区
65.	修改vvBoard桌面图标
66.	修改getit默认使用空格
67.	更新python例程，添加注释
68.	添加使用文档在dosc下

固件版本：xugu_xubuntu16.04_20190104(2019/01/04)
版本更新内容：
69.	on库：pygame、turtle
70.	解决打开浏览器出现密钥框
71.	解决arduino ide串口框打不开
72.	将gedit制表位默认设置为4
73.	Config.txt在windows下没换行问题
74.	Vvboard下，python_log反馈问题
75.	更新gpio使用文档
76.	添加arduino_burn.sh使用文档
77.	添加serson使用文档
78.	添加serson的arduino例程和python例程在vvboard/example目录下
79.	浏览器默认打开vvboard主页，搜索引擎默认为百度
80.	更换pip3源为清华源

固件版本：xugu_xubuntu16.04_20181225(2018/12/25)
版本更新内容：
81.	此固件为全功能固件，适配2+32以上版本的虚谷号

固件版本：xugu_xubuntu16.04_20181225(2018/12/25)
版本更新内容：
82.	针对8G版本专用固件，优化应用程序。
83.	解决Arduino IDE烧写问题
84.	预装Python库：
对以下库opencv3-contrib、VPython、Matplotlib、flask numpy、Pandas、redis、zxing、SymPy、pySerial、pymysql、sqlite3、scipy、pymate-aio的支持。
85.	解决Jupyter不能打开
86.	修改桌面结构，将任务栏下移
87.	添加WIFI自动连接功能，需要在vvBOARD/upload/config.txt中配置SSID以及SSID_PSD，刷新vvBOARD自动连接。
88.	增加联网自动获取时间
89.	将arduino_burn.sh放进全局变量，方便用户调用。
90.	增加backuprootfs备份系统脚本，需要sudo权限执行，命令格式如下 sudo backuprootfs $1 $2,$1是U盘名称，查看方式ls /media/scope/  下面的文件夹既是U盘名字 ， $2是要备份系统大小，既(/dev/root)+500M，查看方式 sudo df -h ，看/dev/root目录的大小加上500M即可。大小以1M为单位。
91.	在vvBOARD/upload/下添加log文件夹，里面存放system_log、wifi_log、python_log、arduino_log。
92.	关闭屏幕保护
93.	添加第一次开机提示界面
94.	Arduino IDE添加ardublock支持，需在File->Prefereces中的Sketchbook location选择/home/scope/software/Larduino_HSP_v3.6c/sketches目录，并重启arduino IDE。
95.	添加loader模式支持，方便烧写固件，按住RST按键，上电后烧写工具识别loader后松开。
96.	在vvBOARD/upload下添加Arduino_lib文件夹，将arduino的库放进此文件夹下，即可使用。

固件版本：xugu_xubuntu16.04_20181218(2018/12/18)
版本更新内容：
97.	内核升级到最新的linux 4.4，同步rk对外发布的最新版本
98.	文件系统使用 64位的ubuntu 16.04版本。
99.	默认安装如下软件： 
Arduino IDE
Python 3.6
Scratch  1.4
Chrome浏览器
Gedit
  Inkscape
  Jupyter
  LX终端
  Processing IDE
  媒体播放器
pdf浏览器
       office应用
       CAD绘图软件
