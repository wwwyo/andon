# Andon

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

本を読んでいて難しい概念（たとえば SF に出てくる量子力学）に当たったとき、読んでいる画面からそのまま聞くと、図と短い解説で「その場面を読むのに要る深さだけ」教えてくれる読書アプリです。解説は概念カードとして溜まり、別の本で同じ概念に出会うと前の出会いとつながります。

名前は行灯（あんどん）から。江戸の人が夜に本を読んだ紙の灯りです。

いまは雛形の段階で、機能はまだありません。

## QuickStart

macOS で [mise](https://mise.jdx.dev/) と Command Line Tools（`xcode-select --install`）を使います。Xcode は要りません。

```bash
mise install && bun install
cd apps/mac && swift run      # 「Andon」のウィンドウが開く
```

```bash
bun run api:dev               # http://127.0.0.1:8787/health が {"ok":true} を返す
```

## License

Licensed under the [MIT license](LICENSE).
