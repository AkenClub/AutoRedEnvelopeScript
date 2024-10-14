from PIL import ImageGrab
import os

# ------ 填写这部分 ---------
# 截取的模板，尽量不要截取太大，建议只截取有固定特征的部分，可以提高识别成功率和运行效率
# 提供图片A、B、C的大概坐标(左上角 x, 左上角y, 截取的宽 w, 截取的高 h)
# 结果弹窗 C，有些时候同样一个按钮因为弹窗内容不同导致宽高不同，可能存在不同的坐标

region_a = (370, 400, 220, 50)  # 假设 模板 图片A的区域
region_b = (390, 410, 170, 90)  # 假设 模板 图片B的区域
region_c = (330, 740, 290, 60)  # 假设 模板 图片C的区域
region_c2 = (330, 740, 290, 60)  # 假设 模板 图片C的区域
region_c3 = (330, 740, 290, 60)  # 假设 模板 图片C的区域
region_c4 = (330, 635, 290, 60)  # 假设 模板 图片C的区域
region_c5 = (360, 635, 270, 60)  # 假设 模板 图片C的区域
region_c6 = (360, 635, 270, 60)  # 假设 模板 图片C的区域
region_c7 = (360, 635, 270, 60)  # 假设 模板 图片C的区域
# ---------------

# 获取当前脚本所在目录作为 root_path
root_path = os.path.dirname(os.path.abspath(__file__))


# 模板图片路径和对应区域坐标的映射
def get_image_regions():
    return {
        # 'image_a': {
        #     'path': os.path.join(root_path, 'img', '1_red_envelope_popup.png'),
        #     'region': region_a
        # },
        # 'image_b': {
        #     'path': os.path.join(root_path, 'img', '2_click_red_envelope.png'),
        #     'region': region_b
        # },
        # 'image_c': {
        #     'path': os.path.join(root_path, 'img',
        #                          '3_red_envelope_result.png'),
        #     'region': region_c
        # },
        # 'image_c2': {
        #     'path': os.path.join(root_path, 'img',
        #                          '3_red_envelope_result_2.png'),
        #     'region': region_c2
        # },
        # 'image_c3': {
        #     'path': os.path.join(root_path, 'img',
        #                          '3_red_envelope_result_3.png'),
        #     'region': region_c3
        # },
        # 'image_c4': {
        #     'path': os.path.join(root_path, 'img',
        #                          '3_red_envelope_result_4.png'),
        #     'region': region_c4
        # },
        # 'image_c5': {
        #     'path': os.path.join(root_path, 'img',
        #                          '3_red_envelope_result_5.png'),
        #     'region': region_c5
        # },
        # 'image_c6': {
        #     'path': os.path.join(root_path, 'img',
        #                          '3_red_envelope_result_6.png'),
        #     'region': region_c6
        # },
        'image_c7': {
            'path': os.path.join(root_path, 'img',
                                 '3_red_envelope_result_7.png'),
            'region': region_c7
        }
    }


image_regions = get_image_regions()


# 主要逻辑循环
def screenshot():
    print("▶ 开始截图 ...")

    # 循环截图和保存
    for value in image_regions.values():
        region = value['region']
        path = value['path']
        screen = ImageGrab.grab(bbox=(region[0], region[1],
                                      region[0] + region[2],
                                      region[1] + region[3]))

        # 输出截图到本地文件
        screen.save(path)
        print(f"✅ 截图成功: {path}")

    print("⏹ 截图结束 ...")


# 启动脚本
if __name__ == '__main__':
    screenshot()
