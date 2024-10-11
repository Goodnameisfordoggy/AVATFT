import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Optional
from PySide6.QtCore import QCoreApplication


def open_file(path: str):
    """ 调用系统默认程序打开文件 """
    if sys.platform == "win32":
        subprocess.Popen(["start", path], shell=True)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:  # Linux
        subprocess.Popen(["xdg-open", path])
    

def load_file_content(path: str, logger: Optional[object] = None, translater: bool = False):
    """ 加载文件内容，根据路径匹配类型 """
    file_path = Path(path)

    # 检查文件是否存在
    if not file_path.is_file():
        if translater:
            msg = QCoreApplication.translate("Log_msg", "文件 {} 不存在").format(file_path)
        else:
            msg = "文件 {} 不存在".format(file_path)
        if logger:
            logger.critical(msg)
        else:
            raise FileNotFoundError(msg)

    # 根据文件扩展名加载内容
    try:
        if file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        elif file_path.suffix in ['.yaml', '.yml']:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        else:
            if translater:
                msg = QCoreApplication.translate("Log_msg", "不支持的文件类型: ").format(file_path.suffix)
            else:
                msg = "不支持的文件类型: ".format(file_path.suffix)
            if logger:
                logger.error(msg)
            else:
                raise ValueError(msg)
    except json.JSONDecodeError:
        if translater:
            msg = QCoreApplication.translate("Log_msg", "文件 {} 不是有效的 JSON 格式").format(file_path)
        else:
            msg = "文件 {} 不是有效的 JSON 格式".format(file_path)
        if logger:
            logger.error(msg)
        else:
            raise ValueError(msg)
    except yaml.YAMLError:
        if translater:
            msg = QCoreApplication.translate("Log_msg", "文件 {} 不是有效的 YAML 格式").format(file_path)
        else:
            msg = "文件 {} 不是有效的 YAML 格式".format(file_path)
        if logger:
            logger.error(msg)
        else:
            raise ValueError(msg)
    except Exception as e:
        if translater:
            msg = QCoreApplication.translate("Log_msg", "加载文件时发生错误：{}").format(e)
        else:
            msg = "加载文件时发生错误：{}".format(e)
        if logger:
            logger.error(msg)
        else:
            raise RuntimeError(msg)

def save_file_content(path: str, data: object, logger: Optional[object] = None, translater: bool = False):
    """ 保存文件内容，根据路径匹配类型 """
    file_path = Path(path)

    # 检查父目录是否存在
    if not file_path.parent.exists():
        if translater:
            msg = QCoreApplication.translate("Log_msg", "目录 {} 不存在").format(file_path.parent)
        else:
            msg = "目录 {} 不存在".format(file_path.parent)
        if logger:
            logger.critical(msg)
        else:
            raise FileNotFoundError(msg)

    try:
        if file_path.suffix == '.json':
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        elif file_path.suffix in ['.yaml', '.yml']:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)
        else:
            if translater:
                msg = QCoreApplication.translate("Log_msg", "不支持的文件类型: ").format(file_path.suffix)
            else:
                msg = "不支持的文件类型: ".format(file_path.suffix)
            if logger:
                logger.error(msg)
            raise ValueError(msg)
    except Exception as e:
        if translater:
            msg = QCoreApplication.translate("Log_msg", "保存文件时发生错误：{}").format(e)
        else:
            msg = "保存文件时发生错误：{}".format(e)
        if logger:
            logger.error(msg)
        else:
            raise RuntimeError(msg)
