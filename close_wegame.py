import subprocess
import sys
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _cfg = json.load(f)

WEGAME_PATH = _cfg["WEGAME_PATH"]
WEGAME_PROCESSES = _cfg["WEGAME_PROCESSES"]


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

    if not closed:
        print("未找到 WeGame 进程")

    return closed


def start_wegame():
    if not os.path.exists(WEGAME_PATH):
        print(f"未找到 WeGame: {WEGAME_PATH}")
        return False

    try:
        subprocess.Popen(WEGAME_PATH)
        print(f"已启动 WeGame: {WEGAME_PATH}")
        return True
    except Exception as e:
        print(f"启动 WeGame 失败: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start_wegame()
    else:
        close_wegame()
