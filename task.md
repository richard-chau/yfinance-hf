「請幫我完成以下任務：



編寫一個 python 腳本，使用 git clone 下載我指定的 Hugging Face 數據集，並將原始數據集設置為 upstream。

確保腳本包含 git lfs 的初始化，以處理大文件。

為該項目創建一個 GitHub Actions Workflow 文件（.yml），實現每天自動從 upstream 同步最新數據到我的倉庫。

請提示我需要在 GitHub Secrets 中添加哪些變量（如 HF_TOKEN）以及如何獲取它們。」
use token in ../.env

最后直接 push to my github using gh

数据集在这, 最后自己检查 ci 是否 work,work 了报 OK
https://huggingface.co/datasets/bwzheng2010/yahoo-finance-data
