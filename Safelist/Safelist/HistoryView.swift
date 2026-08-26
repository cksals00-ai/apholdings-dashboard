import SwiftUI

struct HistoryView: View {
    @EnvironmentObject var store: AvoidStore

    var body: some View {
        NavigationStack {
            Group {
                if store.records.isEmpty { empty } else { list }
            }
            .navigationTitle("기록")
        }
    }

    private var empty: some View {
        VStack(spacing: 12) {
            Image(systemName: "list.bullet.rectangle")
                .font(.system(size: 44, weight: .light)).foregroundStyle(.secondary)
            Text("아직 기록이 없습니다").font(.headline)
            Text("확인한 제품을 기록해 두면\n다음에 살 때 다시 찾아보지 않아도 됩니다.")
                .font(.subheadline).foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(30)
    }

    private var list: some View {
        List {
            Section {
                Text("먹인 뒤 어땠는지 남겨 두세요. 나중에 같은 성분이 든 제품을 볼 때 참고가 됩니다.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            ForEach(store.records) { r in
                VStack(alignment: .leading, spacing: 8) {
                    HStack(spacing: 10) {
                        Circle()
                            .fill(r.verdictWasHit ? Theme.hit : Theme.unknown)
                            .frame(width: 10, height: 10)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(r.productName).font(.subheadline.weight(.semibold))
                            Text(r.date.formatted(date: .abbreviated, time: .omitted))
                                .font(.caption).foregroundStyle(.secondary)
                        }
                        Spacer()
                    }

                    if !r.hitIDs.isEmpty {
                        Text(r.hitIDs.compactMap { AllergenDB.find($0)?.name ?? $0.replacingOccurrences(of: "custom:", with: "") }
                                .joined(separator: " · "))
                            .font(.caption).foregroundStyle(Theme.hit)
                    } else {
                        Text(r.hadBox ? "회피 항목 없음" : "표시란을 찾지 못함")
                            .font(.caption).foregroundStyle(.secondary)
                    }

                    Picker("", selection: Binding(
                        get: { r.feedback },
                        set: { store.setFeedback($0, for: r.id) }
                    )) {
                        ForEach(CheckRecord.Feedback.allCases, id: \.self) { f in
                            Text(f.label).tag(f)
                        }
                    }
                    .pickerStyle(.segmented)
                }
                .padding(.vertical, 4)
            }
            .onDelete { idx in idx.map { store.records[$0] }.forEach(store.delete) }
        }
    }
}
