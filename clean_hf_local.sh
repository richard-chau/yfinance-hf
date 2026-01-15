#!/bin/bash
# 清理 Hugging Face 仓库的本地脚本
# 使用方法: HF_TOKEN=your_token ./clean_hf_local.sh

set -e

if [ -z "$HF_TOKEN" ]; then
    echo "错误: 请设置 HF_TOKEN 环境变量"
    echo "使用方法: HF_TOKEN=your_token ./clean_hf_local.sh"
    exit 1
fi

HF_USERNAME="winterandchaiyun"
TARGET_REPO="https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/datasets/${HF_USERNAME}/yahoo-finance-data"

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "使用临时目录: $TEMP_DIR"

cd "$TEMP_DIR"

# 克隆仓库（不使用 LFS，稍后单独处理）
echo "克隆目标仓库..."
GIT_LFS_SKIP_SMUDGE=1 git clone "$TARGET_REPO" repo
cd repo
git lfs install

# 配置 LFS 使用 token 认证
git config lfs.url "https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/datasets/${HF_USERNAME}/yahoo-finance-data.git/info/lfs"
git lfs pull || echo "LFS pull 警告，继续..."

# 配置 git
git config user.name 'github-actions[bot]'
git config user.email 'github-actions[bot]@users.noreply.github.com'

# 删除所有非数据文件
echo "清理文件..."
# 删除所有文件和目录（除了 .git）
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} \;

# 从 upstream 克隆并复制数据文件
echo "从 upstream 获取数据文件..."
cd ..
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data upstream
cd upstream
git lfs install
git lfs pull || echo "LFS pull 警告，继续..."

# 复制数据文件到目标仓库
echo "复制数据文件..."
cd ../repo

# 复制 .parquet 文件
find ../upstream -name "*.parquet" -exec cp {} . \;

# 复制必要的配置文件
[ -f ../upstream/README.md ] && cp ../upstream/README.md . || true
[ -f ../upstream/.gitattributes ] && cp ../upstream/.gitattributes . || true
[ -f ../upstream/spec.json ] && cp ../upstream/spec.json . || true
[ -f ../upstream/dataset_infos.json ] && cp ../upstream/dataset_infos.json . || true
[ -f ../upstream/dataset_info.json ] && cp ../upstream/dataset_info.json . || true

# 提交并推送
echo "提交更改..."
git add -A

if ! git diff --staged --quiet || ! git diff --quiet; then
    git commit -m "Clean up: remove code and config files, keep only data files" || echo "没有更改需要提交"
    
    echo "推送到 Hugging Face..."
    git lfs push origin main --all || echo "LFS push 警告，继续..."
    git push origin main --force
    echo "✓ 清理完成！"
else
    echo "仓库已经干净，无需更改"
fi

# 清理
cd /
rm -rf "$TEMP_DIR"
echo "✓ 临时目录已清理"
