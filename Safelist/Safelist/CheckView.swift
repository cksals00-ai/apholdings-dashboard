import SwiftUI

/// 이 앱의 심장. 붙여넣은 텍스트를 3초 안에 판정한다.
struct CheckView: View {
    @EnvironmentObject var store: AvoidStore
    @State private var text = ""
    @State private var result: Analysis?
    @State private var productName = ""
    @State private var saved = false
    @FocusState private var focused: Bool

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 16) {
                    inputCard
                    if let result { resultCard(result) }
                    helpCard
                }
                .padding(16)
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("성분 확인")
            .scrollDismissesKeyboard(.interactively)
        }
    }

    // MARK: 입력

    private var inputCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("원재료명·알레르기 표시를 붙여넣으세요")
                .font(.subheadline.weight(.semibold))

            TextEditor(text: $text)
                .frame(minHeight: 120)
                .focused($focused)
                .scrollContentBackground(.hidden)
                .padding(8)
                .background(Color(.tertiarySystemBackground))
                .clipShape(RoundedRectangle(cornerRadius: 10))
                .overlay(alignment: .topLeading) {
                    if text.isEmpty {
                        Text("쇼핑몰 상품 페이지에서 원재료명 부분을 길게 눌러 복사한 뒤, 여기에 붙여넣으세요.")
                            .font(.footnote)
                            .foregroundStyle(.tertiary)
                            .padding(.horizontal, 13).padding(.vertical, 16)
                            .allowsHitTesting(false)
                    }
                }

            HStack(spacing: 10) {
                PasteButton(payloadType: String.self) { items in
                    if let s = items.first { text = s; run() }
                }
                .labelStyle(.titleAndIcon)
                .buttonBorderShape(.capsule)

                Spacer()

                if !text.isEmpty {
                    Button("지우기") { text = ""; result = nil; saved = false }
                        .font(.subheadline)
                }

                Button {
                    focused = false
                    run()
                } label: {
                    Text("확인하기").fontWeight(.semibold)
                        .padding(.horizontal, 14).padding(.vertical, 8)
                }
                .buttonStyle(.borderedProminent)
                .tint(Theme.accent)
                .disabled(text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
            }
        }
        .padding(16)
        .background(Theme.card)
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }

    // MARK: 결과

    @ViewBuilder
    private func resultCard(_ r: Analysis) -> some View {
        VStack(alignment: .leading, spacing: 14) {

            HStack(spacing: 12) {
                Circle()
                    .fill(r.verdict == .hit ? Theme.hit : Theme.unknown)
                    .frame(width: 22, height: 22)
                VStack(alignment: .leading, spacing: 2) {
                    Text(headline(r)).font(.headline)
                    Text(subhead(r)).font(.footnote).foregroundStyle(.secondary)
                }
            }

            if !r.findings.isEmpty {
                Divider()
                VStack(alignment: .leading, spacing: 8) {
                    ForEach(r.findings) { f in
                        HStack(alignment: .firstTextBaseline, spacing: 8) {
                            Text("•").foregroundStyle(Theme.hit)
                            VStack(alignment: .leading, spacing: 2) {
                                Text(f.allergen.name).font(.subheadline.weight(.semibold))
                                Text(f.fromBox
                                     ? String(localized: "알레르기 표시란에서 확인 · '\(f.matched)'")
                                     : String(localized: "원재료명에서 확인 · '\(f.matched)'"))
                                    .font(.caption).foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }

            if r.gelatinAmbiguous {
                notice("젤라틴이 들어 있는데 원료(돼지·소·어류)가 표기되지 않았습니다. 제조사 확인이 필요합니다.")
            }
            if r.crossContact != nil {
                notice("같은 제조시설에서 다른 알레르기 유발물질을 다룬다는 문구가 있습니다.")
            }

            Divider()
            Text("표시된 원재료 기준입니다. 제조 공정 중 혼입은 확인할 수 없습니다.\n최종 판단은 포장의 표시사항과 담당 의사에게 확인하세요.")
                .font(.caption2).foregroundStyle(.secondary)

            // 저장
            if saved {
                Label("기록에 저장했습니다", systemImage: "checkmark.circle.fill")
                    .font(.subheadline).foregroundStyle(Theme.accent)
            } else {
                HStack(spacing: 8) {
                    TextField("제품 이름 (선택)", text: $productName)
                        .textFieldStyle(.roundedBorder)
                    Button("기록") { save(r) }
                        .buttonStyle(.bordered)
                }
            }
        }
        .padding(16)
        .background(Theme.card)
        .clipShape(RoundedRectangle(cornerRadius: 14))
        .overlay(
            RoundedRectangle(cornerRadius: 14)
                .stroke(r.verdict == .hit ? Theme.hit.opacity(0.4) : Color.clear, lineWidth: 1.5)
        )
    }

    private func notice(_ s: String) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundStyle(.orange).font(.footnote)
            Text(s).font(.footnote)
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.orange.opacity(0.12))
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    private var helpCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label("이렇게 쓰세요", systemImage: "lightbulb")
                .font(.subheadline.weight(.semibold))
            Text("1. 쿠팡·네이버 등에서 상품 상세를 엽니다\n2. 「원재료명」과 「알레르기 유발물질」 부분을 길게 눌러 선택하고 복사합니다\n3. 이 앱에 붙여넣고 확인합니다")
                .font(.footnote).foregroundStyle(.secondary)
            Text("표시란이 없거나 이미지로만 되어 있으면 판정할 수 없습니다. 그때는 회색으로 표시됩니다.")
                .font(.caption).foregroundStyle(.tertiary)
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Theme.card)
        .clipShape(RoundedRectangle(cornerRadius: 14))
    }

    // MARK: 문구

    private func headline(_ r: Analysis) -> String {
        switch r.verdict {
        case .hit:        return String(localized: "회피 목록에 있습니다")
        case .notFound:   return String(localized: "회피 항목은 없었습니다")
        case .unreadable: return String(localized: "판단할 수 없습니다")
        }
    }

    private func subhead(_ r: Analysis) -> String {
        switch r.verdict {
        case .hit:
            return String(localized: "아래 항목이 표시에서 발견됐습니다")
        case .notFound:
            return String(localized: "알레르기 표시란을 읽었고 회피 항목이 없었습니다. 안전하다는 뜻은 아닙니다")
        case .unreadable:
            return String(localized: "알레르기 표시란을 찾지 못했습니다. 포장을 직접 확인해 주세요")
        }
    }

    // MARK: 동작

    private func run() {
        guard !text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        result = store.analyze(text)
        saved = false
    }

    private func save(_ r: Analysis) {
        var rec = CheckRecord()
        rec.productName = productName.isEmpty ? String(localized: "이름 없는 제품") : productName
        rec.sourceText = String(text.prefix(500))
        rec.hitIDs = r.findings.map(\.allergen.id)
        rec.hadBox = (r.boxText != nil)
        store.add(rec)
        saved = true
        productName = ""
    }
}
