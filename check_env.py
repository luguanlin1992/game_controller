# 新建check_env.py
import sys
import os
import subprocess
import ctypes

def check_system():
    print("=== 系统环境检测 ===")
    
    # 检查操作系统版本
    print(f"操作系统: {sys.platform} {os.name}")
    
    # 检查管理员权限
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    print(f"管理员权限: {'是' if is_admin else '否（建议右键以管理员身份运行）'}")
    
    # 检查VC++运行库
    vc_versions = [
        r"C:\Windows\System32\vcruntime140.dll",  # VC++ 2015-2019
        r"C:\Windows\System32\vcruntime140_1.dll" # VC++ 2022
    ]
    for dll in vc_versions:
        exists = os.path.exists(dll)
        print(f"{os.path.basename(dll)}: {'存在' if exists else '缺失'}")

if __name__ == "__main__":
    check_system()
    input("\n检测完成，按回车退出...")