import colorsys

__PRIMARY_HUE = ('#ffffff', '#000000') # 黑色区间
__SECONDARY_HUE = ('#e5bafc', '#490071') # 紫色区间
__NEUTRAL_HUE = ('#bdcce6', '#002971') # 蓝色区间

# Hex 转 RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# RGB 转 Hex
def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

# 插值计算 RGB 色阶
def interpolate_color(color1, color2, factor: float):
    return tuple(round(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

# 生成色阶
def generate_color_scale(hex_start, hex_end, steps):
    start_rgb = hex_to_rgb(hex_start)
    end_rgb = hex_to_rgb(hex_end)
    color_scale = [f'rgb{interpolate_color(start_rgb, end_rgb, i / (steps - 1))}' for i in range(steps)]
    return color_scale

primary_scale = generate_color_scale(*__PRIMARY_HUE, 10)
__PRIMARY_100 = primary_scale[0]
__PRIMARY_200 = primary_scale[1]
__PRIMARY_300 = primary_scale[2]
__PRIMARY_400 = primary_scale[3]
__PRIMARY_500 = primary_scale[4]
__PRIMARY_600 = primary_scale[5]
__PRIMARY_700 = primary_scale[6]
__PRIMARY_800 = primary_scale[7]
__PRIMARY_900 = primary_scale[8]
__PRIMARY_1000 = primary_scale[9]
# print(__PRIMARY_100, __PRIMARY_1000)

secondary_scale = generate_color_scale(*__SECONDARY_HUE, 10)
__SECONDARY_100 = secondary_scale[0]
__SECONDARY_200 = secondary_scale[1]
__SECONDARY_300 = secondary_scale[2]
__SECONDARY_400 = secondary_scale[3]
__SECONDARY_500 = secondary_scale[4]
__SECONDARY_600 = secondary_scale[5]
__SECONDARY_700 = secondary_scale[6]
__SECONDARY_800 = secondary_scale[7]
__SECONDARY_900 = secondary_scale[8]
__SECONDARY_1000 = secondary_scale[9]
# print(__SECONDARY_100, __SECONDARY_1000)

neutral_scale = generate_color_scale(*__NEUTRAL_HUE, 10)
__NEUTRAL_100 = neutral_scale[0]
__NEUTRAL_200 = neutral_scale[1]
__NEUTRAL_300 = neutral_scale[2]
__NEUTRAL_400 = neutral_scale[3]
__NEUTRAL_500 = neutral_scale[4]
__NEUTRAL_600 = neutral_scale[5]
__NEUTRAL_700 = neutral_scale[6]
__NEUTRAL_800 = neutral_scale[7]
__NEUTRAL_900 = neutral_scale[8]
__NEUTRAL_1000 = neutral_scale[9]
# print(__NEUTRAL_100, __NEUTRAL_1000)


__TEST = '#0ed02b'

"""
QWidget {{
    color: {__PRIMARY_800};
    border: 2px solid {__NEUTRAL_500};
    border-radius: 10px;   
}}
QWidget::selection {{
    color: {__SECONDARY_600};
}}
QWidget:disabled {{
    color: {__SECONDARY_800};
}}
QWidget:disabled::selection {{
    background-color: {__NEUTRAL_100};
    color: {__PRIMARY_500};
}}
"""

STYLE_SHEET =  f"""
* {{
    padding: 0px;
    margin: 0px;
}}
QMainWindow{{
    background-color: {__PRIMARY_200};
}}
QMainWindow::separator {{
    width: 1px;
    height: 1px;
    background-color: none;
}}
QMainWindow::separator:hover,
QMainWindow::separator:pressed {{
    background-color: none;
}}

QMenu {{
    background-color: {__PRIMARY_300};  /* 菜单背景色 */
    border: 2px solid {__PRIMARY_500};  /* 边框颜色 */
    padding: 0px;               /* 内边距 */
    font-size: 12px;            /* 字体大小 */
    border-radius: 2px;
}}
QMenu::item {{
    background-color: {__PRIMARY_300}; 
    padding: 2px;             /* 项目的内边距 */
    color: {__PRIMARY_800};                /* 字体颜色 */
    margin: 2px 3px;
}}
QMenu::item:selected {{
    background-color: {__PRIMARY_500}; /* 选中的背景色 */
    font-size: 12px;            /* 字体大小 */
    color: {__PRIMARY_200};            /* 选中时的文本颜色 */
}}
QMenu::separator {{
    height: 2px;
    background: {__PRIMARY_200};
    margin: 1px 0px;
}}

QDockWidget#NEUTRAL {{
    border: none; /* 外边框 */
    background-color: {__NEUTRAL_100}; /* 背景颜色 */
    min-width: 150 px;
    min-height: 200 px;
    color: {__PRIMARY_100};             /* 标题字体颜色 */
    font-size: 14px;            /* 字体大小 */
    font-weight: bold;   
}}
QDockWidget#NEUTRAL::title {{
    border: 3px solid {__NEUTRAL_600};
    border-radius: 12px;
    border-style: ridge;
    background-color: {__NEUTRAL_400};  /* 标题栏背景颜色 */
    padding: 5px;               /* 标题栏内边距 */
    spacing: 4px;

}}
QDockWidget#NEUTRAL::close-button, 
QDockWidget#NEUTRAL::float-button {{
    background-color: {__NEUTRAL_400};  /* 背景颜色 */
    padding: 0px;               /* 内边距 */
    border-radius: none;
}}
QDockWidget#NEUTRAL::close-button:hover,
QDockWidget#NEUTRAL::float-button:hover {{
    background-color: {__NEUTRAL_400};
    border-radius: 2px;
}}

QDockWidget#SECONDARY {{
    border: none; /* 外边框 */
    background-color: {__SECONDARY_100}; /* 背景颜色 */
    min-width: 300 px;
    min-height: 200 px;
}}
QDockWidget#SECONDARY::title {{
    border: 2px solid {__SECONDARY_300};
    border-radius: 12px;
    background-color: {__SECONDARY_100};  /* 标题栏背景颜色 */
    padding: 5px;               /* 标题栏内边距 */
    spacing: 4px;
    font-size: 14px;            /* 字体大小 */
    font-weight: bold;   
    color: {__PRIMARY_100};             /* 字体颜色 */
}}
QDockWidget#SECONDARY::close-button, 
QDockWidget#SECONDARY::float-button {{
    border: none;               /* 无边框 */
    background-color: {__SECONDARY_100};  /* 背景颜色 */
    padding: 0px;               /* 内边距 */
}}
QDockWidget#SECONDARY::close-button:hover,
QDockWidget#SECONDARY::float-button:hover {{
    background-color: {__SECONDARY_100};
    border-radius: 2px
}}

QPushButton {{
    max-width: 300px;
    background-color: {__NEUTRAL_500};  /* 按钮的背景颜色 */
    color: {__NEUTRAL_700};                               /* 按钮的文本颜色 */
    border: 2px solid {__NEUTRAL_300};  /* 按钮的边框样式 */
    border-radius: 10px;                        /* 按钮的圆角半径 */
    padding: 5px 10px;                          /* 内边距 */
    font-size: 14px;                            /* 字体大小 */
    font-weight: bold;                          /* 字体加粗 */
}}
QPushButton:hover {{
    background-color: {__NEUTRAL_300}; /* 悬停时的背景颜色 */
    border: 2px solid {__NEUTRAL_500};  /* 悬停时的边框颜色 */
    color: {__NEUTRAL_500};
}}
QPushButton:pressed {{
    background-color: {__NEUTRAL_100};  /* 按下时的背景颜色 */
    border: 2px solid {__NEUTRAL_500};   /* 按下时的边框颜色 */
    color: {__NEUTRAL_300};
}}
QPushButton:disabled {{
    background-color: {__NEUTRAL_500}; /* 禁用时的背景颜色 */
    color: {__NEUTRAL_700};            /* 禁用时的文本颜色 */
    border: none; /* 禁用时的边框颜色 */
}}

#NEUTRAL QLineEdit {{
    background-color: {__NEUTRAL_100}; /* 背景颜色 */
    color: {__PRIMARY_700};               /* 文本颜色 */
    border: 2px solid {__NEUTRAL_300}; /* 边框样式 */
    border-radius: 5px;                         /* 圆角半径 */
    padding: 5px;                               /* 内边距 */
    font-size: 12px;                            /* 字体大小 */
    margin: 0px;
}}
#NEUTRAL QLineEdit:hover {{
    border: 2px solid {__NEUTRAL_300};  /* 鼠标悬停时的边框颜色 */
}}
#NEUTRAL QLineEdit:focus {{                             
    border: 2px solid {__NEUTRAL_500};  /* 焦点时的边框颜色 */
    background-color: {__NEUTRAL_200}; /* 焦点时的背景颜色 */
}}
#NEUTRAL QLineEdit:disabled {{
    background-color: {__NEUTRAL_100}; /* 禁用状态下的背景颜色 */
    color: {__PRIMARY_700};            /* 禁用状态下的文本颜色 */
    border: 2px solid {__NEUTRAL_300}; /* 禁用状态下的边框颜色 */
}}

#SECONDARY QLineEdit {{
    background-color: {__SECONDARY_100}; /* 背景颜色 */
    color: {__PRIMARY_700};               /* 文本颜色 */
    border: 2px solid {__SECONDARY_300}; /* 边框样式 */
    border-radius: 5px;                         /* 圆角半径 */
    padding: 5px;                               /* 内边距 */
    font-size: 12px;                            /* 字体大小 */
}}
#SECONDARY QLineEdit:hover {{
    border: 2px solid {__SECONDARY_300};  /* 鼠标悬停时的边框颜色 */
}}
#SECONDARY QLineEdit:focus {{                             
    border: 2px solid {__SECONDARY_500};  /* 焦点时的边框颜色 */
    background-color: {__SECONDARY_200}; /* 焦点时的背景颜色 */
}}
#SECONDARY QLineEdit:disabled {{
    background-color: {__SECONDARY_100}; /* 禁用状态下的背景颜色 */
    color: {__PRIMARY_700};            /* 禁用状态下的文本颜色 */
    border: 2px solid {__SECONDARY_300}; /* 禁用状态下的边框颜色 */
}}

#NEUTRAL QTreeWidget {{
    background-color: {__NEUTRAL_200}; /* 背景色 */
    color: {__PRIMARY_700};           /* 文字颜色 */
}}
#NEUTRAL QTreeWidget::item:selected {{
    background-color: {__NEUTRAL_400}; /* 选中项背景色 */
    color: white;              /* 选中项文字颜色 */
}}
#NEUTRAL QTreeWidget::branch {{
    margin: 0px;  /* 设置分支之间的间隔 */
}}
#NEUTRAL QTreeWidget::item {{
    min-height: 24px; /* 设置最小行高 */
}}
#NEUTRAL QTreeWidget::item:selected {{
    background-color: {__NEUTRAL_400}; /* 选中项背景色 */
    color: {__PRIMARY_200};              /* 选中项文字颜色 */
    border: none;
}}

#SECONDARY QTreeWidget {{
    background-color: {__SECONDARY_200}; /* 背景色 */
    color: {__PRIMARY_700};           /* 文字颜色 */
    border: 1px solid {__SECONDARY_500};
    border-radius: 5px;
}}
#SECONDARY QTreeWidget::item:selected {{
    background-color: {__SECONDARY_400}; /* 选中项背景色 */
    color: {__PRIMARY_200};              /* 选中项文字颜色 */
}}
#SECONDARY QTreeWidget::branch {{
    margin: 0px;                         /* 设置分支之间的间隔 */
}}
#SECONDARY QTreeWidget::item {{
    min-height: 26px; /* 设置最小行高 */
    border-left: 1px solid {__SECONDARY_500};
    border-right: 1px solid {__SECONDARY_500};
}}
#SECONDARY QTreeWidget::item:first {{
    border-left: none;
}}

#SECONDARY QTreeWidget QHeaderView{{         
    background-color: {__SECONDARY_200}; /* 标题栏背景 */
    height: 30px;
    border: 0px;
    border-radius: 5px;
    color: {__PRIMARY_100};
}}
#SECONDARY QTreeWidget QHeaderView::section {{
    background-color: {__SECONDARY_300};
    border: 2px solid {__SECONDARY_500};
    font-weight: bold;
    border-radius: 10px;
}}

QTextEdit {{
    background-color: white;
    border: 2px solid {__SECONDARY_300};
    border-radius: 2px;
    border-style: dotted;
}}

#NEUTRAL QComboBox {{
    background-color: {__NEUTRAL_100};    /* 下拉框的背景色 */
    border: 2px solid {__NEUTRAL_300};       /* 边框样式 */
    padding: 5px;                 /* 内边距 */
    border-radius: 5px;           /* 圆角 */
    font-size: 12px;              /* 字体大小 */
    font-weight: bold;
    color: {__NEUTRAL_500};
}}
#NEUTRAL QComboBox:open {{
    border: 1px solid {__NEUTRAL_500}; /* 获取焦点或打开时 */
    color: {__NEUTRAL_200};
}}
#NEUTRAL QComboBox QAbstractItemView {{
    border: 1px solid {__NEUTRAL_500}; /* 设置下拉列表边框颜色*/
    background-color: {__NEUTRAL_100}; /* 设置下拉列表中选中项的背景色 */
    color: {__NEUTRAL_700}; /* 设置下拉列表中选中项的文字颜色*/
}}

#SECONDARY QComboBox {{
    background-color: {__SECONDARY_100};    /* 下拉框的背景色 */
    border: 2px solid {__SECONDARY_300};       /* 边框样式 */
    padding: 5px;                 /* 内边距 */
    border-radius: 5px;           /* 圆角 */
    font-size: 12px;              /* 字体大小 */
    font-weight: bold;
    color: {__SECONDARY_500};
}}
#SECONDARY QComboBox:open {{
    border: 1px solid {__SECONDARY_500}; /* 获取焦点或打开时 */
    color: {__SECONDARY_200};
}}
#SECONDARY QComboBox QAbstractItemView {{
    border: 1px solid {__SECONDARY_500}; /* 设置下拉列表边框颜色*/
    background-color: {__SECONDARY_100}; /* 设置下拉列表中选中项的背景色 */
    color: {__SECONDARY_700}; /* 设置下拉列表中选中项的文字颜色*/
}}

#NEUTRAL QCheckBox {{
    height: 25px;
    font-size: 12px;               /* 字体大小 */
    color: {__PRIMARY_600};                /* 字体颜色 */
    padding: 0px;                  /* 内边距 */
    border: 2px solid {__NEUTRAL_500};      /* 主体边框 */
    border-left: 1px solid {__NEUTRAL_400}; /* 左边框 */
    border-radius: 5px;             /* 边框圆角 */
    background-color: {__NEUTRAL_300};     /* 背景色 */
}}
#NEUTRAL QCheckBox::indicator {{
    width: 12px;                   /* 指示器宽度 */
    height: 12px;                  /* 指示器高度 */
}}
#NEUTRAL QCheckBox::indicator:unchecked {{
    background-color: {__PRIMARY_200};     /* 未选中时背景色 */
    border-top: 2px solid {__NEUTRAL_500};  /* 上边框 */
    border-bottom: 2px solid {__NEUTRAL_500};/* 下边框 */
    border-right: 2px solid {__NEUTRAL_500}; /* 右边框 */
}}
#NEUTRAL QCheckBox::indicator:checked {{
    background-color: {__PRIMARY_800};     /* 选中时背景色 */
    border: 1px solid {__NEUTRAL_500};     /* 选中时边框 */
}}

#SECONDARY QCheckBox {{
    height: 25px;
    font-size: 12px;               /* 字体大小 */
    color: {__PRIMARY_600};                /* 字体颜色 */
    padding: 0px;                  /* 内边距 */
    border: 2px solid {__SECONDARY_500};      /* 主体边框 */
    border-left: 1px solid {__SECONDARY_400}; /* 左边框 */
    border-radius: 5px;             /* 边框圆角 */
    background-color: {__SECONDARY_300};     /* 背景色 */
}}
#SECONDARY QCheckBox::indicator {{
    width: 12px;                   /* 指示器宽度 */
    height: 12px;                  /* 指示器高度 */
}}
#SECONDARY QCheckBox::indicator:unchecked {{
    background-color: {__PRIMARY_200};     /* 未选中时背景色 */
    border-top: 2px solid {__SECONDARY_500};  /* 上边框 */
    border-bottom: 2px solid {__SECONDARY_500};/* 下边框 */
    border-right: 2px solid {__SECONDARY_500}; /* 右边框 */
}}
#SECONDARY QCheckBox::indicator:checked {{
    background-color: {__PRIMARY_800};     /* 选中时背景色 */
    border: 1px solid {__SECONDARY_500};     /* 选中时边框 */
}}
"""