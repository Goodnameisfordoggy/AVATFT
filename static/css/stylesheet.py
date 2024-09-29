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
print(__PRIMARY_100, __PRIMARY_1000)

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
print(__SECONDARY_100, __SECONDARY_1000)

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
print(__NEUTRAL_100, __NEUTRAL_1000)


__TEXT = '#0ed02b'

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

QMainWindow::separator {{
    width: 10px;
    height: 4px;
    background-color: {__NEUTRAL_100};
}}
QMainWindow::separator:hover,
QMainWindow::separator:pressed {{
    background-color: {__SECONDARY_100};
}}

QDockWidget {{
    background-color: {__NEUTRAL_200};
    
}}
QDockWidget::title {{
    background-color: {__SECONDARY_100};
    border: 2px solid {__SECONDARY_300};
    border-radius: 12px;
    padding: 5px;
    spacing: 4px;
}}
QDockWidget::close-button:hover,
QDockWidget::float-button:hover {{
    background-color: {__SECONDARY_200};
    border-radius: 2px
}}

QPushButton {{
    background-color: {__NEUTRAL_500};  /* 按钮的背景颜色 */
    color: {__NEUTRAL_700};                               /* 按钮的文本颜色 */
    border: none;  /* 按钮的边框样式 */
    border-radius: 10px;                        /* 按钮的圆角半径 */
    padding: 5px 10px;                          /* 内边距 */
    font-size: 14px;                            /* 字体大小 */
    font-weight: bold;                          /* 字体加粗 */
}}
QPushButton:hover {{
    background-color: {__NEUTRAL_300}; /* 悬停时的背景颜色 */
    border: 2px solid {__NEUTRAL_500};  /* 悬停时的边框颜色 */
}}
QPushButton:pressed {{
    background-color: {__TEXT};  /* 按下时的背景颜色 */
    border: 2px solid {__NEUTRAL_500};   /* 按下时的边框颜色 */
}}
QPushButton:disabled {{
    background-color: {__NEUTRAL_500}; /* 禁用时的背景颜色 */
    color: {__NEUTRAL_700};            /* 禁用时的文本颜色 */
    border: none; /* 禁用时的边框颜色 */
}}

QLineEdit {{
    background-color: {__SECONDARY_100}; /* 背景颜色 */
    color: {__PRIMARY_700};               /* 文本颜色 */
    border: 2px solid {__SECONDARY_300}; /* 边框样式 */
    border-radius: 5px;                         /* 圆角半径 */
    padding: 5px;                               /* 内边距 */
    font-size: 12px;                            /* 字体大小 */
}}
QLineEdit:hover {{
    border: 2px solid {__SECONDARY_300};  /* 鼠标悬停时的边框颜色 */
}}
QLineEdit:focus {{
    border: 2px solid {__SECONDARY_300};  /* 焦点时的边框颜色 */
    background-color: {__PRIMARY_400}; /* 焦点时的背景颜色 */
}}
QLineEdit:disabled {{
    background-color: {__SECONDARY_100}; /* 禁用状态下的背景颜色 */
    color: {__PRIMARY_700};            /* 禁用状态下的文本颜色 */
    border: 2px solid {__SECONDARY_300}; /* 禁用状态下的边框颜色 */
}}

"""