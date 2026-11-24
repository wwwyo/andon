# Andon

## Story

本を読む人が、分からない概念にその場で答えを得て、読書に戻れる。

Core actions:
- 読んでいる画面で分からない言葉を選び、図と短い解説を見る — 読書のたび
- 解説を一段深くする、その場面について追加で質問する — 読書のたび
- 溜まった概念カードを見返し、自分のメモを足す — 週次
- 別の本で同じ概念に再会し、前の出会いとつながる — 月に数回

## Glossary

- **概念カード**: 1 つの概念についての解説・図・出会いの記録・自分のメモ。同じ概念は本をまたいで 1 枚にまとまる
- **出会い**: ある概念に、どの本のどの場面で出会ったかの記録。概念カードに積み重なる
- **解説**: 選んだ箇所の概念を、その場面を読むのに要る深さだけ説明したもの。概念名・図・3〜5 行の文からなる

## ディレクトリ構造

```
andon/
├── apps/
│   ├── mac/        macOS アプリ（SwiftPM。iOS を足すときは apps/ios と共有の library target を作る）
│   └── api/        Cloudflare Worker（Hono）。Claude への問い合わせの代理と概念カードの保存を持つ予定
└── docs/
    ├── prd/        機能ごとの要件・設計書（構造は prd/README.md）
    └── adr/        戻すのが難しい判断（構造は adr/README.md）
```

docs/ は共有文書として Git で管理する。個人のメモは gitignore される `.agent/` に置く。

## セットアップ

ツールは mise で管理している。Swift は Xcode ではなく Command Line Tools のものを使う。

```bash
mise install    # bun・node・swiftformat
bun install     # apps/api の依存（bunfig.toml で exact pin・公開から 7 日待つ）
```

```bash
cd apps/mac && swift build && swift run   # macOS アプリ
bun run api:dev                           # api を http://127.0.0.1:8787 で起動（workerd）
bun run check                             # api の型検査
```

- Command Line Tools だけの環境では、SDK がマクロとして提供する SwiftUI の `@State`・`#Preview` などがビルドできない（マクロの plugin が Xcode にしか無い）。状態は `@Observable` の model に持たせる
- api の deploy・本番リソースの作成・secret の登録は、ユーザーの許可を得てから行う

## 技術スタック

- apps/mac: Swift 6・SwiftUI・SwiftPM（macOS 14+）
- apps/api: TypeScript・Hono・Cloudflare Workers（`cf` CLI と `cloudflare.config.ts`）・bun

## Skills

- 機能の要件を決めるときは `prd` skill、戻すのが難しい判断は `document` skill の ADR 形式で docs/adr/ に残す
- 学び・ハマりどころ・過去の失敗は `.agents/skills/<topic>/` を参照

### 外部 skill

`skillctrl` で取り込んだ upstream のコピーで、中身は書き換えない。取得元と hash は `skills-lock.json`・`.agents/skillctrl/lock.json` が正本。更新は `skillctrl update`、Claude Code へは `.claude/skills/<name>` の相対 symlink で渡す。upstream の license は `.agents/licenses/` に置く（cloudflare/skills は Apache-2.0、honojs/skills は MIT）。

| skill | 使う場面 | 取得元（commit） |
|---|---|---|
| `cloudflare` | Cloudflare の製品選定（D1・KV・R2・AI Gateway など） | cloudflare/skills（`14472d5`） |
| `workers-best-practices` | apps/api の Worker の実装・レビュー・設定 | cloudflare/skills（`14472d5`） |
| `cf-cli` | `cf` CLI でのリソース操作・dev・build・deploy | cloudflare/skills（`14472d5`） |
| `hono` | apps/api のルーティング・middleware・validation・RPC・テスト | honojs/skills（`e54ce51`） |

- これらの skill が Wrangler や `npm install --global cf` を案内しても、この repo では `apps/api` の devDependency の `cf` を `bun run` から使い、Wrangler の設定ファイルは足さない
