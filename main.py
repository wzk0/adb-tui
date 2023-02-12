import os
import json
import random

raw_number=5
str_all='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def random_id():
	zero=0
	tid=[]
	while zero<=4:
		tid.append(random.choice(list(str_all)))
		zero+=1
	return ''.join(tid)

def adb(cmd):
	os.system('adb %s'%cmd)

def search_byaid(datalist,aid):
	for data in datalist:
		if data['aid']==aid:
			return data
		else:
			pass
	return 0

def search(pack_data,pack):
	for p in pack_data:
		if p['pack']==pack:
			return p
		else:
			pass
	return 0

def list_print(raw_list):
	os.system('clear')
	for element in range(len(raw_list)):
		print(str(element)+'. '+str(raw_list[element]),end=' │ ') if (element+1)%raw_number!=0 else print(str(element)+'. '+str(raw_list[element])+' │\n')
	print("\n")

def show_app_list():
	mode=input('只查看第三方软件(-3), 只查看系统软件(-s), 查看所有软件([回车]):')
	adb('shell pm list packages %s | grep %s >> temp'%(mode,input('请输入过滤内容(grep):')))
	with open('temp','r')as file:
		data=file.read().replace('package:','').split('\n')
		os.system('rm temp')
		data.remove('')
	with open('pack.json','r')as pack:
		pack_data=json.loads(pack.read())
	result_list=[]
	for item in data:
		result=search(pack_data,item)
		if result!=0:
			aid=random_id()
			result_list.append({'name':result['name'],'pack':result['pack'],'aid':aid})
			print('┌─ \033[1;34m%s\033[0m\n└── \033[1;37m[包名: %s]\033[0m  \033[1;32m[AID: %s]\033[0m\n'%(result['name'],result['pack'],aid))
		else:
			aid=random_id()
			result_list.append({'pack':item,'name':'','aid':aid})
			print('┌─ \033[1;34m%s\033[0m\n└── \033[1;32m[AID: %s]\033[0m\n'%(item,aid))
	return result_list

def main():
	menu=['查看信息','安装应用','卸载应用']
	list_print(menu)
	mode=int(input('请输入序号以继续:'))
	if mode==0:
		info_menu=['设备列表','进程信息','资源占用','CPU信息','内存信息','电池信息','IP地址','应用列表']
		list_print(info_menu)
		info_mode=int(input('请输入序号以继续:'))
		if info_mode==0:
			adb('devices')
		elif info_mode==1:
			adb('shell ps')
		elif info_mode==2:
			adb('shell top')
		elif info_mode==3:
			adb('shell dumpsys cpuifo')
		elif info_mode==4:
			adb('shell dumpsys meminfo')
		elif info_mode==5:
			adb('shell dumpsys battery')
		elif info_mode==6:
			adb('shell ifconfig')
		elif info_mode==7:
			show_app_list()
	if mode==1:
		address=input('请输入安装包链接或者本地地址:')
		if address.startswith('https://') or address.startswith('http://'):
			print('这似乎是一个链接, 正在调用wget下载...')
			os.system("wget -q '%s' -O 'temp.apk'"%address)
			adb('install temp.apk')
			os.system('rm temp.apk')
			print('安装结束, 已自动删除安装包!')
		else:
			adb('install %s'%address)
			if input('安装结束, 是/否(y/n)删除此安装包:')=='y':
				os.system('rm %s'%address)
			else:
				pass
	if mode==2:
		info=show_app_list()
		aids=input('请输入AID以卸载(多个AID请用,隔开):').split(',')
		for aid in aids:
			name=search_byaid(info,aid)
			if input('请回车以确认卸载\033[1;32m%s\033[0m:'%name['name'])=='':
				print('正在执行指令: adb shell pm uninstall --user 0 %s'%name['pack'])
				adb('shell pm uninstall --user 0 %s'%name['pack'])
			else:
				pass

if __name__ == '__main__':
	main()