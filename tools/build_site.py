#!/usr/bin/env python3
"""
把 repo 裡的 Markdown 轉成 GitHub Pages 靜態網站。

用法：
    pip install markdown
    python3 tools/build_site.py

產出（與 .md 並存，直接 commit）：
    index.html            首頁
    guide.html            備戰地圖（由 README.md 轉出）
    <分類>/index.html     分類索引（由該目錄 README.md 轉出）
    <分類>/<檔名>.html    各篇文件
    assets/site.css       共用樣式

新增一份 .md 之後重跑本腳本即可，不需要改這支程式。
"""
import os, re, sys, html, datetime, pathlib
import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagrams import DIAGRAMS

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_TITLE = "大學申請入學 備戰站"

# 分類目錄 → (顯示名稱, 一句話說明)
SECTIONS = [
    ("docs",      "制度與時程", "官方制度、簡章規定、學年度時程、名詞解釋"),
    ("majors",    "科系研究",   "依理工家族 A–H 分類的科系研究"),
    ("schools",   "校系比較",   "校系分則與比較表，決定志願的顆粒度"),
    ("analysis",  "落點分析",   "歷年篩選標準、落點推估、志願排序策略"),
    ("portfolio", "學習歷程",   "學習歷程檔案、備審資料、面試準備"),
]

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"])


def read_title(text, fallback):
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    return m.group(1) if m else fallback


def read_meta(text):
    """抓第一段 blockquote 當作 meta 摘要（我們的文件開頭都是 > 註記）。"""
    lines, out = text.splitlines(), []
    started = False
    for ln in lines:
        if ln.startswith("> "):
            started = True
            out.append(ln[2:].strip())
        elif started:
            break
    return out


def render_md(text):
    # 連續的 "> " 行在 Markdown 裡會併成同一段，補兩個空白讓它保留換行
    text = re.sub(r"^(> .*?)(?<! )$", r"\1  ", text, flags=re.M)
    MD.reset()
    body = MD.convert(text)
    # 內部連結 .md → .html
    body = re.sub(r'(href="[^"]*?)\.md(["#])', r"\1.html\2", body)
    # 表格加水平捲動容器
    body = re.sub(r"<table>", '<div class="scroll"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)
    # - [ ] 待辦清單
    body = body.replace("<li>[ ] ", '<li class="todo">').replace("<li>[x] ", '<li class="todo done">')
    # <!-- diagram:name --> → 內嵌 SVG
    def _dia(m):
        return DIAGRAMS.get(m.group(1), "")
    body = re.sub(r"<!--\s*diagram:([a-z0-9-]+)\s*-->", _dia, body)
    return body


def build_toc(body):
    """從 h2 建目錄。只取 h2——h3 以下會讓側欄太吵。"""
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if len(items) < 3:
        return ""
    lis = "".join(
        f'<li><a href="#{i}">{re.sub(r"<[^>]+>", "", t).strip()}</a></li>'
        for i, t in items)
    return f'<nav class="toc" aria-label="本頁目錄"><span class="tl">本頁內容</span><ol>{lis}</ol></nav>'


def insert_toc(body):
    toc = build_toc(body)
    if not toc:
        return body
    m = re.search(r"</h1>", body)
    return body[:m.end()] + toc + body[m.end():] if m else toc + body


def nav(depth, active):
    up = "../" * depth
    items = [("", "首頁", "index.html"), ("guide", "總覽", "guide.html")]
    items += [(s, n, f"{s}/index.html") for s, n, _ in SECTIONS]
    out = []
    for key, name, href in items:
        cls = ' class="on"' if key == active else ""
        out.append(f'<a{cls} href="{up}{href}">{html.escape(name)}</a>')
    return "\n      ".join(out)


def page(depth, active, title, content, subtitle="", crumb="", prevnext=""):
    up = "../" * depth
    sub = f'<p class="pagesub">{subtitle}</p>' if subtitle else ""
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}｜{SITE_TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<header class="topbar">
  <div class="bar">
    <a class="brand" href="{up}index.html">大學申請入學 <b>備戰站</b></a>
    <nav>
      {nav(depth, active)}
    </nav>
  </div>
</header>
<main class="wrap">
{crumb}
{sub}
{content}
{prevnext}
</main>
<footer class="foot">
  <p>本站資料為升學備戰整理，<strong>非官方文件</strong>。日期與規定一律以
     <a href="https://www.cac.edu.tw/">大學甄選入學委員會</a>、
     <a href="https://www.ceec.edu.tw/">大學入學考試中心</a> 公告的簡章為準。</p>
  <p class="built">網站產生時間：{datetime.date.today().isoformat()}</p>
</footer>
</body>
</html>
"""


def collect(section):
    """回傳該分類底下的文件（不含 README）。"""
    d = ROOT / section
    if not d.is_dir():
        return []
    out = []
    for f in sorted(d.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8")
        out.append({
            "file": f, "slug": f.stem, "title": read_title(text, f.stem),
            "meta": read_meta(text), "text": text,
        })
    return out


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    all_docs = {s: collect(s) for s, _, _ in SECTIONS}

    # --- 備戰地圖（README.md） ---
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    (ROOT / "guide.html").write_text(
        page(0, "guide", "總覽", insert_toc(render_md(readme)),
             "", '<nav class="crumb"><a href="index.html">首頁</a><span>›</span><span>總覽</span></nav>'),
        encoding="utf-8")

    # --- 各分類 ---
    for sec, name, desc in SECTIONS:
        d = ROOT / sec
        d.mkdir(exist_ok=True)
        idx_md = d / "README.md"
        idx_body = render_md(idx_md.read_text(encoding="utf-8")) if idx_md.exists() else f"<h1>{name}</h1>"
        cards = "".join(
            f'<a class="card" href="{doc["slug"]}.html">'
            f'<span class="ct">{html.escape(doc["title"])}</span>'
            + "".join(f'<span class="cm">{html.escape(m)}</span>' for m in doc["meta"][:2])
            + "</a>"
            for doc in all_docs[sec]
        )
        listing = f'<h2 class="lh">這個分類的文件</h2><div class="cards">{cards}</div>' if cards \
                  else '<h2 class="lh">這個分類的文件</h2><p class="empty">還沒有文件。</p>'
        crumb_cat = f'<nav class="crumb"><a href="../index.html">首頁</a><span>›</span><span>{html.escape(name)}</span></nav>'
        (d / "index.html").write_text(
            page(1, sec, name, idx_body + listing, desc, crumb_cat), encoding="utf-8")

        docs = all_docs[sec]
        for n, doc in enumerate(docs):
            crumb = (f'<nav class="crumb"><a href="../index.html">首頁</a><span>›</span>'
                     f'<a href="index.html">{html.escape(name)}</a><span>›</span>'
                     f'<span>{html.escape(doc["title"])}</span></nav>')
            links = []
            if n > 0:
                links.append(f'<a class="pn prev" href="{docs[n-1]["slug"]}.html">'
                             f'<span class="pl">上一篇</span>'
                             f'<span class="pt">{html.escape(docs[n-1]["title"])}</span></a>')
            if n < len(docs) - 1:
                links.append(f'<a class="pn next" href="{docs[n+1]["slug"]}.html">'
                             f'<span class="pl">下一篇</span>'
                             f'<span class="pt">{html.escape(docs[n+1]["title"])}</span></a>')
            pn = f'<nav class="prevnext">{"".join(links)}</nav>' if links else ""
            (d / f'{doc["slug"]}.html').write_text(
                page(1, sec, doc["title"], insert_toc(render_md(doc["text"])),
                     "", crumb, pn), encoding="utf-8")

    # --- 首頁 ---
    sec_cards = "".join(
        f'<a class="seccard" href="{sec}/index.html">'
        f'<span class="sn">{html.escape(name)}</span>'
        f'<span class="sd">{html.escape(desc)}</span>'
        f'<span class="sc">{len(all_docs[sec])} 份文件</span></a>'
        for sec, name, desc in SECTIONS
    )
    recent = sorted(
        [(sec, name, d) for sec, name, _ in SECTIONS for d in all_docs[sec]],
        key=lambda t: t[2]["slug"], reverse=True)[:6]
    recent_rows = "".join(
        f'<li><a href="{sec}/{d["slug"]}.html"><span class="rt">{html.escape(d["title"])}</span>'
        f'<span class="rc">{html.escape(name)}</span></a></li>'
        for sec, name, d in recent) or "<li class=\"empty\">還沒有文件。</li>"

    home = f"""
<section class="hero">
  <p class="eyebrow">115 學年度高一 · 目標 118 學年度申請入學 · 第二類組／電機資訊</p>
  <h1>大學申請入學 備戰站</h1>
  <p class="standfirst">簡章在哪裡拿、什麼時候拿、要挑哪些校系、現在這個學期該做什麼。
     所有整理都收在這裡，依分類存放，逐年更新。</p>
</section>

<div class="counters" id="counters">
  <div class="counter"><span class="k">本學期結束（學習歷程上傳）</span><span class="v" id="c2">—</span><span class="d">2027/01/20 前後</span></div>
  <div class="counter"><span class="k">118 招生簡章公告</span><span class="v" id="c1">—</span><span class="d">推估 2028/11</span></div>
  <div class="counter"><span class="k">你的學測（118 學年度）</span><span class="v" id="c3">—</span><span class="d">推估 2029/01</span></div>
</div>
<p class="cnote">倒數為依歷年型態<strong>推估</strong>，非官方公告日期。</p>

<section>
  <h2>年度對照</h2>
  <div class="scroll"><table>
    <thead><tr><th>年級</th><th>學年度</th><th>期間</th><th>重點</th></tr></thead>
    <tbody>
      <tr class="now"><td>高一（現在）</td><td>115</td><td>2026/9 – 2027/6</td><td>打基礎、學程式、開始累積學習歷程</td></tr>
      <tr><td>高二</td><td>116</td><td>2027/9 – 2028/6</td><td>選組（科技工程類、數 A）、考 APCS</td></tr>
      <tr><td>高三</td><td>117</td><td>2028/9 – 2029/6</td><td>簡章公告、學測、申請入學</td></tr>
      <tr><td>大一</td><td>118</td><td>2029/9 起</td><td>入學</td></tr>
    </tbody>
  </table></div>
</section>

<section>
  <h2>分類</h2>
  <div class="seccards">{sec_cards}</div>
</section>

<section>
  <h2>最近的文件</h2>
  <ul class="recent">{recent_rows}</ul>
</section>

<script>
(function(){{
  var t=[["c1","2028-11-03"],["c2","2027-01-20"],["c3","2029-01-20"]];
  var n=new Date(), t0=Date.UTC(n.getFullYear(),n.getMonth(),n.getDate());
  t.forEach(function(p){{
    var el=document.getElementById(p[0]); if(!el) return;
    var a=p[1].split("-"), t1=Date.UTC(+a[0],+a[1]-1,+a[2]);
    var d=Math.round((t1-t0)/86400000);
    el.textContent = d>0 ? d+" 天" : (d===0 ? "就是今天" : "已過");
  }});
}})();
</script>
"""
    (ROOT / "index.html").write_text(page(0, "", "首頁", home), encoding="utf-8")

    total = sum(len(v) for v in all_docs.values())
    print(f"建置完成：首頁 + 備戰地圖 + {len(SECTIONS)} 個分類 + {total} 份文件")


CSS = r"""
:root{
  --paper:#f4f6f8; --surface:#fff; --surface-2:#eef1f5;
  --ink:#16212c; --ink-2:#3b4a59; --muted:#66768a;
  --line:#d7dee6; --line-strong:#b9c4d0;
  --seal:#a8322b; --seal-soft:#f6e7e5;
  --accent:#1c5470; --accent-soft:#e2edf3; --ok:#2f6b4f;
  --serif:"Noto Serif TC",Georgia,"Songti TC",serif;
  --sans:"Noto Sans TC",-apple-system,"PingFang TC","Microsoft JhengHei",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0f151b; --surface:#161f28; --surface-2:#1c2732;
  --ink:#e7edf3; --ink-2:#bcc8d4; --muted:#8c9cad;
  --line:#26323e; --line-strong:#39485a;
  --seal:#e4796f; --seal-soft:#2b1c1b;
  --accent:#79b6d4; --accent-soft:#15252e; --ok:#7bc19b;
}}
:root[data-theme="dark"]{
  --paper:#0f151b; --surface:#161f28; --surface-2:#1c2732;
  --ink:#e7edf3; --ink-2:#bcc8d4; --muted:#8c9cad;
  --line:#26323e; --line-strong:#39485a;
  --seal:#e4796f; --seal-soft:#2b1c1b;
  --accent:#79b6d4; --accent-soft:#15252e; --ok:#7bc19b;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.78;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{color:var(--seal)}
:focus-visible{outline:2px solid var(--seal);outline-offset:2px;border-radius:2px}
img{max-width:100%}

/* 頂部導覽 */
.topbar{position:sticky;top:0;z-index:20;background:var(--surface);
  border-bottom:1px solid var(--line)}
.bar{max-width:980px;margin:0 auto;padding:12px 24px;display:flex;
  align-items:baseline;gap:22px;flex-wrap:wrap}
.brand{font-family:var(--serif);font-weight:700;font-size:16px;
  color:var(--ink);text-decoration:none;white-space:nowrap}
.brand b{color:var(--seal)}
.topbar nav{display:flex;gap:16px;flex-wrap:wrap}
.topbar nav a{font-size:13.5px;color:var(--muted);text-decoration:none;white-space:nowrap}
.topbar nav a:hover{color:var(--seal)}
.topbar nav a.on{color:var(--ink);font-weight:700;
  border-bottom:2px solid var(--seal);padding-bottom:2px}

.wrap{max-width:980px;margin:0 auto;padding:36px 24px 88px}
.pagesub{font-family:var(--mono);font-size:12px;letter-spacing:.1em;
  color:var(--muted);margin:0 0 4px}

/* 標題 */
h1{font-family:var(--serif);font-weight:900;font-size:clamp(28px,5vw,42px);
  line-height:1.2;margin:0 0 18px;text-wrap:balance}
h2{font-family:var(--serif);font-weight:700;font-size:24px;line-height:1.4;
  margin:48px 0 10px;padding-bottom:8px;border-bottom:1px solid var(--line);
  text-wrap:balance}
h3{font-family:var(--sans);font-weight:700;font-size:17px;margin:32px 0 8px}
h4{font-family:var(--sans);font-weight:700;font-size:15px;margin:24px 0 6px;color:var(--ink-2)}
p{margin:0 0 15px;max-width:68ch}
ul,ol{max-width:68ch;padding-left:1.4em}
li{margin:5px 0}
hr{border:none;border-top:3px double var(--line-strong);margin:44px 0}
strong{font-weight:700}
code{font-family:var(--mono);font-size:.9em;background:var(--surface-2);
  padding:1px 5px;border-radius:2px;word-break:break-word}
pre{background:var(--surface-2);border:1px solid var(--line);padding:16px;
  overflow-x:auto;font-family:var(--mono);font-size:13px;line-height:1.6}
pre code{background:none;padding:0}
blockquote{margin:0 0 22px;padding:14px 20px;border-left:3px solid var(--seal);
  background:var(--seal-soft)}
blockquote p{margin:0 0 8px;max-width:64ch}
blockquote p:last-child{margin:0}

/* 表格 */
.scroll{overflow-x:auto;border:1px solid var(--line);background:var(--surface);margin:0 0 22px}
table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:480px}
th,td{text-align:left;padding:11px 16px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;
  color:var(--muted);font-weight:500;background:var(--surface-2);
  border-bottom:1px solid var(--line-strong);white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tr.now td{background:var(--accent-soft);font-weight:700}

/* 待辦清單 */
li.todo{list-style:none;position:relative;padding-left:26px;color:var(--ink-2)}
li.todo::before{content:"";position:absolute;left:0;top:.55em;width:13px;height:13px;
  border:1.5px solid var(--line-strong);border-radius:2px}
li.todo.done::before{background:var(--ok);border-color:var(--ok)}

/* 首頁 */
.hero{padding:8px 0 4px}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.12em;
  color:var(--seal);margin:0 0 10px}
.standfirst{font-size:17px;color:var(--ink-2);max-width:60ch}
.counters{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);margin:28px 0 8px}
.counter{background:var(--surface);padding:18px 20px;display:flex;flex-direction:column;gap:2px}
.counter .k{font-size:13px;color:var(--muted)}
.counter .v{font-family:var(--mono);font-size:28px;font-weight:600;
  line-height:1.2;color:var(--seal);font-variant-numeric:tabular-nums}
.counter .d{font-family:var(--mono);font-size:12px;color:var(--muted)}
.cnote{font-size:13px;color:var(--muted);margin:0 0 8px}

.seccards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:18px}
.seccard{display:flex;flex-direction:column;gap:4px;padding:18px 20px;
  background:var(--surface);border:1px solid var(--line);text-decoration:none;color:inherit}
.seccard:hover{border-color:var(--seal)}
.seccard .sn{font-family:var(--serif);font-weight:700;font-size:18px}
.seccard .sd{font-size:13.5px;color:var(--muted);line-height:1.6}
.seccard .sc{font-family:var(--mono);font-size:11.5px;color:var(--seal);margin-top:4px}

.recent{list-style:none;padding:0;margin:16px 0 0}
.recent li{margin:0;border-bottom:1px solid var(--line)}
.recent a{display:flex;justify-content:space-between;align-items:baseline;gap:16px;
  padding:13px 2px;text-decoration:none;color:var(--ink)}
.recent a:hover .rt{color:var(--seal)}
.recent .rt{font-weight:500;font-size:15px}
.recent .rc{font-family:var(--mono);font-size:11px;color:var(--muted);
  border:1px solid var(--line-strong);border-radius:2px;padding:1px 7px;
  white-space:nowrap;flex:none}

/* 分類頁的文件卡 */
.lh{margin-top:44px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:16px}
.card{display:flex;flex-direction:column;gap:6px;padding:18px 20px;
  background:var(--surface);border:1px solid var(--line);
  border-left:3px solid var(--seal);text-decoration:none;color:inherit}
.card:hover{background:var(--surface-2)}
.card .ct{font-family:var(--serif);font-weight:700;font-size:16.5px;line-height:1.45}
.card .cm{font-size:12.5px;color:var(--muted);line-height:1.55}
.empty{color:var(--muted);font-size:14.5px}

/* 麵包屑 */
.crumb{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;
  font-size:12.5px;color:var(--muted);margin:0 0 20px}
.crumb a{color:var(--muted);text-decoration:none}
.crumb a:hover{color:var(--seal);text-decoration:underline}
.crumb span{opacity:.6}

/* 本頁目錄 */
.toc{border:1px solid var(--line);border-left:3px solid var(--accent);
  background:var(--surface);padding:16px 22px 18px;margin:0 0 30px}
.toc .tl{font-family:var(--mono);font-size:11px;letter-spacing:.14em;
  color:var(--muted);display:block;margin-bottom:8px}
.toc ol{margin:0;padding-left:1.5em;max-width:none;columns:2;column-gap:32px}
.toc li{margin:3px 0;font-size:14px;break-inside:avoid}
.toc a{text-decoration:none}
.toc a:hover{text-decoration:underline}
@media (max-width:620px){.toc ol{columns:1}}

/* 圖 */
.fig{margin:28px 0 30px;padding:0}
.fig svg{display:block;width:100%;height:auto;max-width:100%;
  color:var(--ink-2);overflow:visible}
.fig svg text{font-family:var(--sans);fill:currentColor}
.fig svg .t1{font-size:13px;font-weight:700}
.fig svg .t2{font-size:11.5px;opacity:.72}
.fig svg .t3{font-family:var(--mono);font-size:11px;letter-spacing:.06em;opacity:.8}
.fig svg .bx{fill:var(--surface);stroke:currentColor;stroke-width:1}
.fig svg .bx.dim{opacity:.45;stroke-dasharray:4 3}
.fig svg .ln{stroke:currentColor;stroke-width:1.3;fill:none}
.fig svg .dot{fill:currentColor;stroke:none}
.fig svg text.hot{fill:var(--seal)}
.fig svg rect.hot{stroke:var(--seal);stroke-width:1.8;fill:var(--seal-soft)}
.fig svg line.hot{stroke:var(--seal);fill:none}
.fig svg circle.hot{fill:var(--seal);stroke:none}
.fig figcaption{font-size:13px;color:var(--muted);line-height:1.7;
  max-width:68ch;margin-top:10px;border-top:1px solid var(--line);padding-top:10px}
.fig figcaption strong{color:var(--ink-2)}

/* 上下篇 */
.prevnext{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:14px;margin-top:56px;padding-top:26px;border-top:3px double var(--line-strong)}
.pn{display:flex;flex-direction:column;gap:3px;padding:14px 18px;
  background:var(--surface);border:1px solid var(--line);
  text-decoration:none;color:inherit}
.pn:hover{border-color:var(--seal)}
.pn .pl{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;color:var(--seal)}
.pn .pt{font-size:14.5px;font-weight:500;line-height:1.5}
.pn.next{text-align:right}

.foot{border-top:3px double var(--line-strong);background:var(--surface)}
.foot p{max-width:980px;margin:0 auto;padding:18px 24px 0;font-size:13px;color:var(--muted)}
.foot .built{font-family:var(--mono);font-size:11.5px;padding-bottom:28px}

@media (max-width:640px){
  .wrap{padding:26px 18px 64px}
  .bar{padding:10px 18px;gap:12px}
  .topbar nav{gap:12px}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

if __name__ == "__main__":
    main()
