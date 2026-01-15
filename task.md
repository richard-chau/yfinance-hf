「請幫我完成以下任務：



編寫一個 python 腳本，使用 把数据集定期 push 到 hugging face，不是 github，github 只存代码。。用 gha ci下載我指定的 Hugging Face 數據集，並將原始數據集設置為 upstream。

確保腳本包含 git lfs 的初始化，以處理大文件。

為該項目創建一個 GitHub Actions Workflow 文件（.yml），實現每天自動從 upstream 同步最新數據到我的倉庫。

請提示我需要在 GitHub Secrets 中添加哪些變量（如 HF_TOKEN）以及如何獲取它們。」
use token in ../.env

最后直接 push changes to my github using gh

数据集在这, 最后自己**pull most recent ci runs from gh in commandline** you have the right tools **gh** to control remote repo and fetch remote GHA runs, 看是否 work, fix github action failed runs, work 了报 OK
https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data


HF_token=>../.env
already registered to github https://github.com/richard-chau/yfinance-hf

yaml is here:

name: Data Sync to My HF

on:
  schedule:
    - cron: '0 0 * * *' # 每天北京时间早上 8 点左右运行
  workflow_dispatch:      # 允许你点击按钮手动运行

jobs:
  sync-job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          lfs: true # 开启 LFS 支持
          fetch-depth: 0

      - name: Global Config
        run: |
          git config --global user.name 'winterandchaiyun'
          git config --global user.email 'alex.zhou@example.com'
          git lfs install

      - name: Sync Data
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          # 1. 添加原作者地址 (Upstream)
          git remote add upstream https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data
          
          # 2. 添加你自己的地址 (Target)
          git remote add target https://winterandchaiyun:$HF_TOKEN@huggingface.co/datasets/winterandchaiyun/yahoo-finance-data
          
          # 3. 拉取原作者最新的数据到 GitHub 临时空间
          git fetch upstream main
          
          # 4. 合并数据，如果有冲突以原作者的为准 (-X theirs)
          git merge upstream/main -m "Auto-sync from bwzheng2010" -X theirs
          
          # 5. 把合并后的完整数据（含 LFS 大文件）推送到你自己的 HF 页面
          git push target main --force
