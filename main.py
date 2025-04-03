from window_selector import select_window
from screen_processor import capture_window, find_template
import pyautogui
import time
import yaml
import os
import sys

# 加载配置
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

config_path = resource_path("config.yaml")
with open(config_path, encoding='utf-8') as f:
    CONFIG = yaml.safe_load(f)

def main():
    try:
        print("=== 调试信息 ===")
        print("当前工作目录:", os.getcwd())
        print("MEIPASS状态:", hasattr(sys, '_MEIPASS'))
        print("配置文件路径:", resource_path("config.yaml"))
        print("武器模板目录是否存在:", os.path.exists(resource_path(CONFIG['模板配置']['武器选择']['武器模板目录'])))
        
        window = select_window()
        print(f"锁定窗口: {window['title']}")
        
        try:
            while True:
                frame = capture_window(window)
                
                # 优先检测准备状态
                ready_path = resource_path(CONFIG['模板配置']['准备就绪']['路径'])
                ready_pos = find_template(frame, ready_path)
                if ready_pos:
                    x = window['left'] + ready_pos[0] + CONFIG['模板配置']['准备就绪']['偏移'][0]
                    y = window['top'] + ready_pos[1] + CONFIG['模板配置']['准备就绪']['偏移'][1]
                    pyautogui.click(x, y)
                    print("▶ 游戏准备就绪")
                    continue

                # 优先检测返回状态
                back_path = resource_path(CONFIG['模板配置']['返回']['路径'])
                back_pos = find_template(frame, back_path)
                if back_pos:
                    x = window['left'] + back_pos[0] + CONFIG['模板配置']['返回']['偏移'][0]
                    y = window['top'] + back_pos[1] + CONFIG['模板配置']['返回']['偏移'][1]
                    pyautogui.click(x, y)
                    print("▶ 返回就绪")
                    continue
                    
                # 检测武器选择界面
                select_path = resource_path(CONFIG['模板配置']['武器选择']['路径'])
                select_pos = find_template(frame, select_path)
                if select_pos:
                    print("▶ 进入武器选择界面")
                    weapon_dir = resource_path(CONFIG['模板配置']['武器选择']['武器模板目录'])
                    
                    # 获取按数字排序的武器模板列表
                    weapon_files = sorted(
                        [f for f in os.listdir(weapon_dir) if f.endswith('.png')],
                        key=lambda x: int(x.split('.')[0])
                    )
                    
                    # 按序号检测武器
                    for weapon_file in weapon_files:
                        weapon_path = os.path.join(weapon_dir, weapon_file)
                        gun_pos = find_template(frame, weapon_path)
                        
                        if gun_pos:
                            weapon_id = os.path.splitext(weapon_file)[0]
                            print(f"✅ 发现武器ID: {weapon_id}")
                            
                            # 计算点击坐标
                            offset = CONFIG['模板配置']['武器选择']['成功偏移']
                            abs_x = window['left'] + gun_pos[0] + offset[0]
                            abs_y = window['top'] + gun_pos[1] + offset[1]
                            
                            pyautogui.click(abs_x, abs_y)
                            print(f"点击武器位置 [{abs_x}, {abs_y}]")
                            break
                    else:
                        # 没有找到任何武器时执行默认操作
                        default_offset = CONFIG['模板配置']['武器选择']['默认偏移']
                        abs_x = window['left'] + select_pos[0] + default_offset[0]
                        abs_y = window['top'] + select_pos[1] + default_offset[1]
                        pyautogui.click(abs_x, abs_y)
                        print(f"⚠️ 使用默认位置 [{abs_x}, {abs_y}]")
                    
                    time.sleep(0.5)  # 操作后等待防止重复点击
                
                time.sleep(CONFIG['检测间隔'])
                
        except KeyboardInterrupt:
            print("\n程序已安全退出")
    
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"\033[31m致命错误:\033[0m {str(e)}")
        with open(resource_path('error.log'), 'w', encoding='utf-8') as f:
            f.write(error_msg)
        input("按回车退出...")

if __name__ == "__main__":
    main()
