# 🏥 學習病歷產生器 v2

將門診紀錄、急診紀錄或標準化病人腳本，轉換為結構化學習病歷，並提供臨床學習重點與 AI 即時問答。

---

## 🆕 本版新增功能（v2）

| 新功能 | 說明 |
|--------|------|
| 🚪 **入院來源切換** | 急診入院 / 門診入院兩種模式，影響 PI 整體架構 |
| 🩸 **檢驗分三欄輸入** | 血液檢驗 / 生化檢驗 / 其他檢驗分類貼入，AI 分類整合 |
| 🩺 **會診 Impression 優先** | ER 紀錄若含會診回覆，自動採納會診 Impression 為主診斷 |
| 📋 **會診建議無縫整入 Plan** | 不再標示「Per X consult:」，直接融入 Plan 成為統一管理計畫 |
| 💊 **抗生素縮排格式** | 主診斷下方換行縮排：`   Tazocin (2026/04/22-)` |
| 📄 **過去出院診斷保留原樣式** | 貼入內容原封不動放入 Past History，同時摘要至 PI 與 Impression |
| 🤖 **模型自動偵測** | 輸入 API key 後自動查詢並選用最新旗艦模型，不再寫死版本 |
| 🎨 **莫蘭迪色系 UI** | 全新霧霾藍 × 鼠尾草綠 × 奶油米配色，視覺更柔和 |

---

## 功能總覽

| 功能 | 說明 |
|------|------|
| 📝 **學習病歷** | 根據輸入資料產生完整住院病歷（Chief Complaint → Plan） |
| 🚪 **急診 / 門診模式** | 急診寫 ER course（At triage + vital signs）；門診寫 OPD course（主訴 → 檢查 → 住院原因） |
| 🔪 **內科 / 外科模式** | 內科敘述式、外科出院病摘式，一鍵切換 |
| 🎂⚧ **年齡 / 性別輸入** | 明確指定或自動推斷，影響 PI 首句、代名詞、ROS 性別篩選 |
| 🩸🧪🔬 **三類檢驗輸入** | 血液 / 生化 / 其他各自貼入，分類整合至 PI |
| 📄 **過去出院診斷** | 原樣保留，同時摘要至 PI 首句與 Impression Underlying status |
| 🩺 **會診回覆處理** | Impression 採納會診診斷；Plan 整合會診建議（無來源標籤） |
| 💊 **抗生素縮排標示** | 感染診斷下方縮排顯示抗生素名稱與開始日期 |
| 🧩 **分段卡片** | 病歷拆為 8 個獨立區塊，各自獨立顯示 |
| 📋 **一鍵複製** | 每個區塊都有複製按鈕 |
| 🔄 **單段重生 (Redo)** | 不滿意某段？只重新生成該段，其餘不動 |
| 📏 **精簡版** | Present Illness、Impression、Plan 可切換精簡或完整版本 |
| 🔴 **紅字標示** | ROS 與 PE 更動項目自動紅色字體 |
| ✳️ **ROS 異常提示** | ROS 有異常的項目以 `*` 紅字標示 |
| 📚 **臨床學習重點** | 按需生成，含 DDx、藥物、Guideline、EBM、AI 查核 |
| 💬 **AI 問答** | 根據病歷內容即時提問，支援多輪對話 |
| 🤖 **多模型支援** | Claude / OpenAI / Gemini，自動偵測並使用最新版本 |
| 🛡️ **去識別化** | 自動遮蔽姓名、身分證字號、電話號碼 |

---

## 安裝與執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 使用方式

1. 左側欄輸入 API Key（任一即可）
2. 系統自動偵測並顯示選用的最新模型
3. 選擇入院來源（🚑 急診 / 🏥 門診）
4. 填寫左側面板：

| 欄位 | 說明 |
|------|------|
| 🎂 年齡 | 整數，留空則自動推斷 |
| ⚧ 性別 | male / female / 自動推斷 |
| 📋 主要資料 | 門診紀錄 / 急診紀錄 / SP 腳本（含會診回覆亦可） |
| 🩸 血液檢驗 | CBC、DC、凝血功能等（選填） |
| 🧪 生化檢驗 | 肝腎功能、電解質、CRP、心臟標記等（選填） |
| 🔬 其他檢驗 | 尿液、微生物培養、EKG、影像、病理等（選填） |
| 📄 過去出院診斷 | 過去出院或 ER 診斷（選填，原樣保留） |
| 📝 補充資料 | 額外問診結果、病史（選填，PI 中藍字標示） |

5. 按「🩺 產生學習病歷」（內科）或「🔪 產生外科病歷」

---

## 急診 vs 門診 模式差異

| 項目 | 🚑 急診入院 | 🏥 門診入院 |
|------|-----------|-----------|
| PI 結構 | At triage → vital signs → ER course → admission | 主訴 → 症狀 → OPD 檢查 → 建議住院 |
| Vital signs 格式 | `T:XX.X P:XX R:XX SBP:XXX DBP:XX E:X V:X M:X SPO2:XX%` | OPD 僅記錄若有提供，不寫 GCS |
| 結尾 | `admitted for further management` | `admitted from the OPD for further management` |

## 內科 vs 外科 模式差異

| 項目 | 🩺 內科模式 | 🔪 外科模式 |
|------|-----------|-----------|
| PI 風格 | 敘述式段落 | 出院病摘式（條列式 underlying + 敘述主體） |
| Lab 描述 | 異常值列述 | 僅寫有臨床意義的異常 |

---

## 會診回覆處理方式

若急診紀錄（或補充資料）中有會診回覆（會診/Consult/Consultation reply）：

- **Impression**：採納會診 Impression 為主診斷（不用 AI 自行推斷蓋過會診意見）
- **Plan**：會診建議直接整入 Plan，**不加** `Per [Specialty] consult:` 等來源標籤，呈現統一管理計畫

---

## 過去出院診斷保留方式

| 放置位置 | 處理方式 |
|---------|---------|
| 過去病史 (Past History) | **原樣**保留，逐字逐行不更動 |
| PI 首句「underlying disease of:」 | **摘要**（不逐字抄） |
| Impression `<Underlying status>` | **摘要**（不逐字抄） |

---

## 抗生素格式示例

```
 - Community-acquired pneumonia, r/o aspiration pneumonia
   Ceftriaxone (2026/04/22-)
   Azithromycin (2026/04/22-)
 - Acute kidney injury on CKD stage 3 (eGFR 35)
```

---

## 自動模型偵測說明

輸入 API Key 後，系統會：

1. 查詢 provider 的 models API（Anthropic: `models.list`、OpenAI: `models.list`、Gemini: `list_models`）
2. 依照旗艦等級 + 版本號排序，自動選出最新可用模型
3. 在側欄顯示選用的模型 ID
4. 提供「🔄 重新偵測」按鈕，強制更新（當 AI 廠商推出新版本時）

Fallback（查詢失敗時）：`claude-opus-4-5` / `gpt-4o` / `gemini-2.0-flash`

---

## 色彩標示說明

| 標記 | 說明 |
|------|------|
| 🔴 紅色 | ROS / PE 更動項目 |
| `*` 紅色 | ROS 異常項目前方提示（例：`*yes`） |
| 🔵 藍色 | 補充資料內容（僅 Present Illness） |
| 深褐紅縮排 | Impression 中的抗生素名稱與日期 |

---

## 支援模型（自動偵測，不限版本）

| Provider | API Key 類型 | 排序邏輯 |
|----------|------------|---------|
| Claude | Anthropic API Key | opus > sonnet > haiku；最新日期優先 |
| GPT | OpenAI API Key | gpt-5 > o4 > o3 > gpt-4o > gpt-4；mini/nano 略降權 |
| Gemini | Google AI API Key | 版本號 + pro > flash；stable alias 優先 |

---

## 部署

上傳 `app.py` + `requirements.txt` 至 GitHub → [share.streamlit.io](https://share.streamlit.io)

---

## 免責聲明

⚠️ 本工具**僅供醫學教育與學習用途**，不應用於真實臨床診療決策。  
使用者需自行判斷生成內容之正確性，並承擔 API token 消耗之相關費用。
