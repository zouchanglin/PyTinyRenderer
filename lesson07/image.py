class MyImage:
    def __init__(self, size, color=(0, 0, 0)):
        self.width, self.height = size  # 定义图像的宽度和高度
        self.data = [[color for _ in range(self.width)] for _ in range(self.height)]  # 初始化图像数据

    def putpixel(self, position, color):
        x, y = position  # 获取像素位置
        if 0 <= x < self.width and 0 <= y < self.height:  # 检查像素位置是否在图像范围内
            self.data[y][x] = color  # 设置像素颜色

    def save(self, filename):
        with open(filename, 'wb') as f:
            # BMP文件头（14字节）
            f.write(b'BM')  # ID字段
            f.write((14 + 40 + self.width * self.height * 3).to_bytes(4, 'little'))  # 文件大小
            f.write((0).to_bytes(2, 'little'))  # 未使用
            f.write((0).to_bytes(2, 'little'))  # 未使用
            f.write((14 + 40).to_bytes(4, 'little'))  # 偏移至像素数据

            # DIB头（40字节）
            f.write((40).to_bytes(4, 'little'))  # 头大小
            f.write((self.width).to_bytes(4, 'little'))  # 图像宽度
            f.write((self.height).to_bytes(4, 'little'))  # 图像高度
            f.write((1).to_bytes(2, 'little'))  # 颜色平面数量
            f.write((24).to_bytes(2, 'little'))  # 每像素位数
            f.write((0).to_bytes(4, 'little'))  # 压缩方法
            f.write((self.width * self.height * 3).to_bytes(4, 'little'))  # 图像大小
            f.write((0).to_bytes(4, 'little'))  # 水平分辨率
            f.write((0).to_bytes(4, 'little'))  # 垂直分辨率
            f.write((0).to_bytes(4, 'little'))  # 色彩板中的颜色数量
            f.write((0).to_bytes(4, 'little'))  # 重要颜色数量

            # 像素数据
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = self.data[y][x]  # 获取像素颜色
                    f.write(b.to_bytes(1, 'little'))  # 蓝色
                    f.write(g.to_bytes(1, 'little'))  # 绿色
                    f.write(r.to_bytes(1, 'little'))  # 红色

                # 填充至4字节
                for _ in range((self.width * 3) % 4):
                    f.write(b'\x00')  # 写入填充字节
