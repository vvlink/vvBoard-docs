# WebGPIO框架

## 简介

WebGPIO是基于Flask、xugu库开发的虚谷号专用框架，是为了方便用户让虚谷号与手机互动（App inventor）而开发。想法由谢作如提出，李琦完成初稿，yyp在其基础上完善。

WebGPIO采用WebAPI的形式来获取和控制虚谷号板载Arduino芯片的引脚电平状态，用method的方式来判断是获取信息还是控制信号，参数非常简洁。

默认端口：1024

当前版本为0.1。

## 使用说明

WebAPI地址：

http://[虚谷号ip]:1024/

**注**：下面假设虚谷号的IP地址为：192.168.1.101

### 获取引脚状态

功能：读取引脚值

method方式:GET

参数示例：
{
	pin:"D1"
}

**注**：Arduino的引脚范围为：D0--D13，A0--A5，不分大小写。

url范例：http://192.168.1.101:1024/?pin=D1

信息返回：

当pin为D0--D13时，读取数字引脚的数字值，0为低电平，1为高电平。

{
	"pin":"D1",
	"error_code":0,
	"msg":1
}

当pin为A0--A5时，读取模拟引脚的模拟值，0-255之间。

{
	"pin":"A0",
	"error_code":0,
	"msg":255
}

当pin不为D0--D13，A0--A5时，返回错误代码。

{
	"pin":"A7",
	"error_code":1,
	"msg":"error,invalid Pin"
}

### 控制引脚电平

功能：设置引脚电平状态。

method方式: POST

参数示例：

{
	pin:"D1"
	value:255
	type:"digital" 
}

**注**：

1）Arduino的引脚范围为：D0--D13，A0--A5，不分大小写。；
2）type分为digital、analog和servo三种；
	- 当type为digital时，设置引脚的电平值为value的值，0表示LOW，非0表示HIGH；
	- 当type为analog时，设置引脚的PWM值为value的值，即0-255之间；
	- 当type为servo时，设置引脚上舵机的转动角度为value的值，即0-180之间。
3）Digital、Analog、Servo等词语不分大小写，也可以用“1、2、3”等数字来代替。

返回参数：

{
	"pin":"D2",
	"error_code":0,
	"msg":"success,set [pin] to [value] with [types] mode"
}

当pin不在D0--D13，A0--A5之间时：

{
	"pin":"D2",
	"error_code":1
	"msg":"error,invalid Pin"
}

当value不能转换整数时：

{
	"pin":"D2",
	"error_code":1,
	"msg":"error,Value is wrong"
}

当type不正确时：

{
	"pin":"D2",
	"error_code":1,
	"msg":"error,Type is wrong"
}

