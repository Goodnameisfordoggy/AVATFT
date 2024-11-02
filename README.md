# AVATFT 

<center>
<figure>
    <img src="static/icon/app.svg" alt="app-icon" width="600">
</figure>
</center>

*Action visual automatic test framework tool*

*行为可视化自动测试工具*

version: 1.2.2

# 注意
- 该项目实现主要功能必须依赖行为关键字，但由于行为关键字改动频率较高暂不纳入版本管理，后继将会把部分稳定的关键字打成资源包来使用。

# 项目结构

- 等级划分：project > package > module > action

workdir主要结构

- action_keywords
- config
- func
- log
- projects
- src
  - utils
- static
  - css
  - icon
  - template
  - translations
- tests
- main.py

projects目录结构
- projects
  - project(自定义名称)
    - business
      - package(自定义名称)
        - module(自定义名称)
          - action1(module文件内部)
          - action2
          - ...
    - config
    - data
    - log
# 命令
生成ts文件模版
```
pyside6-lupdate src\AVATFT.py src\dock\action.py src\dock\edit.py src\dock\log.py src\dock\project.py src\treeWidgetItem.py src\utils\file.py -ts static\translations\en_US.ts
```
将ts文件转为qm文件(二进制)供程序读取
```
lrelease static\translations\en_US.ts
```

# 感谢
- 关键字UI设计与操作逻辑灵感来自 Apple 快捷指令与自动化 https://support.apple.com/zh-cn/guide/shortcuts/welcome/ios
- 关键字分类灵感来自影刀RPA(https://www.yingdao.com/)的使用体验以及VX公号“enter回车键”的部分文章。
- 图标源 https://github.com/Pictogrammers/pictogrammers.com

# Update log
- 1.2.2: 使用MVC结构重新组织源码。
- 1.2.1: 尝试使用MVC结构重新组织源码。
- 1.2.0: 更新了测试用例运行方式
- 1.1.0: 新增展开/收缩树视图子项功能
- 1.0.0: 项目主体以及功能构建完成；
- 0.4.28: 修复了一些问题
- 0.4.27: 国际化（英文）构建完成
- 0.3.27: 国际化构建中
- 0.3.26: 尝试国际化
- 0.3.25: 项目构建中
- 0.3.24: 项目构建中
- 0.3.23: 进行了一些细微调整
- 0.3.22: 项目构建中
- 0.3.21: 主题（色阶渐变）构建完成
- 0.2.21: 主题构建中
- 0.2.20: 主题构建中
- 0.2.19: 项目构建中
- 0.1.19: 项目构建中
- 0.1.18: 项目构建中
- 0.1.17: 项目构建中
- 0.1.16: 项目构建中
- 0.1.15: 项目构建中，基础UI以及UI主要逻辑构建完成。
- 0.0.15: 修复了一些错误
- 0.0.14: 项目构建中
- 0.0.14: 项目构建中
- 0.0.13: 项目构建中
- 0.0.12: update .gitignore
- 0.0.12: 项目构建中
- 0.0.11: 项目构建中
- 0.0.10: 项目构建中
- 0.0.9: 项目构建中
- 0.0.8: 项目构建中
- 0.0.7: 项目构建中
- 0.0.6: 项目构建中
- 0.0.5: 项目构建中
- 0.0.4: 项目构建中
- 0.0.3: 项目构建中
- 0.0.2: 项目构建中
- 0.0.1: 项目构建中


