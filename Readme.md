## 简介
本工程是一个汉字阅读应用，旨在帮助幼儿识字和学习汉字书写。应用提供了汉字展示、笔画动画、发音功能和设置菜单，用户可以自定义笔画颜色、字号大小、汉字字体和书写动画次数。


## 起源
我是个程序员，每天在电脑前的时间比较长。家里小朋友4岁了，叫小丕，总是喜欢凑到跟前看我在干什么，但是又看不懂密密麻麻的字，比较担忧他看屏幕时间太长，没有给他用电子屏幕放过动画片。所以我就想给他做一个他能用的软件，还能帮助识字。
名字由来：小丕识字/小丕十字/小丕拾字，这三个名字想了好久，最后确定为`小丕拾字`,比较形象。
一次记十个字，也谐音识字。而且笔画也都简单。

## 工程目录
```
reading_app/
│
├── main.py                   # Entry point for the application
├── config.json               # Configuration file
├── characters.txt            # Character database
│
├── assets/                   # Assets directory
│   ├── fonts/                # Font files
│   └── icons/                # UI icons
│
├── core/                     # Core logic components
│   ├── character_manager.py  # Character data management
│   ├── animation_engine.py   # Stroke animation logic
│   ├── config_manager.py     # Configuration handling
│   └── speech_engine.py      # Text-to-speech functionality
│
└── ui/                       # User interface components
    ├── main_window.py        # Main application window
    ├── settings_dialog.py    # Settings dialog
    ├── about_dialog.py       # About dialog
    └── font_dialog.py        # Font management dialog
```
# TODO
- [ ] 多音字
- [ ] 汉字组词-变换背景-接入AI生成对应的图像
- [ ] 背景场景
- [ ] 标注拼音
- [ ] 测试模式，打乱出现顺序。读音滞后
- [ ] 笔画更像人写的话使用Hanzi Writer这个JS库合适，不过就是另外项目了
- [ ] 背景反色
- [ ] 声音音色可选
- [ ] 静音按钮
- [ ] 自动下一个汉字，包括暂停键
- [ ] 笔画动画停止选项
- [ ] 声音不能快速找到并加载，有些字显示了2s声音还没来
- [ ] 更换显示字体，但是整个的绘画逻辑就需要改变。当前使用SVG作图，要得到对应字体的SVG行不通。
- [ ] bug:竖钩的svg显示拐角处翻转了