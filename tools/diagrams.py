# -*- coding: utf-8 -*-
"""網站用的內嵌 SVG 圖。每張圖回答一個問題，不是裝飾。

慣例：線條與文字用 currentColor 繼承主題前景色；只有承載意義的元素用強調色
（--seal，透過 class="hot" 由 site.css 上色），淺色與深色主題都讀得到。
"""

FLOW_APPLY = '''
<figure class="fig">
<svg viewBox="0 0 920 250" role="img" width="920" height="250"
     aria-label="申請入學八個步驟的流程：學測成績公布後報名最多六個校系，第一階段只用學測成績篩選且通過率達八成四，接著準備備審資料進入第二階段甄試，這一關才是真正的淘汰點，最後公告正備取、登記就讀志願序、統一分發。">
  <defs>
    <marker id="ar-flow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- row 1 -->
  <rect x="8"   y="34" width="150" height="52" rx="3" class="bx"/>
  <text x="83"  y="56" text-anchor="middle" class="t1">學測成績公布</text>
  <text x="83"  y="74" text-anchor="middle" class="t2">2/25</text>

  <rect x="198" y="34" width="150" height="52" rx="3" class="bx"/>
  <text x="273" y="56" text-anchor="middle" class="t1">報名</text>
  <text x="273" y="74" text-anchor="middle" class="t2">最多 6 個校系</text>

  <rect x="388" y="34" width="150" height="52" rx="3" class="bx"/>
  <text x="463" y="56" text-anchor="middle" class="t1">第一階段篩選</text>
  <text x="463" y="74" text-anchor="middle" class="t2">只看學測成績</text>

  <rect x="578" y="34" width="150" height="52" rx="3" class="bx"/>
  <text x="653" y="56" text-anchor="middle" class="t1">備審與學習歷程</text>
  <text x="653" y="74" text-anchor="middle" class="t2">4 月</text>

  <line x1="160" y1="60" x2="194" y2="60" class="ln" marker-end="url(#ar-flow)"/>
  <line x1="350" y1="60" x2="384" y2="60" class="ln" marker-end="url(#ar-flow)"/>
  <line x1="540" y1="60" x2="574" y2="60" class="ln" marker-end="url(#ar-flow)"/>
  <text x="463" y="24" text-anchor="middle" class="t3">84.2% 通過</text>

  <!-- wrap down -->
  <path d="M 730 60 L 760 60 L 760 125 L 100 125 L 100 152" class="ln" fill="none"
        marker-end="url(#ar-flow)"/>

  <!-- row 2 -->
  <rect x="8"   y="158" width="176" height="56" rx="3" class="bx hot"/>
  <text x="96"  y="181" text-anchor="middle" class="t1 hot">第二階段甄試</text>
  <text x="96"  y="199" text-anchor="middle" class="t2 hot">筆試・面試・書審</text>

  <rect x="240" y="160" width="150" height="52" rx="3" class="bx"/>
  <text x="315" y="182" text-anchor="middle" class="t1">公告正取備取</text>
  <text x="315" y="200" text-anchor="middle" class="t2">5 月下旬</text>

  <rect x="446" y="160" width="160" height="52" rx="3" class="bx"/>
  <text x="526" y="182" text-anchor="middle" class="t1">登記就讀志願序</text>
  <text x="526" y="200" text-anchor="middle" class="t2">不登記等於放棄</text>

  <rect x="662" y="160" width="150" height="52" rx="3" class="bx"/>
  <text x="737" y="182" text-anchor="middle" class="t1">統一分發放榜</text>
  <text x="737" y="200" text-anchor="middle" class="t2">6/11</text>

  <line x1="186" y1="186" x2="236" y2="186" class="ln" marker-end="url(#ar-flow)"/>
  <line x1="392" y1="186" x2="442" y2="186" class="ln" marker-end="url(#ar-flow)"/>
  <line x1="608" y1="186" x2="658" y2="186" class="ln" marker-end="url(#ar-flow)"/>
  <text x="96" y="238" text-anchor="middle" class="t3 hot">真正的淘汰點</text>
</svg>
<figcaption>申請入學八個步驟。第一階段有 84.2% 的人通過，所以淘汰實際發生在第二階段甄試——頂大電資的二階多含數學筆試。日期為 115 學年度實際日期，你的 118 學年度加 2 年。</figcaption>
</figure>
'''

FUNNEL_SIEVE = '''
<figure class="fig">
<svg viewBox="0 0 760 320" role="img" width="760" height="320"
     aria-label="以台大資工為例的一階篩選漏斗：先用檢定門檻淘汰未達英文前標、數學A頂標、自然前標的人，再依序用英文五倍篩到二百八十五人、數學A三倍篩到一百七十一人、自然五倍不再作用，最後取五十七個名額。倍率最小的數學A是真正的決勝科。">
  <defs>
    <marker id="ar-fun" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <text x="0" y="16" class="t3">台大資工・名額 57 人</text>

  <rect x="0"   y="34"  width="600" height="40" rx="3" class="bx"/>
  <text x="14"  y="59"  class="t1">所有報名者</text>
  <text x="586" y="59"  text-anchor="end" class="t2">檢定：英文前標・數學A頂標・自然前標</text>

  <rect x="60"  y="96"  width="480" height="40" rx="3" class="bx"/>
  <text x="74"  y="121" class="t1">英文 5 倍</text>
  <text x="526" y="121" text-anchor="end" class="t2">57 × 5 ＝ 285 人</text>

  <rect x="150" y="158" width="300" height="44" rx="3" class="bx hot"/>
  <text x="164" y="184" class="t1 hot">數學 A 3 倍</text>
  <text x="436" y="184" text-anchor="end" class="t2 hot">57 × 3 ＝ 171 人</text>

  <rect x="150" y="224" width="300" height="40" rx="3" class="bx dim"/>
  <text x="164" y="249" class="t1">自然 5 倍</text>
  <text x="436" y="249" text-anchor="end" class="t2">285 人・已少於此數，不作用</text>

  <line x1="300" y1="76"  x2="300" y2="92"  class="ln" marker-end="url(#ar-fun)"/>
  <line x1="300" y1="138" x2="300" y2="154" class="ln" marker-end="url(#ar-fun)"/>
  <line x1="300" y1="204" x2="300" y2="220" class="ln" marker-end="url(#ar-fun)"/>
  <line x1="300" y1="266" x2="300" y2="286" class="ln" marker-end="url(#ar-fun)"/>

  <text x="300" y="304" text-anchor="middle" class="t1">進入第二階段甄試</text>
  <text x="620" y="184" class="t3 hot">倍率最小</text>
  <text x="620" y="202" class="t3 hot">＝真正的決勝科</text>
</svg>
<figcaption>一階篩選漏斗，用台大資工 115 學年度的真實數字。檢定是門檻（任一科沒到直接出局），篩選倍率決定誰進二階——<strong>倍率最小的科目才是決勝科</strong>。同分到邊界會超額篩選，實際進二階人數常多於名額乘倍率。</figcaption>
</figure>
'''

TIMELINE_3Y = '''
<figure class="fig">
<svg viewBox="0 0 900 260" role="img" width="900" height="260"
     aria-label="高一到大一的三年時間軸：高一是115學年度，打基礎並開始累積學習歷程；高二是116學年度，選組選科技工程類與數學A，並考APCS；高三是117學年度，11月簡章公告，118年1月學測，3到6月申請入學；118學年度9月入學。">
  <defs>
    <marker id="ar-tl" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <line x1="20" y1="120" x2="862" y2="120" class="ln" marker-end="url(#ar-tl)"/>

  <!-- ticks -->
  <line x1="90"  y1="110" x2="90"  y2="130" class="ln"/>
  <line x1="300" y1="110" x2="300" y2="130" class="ln"/>
  <line x1="510" y1="110" x2="510" y2="130" class="ln"/>
  <line x1="760" y1="110" x2="760" y2="130" class="ln"/>

  <circle cx="90" cy="120" r="6" class="dot hot"/>
  <text x="90"  y="152" text-anchor="middle" class="t1 hot">高一・115</text>
  <text x="90"  y="170" text-anchor="middle" class="t2">你在這裡</text>
  <text x="90"  y="188" text-anchor="middle" class="t2">2026/9 起</text>
  <text x="90"  y="96"  text-anchor="middle" class="t2">學程式・顧學習歷程</text>

  <circle cx="300" cy="120" r="5" class="dot"/>
  <text x="300" y="152" text-anchor="middle" class="t1">高二・116</text>
  <text x="300" y="170" text-anchor="middle" class="t2">2027/9 起</text>
  <text x="300" y="86"  text-anchor="middle" class="t2">選組：科技工程類・數 A</text>
  <text x="300" y="104" text-anchor="middle" class="t2">考 APCS</text>

  <circle cx="510" cy="120" r="5" class="dot"/>
  <text x="510" y="152" text-anchor="middle" class="t1">高三・117</text>
  <text x="510" y="170" text-anchor="middle" class="t2">2028/9 起</text>
  <text x="510" y="96"  text-anchor="middle" class="t2">117/11 簡章公告</text>

  <circle cx="760" cy="120" r="5" class="dot"/>
  <text x="760" y="152" text-anchor="middle" class="t1">大一・118</text>
  <text x="760" y="170" text-anchor="middle" class="t2">2029/9 入學</text>

  <!-- exam marker between 高三 and 大一 -->
  <line x1="600" y1="120" x2="600" y2="60" class="ln hot"/>
  <circle cx="600" cy="120" r="5" class="dot hot"/>
  <text x="600" y="48" text-anchor="middle" class="t1 hot">118/1 學測</text>
  <text x="600" y="30" text-anchor="middle" class="t2 hot">西元 2029/1</text>

  <line x1="672" y1="120" x2="672" y2="200" class="ln"/>
  <circle cx="672" cy="120" r="5" class="dot"/>
  <text x="672" y="218" text-anchor="middle" class="t1">118/3–6 申請入學</text>

  <text x="20" y="240" class="t3">距離學測約 850 天——足夠把數學練到能應付大學自辦筆試，也剛好只夠。</text>
</svg>
<figcaption>你的三年時間軸。學測在民國 118 年 1 月（西元 2029 年 1 月），簡章在 117 年 11 月公告。高二的選組與 APCS 是承先啟後的一年。</figcaption>
</figure>
'''

MAP_MAJORS = '''
<figure class="fig">
<svg viewBox="0 0 880 300" role="img" width="880" height="300"
     aria-label="八個理工家族對應到教育部ColleGo的四個學群：資訊學群含A電機資訊類；工程學群含B機械與航太、C土木環境建築、D化工與材料、H工業工程與不分系；數理化學群含E數理基礎科學、F生醫工程與生命科學；地球環境學群含G地球與環境科學。A電機資訊類是目前選定的方向。">
  <defs>
    <marker id="ar-map" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <rect x="352" y="8" width="176" height="38" rx="3" class="bx"/>
  <text x="440" y="32" text-anchor="middle" class="t1">理工（第二類組）</text>

  <line x1="440" y1="48" x2="440" y2="66" class="ln"/>
  <line x1="110" y1="66" x2="770" y2="66" class="ln"/>

  <line x1="110" y1="66" x2="110" y2="86" class="ln" marker-end="url(#ar-map)"/>
  <line x1="360" y1="66" x2="360" y2="86" class="ln" marker-end="url(#ar-map)"/>
  <line x1="590" y1="66" x2="590" y2="86" class="ln" marker-end="url(#ar-map)"/>
  <line x1="770" y1="66" x2="770" y2="86" class="ln" marker-end="url(#ar-map)"/>

  <text x="110" y="104" text-anchor="middle" class="t3">資訊學群</text>
  <text x="360" y="104" text-anchor="middle" class="t3">工程學群</text>
  <text x="590" y="104" text-anchor="middle" class="t3">數理化學群</text>
  <text x="770" y="104" text-anchor="middle" class="t3">地球環境學群</text>

  <rect x="20"  y="120" width="180" height="46" rx="3" class="bx hot"/>
  <text x="110" y="140" text-anchor="middle" class="t1 hot">A 電機資訊類</text>
  <text x="110" y="158" text-anchor="middle" class="t2 hot">← 你選的方向</text>

  <rect x="232" y="120" width="128" height="40" rx="3" class="bx"/>
  <text x="296" y="145" text-anchor="middle" class="t1">B 機械與航太</text>
  <rect x="372" y="120" width="128" height="40" rx="3" class="bx"/>
  <text x="436" y="145" text-anchor="middle" class="t1">C 土木環境</text>
  <rect x="232" y="172" width="128" height="40" rx="3" class="bx"/>
  <text x="296" y="197" text-anchor="middle" class="t1">D 化工與材料</text>
  <rect x="372" y="172" width="128" height="40" rx="3" class="bx"/>
  <text x="436" y="197" text-anchor="middle" class="t1">H 工管・不分系</text>

  <rect x="522" y="120" width="136" height="40" rx="3" class="bx"/>
  <text x="590" y="145" text-anchor="middle" class="t1">E 數理基礎</text>
  <rect x="522" y="172" width="136" height="40" rx="3" class="bx"/>
  <text x="590" y="197" text-anchor="middle" class="t1">F 生醫工程</text>

  <rect x="690" y="120" width="160" height="40" rx="3" class="bx"/>
  <text x="770" y="145" text-anchor="middle" class="t1">G 地球與環境</text>

  <text x="20" y="250" class="t3">所有家族的共同必修：數學 A ＋ 自然 ＋ 英文。國文只有部分校系採計。</text>
  <text x="20" y="274" class="t3">學群分類依教育部 ColleGo! 選才育才輔助系統。</text>
</svg>
<figcaption>八個理工家族對應到 ColleGo! 的四個學群。分類不是自創的——這是大學招生端實際使用的分類，查校系、查學習準備建議方向時都用得到。</figcaption>
</figure>
'''

DIAGRAMS = {
    "flow-apply": FLOW_APPLY,
    "funnel-sieve": FUNNEL_SIEVE,
    "timeline-3y": TIMELINE_3Y,
    "map-majors": MAP_MAJORS,
}
