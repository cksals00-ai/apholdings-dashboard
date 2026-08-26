import SwiftUI

@main
struct SafelistApp: App {
    @StateObject private var store = AvoidStore()

    var body: some Scene {
        WindowGroup {
            RootView().environmentObject(store)
        }
    }
}

struct RootView: View {
    @EnvironmentObject var store: AvoidStore

    var body: some View {
        if store.onboarded {
            TabView {
                CheckView()
                    .tabItem { Label("확인", systemImage: "magnifyingglass") }
                AvoidListView()
                    .tabItem { Label("회피 목록", systemImage: "checklist") }
                HistoryView()
                    .tabItem { Label("기록", systemImage: "list.bullet.rectangle") }
                GuideView()
                    .tabItem { Label("안내", systemImage: "info.circle") }
            }
            .tint(Theme.accent)
        } else {
            OnboardingView()
        }
    }
}
