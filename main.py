import cv2
import numpy as np
import pyautogui
import time
import random
from PIL import ImageGrab
import os
from datetime import datetime

# ------ 填写这部分 ---------
# 提供 实时截图 A、B、C 的大概坐标(左上角 x, 左上角y, 截取的宽 w, 截取的高 h)
# 尽量和 screenshot.py 截取的模板坐标一致，可以提高识别成功率和运行效率
# 结果弹窗 C，有些时候同样一个按钮因为弹窗内容不同导致宽高不同，可能存在不同的坐标

region_a = (370, 400, 220, 50)  # 假设 实时截图 A 的区域
region_b = (390, 410, 170, 80)  # 假设 实时截图 B 的区域
region_c = (330, 740, 290, 60)  # 假设 实时截图 C 的区域
region_c2 = (330, 740, 290, 60)  # 假设 实时截图 C 的区域
region_c3 = (330, 740, 290, 60)  # 假设 模板 图片C的区域
region_c4 = (330, 635, 290, 60)  # 假设 模板 图片C的区域
region_c5 = (360, 635, 270, 60)  # 假设 模板 图片C的区域
region_c6 = (360, 635, 270, 60)  # 假设 模板 图片C的区域

# ---------------

# 获取当前脚本所在目录作为 root_path
root_path = os.path.dirname(os.path.abspath(__file__))

# 谨慎设置 True，容易爆满 tmp 文件夹，建议看懂代码，想调试哪里再自己打开
DEBUG = False

log_num = 1

screenshot_num = 0

success_num = 0

# 模板图片路径, 请根据实际情况修改
image_a_path = os.path.join(root_path, 'img',
                            '1_red_envelope_popup.png')  # 红包提示开始弹窗
image_b_path = os.path.join(root_path, 'img',
                            '2_click_red_envelope.png')  # 红包连续点击弹窗
image_c_path = os.path.join(root_path, 'img',
                            '3_red_envelope_result.png')  # 抢红包结果弹窗
image_c2_path = os.path.join(root_path, 'img',
                             '3_red_envelope_result_2.png')  # 抢红包结果弹窗
image_c3_path = os.path.join(root_path, 'img',
                             '3_red_envelope_result_3.png')  # 抢红包结果弹窗
image_c4_path = os.path.join(root_path, 'img',
                             '3_red_envelope_result_4.png')  # 抢红包结果弹窗
image_c5_path = os.path.join(root_path, 'img',
                             '3_red_envelope_result_5.png')  # 抢红包结果弹窗
image_c6_path = os.path.join(root_path, 'img',
                             '3_red_envelope_result_6.png')  # 抢红包结果弹窗


# 模拟点击函数，点击可点击区域的随机位置
def click_randomly_in_region(region):
    x, y, w, h = region
    rand_x = random.randint(x, x + w)
    rand_y = random.randint(y, y + h)

    # 模拟人手点击，点击前后的时间间隔随机
    # pyautogui.moveTo(rand_x, rand_y, duration=random.uniform(0.2, 0.3))
    pyautogui.moveTo(rand_x, rand_y)
    pyautogui.click()
    # print("👉 点击区域: ({}, {})".format(rand_x, rand_y))


# 匹配图片模板的函数
def match_template(screen,
                   template_image_path,
                   origin_x,
                   origin_y,
                   threshold=0.8):
    # print("☢ 匹配模板图片 - {}".format(template_image_path))

    template = cv2.imread(template_image_path, 0)  # 读取模板图片
    screen_gray = cv2.cvtColor(np.array(screen),
                               cv2.COLOR_BGR2GRAY)  # 屏幕截图转为灰度图像

    # print(f"-- 模板尺寸: {template.shape if template is not None else '未加载'}")
    # print(f"-- 截图尺寸: {screen_gray.shape}")

    # 模板匹配
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # print(f"-- 匹配度: {max_val}")
    if max_val >= threshold:
        template_w, template_h = template.shape[::-1]
        return (max_loc[0] + origin_x, max_loc[1] + origin_y, template_w,
                template_h)  # 返回匹配的区域
    return None


# 限制日志频繁输出
def print_log(content, limit_disable=False):
    if (limit_disable):
        print(content)

    global log_num
    log_num += 1

    if log_num % 10 == 0:
        print(content)

    if log_num > 10000:
        log_num = 1


# 通用函数: 截图、匹配模板并点击关闭
def process_screen_click(image_path, region, screenshot_prefix):
    global screenshot_num

    # 截取指定区域的屏幕截图
    screen = ImageGrab.grab(bbox=(region[0], region[1], region[0] + region[2],
                                  region[1] + region[3]))

    if DEBUG:
        # 输出截图到本地文件
        screenshot_num += 1
        screen.save(
            f'{root_path}/tmp/{screenshot_prefix}_{screenshot_num}.png')

    # 匹配模板
    match_result = match_template(screen, image_path, region[0], region[1])
    if match_result:
        # 点击关闭结果弹窗
        click_randomly_in_region(match_result)
        return True

    return False


# 检测 结果 弹窗，包括 再来一次、开心收下 等等
def check_result_dialog(log_flag=False):
    global success_num

    if log_flag:
        print_log("阶段 C....", True)

    # 使用通用函数依次处理不同的弹窗情况
    if process_screen_click(image_c_path, region_c, 'screen_c'):
        success_num += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🎉 抢到红包 +1，总共抢红包 {success_num} 次！-- {current_time}")
        print("👉 关闭抢红包结果 C 成功，等待下一次红包...")
        return True

    if process_screen_click(image_c2_path, region_c2, 'screen_c2'):
        print("👉 关闭抢红包结果 C2，（再来一次）等待下一次红包...")
        return True

    if process_screen_click(image_c3_path, region_c3, 'screen_c3'):
        print("👉 关闭抢红包结果 C3，（我知道了）！等待下一次红包...")
        return True

    if process_screen_click(image_c4_path, region_c4, 'screen_c4'):
        print("👉 关闭抢红包结果 C4，（我知道了）等待下一次红包...")
        return True

    if process_screen_click(image_c5_path, region_c5, 'screen_c5'):
        print("👉 关闭抢红包结果 C5，（再来一次）等待下一次红包...")
        return True

    if process_screen_click(image_c6_path, region_c6, 'screen_c6'):
        print("👉 关闭抢红包结果 C6，（我知道了）等待下一次红包...")
        return True

    return False


# 主要逻辑循环
def red_envelope_bot():
    print("启动红包抢夺脚本...")

    while True:
        print_log('阶段A....')

        if process_screen_click(image_a_path, region_a, 'screen_a'):

            print("👉 点击红包弹窗 A 成功，等待开始连续点击红包 B...")

            # 循环检测图片B，进行连续点击
            while True:
                print_log('阶段B...')

                # time.sleep(random.uniform(0.2, 0.3))  # 模拟人手点击间隔
                if process_screen_click(image_b_path, region_b, 'screen_b'):
                    print("👉 点击红包区域 B 成功，继续等待下一次点击 或者 出抢红包结果...")
                else:
                    # 如果连续点击的弹窗消失，则判断是不是出现了结果弹窗
                    result = check_result_dialog(True)
                    if result:
                        # 有结果后等待弹窗关闭动画，避免再次检测
                        time.sleep(0.3)
                        break

        else:
            # 检查是不是有结果弹窗，避免有时候一些直播间红包弹窗逻辑没有处理好
            # 这里主要检测有漏处理的结果弹窗
            result = check_result_dialog()
            if result:
                # 有结果后等待弹窗关闭动画，避免再次检测
                time.sleep(0.3)

        # 需不需要睡眠延迟自定
        # time.sleep(0.1)


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
