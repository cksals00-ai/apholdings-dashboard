import SwiftUI

struct OnboardingView: View {
    @EnvironmentObject var store: AvoidStore
    @State private var page = 0

    var body: some View {
        VStack(spacing: 0) {
            TabView(selection: $page) {
                slide("checklist",
                      "무엇을 피할지 정하세요",
                      "알레르기 검사 결과에 나온 항목을 골라 두면 됩니다. 우유와 밀은 미리 켜 두었고, 언제든 끌 수 있습니다.")
                    .tag(0)
                slide("doc.on.clipboard",
                      "복사해서 붙여넣으세요",
                      "쇼핑몰 상품 페이지에서 「원재료명」과 「알레르기 유발물질」 부분을 복사해 붙여넣으면, 정해 두신 항목이 들어 있는지 바로 알려드립니다.")
                    .tag(1)
                slide("circle.lefthalf.filled",
                      "초록불은 만들지 않았습니다",
                      "빨강은 회피 항목이 있다는 뜻이고, 회색은 확인되지 않았다는 뜻입니다. '안전하다'고는 말하지 않습니다. 그건 저희가 할 수 있는 말이 아니기 때문입니다.")
                    .tag(2)
                slide("lock.shield",
                      "기기 밖으로 나가지 않습니다",
                      "회피 목록도 기록도 이 기기 안에만 저장됩니다. 이 앱은 서버가 없습니다.")
                    .tag(3)
            }
            .tabViewStyle(.page)

            Button {
                if page < 3 { withAnimation { page += 1 } } else { store.onboarded = true }
            } label: {
                Text(page < 3 ? "다음" : "시작하기")
                    .fontWeight(.semibold)
                    .frame(maxWidth: .infinity).padding(.vertical, 14)
            }
            .buttonStyle(.borderedProminent)
            .tint(Theme.accent)
            .padding(20)
        }
    }

    private func slide(_ icon: String, _ title: String, _ body: String) -> some View {
        VStack(spacing: 18) {
            Spacer()
            Image(systemName: icon)
                .font(.system(size: 56, weight: .light))
                .foregroundStyle(Theme.accent)
            Text(title).font(.title2.bold()).multilineTextAlignment(.center)
            Text(body)
                .font(.subheadline).foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 32)
            Spacer(); Spacer()
        }
    }
}
