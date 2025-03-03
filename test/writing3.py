import json
import os
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches

# 解析SVG路径字符串
def parse_svg_path(path_string):
    # 正则表达式匹配SVG路径中的命令和坐标
    pattern = r'([MLQCZ])[\s,]*([^MLQCZ]*)'
    matches = re.findall(pattern, path_string)
    
    commands = []
    for cmd_type, args_str in matches:
        # 提取数值参数
        args = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', args_str)]
        
        if cmd_type == 'M':  # 移动到
            commands.append(['M', args[0], args[1]])
        elif cmd_type == 'L':  # 线到
            commands.append(['L', args[0], args[1]])
        elif cmd_type == 'Q':  # 二次贝塞尔曲线
            if len(args) >= 4:
                commands.append(['Q', args[2], args[3], args[0], args[1]])
        elif cmd_type == 'C':  # 三次贝塞尔曲线
            if len(args) >= 6:
                commands.append(['C', args[4], args[5], args[0], args[1], args[2], args[3]])
        # Z (闭合路径) 不需要额外处理
    
    return commands

# 加载汉字数据
def load_hanzi_data(character):
    try:
        with open('test\\graphics.txt', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data['character'] == character:
                    print(f"找到汉字 '{character}' 的数据")
                    return data
        print(f"找不到汉字 '{character}' 的数据")
    except Exception as e:
        print(f"加载数据时出错: {e}")
    return None

# 解析笔画数据并准备绘制
def prepare_strokes(hanzi_data):
    if not hanzi_data or 'strokes' not in hanzi_data:
        return []
    
    strokes = []
    # 计算边界值，用于归一化
    # 先解析所有路径以找到最小和最大坐标
    all_commands = []
    for stroke_path in hanzi_data['strokes']:
        commands = parse_svg_path(stroke_path)
        all_commands.extend(commands)
    
    # 提取所有x和y坐标
    x_coords = []
    y_coords = []
    for cmd in all_commands:
        if len(cmd) >= 3:  # 确保命令有坐标
            x_coords.append(cmd[1])
            y_coords.append(cmd[2])
    
    # 计算边界
    if x_coords and y_coords:
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)
    else:
        # 默认边界值，避免除以零错误
        min_x, max_x = 0, 1000
        min_y, max_y = 0, 1000
    
    # 处理每个笔画
    for stroke_path in hanzi_data['strokes']:
        path_data = []
        commands = parse_svg_path(stroke_path)
        
        for cmd in commands:
            if len(cmd) < 3:
                continue
                
            # 归一化坐标 - 不再翻转Y轴
            x = (cmd[1] - min_x) / (max_x - min_x)
            y = (cmd[2] - min_y) / (max_y - min_y)  # 修改：不再翻转Y轴
            
            if cmd[0] == 'M':  # 移动到
                path_data.append((Path.MOVETO, (x, y)))
            elif cmd[0] == 'L':  # 线到
                path_data.append((Path.LINETO, (x, y)))
            elif cmd[0] == 'Q' and len(cmd) >= 5:  # 二次贝塞尔曲线
                # 控制点
                cx = (cmd[3] - min_x) / (max_x - min_x)
                cy = (cmd[4] - min_y) / (max_y - min_y)  # 修改：不再翻转Y轴
                
                path_data.append((Path.CURVE3, (cx, cy)))
                path_data.append((Path.CURVE3, (x, y)))
            elif cmd[0] == 'C' and len(cmd) >= 7:  # 三次贝塞尔曲线
                # 控制点1
                c1x = (cmd[3] - min_x) / (max_x - min_x)
                c1y = (cmd[4] - min_y) / (max_y - min_y)  # 修改：不再翻转Y轴
                # 控制点2
                c2x = (cmd[5] - min_x) / (max_x - min_x)
                c2y = (cmd[6] - min_y) / (max_y - min_y)  # 修改：不再翻转Y轴
                
                path_data.append((Path.CURVE4, (c1x, c1y)))
                path_data.append((Path.CURVE4, (c2x, c2y)))
                path_data.append((Path.CURVE4, (x, y)))
        
        if path_data:
            path_data.append((Path.CLOSEPOLY, (0, 0)))
            strokes.append(path_data)
    
    return strokes

def create_animation(character):
    # 加载汉字数据
    hanzi_data = load_hanzi_data(character)
    if not hanzi_data:
        return None
    
    # 准备笔画数据
    strokes = prepare_strokes(hanzi_data)
    if not strokes:
        print("没有找到可用的笔画数据")
        return None
    
    # 创建图形和轴
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    # ax.set_title(f'汉字 "{character}" 的笔画顺序', fontsize=20)
    
    # 存储所有笔画路径
    path_patches = []
    completed_strokes = []
    
    # 初始化函数
    def init():
        return []
    
    # 动画更新函数
    def update(frame):
        # 清除上一帧的临时笔画
        while path_patches:
            patch = path_patches.pop()
            patch.remove()
        
                    # 绘制已完成的笔画（灰色填充）
        for path_data in completed_strokes:
            path = Path([x[1] for x in path_data], [x[0] for x in path_data])
            patch = patches.PathPatch(path, facecolor='lightgray', edgecolor='gray', linewidth=2, alpha=0.6)
            ax.add_patch(patch)
            path_patches.append(patch)
        
        # 处理当前帧
        stroke_index = frame // 2  # 每个笔画显示两帧
        
        if stroke_index < len(strokes):
            # 是否是完成状态
            if frame % 2 == 1:
                # 将当前笔画添加到已完成列表
                completed_strokes.append(strokes[stroke_index])
            
            # 绘制当前笔画（使用颜色填充）
            path_data = strokes[stroke_index]
            path = Path([x[1] for x in path_data], [x[0] for x in path_data])
            # 使用不同颜色填充当前笔画
            colors = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', '#99FFFF', '#FFB347', '#B39EB5']
            color_index = stroke_index % len(colors)
            patch = patches.PathPatch(path, facecolor=colors[color_index], edgecolor='black', linewidth=3, alpha=0.9)
            ax.add_patch(patch)
            path_patches.append(patch)
        
        return path_patches
    
    # 创建动画
    frames = len(strokes) * 2  # 每个笔画有两帧：绘制和完成
    ani = animation.FuncAnimation(fig, update, frames=frames,
                                 init_func=init, blit=True, interval=500)
    
    return ani

# 主函数
def main():
    character = '永'  # 可以换成任何想要的汉字
    print(f"尝试创建汉字 '{character}' 的动画...")
    
    ani = create_animation(character)
    if ani:
        print("动画创建成功，保存为GIF...")
        # 保存为GIF
        ani.save(f'{character}_strokes.gif', writer='pillow', fps=2)
        print(f"已保存为 {character}_strokes.gif")
        
        # 显示动画
        plt.show()
    else:
        print("创建动画失败")

if __name__ == "__main__":
    main()