import subprocess
import sys


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


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        if is_deltaforce_running():
            print("DeltaForce 正在运行")
            sys.exit(0)
        else:
            print("DeltaForce 未在运行")
            sys.exit(1)

    print("正在持续检测 DeltaForce 运行状态（按 Ctrl+C 退出）...")
    try:
        while True:
            running = is_deltaforce_running()
            status = "运行中" if running else "未运行"
            print(f"\r当前状态: {status}", end="", flush=True)
    except KeyboardInterrupt:
        print("\n已退出检测")


if __name__ == "__main__":
    main()
