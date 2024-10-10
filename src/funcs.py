'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-10 23:23:03
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\AVATFT\src\funcs.py
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
import typing
from src.func.web import *
from src.utils.logger import get_logger
from src import BASE_DIR
LOG = get_logger()

action_type_dict = {
	'WebAction': web_dict
}
PLAYWRIGHT = None
PAGE_GROUP = {
	
}


def initialize_playwright():
	"""检查并初始化 Playwright"""
	global PLAYWRIGHT
	if not PLAYWRIGHT:
		PLAYWRIGHT = sync_playwright().start()
		LOG.trace('Playwright start')

def run_module(path: str = ''):
	""" 运行单个模块 """
	current_browser = None
	current_page_id = 0
	
	try:
		with open(path, 'r', encoding='utf-8') as f:
			module_content = yaml.safe_load(f)
	except FileNotFoundError:
		LOG.critical(f"File {path} not found.")
		return
	except yaml.YAMLError as e:
		LOG.error(f"Error parsing YAML: {e}")
		return
	LOG.success(f'正在运行--{module_content['info']['describe']}--id:{module_content['info']['id']}--title:{module_content['info']['title']}')
	initialize_playwright()
	
	for step_content in module_content['step']:
		action_type: str = step_content['action']
		method_name: str = step_content['method']
		params: dict = step_content['params']
		# 获取要调用的方法对象
		method = action_type_dict[action_type][method_name]
		LOG.trace(f'{method.__module__}:{method.__name__}')
		if action_type == 'WebAction':
			# 使用 **params 将字典作为关键字参数传入方法
			if method_name == 'NewBrowser':
				current_browser = method(**params, playwright=PLAYWRIGHT)
			elif method_name == 'CloseBrowser':
				method(**params, browser=current_browser)
			elif method_name == 'NewPage':
				page = method(**params, playwright=PLAYWRIGHT, browser=current_browser)
				page_id = params['id']
				PAGE_GROUP[page_id] = page
				current_page_id = page_id
			else:
				method(**params, page=PAGE_GROUP[current_page_id])
				
@typing.overload
def run(task_list: list[(int, str)]):...
@typing.overload
def run(path_list: list[str]):...
def run(task_list: list[(int, str)] = [], path_list: list[str] = []):
	""" 
	运行，根据任务队列 
	
	:param task_list: [ ( id(int), path(str) ) ] path: 可运行的单个模块的路径；id: 该模块运行次序
	:param path_list: [ path(str) ] 可运行的单个模块的路径列表
	"""
	task_queue = []
	if path_list:
		for path in path_list:
			try:
				with open(path, 'r', encoding='utf-8') as f:
					module_content = yaml.safe_load(f)
			except FileNotFoundError:
				LOG.critical(f"File {path} not found.")
				return
			except yaml.YAMLError as e:
				LOG.error(f"Error parsing YAML: {e}")
				return
			module_id = module_content['info']['id']
			task_queue.append((module_id, path))
	elif task_list:
		task_queue = task_list
	task_queue.sort(key=lambda x: x[0])
	
	for task in task_queue:
		run_module(task[1])