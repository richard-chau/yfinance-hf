#!/usr/bin/env python3
"""
清理 Hugging Face 仓库，只保留数据文件
该脚本会：
1. 克隆目标 HF 仓库
2. 删除所有非数据文件（代码、workflow、配置文件等）
3. 只保留数据文件（.parquet, README.md, .gitattributes, spec.json）
4. 推送到 HF
"""

import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# 配置
HF_USERNAME = "winterandchaiyun"
TARGET_REPO = f"https://huggingface.co/datasets/{HF_USERNAME}/yahoo-finance-data"
HF_TOKEN = os.getenv("HF_TOKEN")

# 允许保留的文件和目录
ALLOWED_FILES = {
    # 数据文件
    '*.parquet',
    # 必需的文件
    'README.md',
    '.gitattributes',
    'spec.json',
    # 可能的配置文件
    'dataset_infos.json',
    'dataset_info.json',
}

# 需要删除的文件和目录模式
DELETE_PATTERNS = {
    '*.py',
    '*.pyc',
    '*.pyo',
    '.github',
    '.gitignore',
    '*.md',  # 除了 README.md
    '*.txt',
    '*.sh',
    '*.yml',
    '*.yaml',
    'task.md',
    'SETUP*.md',
    '__pycache__',
    '.env',
    '.env.*',
}

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

def should_keep_file(file_path):
    """判断文件是否应该保留"""
    name = file_path.name
    
    # 检查是否在允许列表中
    if name == 'README.md' or name == '.gitattributes' or name == 'spec.json':
        return True
    
    if name in ['dataset_infos.json', 'dataset_info.json']:
        return True
    
    # 检查是否是 .parquet 文件
    if name.endswith('.parquet'):
        return True
    
    # 其他文件都不保留
    return False

def main():
    """主函数"""
    print("=" * 60)
    print("清理 Hugging Face 仓库")
    print("=" * 60)
    
    if not HF_TOKEN:
        print("错误: HF_TOKEN 未设置")
        print("提示: 请在 ../.env 文件中设置 HF_TOKEN")
        sys.exit(1)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    print(f"\n使用临时目录: {temp_dir}")
    
    try:
        # 1. 克隆目标仓库
        print("\n[1/4] 克隆目标仓库...")
        repo_dir = os.path.join(temp_dir, "repo")
        target_url = f"https://{HF_USERNAME}:{HF_TOKEN}@huggingface.co/datasets/{HF_USERNAME}/yahoo-finance-data"
        run_command(["git", "clone", target_url, repo_dir])
        os.chdir(repo_dir)
        run_command(["git", "lfs", "install"])
        run_command(["git", "lfs", "pull"])
        print("✓ 仓库已克隆")
        
        # 2. 列出所有文件
        print("\n[2/4] 扫描文件...")
        all_files = []
        for root, dirs, files in os.walk('.'):
            # 跳过 .git 目录
            if '.git' in root:
                continue
            for file in files:
                file_path = Path(root) / file
                all_files.append(file_path)
        
        print(f"找到 {len(all_files)} 个文件")
        
        # 3. 删除不需要的文件
        print("\n[3/4] 清理不需要的文件...")
        deleted_count = 0
        kept_count = 0
        
        for file_path in all_files:
            if should_keep_file(file_path):
                kept_count += 1
                print(f"  保留: {file_path}")
            else:
                deleted_count += 1
                print(f"  删除: {file_path}")
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"    警告: 无法删除 {file_path}: {e}")
        
        # 删除空目录（除了 .git）
        for root, dirs, files in os.walk('.', topdown=False):
            if '.git' in root:
                continue
            try:
                if not os.listdir(root):
                    os.rmdir(root)
                    print(f"  删除空目录: {root}")
            except:
                pass
        
        print(f"\n✓ 清理完成: 保留 {kept_count} 个文件，删除 {deleted_count} 个文件")
        
        # 4. 提交并推送
        print("\n[4/4] 提交更改...")
        run_command(["git", "config", "user.name", "github-actions[bot]"])
        run_command(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
        
        run_command(["git", "add", "-A"])
        
        # 检查是否有更改
        result = run_command(["git", "status", "--porcelain"], capture_output=True)
        if result.strip():
            run_command(["git", "commit", "-m", "Clean up: remove code and config files, keep only data files"])
            print("✓ 更改已提交")
            
            print("\n推送到 Hugging Face...")
            run_command(["git", "lfs", "push", "origin", "main", "--all"])
            run_command(["git", "push", "origin", "main", "--force"])
            print("✓ 已推送到 Hugging Face")
        else:
            print("没有更改需要提交")
        
        print("\n" + "=" * 60)
        print("清理完成！")
        print("=" * 60)
        
    finally:
        # 清理临时目录
        os.chdir('/')
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"\n已清理临时目录: {temp_dir}")

if __name__ == "__main__":
    main()
