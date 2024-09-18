import pygame  # 导入pygame库
from pygame.locals import *  # 导入pygame的本地常量
import sys  # 导入系统模块
from random import shuffle, randint  # 导入随机函数
import os  # 导入操作系统模块

# 常量定义
WINDOW_WIDTH = 800  # 窗口宽度
WINDOW_HEIGHT = 600  # 窗口高度
ICON_SIZE = 70  # 图标大小
OVERLAP_PERCENTAGE = 0.2  # 图标重叠比例
WHITE = pygame.Color(255, 255, 255)  # 定义白色
BLACK = pygame.Color(0, 0, 0)  # 定义黑色
RED = pygame.Color(255, 0, 0)  # 定义红色
GREEN = pygame.Color(0, 255, 0)  # 定义绿色
STORAGE_BACKGROUND_COLOR = pygame.Color(230, 230, 230)  # 存储区背景色
STORAGE_BOX_COLOR = pygame.Color(240, 240, 240)  # 存储框颜色常量
STORAGE_BOX_BORDER_COLOR = pygame.Color(180, 180, 180)  # 存储框边框颜色
SCORES_FILE = "scores.txt"  # 文件名用于保存排行榜

# 背景图路径
MAIN_BG = 'main_bg.jpg'  # 主菜单背景
GAME_BG = 'game_bg.jpg'  # 游戏背景
WIN_BG = 'win_bg.jpg'  # 胜利界面背景
DEFEAT_BG = 'defeat_bg.jpg'  # 失败界面背景

# 图像路径列表（假设所有图像按 sheep1.png 到 sheep15.png 命名）
sheep_images = [f"sheep{i}.png" for i in range(1, 16)]  # 生成羊图像的文件名列表

# 加载图像并调整大小
def load_sheep_images(used_image_count):
    """加载指定数量的羊图像并调整其大小"""
    images = []  # 用于存储加载的图像
    for i in range(used_image_count):  # 遍历使用的图像数量
        img = pygame.image.load(sheep_images[i])  # 加载图像
        img = pygame.transform.scale(img, (ICON_SIZE, ICON_SIZE))  # 调整图像大小
        images.append(img)  # 将调整后的图像添加到列表中
    return images  # 返回加载的图像列表

# 加载背景图像并调整大小
def load_background_image(path):
    """加载背景图像并调整为窗口大小"""
    img = pygame.image.load(path)  # 加载背景图像
    return pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # 调整为窗口大小并返回

# 保存分数到排行榜
def save_score(score):
    """将得分保存到排行榜文件中"""
    scores = load_scores()  # 加载现有分数
    scores.append(score)  # 将新的得分添加到分数列表中
    scores = sorted(scores, reverse=True)[:5]  # 只保留前五名的最高分
    with open(SCORES_FILE, 'w') as file:  # 以写入模式打开文件
        for s in scores:  # 遍历分数
            file.write(f"{s}\n")  # 写入分数到文件

# 加载排行榜分数
def load_scores():
    """从文件加载排行榜分数"""
    if not os.path.exists(SCORES_FILE):  # 检查文件是否存在
        return []  # 如果不存在，返回空列表
    with open(SCORES_FILE, 'r') as file:  # 以读取模式打开文件
        return [int(line.strip()) for line in file.readlines()]  # 返回文件中所有分数的列表

# 显示排行榜
def show_leaderboard(screen):
    """显示排行榜界面"""
    scores = load_scores()  # 加载分数
    font = pygame.font.Font(pygame.font.match_font('simhei'), 50)  # 创建标题字体
    small_font = pygame.font.Font(pygame.font.match_font('simhei'), 30)  # 创建分数字体

    background = load_background_image(MAIN_BG)  # 使用主菜单背景
    screen.blit(background, (0, 0))  # 绘制背景

    title_text = font.render("排行榜", True, BLACK)  # 渲染排行榜标题文本
    screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 50))  # 显示标题文本

    if scores:  # 如果有分数记录
        for i, score in enumerate(scores):  # 遍历分数
            score_text = small_font.render(f"{i + 1}. {score}", True, BLACK)  # 渲染分数文本
            screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 150 + i * 50))  # 显示分数
    else:  # 如果没有分数记录
        no_scores_text = small_font.render("没有记录的分数", True, BLACK)  # 渲染无分数文本
        screen.blit(no_scores_text, (WINDOW_WIDTH // 2 - no_scores_text.get_width() // 2, 150))  # 显示无分数文本

    pygame.display.flip()  # 更新显示
    pygame.time.wait(5000)  # 显示排行榜5秒后返回主菜单
    main_menu()  # 返回主菜单

# 游戏胜利界面
def show_victory_screen(screen, score):
    """显示游戏胜利界面"""
    save_score(score)  # 在胜利时保存分数到排行榜
    font = pygame.font.Font(pygame.font.match_font('simhei'), 60)  # 创建胜利文本字体

    background = load_background_image(WIN_BG)  # 使用胜利背景
    screen.blit(background, (0, 0))  # 绘制背景

    victory_text = font.render("游戏胜利!", True, GREEN)  # 渲染胜利文本
    score_text = font.render(f"得分: {score}", True, BLACK)  # 渲染得分文本
    screen.blit(victory_text, (WINDOW_WIDTH // 2 - victory_text.get_width() // 2, WINDOW_HEIGHT // 2 - 150))  # 显示胜利文本
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))  # 显示得分文本
    pygame.display.flip()  # 更新显示
    pygame.time.wait(3000)  # 等待3秒
    show_leaderboard(screen)  # 显示排行榜

# 游戏失败界面
def show_defeat_screen(screen):
    """显示游戏失败界面"""
    font = pygame.font.Font(pygame.font.match_font('simhei'), 60)  # 创建失败文本字体

    background = load_background_image(DEFEAT_BG)  # 使用失败背景
    screen.blit(background, (0, 0))  # 绘制背景

    defeat_text = font.render("游戏失败!", True, RED)  # 渲染失败文本
    screen.blit(defeat_text, (WINDOW_WIDTH // 2 - defeat_text.get_width() // 2, WINDOW_HEIGHT // 2 - 150))  # 显示失败文本
    pygame.display.flip()  # 更新显示
    pygame.time.wait(3000)  # 等待3秒
    show_leaderboard(screen)  # 显示排行榜

# 悔棋操作：将最后的存储图标放回原网格
def undo_last_move(layers, store, move_history):
    """将最后的存储图标放回原网格"""
    if move_history:  # 如果有历史记录
        last_move = move_history.pop()  # 获取最后的移动
        r, c, icon_index = last_move  # 解包移动的行、列和图标索引
        store[store.index(icon_index)] = 0  # 将存储中的图标清空
        layers[r][c].append(icon_index - 1)  # 将图标放回原网格
        return True  # 返回成功
    return False  # 返回失败

# 主菜单函数
def main_menu():
    """显示主菜单"""
    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 创建窗口
    pygame.display.set_caption('石了个石 - 主菜单')  # 设置窗口标题

    font = pygame.font.Font(pygame.font.match_font('simhei'), 50)  # 创建主标题字体
    small_font = pygame.font.Font(pygame.font.match_font('simhei'), 30)  # 创建菜单选项字体

    menu_options = ["简单模式", "普通模式", "困难模式", "排行榜", "退出"]  # 菜单选项
    selected_option = 0  # 当前选中的选项索引

    while True:
        background = load_background_image(MAIN_BG)  # 使用主菜单背景
        screen.blit(background, (0, 0))  # 绘制背景

        title_text = font.render("石了个石_陈石石石", True, BLACK)  # 渲染标题文本
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100))  # 显示标题文本

        # 显示菜单选项
        for index, option in enumerate(menu_options):
            color = RED if index == selected_option else WHITE  # 选中的选项为红色，其他为白色
            menu_text = small_font.render(option, True, color)  # 渲染菜单文本
            screen.blit(menu_text, (WINDOW_WIDTH // 2 - menu_text.get_width() // 2, 300 + index * 50))  # 显示菜单选项

        for event in pygame.event.get():  # 处理事件
            if event.type == QUIT:  # 如果退出事件
                pygame.quit()  # 退出pygame
                sys.exit()  # 退出程序
            elif event.type == KEYDOWN:  # 如果按下键盘
                if event.key == K_UP:  # 向上箭头
                    selected_option = (selected_option - 1) % len(menu_options)  # 选择上一个选项
                elif event.key == K_DOWN:  # 向下箭头
                    selected_option = (selected_option + 1) % len(menu_options)  # 选择下一个选项
                elif event.key == K_RETURN:  # 回车键
                    if selected_option == 0:  # 简单模式
                        game_loop(difficulty="easy")  # 启动简单模式游戏
                    elif selected_option == 1:  # 普通模式
                        game_loop(difficulty="normal")  # 启动普通模式游戏
                    elif selected_option == 2:  # 困难模式
                        game_loop(difficulty="hard")  # 启动困难模式游戏
                    elif selected_option == 3:  # 排行榜
                        show_leaderboard(screen)  # 显示排行榜
                    elif selected_option == 4:  # 退出
                        pygame.quit()  # 退出pygame
                        sys.exit()  # 退出程序

        pygame.display.flip()  # 更新显示

# 游戏循环函数，包含难度级别
def game_loop(difficulty):
    """游戏主循环"""
    pygame.init()  # 初始化pygame
    play_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 创建游戏窗口
    pygame.display.set_caption(f'石了个石 - {difficulty.capitalize()} 模式')  # 设置窗口标题

    # 根据难度设置图像数量和时间限制
    if difficulty == "easy":
        used_image_count = 7
        time_limit = 180
    elif difficulty == "normal":
        used_image_count = 10
        time_limit = 180
    elif difficulty == "hard":
        used_image_count = 15
        time_limit = 90

    images = load_sheep_images(used_image_count)  # 加载图像

    font = pygame.font.Font(pygame.font.match_font('simhei'), 25)  # 创建游戏字体
    fps_clock = pygame.time.Clock()  # 创建时钟对象

    grid_cols = 8  # 网格列数
    grid_rows = 5  # 网格行数
    offset_x = (WINDOW_WIDTH - (grid_cols * (ICON_SIZE + 10))) // 2  # 水平偏移量
    offset_y = (WINDOW_HEIGHT - (grid_rows * (ICON_SIZE + 10))) // 2  # 垂直偏移量
    max_item_count = 7  # 最大物品数量
    item_count = 3  # 当前物品数量
    store = [0] * max_item_count  # 存储区初始化
    score = 0  # 当前得分
    total_score = 0  # 总得分
    seconds = time_limit  # 剩余时间

    start_ticks = pygame.time.get_ticks()  # 记录游戏开始时间

    # 生成游戏网格
    layers = generate_solvable_grid(used_image_count, grid_cols, grid_rows)

    selected_icons = []  # 选中的图标列表
    move_history = []  # 移动历史记录

    while True:
        background = load_background_image(GAME_BG)  # 使用游戏背景
        play_surface.blit(background, (0, 0))  # 绘制背景

        seconds = time_limit - (pygame.time.get_ticks() - start_ticks) // 1000  # 计算剩余时间

        # 绘制图标网格
        for r in range(grid_rows):  # 遍历行
            for c in range(grid_cols):  # 遍历列
                x = offset_x + c * (ICON_SIZE + 10)  # 计算图标的x坐标
                base_y = offset_y + r * (ICON_SIZE + 10)  # 计算图标的基准y坐标
                if layers[r][c]:  # 如果该格子有物品
                    stack_height = len(layers[r][c])  # 堆叠高度
                    for level in range(stack_height):  # 遍历堆叠的每一层
                        icon_index = layers[r][c][level]  # 获取当前层的图标索引
                        y = base_y - level * int(ICON_SIZE * OVERLAP_PERCENTAGE)  # 计算图标的y坐标
                        play_surface.blit(images[icon_index], (x, y))  # 绘制图标

        # 绘制存储区
        storage_x = WINDOW_WIDTH // 2 - (max_item_count * ICON_SIZE) // 2  # 存储区x坐标
        storage_y = WINDOW_HEIGHT - 100  # 存储区y坐标
        for i in range(max_item_count):  # 遍历存储区
            pygame.draw.rect(play_surface, STORAGE_BOX_COLOR,  # 绘制存储框
                             (storage_x + i * ICON_SIZE, storage_y, ICON_SIZE, ICON_SIZE))
            if store[i]:  # 如果存储区有物品
                play_surface.blit(images[store[i] - 1], (storage_x + i * ICON_SIZE, storage_y))  # 绘制物品

        # 显示分数和计时器
        mission_text = f"总分: {total_score}"  # 总分文本
        score_text = f"当前分数: {score}"  # 当前分数文本
        countdown_text = f"时间: {seconds}"  # 剩余时间文本

        play_surface.blit(font.render(mission_text, True, RED), (10, 10))  # 显示总分
        play_surface.blit(font.render(score_text, True, GREEN), (10, 40))  # 显示当前分数
        play_surface.blit(font.render(countdown_text, True, GREEN), (WINDOW_WIDTH / 2 - 50, 10))  # 显示剩余时间

        for event in pygame.event.get():  # 处理事件
            if event.type == QUIT:  # 如果退出事件
                pygame.quit()  # 退出pygame
                sys.exit()  # 退出程序
            if event.type == MOUSEBUTTONUP:  # 鼠标点击事件
                (mouse_x, mouse_y) = event.pos  # 获取鼠标点击位置
                for r in range(grid_rows):  # 遍历行
                    for c in range(grid_cols):  # 遍历列
                        x = offset_x + c * (ICON_SIZE + 10)  # 计算图标的x坐标
                        base_y = offset_y + r * (ICON_SIZE + 10)  # 计算图标的基准y坐标
                        if layers[r][c]:  # 如果该格子有物品
                            top_image_y = base_y - (len(layers[r][c]) - 1) * int(ICON_SIZE * OVERLAP_PERCENTAGE)  # 顶层图标y坐标
                            # 检查鼠标点击位置是否在图标上
                            if x < mouse_x < x + ICON_SIZE and top_image_y < mouse_y < top_image_y + ICON_SIZE:
                                clicked_icon = layers[r][c].pop()  # 获取被点击的图标
                                move_history.append((r, c, clicked_icon + 1))  # 记录移动历史
                                for i in range(7):  # 将图标放入存储区
                                    if store[i] == 0:  # 找到空位
                                        store[i] = clicked_icon + 1  # 放入图标
                                        break

                                # 检查是否消除
                                if store.count(clicked_icon + 1) == 3:
                                    store = [0 if icon == clicked_icon + 1 else icon for icon in store]  # 清空对应的图标
                                    score += 10  # 每次消除得分
                                    total_score += 10  # 更新总分

                                    if score > 20:  # 每20分增加一个存储位
                                        item_count = min(item_count + 1, max_item_count)  # 增加物品数量
                                        score = 0  # 重置当前得分

            if event.type == KEYDOWN:  # 按键事件
                if event.key == K_BACKSPACE:  # 用户按下退格键来悔棋
                    undo_last_move(layers, store, move_history)  # 进行悔棋操作

        if seconds <= 0:  # 如果时间结束
            show_defeat_screen(play_surface)  # 显示失败界面

        if all(store) and not any(store.count(icon) == 3 for icon in store if icon != 0):  # 存储区已满且没有消除
            show_defeat_screen(play_surface)  # 显示失败界面

        if not any(layers[r][c] for r in range(grid_rows) for c in range(grid_cols)):  # 如果网格没有物品
            show_victory_screen(play_surface, total_score)  # 显示胜利界面

        pygame.display.flip()  # 刷新窗口
        fps_clock.tick(30)  # 控制帧率

# 生成有解的游戏网格
def generate_solvable_grid(used_image_count, grid_cols, grid_rows):
    """生成一个可解的游戏网格"""
    total_cells = grid_cols * grid_rows  # 计算总格子数
    images_per_type = (total_cells // used_image_count // 3) * 3  # 每种图像的数量
    if images_per_type == 0:
        images_per_type = 3  # 最小为3

    image_list = []  # 图像列表
    for i in range(used_image_count):  # 遍历每种图像
        image_list.extend([i] * images_per_type)  # 将图像添加到列表中

    shuffle(image_list)  # 打乱图像列表
    layers = []  # 存储每一层的图像
    index = 0  # 当前索引

    for _ in range(grid_rows):  # 遍历每一行
        row = []  # 当前行
        for _ in range(grid_cols):  # 遍历每一列
            count = randint(1, 3)  # 随机选择1到3个图像
            if index + count > len(image_list):  # 检查索引是否超出范围
                count = len(image_list) - index  # 调整为剩余的图像数量
            row.append(image_list[index:index + count])  # 添加图像到当前行
            index += count  # 更新索引
        layers.append(row)  # 添加当前行到图层

    return layers  # 返回生成的网格

if __name__ == "__main__":  # 主程序入口
    main_menu()  # 启动主菜单
