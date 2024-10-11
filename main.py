import cv2
import numpy as np
import pyautogui
import time
import random
from PIL import ImageGrab
import os

# ------ 填写这部分 ---------
# 提供 实时截图 A、B、C 的大概坐标(左上角 x, 左上角y, 截取的宽 w, 截取的高 h)
# 尽量和 screenshot.py 截取的模板坐标一致，可以提高识别成功率和运行效率
region_a = (50, 115, 277, 171)  # 假设 实时截图 A 的区域
region_b = (50, 115, 277, 171)  # 假设 实时截图 B 的区域
region_c = (50, 115, 250, 171)  # 假设 实时截图 C 的区域
# ---------------

# 获取当前脚本所在目录作为 root_path
root_path = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

# 模板图片路径, 请根据实际情况修改
image_a_path = os.path.join(root_path, 'img',
                            '1_red_envelope_popup.png')  # 红包提示开始弹窗
image_b_path = os.path.join(root_path, 'img',
                            '2_click_red_envelope.png')  # 红包连续点击弹窗
image_c_path = os.path.join(root_path, 'img',
                            '3_red_envelope_result.png')  # 抢红包结果弹窗


# 模拟点击函数，点击可点击区域的随机位置
def click_randomly_in_region(region):
    x, y, w, h = region
    rand_x = random.randint(x, x + w)
    rand_y = random.randint(y, y + h)

    # 模拟人手点击，点击前后的时间间隔随机
    pyautogui.moveTo(rand_x, rand_y, duration=random.uniform(0.2, 0.5))
    pyautogui.click()
    print("👉 点击区域: ({}, {})".format(rand_x, rand_y))


# 匹配图片模板的函数
def match_template(screen, template_image_path, threshold=0.8):
    print("☢ 匹配模板图片 - {}".format(template_image_path))

    template = cv2.imread(template_image_path, 0)  # 读取模板图片
    screen_gray = cv2.cvtColor(np.array(screen),
                               cv2.COLOR_BGR2GRAY)  # 屏幕截图转为灰度图像

    print(f"-- 模板尺寸: {template.shape if template is not None else '未加载'}")
    print(f"-- 截图尺寸: {screen_gray.shape}")

    # 模板匹配
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"-- 匹配度: {max_val}")
    if max_val >= threshold:
        template_w, template_h = template.shape[::-1]
        return (max_loc[0], max_loc[1], template_w, template_h)  # 返回匹配的区域
    return None


# 主要逻辑循环
def red_envelope_bot():
    print("启动红包抢夺脚本...")

    screenshot_num = 0

    while True:
        # 获取指定区域的屏幕截图
        screen_a = ImageGrab.grab(bbox=(region_a[0], region_a[1],
                                        region_a[0] + region_a[2],
                                        region_a[1] + region_a[3]))

        if DEBUG:
            # 输出截图到本地文件
            screenshot_num += 1
            screen_a.save(f'{root_path}/tmp/screen_a_{screenshot_num}.png')

        print("▶ 获取 开始抢红包 A 弹窗 屏幕截图...")
        # 检测是否出现图片A（红包可抢提示）
        match_result_a = match_template(screen_a, image_a_path)
        if match_result_a:
            print("🎯 检测到红包弹窗 A，开始抢红包...")
            click_randomly_in_region(match_result_a)  # 点击红包
            print("🎉 点击红包弹窗 A 成功，等待开始连续点击红包 B...")

            # 循环检测图片B，进行连续点击
            while True:
                time.sleep(random.uniform(0.5, 1.5))  # 模拟人手点击间隔
                print("▶ 获取 需要连续点击红包 B 弹窗 屏幕截图...")
                screen_b = ImageGrab.grab(bbox=(region_b[0], region_b[1],
                                                region_b[0] + region_b[2],
                                                region_b[1] + region_b[3]))
                if DEBUG:
                    # 输出截图到本地文件
                    screenshot_num += 1
                    screen_b.save(
                        f'{root_path}/tmp/screen_b_{screenshot_num}.png')

                match_result_b = match_template(screen_b, image_b_path)
                if match_result_b:
                    print("🎯 检测到点击红包区域 B，继续点击...")
                    click_randomly_in_region(match_result_b)  # 连续点击直到成功
                    print("🎉 点击红包区域 B 成功，继续等待下一次点击 或者 出抢红包结果...")
                else:
                    print("▶ 获取 抢红包结果 C 弹窗 屏幕截图...")
                    # 如果检测不到图片B，说明红包已抢完，开始检查是否有图片C
                    screen_c = ImageGrab.grab(bbox=(region_c[0], region_c[1],
                                                    region_c[0] + region_c[2],
                                                    region_c[1] + region_c[3]))
                    if DEBUG:
                        # 输出截图到本地文件
                        screenshot_num += 1
                        screen_c.save(
                            f'{root_path}/tmp/screen_c_{screenshot_num}.png')

                    match_result_c = match_template(screen_c, image_c_path)
                    if match_result_c:
                        print("🎯 检测到抢红包结果 C，关闭弹窗...")
                        click_randomly_in_region(match_result_c)  # 点击关闭结果弹窗
                        print("🎉 关闭抢红包结果 C 成功，等待下一次红包...")
                        break

        time.sleep(2)


# 启动脚本
if __name__ == '__main__':
    # 清理 tmp 文件夹
    if DEBUG:
        if os.path.exists(f'{root_path}/tmp'):
            for file in os.listdir(f'{root_path}/tmp'):
                os.remove(f'{root_path}/tmp/{file}')
        else:
            os.mkdir(f'{root_path}/tmp')

    # 启动红包抢夺脚本
    red_envelope_bot()
