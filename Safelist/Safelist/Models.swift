import Foundation

/// 판정 한 건의 기록. 전부 이 기기 안에만 남는다.
struct CheckRecord: Identifiable, Codable, Hashable {
    var id = UUID()
    var date = Date()
    var productName: String = ""
    var sourceText: String = ""             // 붙여넣은 원문
    var hitIDs: [String] = []               // 걸린 성분 id
    var hadBox: Bool = false                // 알레르기 표시란을 찾았는가
    var feedback: Feedback = .none

    enum Feedback: String, Codable, CaseIterable {
        case none, ok, trouble
        var label: String {
            switch self {
            case .none:    return String(localized: "아직 없음")
            case .ok:      return String(localized: "괜찮았어요")
            case .trouble: return String(localized: "트러블 났어요")
            }
        }
    }

    var verdictWasHit: Bool { !hitIDs.isEmpty }
}
