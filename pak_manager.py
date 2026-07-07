import os
import shutil
import sys
import subprocess
import time
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _cfg = json.load(f)

PAK_DIR = _cfg["PAK_DIR"]
RAIL_DIR = _cfg["RAIL_DIR"]
WEGAME_PATH = _cfg["WEGAME_PATH"]
PAK_ORIG = _cfg["PAK_ORIG"]
PAK_NEW = _cfg["PAK_NEW"]
DAT_NAME = _cfg["DAT_NAME"]
DAT_SRC_DIR = _cfg["DAT_SRC_DIR"]
WEGAME_PROCESSES = _cfg["WEGAME_PROCESSES"]


def modify():
    pak_src = os.path.join(PAK_DIR, PAK_ORIG)
    pak_dst = os.path.join(PAK_DIR, PAK_NEW)
    if os.path.exists(pak_src):
        os.rename(pak_src, pak_dst)
        print(f"已重命名: {PAK_ORIG} -> {PAK_NEW}")
    else:
        print(f"未找到文件: {pak_src}")


def restore():
    pak_src = os.path.join(PAK_DIR, PAK_NEW)
    pak_dst = os.path.join(PAK_DIR, PAK_ORIG)
    if os.path.exists(pak_src):
        os.rename(pak_src, pak_dst)
        print(f"已重命名: {PAK_NEW} -> {PAK_ORIG}")
    else:
        print(f"未找到文件: {pak_src}")

    dat_src = os.path.join(DAT_SRC_DIR, DAT_NAME)
    dat_dst = os.path.join(RAIL_DIR, DAT_NAME)
    if os.path.exists(dat_src):
        if os.path.exists(dat_dst):
            os.remove(dat_dst)
            print(f"已删除原文件: {DAT_NAME}")
        shutil.copy2(dat_src, dat_dst)
        print(f"已替换: {DAT_NAME}")
    else:
        print(f"未找到源文件: {dat_src}")


def is_deltaforce_running():
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq DeltaForce*"],
            capture_output=True,
            text=True,
            encoding="gbk"
        )
        return "DeltaForce" in result.stdout
    except Exception as e:
        print(f"检测失败: {e}")
        return False


def start_wegame():
    if not os.path.exists(WEGAME_PATH):
        print(f"未找到 WeGame: {WEGAME_PATH}")
        return False
    try:
        subprocess.Popen(WEGAME_PATH)
        print(f"已启动 WeGame")
        return True
    except Exception as e:
        print(f"启动 WeGame 失败: {e}")
        return False


def close_wegame():
    closed = False
    for proc in WEGAME_PROCESSES:
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/IM", proc],
                capture_output=True,
                text=True,
                encoding="gbk"
            )
            if "成功" in result.stdout or "SUCCESS" in result.stdout.upper():
                print(f"已关闭: {proc}")
                closed = True
        except Exception as e:
            print(f"关闭 {proc} 失败: {e}")
    return closed


def restart_wegame():
    print("正在关闭 WeGame...")
    close_wegame()
    time.sleep(2)
    print("正在启动 WeGame...")
    start_wegame()


def wait_for_exit(exit_num, tip_on_start=None, tip_on_exit=None):
    prev_running = is_deltaforce_running()
    if prev_running:
        print(f"检测到游戏正在运行，等待第{exit_num}次大退...")
    else:
        print(f"游戏未运行，请启动游戏...")

    while True:
        time.sleep(1)
        current_running = is_deltaforce_running()

        if not prev_running and current_running:
            print(f"检测到游戏已启动，等待大退...")
            if tip_on_start:
                print(f"【提示】{tip_on_start}")

        if prev_running and not current_running:
            print(f"检测到第{exit_num}次大退！")
            if tip_on_exit:
                print(f"【提示】{tip_on_exit}")
            return

        prev_running = current_running


def auto_mode():
    print("\n===== 自动化模式（循环执行） =====")
    print("流程: 第1次大退 → 脚本修改 → 第2次大退 → 脚本恢复 → 重启WeGame → 第3次大退 → 重启WeGame → 循环")
    print("按 Ctrl+C 可随时停止\n")

    round_num = 0
    try:
        while True:
            round_num += 1
            print(f"\n========== 第 {round_num} 轮 ==========")

            print("--- 阶段1: 等待第一次大退 ---")
            wait_for_exit(1, tip_on_start="请裸装进入长弓然后在选人界面大退")

            print("\n--- 阶段2: 执行脚本修改 ---")
            modify()
            print("脚本修改完成")
            print("【提示】请去删除地图，然后上装备后大退")

            print("\n--- 阶段3: 等待第二次大退 ---")
            wait_for_exit(2, tip_on_start="把要卡的东西放在身上然后大退")

            print("\n--- 阶段4: 执行脚本恢复 ---")
            restore()
            print("脚本恢复完成")

            print("\n--- 阶段5: 重启 WeGame ---")
            restart_wegame()

            print("\n--- 阶段6: 等待第三次大退 ---")
            wait_for_exit(3, tip_on_start="上号重连进长弓自雷以后大退 完成后自动循环回到第1阶段")

            print("\n--- 阶段7: 重启 WeGame ---")
            restart_wegame()

            print(f"\n第 {round_num} 轮完成，准备下一轮...")

    except KeyboardInterrupt:
        print("\n\n已停止自动化模式")


def main():
    while True:
        print("\n===== 功能菜单 =====")
        print("1. 修改")
        print("2. 恢复")
        print("3. 自动化")
        print("0. 退出")
        print("====================")
        choice = input("请输入选项 (0/1/2/3): ").strip()

        if choice == "1":
            modify()
        elif choice == "2":
            restore()
        elif choice == "3":
            auto_mode()
        elif choice == "0":
            print("已退出")
            break
        else:
            print("输入无效，请重新输入")


if __name__ == "__main__":
    main()
