# Design — Andon

Locked design system。この repo の視覚値の正本。値を変えるときはこのファイルだけを編集し、派生物（`assets/logo/` の SVG など）は再生成する。

いまは Logo だけが決まっている。色・文字・余白などの token、component、icon、motion は未制定で、UI を作る段階で設計してこのファイルに足す。

## System
- Genre · 未制定
- Theme · 未制定（ロゴで使っている色は下の Logo 節に記録してある。token として採用するかは UI の設計で決める）
- Vibe · 未制定

## Tokens

UI の token（`--background`・`--primary` など）は未制定。いま決まっているのはロゴの色だけで、`--logo-*` として宣言する。UI の token を設計するときに、ここから採るかを決める。

```css
:root {
  --logo-light: #f0a43a;   /* 灯り・wordmark の o */
  --logo-ink: #2b2420;     /* 目・本の縁・wordmark の字（ライト） */
  --logo-paper: #f6ecd8;   /* 本のページ */
  --logo-rim: #2b2420;     /* 本の縁 */
  --logo-gutter: #2b2420;  /* 本ののど */
  --logo-text: #2b2420;    /* wordmark の字 */
}
.dark {
  --logo-rim: #cbb999;
  --logo-gutter: #b3a183;
  --logo-text: #e6edf3;
}
```

## Components

未制定。

## Icons
- 未制定

## Logo
- Logomark（R2「本を読む灯り」）: 開いた本の向こうから、丸い灯りが本を読んでいる。64 × 64 の grid で、灯りは中心 (32, 36)・半径 17、目は中心 (29.4, 32.2) と (39.4, 32.2)・半径 2.7。灯りと目を (32, 46) を軸に左へ 10° 傾け、目は傾けた側と対角の右ページを見る（縦書きの本は右ページから読むため）。本は左右のページを 2 本の二次曲線で描き（左 `M6 40 Q19 34 32 40 V56 Q19 50 6 56 Z`、右はその鏡像）、縁の線幅 3・角は round、のどに線幅 2 の線を引く。目は本の縁に触れない位置に置く
  - 色: 灯り `#f0a43a`、目 `#2b2420`、ページ `#f6ecd8`。本の縁とのどはライトで `#2b2420`、ダークで縁 `#cbb999`・のど `#b3a183`（白い縁も黒い縁も暗い背景で浮くため、くすんだ紙色にした）
  - 目の光（ハイライト）は入れない
- Wordmark（「o が灯り」）: 「Andon」を Zen Maru Gothic Bold（OFL）で組み、図形に変換して固定する。2 つ目の o は灯りの色 `#f0a43a` のべた塗りの円に置き換え、中心は o の外形の中心、直径は o の外形の高さの 90%（線の字と同じ重さに見えるよう縮める）
  - 字の色: ライト `#2b2420`、ダーク `#e6edf3`
  - 字間（全体）0。ペア別の詰め（1 字の高さ = 1000 の単位）: A–n −15、n–d −5、d–● −15、●–n −15
  - 頭文字だけ大文字（Andon）。改行しない。OpenType feature は使わない
  - 記号と組むとき: 記号の高さは大文字の高さ（700）の 1.25 倍。記号と文字の間は 220。記号は、本の底が文字のベースラインにそろう位置から 80 下げ、記号の上下の中心を大文字の高さの中心にそろえる
- Usage: 記号つきの横組み（logo）を基本にし、README の見出し・アプリのウィンドウ・Web のヘッダーに使う。正方形の場所（アプリアイコン・favicon・avatar）は記号単体（symbol）。記号を置けない横長の小さい場所は文字だけ（wordmark）。最小サイズは記号単体 16px、記号つきの横組みは高さ 20px、文字だけは高さ 16px。アプリアイコンは macOS の角丸の地に記号を載せる（地の色は未制定）
- Assets: `assets/logo/` — `andon-logo.svg`・`andon-symbol.svg`・`andon-wordmark.svg` と、それぞれのダーク版 `-dark.svg`。背景は透明。clearspace は記号の目の直径 ×2 以上を四方に空ける。字形は Zen Maru Gothic から作った輪郭で、OFL の本文を `assets/logo/OFL-ZenMaruGothic.txt` に置く

## Motion
- 未制定

## Exports
- `assets/logo/*.svg` は本ファイルの Logo 節の値から `uv run tools/logo/build.py` で生成する。直接編集せず、値を変えたら `tools/logo/build.py` の定数も合わせて再生成する

## Notes
- symbol は行灯（A〜C）・本を混ぜた案（D〜H）・avatar 型（I〜M）から M を選び、目を本に向けて（M4）頭を傾けた R2 にした。左右対称の M4 より、傾きと対角の目線で「本に見入っている」姿勢が出る
- wordmark の字体は、SF Pro Rounded（ロゴに使えないライセンス）から、OFL の Nunito・M PLUS Rounded 1c・Zen Maru Gothic を比べて Zen Maru Gothic にした。字幅が狭くまとまり、手書きに近いやわらかさが灯りの丸と合う
- 字間は調整パネルの初期値のまま採用した（2026-11-27）
