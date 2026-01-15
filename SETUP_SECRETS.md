# GitHub Secrets 设置指南

本指南将帮助你设置 GitHub Actions 所需的 Secrets，以便自动同步 Hugging Face 数据集。

## 需要设置的 Secrets

### 1. HF_TOKEN (必需)

这是你的 Hugging Face 访问令牌，用于推送到你的 Hugging Face 数据集仓库。

#### 如何获取 HF_TOKEN：

1. 访问 [Hugging Face 账户设置](https://huggingface.co/settings/tokens)
2. 点击 "New token" 创建新令牌
3. 设置令牌名称（例如：`github-actions-sync`）
4. 选择权限：
   - **至少需要 `write` 权限**（用于推送数据）
   - 推荐选择 `write` 权限
5. 点击 "Generate token"
6. **重要：立即复制令牌**，因为之后无法再次查看

#### 如何在 GitHub 中设置：

1. 进入你的 GitHub 仓库页面：https://github.com/richard-chau/yfinance-hf
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 名称输入：`HF_TOKEN`
5. 值输入：你刚才复制的 Hugging Face 令牌
6. 点击 **Add secret**

## 验证设置

设置完成后，你可以：

1. 手动触发工作流：
   - 进入仓库的 **Actions** 标签页
   - 选择 "Data Sync to My HF" 工作流
   - 点击 **Run workflow** → **Run workflow**

2. 检查工作流运行状态：
   ```bash
   gh run list --workflow="Data Sync to My HF"
   ```

3. 查看工作流日志：
   ```bash
   gh run view <run-id> --log
   ```

## 本地开发

如果你需要在本地测试，可以在项目根目录的父目录创建 `.env` 文件：

```bash
# 在 /home/ubuntu/data/.env 文件中
HF_TOKEN=your_huggingface_token_here
```

然后运行同步脚本：

```bash
python3 sync_to_hf.py
```

或者运行设置脚本：

```bash
python3 setup_upstream.py
```

## 工作流程说明

1. **GitHub Actions 每天自动运行**（UTC 0:00，北京时间早上 8:00）
2. **从 upstream 拉取数据**：从 `bwzheng2010/yahoo-finance-data` 拉取最新数据
3. **推送到你的 HF 仓库**：推送到 `winterandchaiyun/yahoo-finance-data`
4. **GitHub 仓库只存储代码**，不存储数据集本身

## 注意事项

- ⚠️ **不要**将 `HF_TOKEN` 提交到 Git 仓库
- ⚠️ **不要**在代码中硬编码令牌
- ✅ 使用 GitHub Secrets 存储敏感信息
- ✅ 令牌过期后需要重新生成并更新
- ✅ GitHub 仓库只存储代码，数据集存储在 Hugging Face

## 故障排除

### 问题：工作流失败，提示 "HF_TOKEN 未设置"
**解决方案：** 确保在 GitHub Secrets 中正确设置了 `HF_TOKEN`

### 问题：推送失败，提示认证错误
**解决方案：** 
1. 检查 HF_TOKEN 是否正确
2. 确保令牌有 `write` 权限
3. 确保你的 Hugging Face 用户名是 `winterandchaiyun`
4. 确保 Hugging Face 仓库已创建

### 问题：LFS 文件上传失败
**解决方案：**
- 确保工作流中启用了 `lfs: true`
- 检查 Git LFS 是否正确安装：`git lfs install`
- 确保 LFS 文件已正确拉取：`git lfs pull upstream main`

### 问题：合并冲突
**解决方案：**
- 工作流使用 `-X theirs` 策略，自动以 upstream 为准
- 如果仍有问题，可以手动运行 `git reset --hard upstream/main`

## 相关链接

- [Hugging Face 令牌文档](https://huggingface.co/docs/hub/security-tokens)
- [GitHub Actions Secrets 文档](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [上游数据集](https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data)
- [你的数据集](https://huggingface.co/datasets/winterandchaiyun/yahoo-finance-data)
