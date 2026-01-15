#!/usr/bin/env python3
"""
设置 Hugging Face 数据集 upstream 的脚本
该脚本会：
1. 初始化 Git LFS
2. 添加 upstream remote（原始数据集）
3. 添加 target remote（你的 Hugging Face 仓库）
4. 从 upstream 拉取最新数据
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# 配置
UPSTREAM_REPO = "https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data"
HF_USERNAME = "winterandchaiyun"
TARGET_REPO = f"https://huggingface.co/datasets/{HF_USERNAME}/yahoo-finance-data"
HF_TOKEN = os.getenv("HF_TOKEN")

def run_command(cmd, check=True, capture_output=False):
    """运行 shell 命令"""
    print(f"执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True
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
        sys.exit(1)

def main():
    """主函数"""
    print("=" * 60)
    print("设置 Hugging Face 数据集 upstream")
    print("=" * 60)
    
    # 检查是否在 Git 仓库中
    if not os.path.exists(".git"):
        print("错误: 当前目录不是 Git 仓库")
        sys.exit(1)
    
    # 1. 初始化 Git LFS
    print("\n[1/5] 初始化 Git LFS...")
    run_command(["git", "lfs", "install"])
    print("✓ Git LFS 已初始化")
    
    # 2. 配置 Git 用户信息
    print("\n[2/5] 配置 Git 用户信息...")
    run_command(["git", "config", "user.name", HF_USERNAME])
    run_command(["git", "config", "user.email", f"{HF_USERNAME}@example.com"])
    print("✓ Git 用户信息已配置")
    
    # 3. 添加 upstream remote
    print("\n[3/5] 添加 upstream remote...")
    # 检查是否已存在
    remotes = run_command(["git", "remote", "-v"], capture_output=True)
    if "upstream" in remotes:
        print("⚠ upstream remote 已存在，跳过添加")
    else:
        run_command(["git", "remote", "add", "upstream", UPSTREAM_REPO])
        print(f"✓ 已添加 upstream: {UPSTREAM_REPO}")
    
    # 4. 添加 target remote（如果提供了 HF_TOKEN）
    print("\n[4/5] 添加 target remote...")
    if not HF_TOKEN:
        print("⚠ HF_TOKEN 未设置，跳过添加 target remote")
        print("  提示: 请在 .env 文件中设置 HF_TOKEN")
    else:
        target_url = f"https://{HF_USERNAME}:{HF_TOKEN}@huggingface.co/datasets/{HF_USERNAME}/yahoo-finance-data"
        if "target" in remotes:
            print("⚠ target remote 已存在，更新 URL...")
            run_command(["git", "remote", "set-url", "target", target_url])
        else:
            run_command(["git", "remote", "add", "target", target_url])
        print(f"✓ 已添加 target: {TARGET_REPO}")
    
    # 5. 从 upstream 拉取最新数据
    print("\n[5/5] 从 upstream 拉取最新数据...")
    try:
        run_command(["git", "fetch", "upstream", "main"])
        print("✓ 已从 upstream 拉取最新数据")
        
        # 显示远程分支信息
        branches = run_command(["git", "branch", "-r"], capture_output=True)
        print("\n远程分支:")
        for line in branches.split('\n'):
            if 'upstream' in line:
                print(f"  {line.strip()}")
    except subprocess.CalledProcessError:
        print("⚠ 无法从 upstream 拉取数据（可能仓库不存在或需要认证）")
        print("  这通常不是问题，GitHub Actions 会自动处理")
    
    # 显示当前 remotes
    print("\n" + "=" * 60)
    print("当前配置的 remotes:")
    print("=" * 60)
    run_command(["git", "remote", "-v"], check=False)
    
    print("\n" + "=" * 60)
    print("设置完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 确保在 GitHub Secrets 中设置了 HF_TOKEN")
    print("2. GitHub Actions 会自动每天同步数据到你的 Hugging Face 仓库")
    print("3. 查看 .github/workflows/sync_hf_data.yml 了解工作流程")

if __name__ == "__main__":
    main()
