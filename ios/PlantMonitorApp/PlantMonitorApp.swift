import SwiftUI

@main
struct PlantMonitorApp: App {
    @StateObject private var store = ReadingsStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
                .task {
                    await store.refresh()
                }
        }
    }
}
