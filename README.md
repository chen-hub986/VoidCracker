# 🛡️ VoidCracker (虛空破解者) - 資安密碼攻防系統

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
- 內建包含數千組常見弱密碼的測試字典

### 4. **暴力窮舉攻擊** (Brute Force Attack)
- 運用高階算力逐一嘗試所有可能的密碼組合
- 支援自定義最大密碼長度
- 涵蓋小寫英文字母與數字組合
- 即時顯示破解耗時 (Time taken) 和總嘗試次數 (Attempts)

## 🚀 快速開始

### 系統環境要求
- Python 3.8+
- 僅使用 Python 內建標準函式庫（`hashlib`, `string`, `itertools`, `time`, `os`），無需安裝額外套件。

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
Hash: 36f028580bb02330ee268c1d7be155c1245a6acb668d2b60245dc9d840a40f1b
```

#### 2. 生成加鹽防禦雜湊 (Salted Hash)
```
Enter your choice: 2
Enter the password to hash: mypassword
Salt: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Salted Hash: 7f8e9d0c1b2a3f4e5d6c7b8a9f0e1d2c
```

#### 3. 字典攻擊
```
Enter your choice: 3
Enter the hash to crack: 5f4dcc3b5aa765d61d8327deb882cf99
Password found: manager
```

#### 4. 暴力窮舉攻擊
```
Enter your choice: 4
Enter the hash to crack: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
Enter the maximum password length for brute-force attack: 5
Password found: pass
Attempts: 913521
Time taken: 4.23
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
    └── brute_force.py       # 暴力破解模組
```

## 🔧 模組說明

### `hash_generator.py`
提供靜態方法 `generate_hash()`，用於產生 SHA256 雜湊值。

### `dictionary_attack.py`
- `DictionaryAttack` 類別用於執行字典攻擊
- 使用指定密碼字典逐筆比對目標雜湊值
- 支援檔案不存在等例外處理

### `brute_force.py`
- `BruteForce` 類別用於執行暴力破解
- 支援小寫字母、數字與特殊符號組合
- 記錄嘗試次數與耗時

## ⚠️ 安全提醒

本工具僅供教學與經授權的安全測試使用：

- ✅ 只在自己擁有的系統或本地環境上進行測試。
- ✅ 必須獲得明確授權後，才能對目標進行安全驗證。
- ❌ 禁止用於非法入侵或未授權存取
- ❌ 禁止破解他人帳號、密碼或系統

## 📊 效能建議

- **字典攻擊**：極度快速且高效，是針對「常見弱密碼」的首選攻擊手段。
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

---

**最後更新**：2026 年 3 月 17 日
