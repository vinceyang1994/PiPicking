import pygame
import json
import time
import sys

def load_hanzi_data(character):
    # 从Make Me a Hanzi的数据文件中读取
    with open('test\\graphics.txt', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data['character'] == character:
                return data
    return None

def animate_with_pygame(character):
    hanzi_data = load_hanzi_data(character)
    if not hanzi_data:
        print(f"找不到汉字 '{character}' 的数据")
        return
    
    # 初始化PyGame
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f'汉字 {character} 笔顺动画')
    
    # 设置颜色和画笔
    background_color = (255, 255, 255)
    stroke_color = (0, 0, 0)
    complete_stroke_color = (100, 100, 100)
    
    # 缩放系数
    scale_x = width / (hanzi_data['bounds'][2] - hanzi_data['bounds'][0])
    scale_y = height / (hanzi_data['bounds'][3] - hanzi_data['bounds'][1])
    
    # 动画主循环
    running = True
    current_stroke = 0
    stroke_progress = 0
    stroke_speed = 0.05  # 控制绘制速度
    
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 清屏
        screen.fill(background_color)
        
        # 绘制已完成的笔画
        for i in range(current_stroke):
            points = []
            for cmd in hanzi_data['strokes'][i]:
                x = (cmd[1] - hanzi_data['bounds'][0]) * scale_x
                y = (cmd[2] - hanzi_data['bounds'][1]) * scale_y
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, complete_stroke_color, False, points, 3)
        
        # 绘制当前正在写的笔画
        if current_stroke < len(hanzi_data['strokes']):
            points = []
            stroke = hanzi_data['strokes'][current_stroke]
            
            # 计算到当前进度的点
            progress_index = int(len(stroke) * stroke_progress)
            for i in range(min(progress_index + 1, len(stroke))):
                cmd = stroke[i]
                x = (cmd[1] - hanzi_data['bounds'][0]) * scale_x
                y = (cmd[2] - hanzi_data['bounds'][1]) * scale_y
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, stroke_color, False, points, 3)
            
            # 更新进度
            stroke_progress += stroke_speed
            if stroke_progress >= 1:
                stroke_progress = 0
                current_stroke += 1
                if current_stroke >= len(hanzi_data['strokes']):
                    time.sleep(1)  # 完成所有笔画后暂停
                    current_stroke = 0  # 循环播放
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

# 使用示例
character = '永'
animate_with_pygame(character)