import os
import shutil
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _cfg = json.load(f)

PAK_DIR = _cfg["PAK_DIR"]
RAIL_DIR = _cfg["RAIL_DIR"]
PAK_PAIRS = _cfg["PAK_PAIRS"]
DAT_NAME = _cfg["DAT_NAME"]
DAT_BACKUP_DIR = _cfg["DAT_BACKUP_DIR"]
DAT_BACKUP_PATH = os.path.join(DAT_BACKUP_DIR, DAT_NAME + ".bak")


def restore():
    for pak_orig, pak_new in PAK_PAIRS:
        pak_src = os.path.join(PAK_DIR, pak_new)
        pak_dst = os.path.join(PAK_DIR, pak_orig)
        if os.path.exists(pak_src):
            os.rename(pak_src, pak_dst)
            print(f"已重命名: {pak_new} -> {pak_orig}")
        else:
            print(f"未找到文件: {pak_src}")

    dat_dst = os.path.join(RAIL_DIR, DAT_NAME)
    if os.path.exists(DAT_BACKUP_PATH):
        if os.path.exists(dat_dst):
            os.remove(dat_dst)
            print(f"已删除原文件: {DAT_NAME}")
        shutil.copy2(DAT_BACKUP_PATH, dat_dst)
        print(f"已还原: {DAT_NAME}")
    else:
        print(f"未找到备份: {DAT_BACKUP_PATH}")


if __name__ == "__main__":
    restore()
    print("\n恢复完成")