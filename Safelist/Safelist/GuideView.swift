import SwiftUI

/// 정보 화면. 의학적 조언이 아니라 행정 정보와 사용법만 담는다.
struct GuideView: View {
    @EnvironmentObject var store: AvoidStore

    var body: some View {
        NavigationStack {
            List {
                Section {
                    row("어디로도 전송하지 않습니다",
                        "회피 목록과 기록은 이 기기 안에만 저장됩니다. 이 앱은 서버를 운영하지 않고, 인터넷으로 아무것도 보내지 않습니다.",
                        "lock.shield")
                } header: { Text("개인정보") }

                Section {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("MD크림은 실손보험 청구가 될 수 있습니다")
                            .font(.subheadline.weight(.semibold))
                        Text("MD크림은 식약처 2등급 의료기기로 허가된 보습제로, 처방이 필요하고 건강보험은 비급여입니다. 다만 아토피 피부염 등 진단에 따른 치료 목적 처방이면 실손보험 청구가 가능한 경우가 있습니다.")
                            .font(.footnote)
                        Text("보통 필요한 서류 3가지")
                            .font(.footnote.weight(.semibold)).padding(.top, 2)
                        Text("① 진료비 영수증\n② 진료비 세부내역서\n③ 질병코드가 적힌 서류 (소견서·진단서·진료확인서 중 하나)")
                            .font(.footnote).foregroundStyle(.secondary)
                        Text("병원에서 나오기 전에 세 가지를 함께 요청하면 다시 방문하지 않아도 됩니다. 단순 보습·미용 목적은 청구 대상이 아니며, 보장 여부는 가입한 상품에 따라 다릅니다. 가입한 보험사에 확인하세요.")
                            .font(.caption).foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 4)
                } header: { Text("알아두면 좋은 것") }

                Section {
                    row("초록불은 없습니다",
                        "이 앱은 빨강(회피 항목 있음)과 회색(확인되지 않음) 두 가지만 씁니다. '발견되지 않음'과 '안전함'은 다른 말이고, 그 둘을 같은 색으로 칠하면 위험하기 때문입니다.",
                        "circle.lefthalf.filled")
                    row("표시란이 가장 정확합니다",
                        "법정 22종은 제조사가 「알레르기 유발물질」 표시란에 반드시 적어야 합니다. 그 문구까지 함께 복사하면 판정이 정확해집니다.",
                        "text.magnifyingglass")
                    row("아무것도 팔지 않습니다",
                        "이 앱은 제품을 추천하거나 판매하지 않고, 어떤 판매처와도 제휴하지 않습니다. 판단 기준은 오직 회원님이 정한 회피 목록입니다.",
                        "hand.raised")
                } header: { Text("이 앱의 원칙") }

                Section {
                    Text("이 앱은 의료기기가 아니며 진단·치료·처방을 하지 않습니다. 표시된 원재료를 대조해 보여줄 뿐이며, 제조 공정 중 혼입이나 표시 오류는 확인할 수 없습니다. 아이의 식이와 치료는 반드시 담당 의사와 상의해 결정하세요.")
                        .font(.caption).foregroundStyle(.secondary)
                } header: { Text("고지") }

                Section {
                    HStack { Text("버전"); Spacer(); Text("1.0").foregroundStyle(.secondary) }
                    HStack { Text("만든 곳"); Spacer(); Text("에이피홀딩스").foregroundStyle(.secondary) }
                } header: { Text("정보") }
            }
            .navigationTitle("안내")
        }
    }

    private func row(_ title: String, _ body: String, _ icon: String) -> some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: icon)
                .foregroundStyle(Theme.accent).frame(width: 24)
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.subheadline.weight(.semibold))
                Text(body).font(.footnote).foregroundStyle(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}
