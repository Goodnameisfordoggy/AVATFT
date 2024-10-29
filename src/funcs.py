'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-10-29 23:55:48
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
import re
import typing
from multiprocessing import Process, Pool

from src.utils.file import load_file_content, save_file_content
from src.func import *
from src.utils.logger import get_logger
LOG = get_logger()

PLAYWRIGHT = None
PAGE_GROUP = {} 


def run_module(path: str = ''):
	""" 运行单个模块 """
	VARIABLES = {} # 变量生命周期为单个模块运行期间
	current_browser = None
	current_page_id = 0
	
	module_content = load_file_content(path, logger=LOG, translater=True)
	LOG.success(f'正在运行--{module_content['info']['describe']}--id:{module_content['info']['id']}--title:{module_content['info']['title']}')
	__initialize_playwright()
	
	for step_content in module_content['step']:
		action_type: str = step_content['action']
		method_name: str = step_content['method']
		params: dict = step_content['params']
		# 获取要调用的方法对象
		method = ACTION_TYPE[action_type][method_name]
		LOG.trace(f'{method.__module__}:{method.__name__}')
		
		for key, value in params.items():
			match = re.match(r'\$\{(.+?)\}', str(value)) # value 符合参数格式'${var_name}'
			if match and match.group(0) == value: # 参数格式匹配，且内含参数名也一致
				if match.group(1) in list(VARIABLES.keys()): # 参数名在 VARIABLES 中存在时
					params[key] = VARIABLES[match.group(1)]
				else:
					if key == "Result":
						LOG.trace("创建参数 '{}' 成功".format(match.group(1)))
					else:
						# 参数名在 VARIABLES 不存在，
						LOG.warning("不能使用未定义的参数 '{}' 作为值".format(match.group(1)))
		if action_type == 'WebAction':
			# 使用 **params 将字典作为关键字参数传入方法
			if method_name == 'NewBrowser':
				current_browser, current_context = method(**params, playwright=PLAYWRIGHT)
			elif method_name == 'CloseBrowser':
				method(**params, browser=current_browser)
			elif method_name == 'NewPage':
				page = method(**params, context=current_context)
				page_id = params['id']
				PAGE_GROUP[page_id] = page
				current_page_id = page_id
			else:
				result = method(**params, page=PAGE_GROUP[current_page_id])
				# 根据返回值创建变量
				if result and 'Result' in params:
					match = re.match(r'\$\{(.+?)\}', str(params['Result']))
					var_name = match.group(1)
					var_value = result
					VARIABLES[var_name] = var_value
		else:
			result = method(**params)
			# 根据返回值创建变量
			if result and 'Result' in params:
				match = re.match(r'\$\{(.+?)\}', str(params['Result']))
				var_name = match.group(1)
				var_value = result
				VARIABLES[var_name] = var_value
		# LOG.debug(f'{VARIABLES}')

@typing.overload
def get_ordered_queue(task_list: list[(int, str)]) -> list:...
@typing.overload
def get_ordered_queue(path_list: list[str]) -> list:...
def get_ordered_queue(task_list: list[(int, str)] = [], path_list: list[str] = []) -> list:
	""" 
	获取有序的任务队列 
	
	:param task_list: [ ( id(int), path(str) ) ] path: 可运行的单个模块的路径；id: 该模块运行次序
	:param path_list: [ path(str) ] 可运行的单个模块的路径列表
	"""
	task_queue = []
	if path_list:
		for path in path_list:
			module_content = load_file_content(path, logger=LOG, translater=True)
			module_id = module_content['info']['id']
			task_queue.append((module_id, path))
	elif task_list:
		task_queue = task_list
		
	task_queue.sort(key=lambda x: x[0])
	return task_queue

def run_module_process(path: str):
	""" 使用新进程运行单个模块 """
	process_name = os.path.splitext(os.path.basename(path))[0]
	process = Process(target=run_module, name=process_name, args=(path,))
	process.start()
	process.join()

def run_modules_processes_concurrently(task_queue: list[typing.Tuple[int, str]]):
	"""使用多进程并发的模式运行多个模块"""
	pool_size = min(len(task_queue), os.cpu_count() / 2)  # 使用CPU核心数量的1/2或任务数量中的最小值
	with Pool(processes=pool_size) as pool:
		# 使用map方法将任务分配给进程池中的进程
		pool.map(run_module, [task[1] for task in task_queue])  # paths为路径列表
		pool.close()
		pool.join()

def run_modules_processes_sequentially(task_queue: list[typing.Tuple[int, str]]):
    """使用进程依次运行多个模块"""
    processes = []
    
    for task in task_queue:
        # 为每个任务创建新的进程
        process = Process(target=run_module, args=(task[1],))
        processes.append(process)
        process.start()  # 启动进程
        process.join() # 等待当前进程完成，再启动下一个进程

def __initialize_playwright():
	"""检查并初始化 Playwright"""
	global PLAYWRIGHT # sync_playwright() 不支持跨线程调用，启用进程执行任务时使用全局 PLAYWRIGHT
	if not PLAYWRIGHT:
		PLAYWRIGHT = sync_playwright().start()
		LOG.trace('Playwright start')