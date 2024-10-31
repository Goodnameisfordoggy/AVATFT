import os
import shutil
from PySide6.QtCore import Qt, QCoreApplication

from . import LOG
from src import TEMPLATE_DIR

def new_module_file(path: str) -> bool:
    """ 
    ���� module �������ļ� 
    
    :param path: Ŀ���ļ�·��
    """
    if not os.path.exists(path):
        if paste_file(os.path.join(TEMPLATE_DIR, 'module_template.yaml'), path, 'COPY'): # ֱ��ʹ��ģ���ļ���ʼ��
            LOG.success(QCoreApplication.translate("ProjectDock", "���������Ѿ�ʹ��ģ���ļ���ʼ��", "Log_msg"))
            return True
        # config_data = {}
        # # ������д�� YAML �ļ�
        # with open(path, 'w') as f:
        #     yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    else:
        LOG.warning(QCoreApplication.translate("ProjectDock", "Ŀ��λ���д���ͬ���ļ����½�������ȡ��", "Log_msg"))

def new_package_file(path: str) -> bool:
    """ 
    ���� package Ŀ¼
    
    :param path: Ŀ��Ŀ¼·��
    """
    if path:
        try:
            os.mkdir(path)
            LOG.success(QCoreApplication.translate("ProjectDock", "���Լ� {} �����ɹ���", "Log_msg").format(path))
            return True
        except FileExistsError:
            LOG.warning(QCoreApplication.translate("ProjectDock", "Ŀ¼ {} �Ѵ���", "Log_msg").format(path))

def paste_file(source: str, target: str, pre_event: str = '') -> bool:
    """ 
    ���л��ƺ�ճ���ļ� 
    
    :param source: ԭ�ļ�·��
    :param target: Ŀ��λ·��
    :param pre_event: CUT | COPY
    """
    if source:
        if os.path.exists(target): # Ŀ��λ�ô����ļ�
            LOG.trace('A file with the same name exists at the destination location, pasting has been canceled')
            return
        if os.path.splitext(os.path.basename(source))[1] != os.path.splitext(os.path.basename(target))[1]:
            LOG.warning(QCoreApplication.translate("ProjectDock", "��ע�⣬Դ�ļ��ĺ�׺��Ŀ���ļ���ͬ", "Log_msg"))
        if not pre_event:
            LOG.trace('Param pre_event should be set to CUT or COPY')
        # ����ճ��
        if pre_event == 'CUT': 
            shutil.move(source, target) # �ƶ��ļ���Ŀ¼
            return True
        # ����ճ��
        elif pre_event == 'COPY': 
            # �����ļ���Ŀ¼
            if os.path.isfile(source):
                shutil.copy(source, target)
                LOG.trace(f'File copy successfully at {target}')
                return True
            elif os.path.isdir(source):
                shutil.copytree(source, target)
                LOG.trace(f'Directory copy successfully at {target}')
                return True
            else:
                LOG.error(QCoreApplication.translate("ProjectDock", "{} �����ļ���Ŀ¼", "Log_msg").format(source))

def delete_file(path: str) -> bool:
    """" 
    ɾ���ļ� 
    
    :param path: Ŀ���ļ�·��
    """
    if os.path.exists(path):  # ���·���Ƿ����
        if os.path.isfile(path):
            try:
                os.remove(path)
                LOG.trace(f"File at '{path}' delete successfully")
                return True
            except PermissionError:
                LOG.warning(QCoreApplication.translate("ProjectDock", "û��Ȩ��ɾ���ļ�: {}", "Log_msg").format(path))
            except Exception as e:
                LOG.error(QCoreApplication.translate("ProjectDock", "��������{}", "Log_msg").format(e))
        elif os.path.isdir(path): # �����Ŀ¼ֱ��ɾ�����������Ƿ�Ϊ��
            try:
                shutil.rmtree(path)
                LOG.trace(f"Directory at {path} delete successfully")
                return True
            except PermissionError:
                LOG.warning(QCoreApplication.translate("ProjectDock", "û��Ȩ��ɾ��Ŀ¼: {}", "Log_msg").format(path))
            except Exception as e:
                LOG.error(QCoreApplication.translate("ProjectDock", "��������{}", "Log_msg").format(e))
        else:
            LOG.warning(QCoreApplication.translate("ProjectDock", "�ļ� {} ������", "Log_msg").format(path))

def rename_file(path: str, name: str = '') -> str:
    """ 
    �������ļ���Ŀ¼
    
    :param path: Ŀ���ļ�·��
    :param name: Ҫ���ĵ�����
    :return: ���������Ƶ��ļ�����·��
    """
    if os.path.exists(path):  # ���·���Ƿ����
        dirname = os.path.dirname(path)
        if os.path.isfile(path): # �ļ�
            extension = os.path.splitext(os.path.basename(path))[1]
            newPath = os.path.join(dirname, name + extension)
        else: # Ŀ¼
            newPath = os.path.join(dirname, name)
        try:
            os.rename(path, newPath)
            LOG.trace(f'The file or directory has been successfully renamed to {name} at {newPath}')
            return newPath
        except FileNotFoundError:
            LOG.warning(QCoreApplication.translate("ProjectDock", "�ļ���Ŀ¼ {} ������", "Log_msg").format(path))
        except PermissionError:
            LOG.warning(QCoreApplication.translate("ProjectDock", "û��Ȩ���������ļ���Ŀ¼��{}", "Log_msg").format(path))
        except Exception as e:
            LOG.error(QCoreApplication.translate("ProjectDock", "��������{}", "Log_msg").format(e))
    else:
        LOG.trace(f"{path} does not exist")