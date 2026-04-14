# 🛡️ VoidCracker (虛空破解者) - 資安密碼攻防系統

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-CLI%20Tool-success)
![Style](https://img.shields.io/badge/Style-OOP-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

一個用 Python 物件導向架構 (OOP) 編寫的密碼安全測試專案，提供多種密碼破解與防禦驗證方法，包含標準雜湊生成、加鹽防禦機制、字典攻擊和暴力窮舉功能。

## 📋 功能特性

### 1. **標準雜湊生成** (Generate Hash)
- 使用 SHA-256 演算法生成密碼的雜湊值 (Hash)
- 快速生成單個密碼的數位指紋

### 2. **加鹽雜湊防禦** (Generate Salted Hash)
- 結合 16 Bytes 隨機鹽值 (Salt) 與 SHA-256 演算法
- 大幅提升密碼安全性，有效防禦彩虹表與字典攻擊

### 3. **字典攻擊** (Dictionary Attack)
- 讀取預先定義的密碼字典檔進行碰撞比對
- 適合快速破解常見的弱密碼
- 內建密碼變形機制（大小寫、替換字元、常見前後綴）
- 使用 `ProcessPoolExecutor` 進行平行比對，找到答案後會提早停止未完成工作

### 4. **暴力窮舉攻擊** (Brute Force Attack)
- 逐一嘗試所有可能的密碼組合
- 支援自定義最大密碼長度
- 涵蓋小寫英文字母、數字與符號組合
- 使用 `ProcessPoolExecutor` 批次平行運算，降低單筆提交開銷
- 即時顯示破解耗時 (Time taken) 和總嘗試次數 (Attempts)

## 🚀 快速開始

### 系統環境要求
- Python 3.10+
- 僅使用 Python 內建標準函式庫（如 `hashlib`, `os`, `time`, `string`, `itertools`, `concurrent.futures`, `sys`），無需安裝額外套件。

### 安裝與執行

```bash
# 複製 (Clone) 或下載本專案
git clone https://github.com/chen-hub986/VoidCracker.git
cd VoidCracker

# 直接運行主程式
python main.py
```
## 📖 使用方式

執行程式後會顯示選單，選擇對應功能：

```
Password Cracking Tool
1. Generate Hash
2. Generate salted Hash
3. Dictionary Attack
4. Brute Force Attack
5. Exit
```

### 操作範例

#### 1. 生成標準雜湊 (Hash)
```
Enter your choice: 1
Enter the password to hash: mypassword
Hash: 89e01536ac207279409d4de1e5253e01f4a1769e696db0d6062ca9b8f56767c8
```

#### 2. 生成加鹽防禦雜湊 (Salted Hash)
```
Enter your choice: 2
Enter the password to hash: mypassword
Salt: a1b2c3d4e5f60718293a4b5c6d7e8f90
Salted Hash: ef3e405dc8e91211f9226b58749d63eb7c0a15f2b38512c98d3197b172a6e0cb
```

#### 3. 字典攻擊
```
Enter your choice: 3
Enter the hash to crack: 6ee4a469cd4e91053847f5d3fcb61dbcc91e8f0ef10be7748da4c4a1ba382d17
Password found: manager
```

#### 4. 暴力窮舉攻擊
```
Enter your choice: 4
Enter the hash to crack: d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1
Enter the maximum password length for brute-force attack: 4
Password found: pass
Attempts: 5036847
Time taken: (依電腦效能不同)
```

## 📁 專案結構

```
security_tools/
├── main.py                  # 主程式入口
├── passwords.txt            # 密碼字典
├── README.md                # 專案說明文件
└── src/
    ├── hash_generator.py    # Hash 產生模組
    ├── dictionary_attack.py # 字典攻擊模組
    ├── mutation_engine.py   # 密碼變形模組
    ├── brute_force.py       # 暴力破解模組
    └── executor_utils.py    # Executor 共用工具模組
```

## 🔧 模組說明

### `hash_generator.py`
提供靜態方法 `generate_hash()`，用於產生 SHA256 雜湊值。

### `dictionary_attack.py`
- `DictionaryAttack` 類別用於執行字典攻擊
- 使用指定密碼字典與密碼變形結果逐筆比對目標雜湊值
- 以 `ProcessPoolExecutor` 進行平行比對並支援提早停止
- 支援檔案不存在等例外處理

### `mutation_engine.py`
- `MutationEngine` 類別用於產生密碼變形清單
- 包含大小寫轉換、替換字元與常見前後綴規則

### `brute_force.py`
- `BruteForce` 類別用於執行暴力破解
- 支援小寫字母、數字與特殊符號組合
- 使用批次任務搭配 `ProcessPoolExecutor`，並記錄嘗試次數與耗時

### `executor_utils.py`
- 提供共用的 executor 停止工具函式
- 統一處理 pending 工作取消與提早 shutdown

## ⚠️ 安全提醒

本工具僅供教學與經授權的安全測試使用：

- ✅ 只在自己擁有的系統或本地環境上進行測試。
- ✅ 必須獲得明確授權後，才能對目標進行安全驗證。
- ❌ 禁止用於非法入侵或未授權存取
- ❌ 禁止破解他人帳號、密碼或系統

## 📊 效能建議

- **字典攻擊**：通常比暴力破解更快，適合先測試常見弱密碼。
- **暴力破解**：運算成本呈指數級增長，受限於 CPU 算力，建議測試長度不超過 6 位數。
  - 5 碼：時間成本中等
  - 6 碼以上：時間成本會明顯上升

## 🐛 已知限制

- 暴力破解面對高強度長密碼時，運算耗時過長（這也反向證明了密碼長度的重要性）。
- 字典攻擊完全依賴預先準備的密碼清單品質。
- 目前僅支援 SHA256

## 📝 使用授權

本專案僅供教育與學習用途。

## 🤝 貢獻方式

歡迎提出 Issue 或提交 Pull Request！

## LICENSE
MIT License

---

**最後更新**：2026-03-19
