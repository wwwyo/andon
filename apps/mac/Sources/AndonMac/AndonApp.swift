import AppKit
import SwiftUI

@main
struct AndonApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    var body: some Scene {
        WindowGroup("Andon") {
            Text("Andon")
                .font(.largeTitle)
                .frame(minWidth: 480, minHeight: 320)
        }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_: Notification) {
        // .app にまとめず swift run で起動しても、Dock に出る通常のウィンドウにする
        NSApp.setActivationPolicy(.regular)
        NSApp.activate()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_: NSApplication) -> Bool {
        true
    }
}
