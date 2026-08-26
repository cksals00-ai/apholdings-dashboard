import SwiftUI

struct AvoidListView: View {
    @EnvironmentObject var store: AvoidStore
    @State private var newTerm = ""

    var body: some View {
        NavigationStack {
            List {
                Section {
                    Text("무엇을 피할지는 알프레드가 정합니다. 이 앱은 그것이 들어 있는지 없는지만 알려줍니다.")
                        .font(.footnote).foregroundStyle(.secondary)
                }

                ForEach(AllergenGroup.allCases, id: \.self) { group in
                    Section {
                        ForEach(AllergenDB.all.filter { $0.group == group }) { a in
                            Toggle(isOn: binding(a.id)) {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(a.name)
                                    if a.defaultOn {
                                        Text("많은 아토피 아이가 피합니다. 담당 의사와 상의해 정하세요.")
                                            .font(.caption2).foregroundStyle(.secondary)
                                    }
                                }
                            }
                            .tint(Theme.accent)
                        }
                    } header: {
                        Text(group.title)
                    } footer: {
                        Text(group.note)
                    }
                }

                Section {
                    ForEach(store.custom, id: \.self) { t in
                        Text(t)
                    }
                    .onDelete { idx in store.custom.remove(atOffsets: idx) }

                    HStack {
                        TextField("예: 검사지에 나온 항목", text: $newTerm)
                        Button("추가") {
                            let t = newTerm.trimmingCharacters(in: .whitespaces)
                            guard t.count >= 2, !store.custom.contains(t) else { return }
                            store.custom.append(t); newTerm = ""
                        }
                        .disabled(newTerm.trimmingCharacters(in: .whitespaces).count < 2)
                    }
                } header: {
                    Text("직접 추가")
                } footer: {
                    Text("알레르기 검사 결과에 나온 항목 중 위 목록에 없는 것을 적어 두세요. 원재료명에서 그 글자를 찾습니다. 두 글자 이상만 됩니다.")
                }
            }
            .navigationTitle("회피 목록")
        }
    }

    private func binding(_ id: String) -> Binding<Bool> {
        Binding(
            get: { store.selected.contains(id) },
            set: { on in
                if on { store.selected.insert(id) } else { store.selected.remove(id) }
            }
        )
    }
}
