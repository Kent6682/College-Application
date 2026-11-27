# 專案說明給 Claude

這是一個大學申請入學的備戰資料庫，不是程式專案。

## 使用者現況（重要）

- **115 學年度入學**（2026/9 升高一）。目標升學年度是 **118 學年度**（2029/9 入學），學測在 **民國 118 年 1 月**。
- **年級依今天日期推算，不要寫死**：2026/9–2027/6 高一、2027/9–2028/6 高二、2028/9–2029/6 高三、2029/9 起大一。
- 方向：**A 家族 電機資訊類**（第二類組）。
- 因此：README 備戰地圖裡的 116 學年度時程**不是他的年度**，是範本。凡是寫日期，務必先確認是哪一屆的，並標示清楚。
- 他表示要「每年都來關注這些事情」，所以文件要寫成**可以逐年回來翻**的形式，不是一次性的懶人包。

## 每次對話產出的內容都要歸檔

使用者的長期指示：**對話產出的內容要分門別類 commit 並 push，不要只留在對話裡。**

依主題放進對應目錄：

| 目錄 | 放什麼 |
|---|---|
| `docs/` | 官方制度與簡章資料、入學管道說明、名詞解釋 |
| `majors/` | 科系研究，依理工家族 A–H 分類（家族定義見 `README.md` 第五節） |
| `schools/` | 校系分則、校系比較表 |
| `analysis/` | 落點分析、歷年篩選標準、志願排序策略 |
| `portfolio/` | 學習歷程檔案、備審資料、面試準備 |

`README.md` 是總覽（備戰地圖），只在整體結論改變時更新，不當成雜物堆。

## 網站（GitHub Pages）

這個 repo 同時是一個 GitHub Pages 網站，網站內容由 Markdown 產生。

**每次新增或修改 `.md` 之後，一定要重跑建置再 commit：**

```bash
python3 -m pip install markdown   # 第一次才需要（用 python3 -m pip，避免裝到別的 Python 版本）
python3 tools/build_site.py
```

- 產生器：`tools/build_site.py`。新增文件不需要改這支程式，它會自動掃 `docs/ majors/ schools/ analysis/ portfolio/` 底下的 `.md`。
- 產出：`index.html`、`guide.html`（由 `README.md` 轉出）、各分類的 `index.html` 與各篇 `.html`、`assets/site.css`。
- **產生的 HTML 要一起 commit**，Pages 直接吃 branch 根目錄（有 `.nojekyll`，不走 Jekyll）。
- 不要手改產生出來的 `.html`，會被下次建置覆蓋。要改樣式或版型就改 `tools/build_site.py`。
- 新增分類目錄時，在 `build_site.py` 的 `SECTIONS` 加一行，並在該目錄放一份 `README.md` 當索引。
- **流程圖**：在 Markdown 裡寫 `<!-- diagram:名稱 -->` 會插入 `tools/diagrams.py` 裡的內嵌 SVG。
  目前有 `flow-apply`（申請入學八步驟）、`funnel-sieve`（一階篩選漏斗）、
  `timeline-3y`（高一到大一時間軸）、`map-majors`（理工八家族對應學群）。
  新圖加在 `diagrams.py` 的 `DIAGRAMS`：線條文字用 `currentColor`，只有承載意義的元素加 `class="hot"`
  （由 site.css 上成強調色），深淺兩種主題都要讀得到。圖要說明機制，不是裝飾。
- 文件有 3 個以上 `##` 標題時會自動產生「本頁內容」目錄，不必手寫。

## 規則

1. 檔名用 `YYYY-MM-DD-主題.md`，方便依時間排序。
2. 新增檔案後，同步在該目錄的 `README.md` 索引表補一行。
3. 有時效性的資料（簡章版本、時程、篩選標準）在檔案開頭註明**學年度**與**整理日期**。
4. **區分已查證與推估**。沿用舊學年度資料、或屬於個人判斷的排序與建議，要明確標示，不要寫成官方定論。這一點很重要——這些資料會被用來做真實的志願決定。
5. 官方資料以這幾個來源為準：大學甄選入學委員會（cac.edu.tw）、大學入學考試中心（ceec.edu.tw）、大學招生委員會聯合會（jbcrc.edu.tw）。補習班與媒體整理只能當輔助。
6. 開發分支：`claude/intelligent-brahmagupta-fpbflt`。完成後 commit 並 push。

## 環境與網路

- **`College-Application` 雲端環境**（2026/11/27 建立）開放了四個官方網站：
  `www.cac.edu.tw`、`www.ceec.edu.tw`、`www.jbcrc.edu.tw`、`apcs.csie.ntnu.edu.tw`。
  在這個環境裡**直接用 curl 讀官方一手資料**，不要用搜尋摘要代替。
- **Default 環境**讀不到上述網站（代理回 403），只能用網頁搜尋取得二手摘要，資料要標 🟡 並提醒使用者自行核對。
- 各大學自己的校網（ntu.edu.tw 等）兩個環境都沒開放；需要時用網頁搜尋，或請使用者核對。

## 定期簡章追蹤

排程任務「大學申請簡章追蹤」在每年 **4/15、6/15、8/15、11/15**（台灣時間 10:00）於 `College-Application` 環境開新 session 執行。
它會讀官方網站、產出對應文件、在 `docs/2026-11-27-簡章追蹤紀錄.md` 的紀錄表最上面加一筆、重建網站、push。
被排程喚醒時，照排程 prompt 做；手動對話時若有新資訊，也同步更新那份追蹤紀錄。
