起名字：小丕识字/小丕十字/小丕拾字，这三个名字想了好久。
一次记十个字，也谐音识字。而且笔画也都简单。

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

# 笔画绘制
animation_engine.py代码的主要功能是管理汉字的动画和渲染，特别是笔画的显示。以下是代码中如何绘制笔画的详细解释：

1. **StrokeInfo 类**:
   - 该类用于存储每个笔画的信息，包括笔画的路径 (`path`) 和是否可见的状态 (`visible`)。

2. **AnimationEngine 类**:
   - 该类负责管理汉字的动画和渲染。它包含多个信号，用于在动画状态变化时通知其他部分。

3. **set_character 方法**:
   - 该方法设置当前要动画的汉字，并调用 `prepare_strokes` 方法准备笔画路径。

4. **prepare_strokes 方法**:
   - 该方法为当前汉字准备笔画路径。它创建一个 `QPainterPath` 对象来表示汉字的形状，并根据随机生成的笔画数量（3到8个）将汉字的边界矩形划分为多个“笔画”。
   - 每个“笔画”是通过在汉字的边界矩形内创建小的矩形来模拟的。

5. **start_stroke_animation 方法**:
   - 该方法开始笔画动画序列。它将所有笔画的可见性设置为 `False`，然后启动动画定时器。

6. **animate_next_stroke 方法**:
   - 该方法负责逐个显示笔画。它查找下一个不可见的笔画，将其设置为可见，并发出信号以更新显示。
   - 当所有笔画都可见时，停止动画定时器，并根据目标动画计数决定是否结束动画序列。

7. **render 方法**:
   - 该方法负责渲染当前的动画状态。它使用 `QPainter` 对象绘制汉字和笔画。
   - 首先，设置字体并创建汉字的完整路径。然后，绘制汉字的轮廓。
   - 如果不处于空心模式，则绘制可见的笔画。根据配置，可以为每个笔画使用不同的颜色或统一颜色。

### 总结
代码通过创建汉字的路径和模拟笔画的显示，使用 `QPainter` 对象在窗口中绘制汉字和其笔画。每个笔画的显示是通过控制其可见性和使用定时器逐个显示来实现的。

## 打包成EXE

### 步骤 1: 安装 PyInstaller

如果您还没有安装 `PyInstaller`，可以通过以下命令安装：

```bash
pip install pyinstaller
```

### 步骤 2: 准备项目结构

确保您的项目结构如下：

```
your_project/
│
├── main.py                   # 应用程序的入口点
├── config.json               # 配置文件
├── characters.txt            # 字符数据库
│
├── assets/                   # 资源目录
│   ├── graphics.txt          # 笔画数据文件
│   ├── fonts/                # 字体文件（如果有）
│   └── icons/                # UI 图标（如果有）
│
├── core/                     # 核心逻辑组件
│   ├── character_manager.py  # 字符数据管理
│   ├── animation_engine.py   # 笔画动画逻辑
│   ├── config_manager.py     # 配置处理
│   └── speech_engine.py      # 文本转语音功能
│
└── ui/                       # 用户界面组件
    ├── main_window.py        # 主应用程序窗口
    ├── settings_dialog.py    # 设置对话框
    ├── about_dialog.py       # 关于对话框
    └── font_dialog.py        # 字体管理对话框
```

### 步骤 3: 创建可执行文件

在项目根目录下打开命令行或终端，运行以下命令：

```bash
pyinstaller --onefile --add-data "assets/graphics.txt;assets" main.py
```

- `--onefile` 选项将所有文件打包成一个单独的可执行文件。
- `--add-data` 选项用于将 `assets/graphics.txt` 文件包含在可执行文件中。注意在 Windows 上使用分号 `;` 分隔源和目标路径，在 Linux 或 macOS 上使用冒号 `:`。

### 步骤 4: 查找生成的可执行文件

打包完成后，您将在项目目录下生成一个 `dist` 文件夹，里面包含生成的可执行文件 `main.exe`（或在 Linux/macOS 上为 `main`）。

### 步骤 5: 测试可执行文件

在 `dist` 文件夹中找到生成的可执行文件，双击运行以确保它能够正常工作，并且能够访问 `assets/graphics.txt` 文件。

### 注意事项

- 确保在打包之前，您的代码没有错误，并且可以在开发环境中正常运行。
- 如果您的应用程序依赖于其他资源（如字体、图标等），请确保将它们也包含在打包命令中。
