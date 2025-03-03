import tkinter as tk
class WinGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_tabs_menu = self.__tk_tabs_menu(self)
        self.tk_text_koujue = self.__tk_text_koujue(self.tk_tabs_menu_4)
        self.tk_text_ext_rule = self.__tk_text_ext_rule(self.tk_tabs_menu_3)
        self.tk_text_common_rule = self.__tk_text_common_rule(self.tk_tabs_menu_2)
        self.tk_label_bihua_name_image = self.__tk_label_bihua_name_image(self.tk_tabs_menu_1)
        self.tk_text_title = self.__tk_text_title(self.tk_tabs_menu_0)
        self.tk_input_search_chinese = self.__tk_input_search_chinese(self.tk_tabs_menu_0)
        self.tk_button_search_btn = self.__tk_button_search_btn(self.tk_tabs_menu_0)
        self.tk_text_bihua_num = self.__tk_text_bihua_num(self.tk_tabs_menu_0)
        self.tk_text_pinyin = self.__tk_text_pinyin(self.tk_tabs_menu_0)
        self.tk_label_bishun_img = self.__tk_label_bishun_img(self.tk_tabs_menu_0)
        self.tk_button_pre_img = self.__tk_button_pre_img(self.tk_tabs_menu_0)
        self.tk_button_next_img = self.__tk_button_next_img(self.tk_tabs_menu_0)
        self.bihua_num = 0
        self.current_tile = -1

    def __win(self):
        self.title("汉字笔画工具")
        # 设置窗口大小、居中
        width = 500
        height = 400
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_tabs_menu(self, parent):
        frame = Notebook(parent)
        self.tk_tabs_menu_0 = self.__tk_frame_menu_0(frame)
        frame.add(self.tk_tabs_menu_0, text="笔画")
        self.tk_tabs_menu_1 = self.__tk_frame_menu_1(frame)
        frame.add(self.tk_tabs_menu_1, text="笔画名称表")
        self.tk_tabs_menu_2 = self.__tk_frame_menu_2(frame)
        frame.add(self.tk_tabs_menu_2, text="笔顺一般规则")
        self.tk_tabs_menu_3 = self.__tk_frame_menu_3(frame)
        frame.add(self.tk_tabs_menu_3, text="笔顺补充规则")
        self.tk_tabs_menu_4 = self.__tk_frame_menu_4(frame)
        frame.add(self.tk_tabs_menu_4, text="笔顺口诀")
        frame.place(x=0, y=0, width=500, height=400)
        return frame

    def __tk_frame_menu_0(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=500, height=400)
        return frame

    def __tk_frame_menu_1(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=500, height=400)
        return frame

    def __tk_frame_menu_2(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=500, height=400)
        return frame

    def __tk_frame_menu_3(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=500, height=400)
        return frame

    def __tk_frame_menu_4(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=500, height=400)
        return frame

    def __tk_text_koujue(self, parent):
        """
        笔顺口诀
        """
        text = tk.Text(parent, spacing2=25, bd=0, wrap="word", font=("微软雅黑", 14))
        text.place(x=0, y=0, width=500, height=400)
        text.insert(tk.END, "从上到下为主，从左到右为辅。\r\n上下左右俱全，根据层次分组；\r\n横竖交叉先横，撇捺交叉先撇；\r\n中间突出先中，右上有点后补；\r\n上包下时先外，下包上时先内；\r\n"
                            "三框首横末折，大囗最后封底；\r\n分歧遵照《规范》，做到流畅美观。")
        text.config(state='disabled')
        return text

    def __tk_text_ext_rule(self, parent):
        text = tk.Text(parent, spacing2=25, bd=0, wrap="word", font=("微软雅黑", 14))
        text.place(x=0, y=0, width=500, height=400)
        text.insert(tk.END,
                    "1.点在上部或左上，先写点：衣 立 为\r\n2.点在右上或在字里，后写点：发 瓦 我\r\n3.上右和上左包围结构的字，先外后里：厅 座 屋\r\n4.左下包围结构的字，先里后外：远 "
                    "建 廷\r\n5.左下右包围结构的字，先里后外：凶 画\r\n6.左上右包围结构的字，先里后外：同 用 风\r\n7.上左下包围结构的字，先上后里在左下：医 巨 匠 区")
        text.config(state='disabled')
        return text

    def __tk_text_common_rule(self, parent):
        text = tk.Text(parent, spacing2=25, bd=0, wrap="word", font=("微软雅黑", 14))
        text.place(x=0, y=0, width=500, height=400)
        text.insert(tk.END,
                    "1.先撇后捺 ： 人 八 入\r\n2.先横后竖：十 王 干\r\n3.从上到下：三 竟 音\r\n4.从左到右：理 利 礼 明 湖\r\n5.先外后里： 问 同 "
                    "司\r\n6.先外后里在封口：国 圆 园 圈\r\n7.先中间后两边：小 水\r\n")
        text.config(state='disabled')
        return text

    def __tk_label_bihua_name_image(self, parent):
        global img  # 使用全局变量来保持对图片对象的引用
        try:
            # 打开图片文件
            img = Image.open("bihua.png")
            # 获取Label的宽度和高度
            label_width = 500
            label_height = 400

            # 计算图片的原始宽高比
            original_ratio = img.size[0] / img.size[1]

            # 根据Label的尺寸和图片的宽高比计算新的图片尺寸
            if original_ratio >= 1:  # 宽度大于高度
                new_width = label_width
                new_height = int(new_width / original_ratio)
            else:  # 高度大于宽度
                new_height = label_height
                new_width = int(new_height * original_ratio)

            # 调整图片尺寸以适应Label的尺寸，同时保持宽高比
            img = img.resize((new_width, new_height - 35), )

            # 将PIL图片对象转换为Tkinter的PhotoImage对象
            img = ImageTk.PhotoImage(img)

            # 创建Label，并设置图片和位置
            label = Label(parent, image=img, anchor="center")
            label.place(x=(label_width - new_width) // 2, y=(label_height - new_height) // 2, width=new_width,
                        height=new_height)

            return label
        except IOError:
            logging.error("图片文件bihua.png未找到或无法打开。")

    def __tk_text_title(self, parent):
        ipt = Entry(parent, justify="center", font=("微软雅黑", 18), foreground="red")
        ipt.place(x=175, y=12, width=150, height=53)
        ipt.insert(tk.END, "汉字笔画工具")
        ipt.config(state='disabled')
        return ipt

    def __tk_input_search_chinese(self, parent):
        ipt = Entry(parent, justify="center", font=("微软雅黑", 24))
        ipt.place(x=20, y=116, width=59, height=58)
        return ipt

    def __tk_button_search_btn(self, parent):
        btn = Button(parent, text="搜索", takefocus=False, command=self.tk_button_search_click)
        btn.place(x=91, y=117, width=66, height=57)
        return btn

    def tk_button_search_click(self):
        # 清除数据
        self.bihua_num = 0
        self.current_tile = -1
        self.tk_text_bihua_num = self.__tk_text_bihua_num(self.tk_tabs_menu_0)
        self.tk_text_pinyin = self.__tk_text_pinyin(self.tk_tabs_menu_0)

        chinese = self.tk_input_search_chinese.get()
        if not chinese:
            messagebox.showerror("提示", message="搜索汉字不能为空")
            return
        elif len(chinese) > 1:
            messagebox.showerror("提示", message="搜索汉字不能超过1个")
            return

        assets = './assets'
        if not os.path.exists(assets):
            os.mkdir(assets)

        chinese_dir = os.path.join(assets, chinese)
        if not os.path.exists(chinese_dir):
            # 创建目录
            os.mkdir(chinese_dir)
            # 假设chinese是单个汉字字符，chinese_ord是其Unicode编码
            chinese_ord = ord(chinese)

            # 构造汉字笔顺动画图片和笔顺规范图片的URL
            hanzi_url = f'https://bishun.net/hanzi/{chinese_ord}'
            donghua_url = f'https://bishun.net/assets/bishun/donghua/bishundonghua-{chinese_ord}.gif'
            fenbu_url = f'https://bishun.net/assets/bishun/fenbu/bishun-{chinese_ord}.png'

            try:
                # 请求汉字信息页面
                response = requests.get(hanzi_url)
                if response.status_code == 200:
                    # 解析网页内容
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # 这里需要根据网页结构来定位笔画数和读音的元素
                    # 例如，如果它们位于具有特定class的元素内，可以使用soup.find()或soup.select()
                    # 以下代码仅为示例，需要根据实际网页结构进行调整
                    bi_shu = soup.select('.bishun-hanzi-info-right')[1].text
                    du_yin = soup.select('.bishun-hanzi-info-right')[2].text
                    print(f"笔画数：{bi_shu}，读音：{du_yin}")
                    with open(os.path.join(chinese_dir, f'{chinese}.txt'), 'w', encoding='utf-8') as f:
                        f.write(f"{bi_shu}\n{du_yin}")

                    # 请求并下载笔顺动画图片
                    donghua_response = requests.get(donghua_url)
                    if donghua_response.status_code == 200:
                        with open(os.path.join(chinese_dir, f'{chinese}.gif'), 'wb') as f:
                            f.write(donghua_response.content)

                    # 请求并下载笔顺规范图片
                    fenbu_response = requests.get(fenbu_url)
                    if fenbu_response.status_code == 200:
                        with open(os.path.join(chinese_dir, f'{chinese}.png'), 'wb') as f:
                            f.write(fenbu_response.content)

            except requests.exceptions.RequestException as e:
                logging.error(f"请求失败：{e}")

        # 读取汉字信息文件
        with open(os.path.join(chinese_dir, f'{chinese}.txt'), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            bi_shu = lines[0].strip()
            self.tk_text_bihua_num.insert(tk.END, f'笔画: {bi_shu}')
            self.tk_text_bihua_num.config(state='disabled')

            du_yin = lines[1].strip()
            self.tk_text_pinyin.insert(tk.END, f'读音: {du_yin}')
            self.tk_text_pinyin.config(state='disabled')

            self.bihua_num = int(bi_shu)

        # 显示完整字图片gif self.tk_label_bishun_img
        global img1  # 使用全局变量来保持对图片对象的引用
        # 打开图片文件
        img1 = Image.open(os.path.join(chinese_dir, f'{chinese}.gif'))
        # 获取Label的宽度和高度
        label_width = 137
        label_height = 138

        # 计算图片的原始宽高比
        original_ratio = img1.size[0] / img1.size[1]

        # 根据Label的尺寸和图片的宽高比计算新的图片尺寸
        if original_ratio >= 1:  # 宽度大于高度
            new_width = label_width
            new_height = int(new_width / original_ratio)
        else:  # 高度大于宽度
            new_height = label_height
            new_width = int(new_height * original_ratio)

        # 调整图片尺寸以适应Label的尺寸，同时保持宽高比
        img1 = img1.resize((new_width - 15, new_height - 15), )

        # 将PIL图片对象转换为Tkinter的PhotoImage对象
        img1 = ImageTk.PhotoImage(img1)
        self.tk_label_bishun_img.config(image=img1)

        # 提前加载笔顺规范
        global tiles
        tiles = self.load_and_split_image(os.path.join(chinese_dir, f'{chinese}.png'), self.bihua_num)

    def __tk_text_bihua_num(self, parent):
        ipt = Entry(parent, justify="left", font=("微软雅黑", 16))
        ipt.place(x=169, y=115, width=91, height=60)
        return ipt

    def __tk_text_pinyin(self, parent):
        ipt = Entry(parent, justify="left", font=("微软雅黑", 14))
        ipt.place(x=272, y=116, width=220, height=58)
        return ipt

    def __tk_label_bishun_img(self, parent):
        label = Label(parent, text="", anchor="center", )
        label.place(x=180, y=215, width=137, height=138)
        return label

    def __tk_button_pre_img(self, parent):
        btn = Button(parent, text="上一笔", takefocus=False, command=lambda: self.__pre_img_click())
        btn.place(x=80, y=257, width=77, height=56)
        return btn

    def __tk_button_next_img(self, parent):
        btn = Button(parent, text="下一笔", takefocus=False, command=lambda: self.__next_img_click())
        btn.place(x=337, y=254, width=82, height=59)
        return btn

    def __pre_img_click(self):
        if 0 < self.current_tile < self.bihua_num:
            self.current_tile -= 1
        else:
            self.current_tile = 0
        self.tk_label_bishun_img.config(image=tiles[self.current_tile])

    def __next_img_click(self):
        if self.current_tile < 0:
            self.current_tile = 0
        elif self.current_tile == self.bihua_num - 1:
            self.current_tile = self.bihua_num - 1
        else:
            self.current_tile += 1
        self.tk_label_bishun_img.config(image=tiles[self.current_tile])

    # 加载图片并分割成多个部分
    def load_and_split_image(self, image_path, bi_shu):
        img = Image.open(image_path)
        width, height = img.size
        const_per_row = 5  # 每一行最多5笔
        total_row = math.ceil(bi_shu / const_per_row)  # 向上取整,不能四舍五入
        tile_width, tile_height = (width // const_per_row, height // total_row)
        tiles = []
        for y in range(0, height, tile_height):
            for x in range(0, width, tile_width):
                tile = img.crop((x, y, x + tile_width, y + tile_height))
                tile = tile.resize((tile_width - 35, tile_height - 35), )
                tiles.append(ImageTk.PhotoImage(tile))
        return tiles

