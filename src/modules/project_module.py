import os
import shutil
from PySide6.QtCore import Qt, QCoreApplication

from . import LOG
from src import TEMPLATE_DIR

def new_module_file(path: str) -> bool:
    """ 
    创建 module 级配置文件 
    
    :param path: 目标文件路径
    """
    if not os.path.exists(path):
        if paste_file(os.path.join(TEMPLATE_DIR, 'module_template.yaml'), path, 'COPY'): # 直接使用模版文件初始化
            LOG.success(QCoreApplication.translate("ProjectDock", "测试用例已经使用模板文件初始化", "Log_msg"))
            return True
        # config_data = {}
        # # 创建并写入 YAML 文件
        # with open(path, 'w') as f:
        #     yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    else:
        LOG.warning(QCoreApplication.translate("ProjectDock", "目标位置中存在同名文件，新建操作已取消", "Log_msg"))

def new_package_file(path: str) -> bool:
    """ 
    创建 package 目录
    
    :param path: 目标目录路径
    """
    if path:
        try:
            os.mkdir(path)
            LOG.success(QCoreApplication.translate("ProjectDock", "测试集 {} 创建成功：", "Log_msg").format(path))
            return True
        except FileExistsError:
            LOG.warning(QCoreApplication.translate("ProjectDock", "目录 {} 已存在", "Log_msg").format(path))

def paste_file(source: str, target: str, pre_event: str = '') -> bool:
    """ 
    剪切或复制后粘贴文件 
    
    :param source: 原文件路径
    :param target: 目标位路径
    :param pre_event: CUT | COPY
    """
    if source:
        if os.path.exists(target): # 目标位置存在文件
            LOG.trace('A file with the same name exists at the destination location, pasting has been canceled')
            return
        if os.path.splitext(os.path.basename(source))[1] != os.path.splitext(os.path.basename(target))[1]:
            LOG.warning(QCoreApplication.translate("ProjectDock", "请注意，源文件的后缀与目标文件不同", "Log_msg"))
        if not pre_event:
            LOG.trace('Param pre_event should be set to CUT or COPY')
        # 剪切粘贴
        if pre_event == 'CUT': 
            shutil.move(source, target) # 移动文件或目录
            return True
        # 复制粘贴
        elif pre_event == 'COPY': 
            # 拷贝文件或目录
            if os.path.isfile(source):
                shutil.copy(source, target)
                LOG.trace(f'File copy successfully at {target}')
                return True
            elif os.path.isdir(source):
                shutil.copytree(source, target)
                LOG.trace(f'Directory copy successfully at {target}')
                return True
            else:
                LOG.error(QCoreApplication.translate("ProjectDock", "{} 不是文件或目录", "Log_msg").format(source))

def delete_file(path: str) -> bool:
    """" 
    删除文件 
    
    :param path: 目标文件路径
    """
    if os.path.exists(path):  # 检查路径是否存在
        if os.path.isfile(path):
            try:
                os.remove(path)
                LOG.trace(f"File at '{path}' delete successfully")
                return True
            except PermissionError:
                LOG.warning(QCoreApplication.translate("ProjectDock", "没有权限删除文件: {}", "Log_msg").format(path))
            except Exception as e:
                LOG.error(QCoreApplication.translate("ProjectDock", "发生错误：{}", "Log_msg").format(e))
        elif os.path.isdir(path): # 如果是目录直接删除，不考虑是否为空
            try:
                shutil.rmtree(path)
                LOG.trace(f"Directory at {path} delete successfully")
                return True
            except PermissionError:
                LOG.warning(QCoreApplication.translate("ProjectDock", "没有权限删除目录: {}", "Log_msg").format(path))
            except Exception as e:
                LOG.error(QCoreApplication.translate("ProjectDock", "发生错误：{}", "Log_msg").format(e))
        else:
            LOG.warning(QCoreApplication.translate("ProjectDock", "文件 {} 不存在", "Log_msg").format(path))

def rename_file(path: str, name: str = '') -> str:
    """ 
    重命名文件或目录
    
    :param path: 目标文件路径
    :param name: 要更改的名称
    :return: 更改完名称的文件绝对路径
    """
    if os.path.exists(path):  # 检查路径是否存在
        dirname = os.path.dirname(path)
        if os.path.isfile(path): # 文件
            extension = os.path.splitext(os.path.basename(path))[1]
            newPath = os.path.join(dirname, name + extension)
        else: # 目录
            newPath = os.path.join(dirname, name)
        try:
            os.rename(path, newPath)
            LOG.trace(f'The file or directory has been successfully renamed to {name} at {newPath}')
            return newPath
        except FileNotFoundError:
            LOG.warning(QCoreApplication.translate("ProjectDock", "文件或目录 {} 不存在", "Log_msg").format(path))
        except PermissionError:
            LOG.warning(QCoreApplication.translate("ProjectDock", "没有权限重命名文件或目录：{}", "Log_msg").format(path))
        except Exception as e:
            LOG.error(QCoreApplication.translate("ProjectDock", "发生错误：{}", "Log_msg").format(e))
    else:
        LOG.trace(f"{path} does not exist")