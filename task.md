「請幫我完成以下任務：



編寫一個 python 腳本，使用 把数据集定期 push 到 hugging face，不是 github，github 只存代码。。用 gha ci下載我指定的 Hugging Face 數據集，並將原始數據集設置為 upstream。

確保腳本包含 git lfs 的初始化，以處理大文件。

為該項目創建一個 GitHub Actions Workflow 文件（.yml），實現每天自動從 upstream 同步最新數據到我的倉庫。

請提示我需要在 GitHub Secrets 中添加哪些變量（如 HF_TOKEN）以及如何獲取它們。」
use token in ../.env

最后直接 push changes to my github using gh

数据集在这, 最后自己**pull most recent ci runs from gh in commandline** you have the right tools **gh** to control remote repo and fetch remote GHA runs, 看是否 work, fix github action failed runs, work 了报 OK
https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data


這份 Workflow 寫得非常有邏輯，特別是使用了 `rsync` 來處理文件同步，這比單純的 `git merge` 更可控（尤其是在你只想單向覆蓋數據時）。

不過，針對 **Hugging Face** 的特殊機制，這份代碼有幾個隱藏的「坑」需要優化，否則在處理大文件時會報錯或同步失敗：

### 1. 核心風險：`rsync` 會弄壞 Git LFS 指針

**問題：** 當你用 `rsync` 從 `upstream-repo` 拷貝到 `target-repo` 時，你拷貝的是**已經被 Git LFS 替換過的實體文件**。

* 如果你的 `target-repo` 也是一個 Hugging Face 倉庫，當你執行 `git add .` 時，Git 會嘗試重新把這些幾 GB 的大文件再次 LFS 化，這會導致 CI 內存溢出或上傳速度極慢。
* **更好的做法：** 直接在同一個 Git 倉庫中操作兩個 `remote`，讓 Git 在指針層面完成同步。


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
