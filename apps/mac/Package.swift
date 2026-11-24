// swift-tools-version: 6.0
// macOS アプリ。Xcode なし（Command Line Tools）の swift build で通す。
// iOS を足すときは、共有するコードをここの library target に切り出して apps/ios から使う。
import PackageDescription

let package = Package(
    name: "Andon",
    defaultLocalization: "ja",
    platforms: [.macOS(.v14)],
    products: [
        .executable(name: "Andon", targets: ["AndonMac"]),
    ],
    targets: [
        .executableTarget(name: "AndonMac"),
    ]
)
