'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-09-23 22:49:58
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\VATFT\src\funcs.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import os
import yaml
from func.web import *
from utils.logger import get_logger
from src import BASE_DIR
LOG = get_logger()

action_type_dict = {
	'WebAction': web_dict
}

PAGE_GROUP = {
		
}

def run_module(path: str = ''):
	
	current_browser = None
	current_page_id = 0
	
	with open(path, 'r', encoding='utf-8') as f:
		module_content = yaml.safe_load(f)
	
	for step_content in module_content['step']:
		action_type = step_content['action']
		method_name = step_content['method']
		params = step_content['params']
		
		if action_type == 'WebAction':
			# 获取要调用的方法对象
			method = action_type_dict[action_type][method_name]
			print(method)
			# 使用 **params 将字典作为关键字参数传入方法
			if method_name == 'NewBrowser':
				current_browser = method(**params)
			elif method_name == 'CloseBrowser':
				method(**params, browser=current_browser)
			elif method_name == 'NewPage':
				page = method(**params, browser=current_browser)
				page_id = params['id']
				PAGE_GROUP[page_id] = page
				current_page_id = page_id
			else:
				method(**params, page=PAGE_GROUP[current_page_id])


