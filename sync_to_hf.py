#!/usr/bin/env python3
"""
同步数据集到 Hugging Face 的脚本
该脚本会：
1. 初始化 Git LFS
2. 从 upstream (bwzheng2010/yahoo-finance-data) 拉取最新数据
3. 推送到目标 Hugging Face 仓库 (winterandchaiyun/yahoo-finance-data)
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件（从父目录）
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# 配置
UPSTREAM_REPO = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
HF_USERNAME = "winterandchaiyun"
TARGET_REPO = f"https://huggingface.co/datasets/{HF_USERNAME}/yahoo-finance-data"
HF_TOKEN = os.getenv("HF_TOKEN")

def run_command(cmd, check=True, capture_output=False, cwd=None):
    """运行 shell 命令"""
    print(f"执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True,
            cwd=cwd
        )
        if capture_output:
            return result.stdout.strip()
        return result
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if capture_output and e.stdout:
            print(f"输出: {e.stdout}")
        if capture_output and e.stderr:
            print(f"错误输出: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("同步数据集到 Hugging Face")
    print("=" * 60)
    
    # 检查是否在 Git 仓库中
    if not os.path.exists(".git"):
        print("错误: 当前目录不是 Git 仓库")
        sys.exit(1)
    
    # 检查 HF_TOKEN
    if not HF_TOKEN:
        print("错误: HF_TOKEN 未设置")
        print("提示: 请在 ../.env 文件中设置 HF_TOKEN")
        sys.exit(1)
    
    # 1. 初始化 Git LFS
    print("\n[1/6] 初始化 Git LFS...")
    run_command(["git", "lfs", "install"])
    print("✓ Git LFS 已初始化")
    
    # 2. 配置 Git 用户信息
    print("\n[2/6] 配置 Git 用户信息...")
    run_command(["git", "config", "user.name", HF_USERNAME])
    run_command(["git", "config", "user.email", f"{HF_USERNAME}@example.com"])
    print("✓ Git 用户信息已配置")
    
    # 3. 添加/更新 upstream remote
    print("\n[3/6] 配置 upstream remote...")
    remotes_output = run_command(["git", "remote", "-v"], capture_output=True, check=False)
    remotes = remotes_output if remotes_output else ""
    
    if "upstream" in remotes:
        print("⚠ upstream remote 已存在，更新 URL...")
        run_command(["git", "remote", "set-url", "upstream", UPSTREAM_REPO])
    else:
        run_command(["git", "remote", "add", "upstream", UPSTREAM_REPO])
    print(f"✓ upstream 已配置: {UPSTREAM_REPO}")
    
    # 4. 添加/更新 target remote
    print("\n[4/6] 配置 target remote...")
    target_url = f"https://{HF_USERNAME}:{HF_TOKEN}@huggingface.co/datasets/{HF_USERNAME}/yahoo-finance-data"
    if "target" in remotes:
        print("⚠ target remote 已存在，更新 URL...")
        run_command(["git", "remote", "set-url", "target", target_url])
    else:
        run_command(["git", "remote", "add", "target", target_url])
    print(f"✓ target 已配置: {TARGET_REPO}")
    
    # 5. 从 upstream 拉取最新数据
    print("\n[5/6] 从 upstream 拉取最新数据...")
    try:
        # 先获取所有 LFS 文件
        run_command(["git", "lfs", "fetch", "upstream", "main"], check=False)
        run_command(["git", "fetch", "upstream", "main"])
        print("✓ 已从 upstream 拉取最新数据")
        
        # 合并数据（如果有冲突以 upstream 为准）
        current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True)
        if current_branch != "main":
            print(f"⚠ 当前分支是 {current_branch}，切换到 main...")
            run_command(["git", "checkout", "-b", "main"], check=False)
        
        # 尝试合并
        merge_result = run_command(
            ["git", "merge", "upstream/main", "-m", "Auto-sync from bwzheng2010", "-X", "theirs", "--allow-unrelated-histories"],
            check=False
        )
        if merge_result is None:
            print("⚠ 合并失败，尝试重置...")
            run_command(["git", "reset", "--hard", "upstream/main"], check=False)
        
        # 拉取 LFS 文件
        run_command(["git", "lfs", "pull", "upstream", "main"], check=False)
        print("✓ 数据已合并")
    except Exception as e:
        print(f"⚠ 拉取数据时出现问题: {e}")
        print("  这通常不是问题，GitHub Actions 会自动处理")
    
    # 6. 推送到 target (Hugging Face)
    print("\n[6/6] 推送到 Hugging Face...")
    try:
        # 确保 LFS 文件也被推送
        run_command(["git", "lfs", "push", "target", "main", "--all"], check=False)
        push_result = run_command(
            ["git", "push", "target", "main", "--force"],
            check=False
        )
        if push_result is None:
            print("⚠ 推送失败，可能是仓库不存在或权限问题")
        else:
            print("✓ 数据已推送到 Hugging Face")
    except Exception as e:
        print(f"⚠ 推送时出现问题: {e}")
        print("  提示: 确保 Hugging Face 仓库已创建")
    
    # 显示当前 remotes
    print("\n" + "=" * 60)
    print("当前配置的 remotes:")
    print("=" * 60)
    run_command(["git", "remote", "-v"], check=False)
    
    print("\n" + "=" * 60)
    print("同步完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
