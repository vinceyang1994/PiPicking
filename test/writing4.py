import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt5.QtCore import QTimer, Qt
import re

class StrokeAnimation(QMainWindow):
    def __init__(self, character, hanzi_data):
        super().__init__()
        self.setWindowTitle(f'汉字 {character} 笔顺动画')
        self.setGeometry(200, 200, 1000, 1000)
        
        self.character = character
        # 解析所有笔画
        self.strokes = [parse_svg_path(stroke) for stroke in hanzi_data['strokes']]
        self.current_stroke = 0
        
        # 设置定时器控制动画
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500)  # 每500毫秒更新一次
        
        self.setStyleSheet("background-color: black;")  # 设置黑色背景
    
    def update_animation(self):
        if self.current_stroke < len(self.strokes):
            self.current_stroke += 1
            self.update()  # 触发重绘
        else:
            self.timer.stop()  # 所有笔画显示完毕，停止动画

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # ==== 核心计算缩放和偏移：坐标系翻转与居中逻辑 ====
        scale = min(self.width(), self.height()) * 0.9  # 使用90%的窗口空间
        offset_x = self.width() / 2
        offset_y = self.height() / 2
        painter.translate(offset_x, offset_y)         # 原点移到窗口中心，让文字始终绘制在窗口中央
        painter.scale(scale / 1024, -scale / 1024)    # Y轴添加负号翻转
        painter.translate(-512, -412)  # 原始数据中心点为(512,512)，平移确保翻转后仍居中（考虑控件本身位置微调）
        
        # 绘制当前及之前的笔画
        for i in range(min(self.current_stroke, len(self.strokes))):
            self.draw_stroke(painter, self.strokes[i], QColor(255, 255, 255))

    def draw_stroke(self, painter, path, color):
        pen = QPen(color, 3)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        painter.drawPath(path)

# SVG 路径解析函数
def parse_svg_path(path_string):
    path = QPainterPath()
    commands = re.findall(r'([MLQCZ])\s*([-\d.,\s]*)', path_string)
    for cmd, args_str in commands:
        args = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', args_str)]
        if cmd == 'M' and len(args) >= 2:
            path.moveTo(args[0], args[1])
        elif cmd == 'L' and len(args) >= 2:
            path.lineTo(args[0], args[1])
        elif cmd == 'Q' and len(args) >= 4:
            path.quadTo(args[0], args[1], args[2], args[3])
        elif cmd == 'C' and len(args) >= 6:
            path.cubicTo(args[0], args[1], args[2], args[3], args[4], args[5])
        elif cmd == 'Z':
            path.closeSubpath()
    return path

# 您提供的“永”字数据
hanzi_data = {
    "character": "永",
    "strokes": [
        "M 440 788 Q 497 731 535 718 Q 553 717 562 732 Q 569 748 564 767 Q 546 815 477 828 Q 438 841 421 834 Q 414 831 418 817 Q 421 804 440 788 Z",
        "M 532 448 Q 532 547 546 570 Q 559 589 546 601 Q 524 620 486 636 Q 462 645 413 615 Q 371 599 306 589 Q 290 588 299 578 Q 309 568 324 562 Q 343 558 370 565 Q 406 575 441 587 Q 460 594 467 584 Q 473 566 475 538 Q 482 271 470 110 Q 469 80 459 67 Q 453 61 369 82 Q 342 95 344 79 Q 411 27 450 -13 Q 463 -32 480 -38 Q 490 -42 499 -32 Q 541 16 540 77 Q 533 207 532 403 L 532 448 Z",
        "M 117 401 Q 104 401 102 392 Q 101 385 117 377 Q 163 352 192 363 Q 309 397 320 395 Q 333 392 323 365 Q 280 256 240 205 Q 200 147 126 86 Q 111 73 122 71 Q 132 70 153 80 Q 220 114 275 172 Q 327 224 394 362 Q 404 384 416 397 Q 431 409 422 419 Q 412 432 374 445 Q 353 455 305 434 Q 215 412 117 401 Z",
        "M 567 407 Q 639 452 745 526 Q 767 542 793 552 Q 817 562 806 582 Q 793 601 765 618 Q 740 634 725 632 Q 712 631 715 616 Q 719 582 641 505 Q 601 465 556 420 C 535 399 542 391 567 407 Z",
        "M 556 420 Q 543 436 532 448 C 512 470 515 427 532 403 Q 737 114 799 116 Q 871 126 933 135 Q 960 138 960 145 Q 961 152 930 165 Q 777 217 733 253 Q 678 296 567 407 L 556 420 Z"
    ]
}

def main():
    app = QApplication(sys.argv)
    window = StrokeAnimation(hanzi_data['character'], hanzi_data)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
