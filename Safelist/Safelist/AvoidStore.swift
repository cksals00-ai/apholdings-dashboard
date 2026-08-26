import SwiftUI

/// 회피 목록과 판정 이력을 보관한다.
/// 저장 위치는 이 기기의 앱 전용 폴더뿐이다. 네트워크로 나가는 경로는 앱 어디에도 없다.
@MainActor
final class AvoidStore: ObservableObject {

    @Published var selected: Set<String> = [] { didSet { save() } }
    @Published var custom: [String] = []      { didSet { save() } }   // 사용자가 직접 적은 것
    @Published var records: [CheckRecord] = [] { didSet { saveRecords() } }
    @Published var onboarded: Bool = false     { didSet { save() } }

    private let dir = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
    private var settingsURL: URL { dir.appendingPathComponent("safelist_settings.json") }
    private var recordsURL: URL  { dir.appendingPathComponent("safelist_records.json") }

    private struct Settings: Codable {
        var selected: [String]; var custom: [String]; var onboarded: Bool
    }

    init() {
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        if let d = try? Data(contentsOf: settingsURL),
           let s = try? JSONDecoder().decode(Settings.self, from: d) {
            selected = Set(s.selected); custom = s.custom; onboarded = s.onboarded
        } else {
            selected = AllergenDB.defaultOnIDs      // 우유 · 밀
        }
        if let d = try? Data(contentsOf: recordsURL),
           let r = try? JSONDecoder().decode([CheckRecord].self, from: d) {
            records = r
        }
    }

    private func save() {
        let s = Settings(selected: Array(selected), custom: custom, onboarded: onboarded)
        try? JSONEncoder().encode(s).write(to: settingsURL, options: .atomic)
    }
    private func saveRecords() {
        try? JSONEncoder().encode(records).write(to: recordsURL, options: .atomic)
    }

    // MARK: 판정
    func analyze(_ text: String) -> Analysis {
        var ids = selected
        // 직접 적은 항목은 즉석 성분으로 만들어 함께 본다
        for c in custom where !c.isEmpty { ids.insert("custom:" + c) }
        var result = Matcher.analyze(text, avoiding: selected)
        // 사용자 정의어는 단순 포함 검사
        let norm = Matcher.normalize(text)
        for c in custom {
            let n = Matcher.normalize(c)
            guard n.count >= 2, norm.contains(n) else { continue }
            let a = Allergen(id: "custom:" + c, name: c, group: .common, terms: [c])
            result.findings.append(Finding(allergen: a, matched: c, fromBox: false))
        }
        if !result.findings.isEmpty { result.verdict = .hit }
        return result
    }

    func add(_ record: CheckRecord) { records.insert(record, at: 0) }
    func delete(_ record: CheckRecord) { records.removeAll { $0.id == record.id } }
    func setFeedback(_ f: CheckRecord.Feedback, for id: UUID) {
        guard let i = records.firstIndex(where: { $0.id == id }) else { return }
        records[i].feedback = f
    }

    var watchedNames: [String] {
        AllergenDB.all.filter { selected.contains($0.id) }.map(\.name) + custom
    }
}
