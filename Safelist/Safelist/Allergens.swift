//
//  Allergens.swift
//  세이프리스트 — 성분 데이터
//
//  한국 「식품등의 표시·광고에 관한 법률」 시행규칙 [별표 2] 의
//  알레르기 유발물질 표시 대상(22종)을 기준으로 삼는다.
//  법이 표준 용어로 표시하도록 강제하므로, 그 용어가 곧 우리의 기준어다.
//
//  ⚠ 이 파일은 "무엇이 들어 있는가"만 다룬다.
//     "무엇이 몸에 좋은가/나쁜가"는 판단하지 않는다. 그건 우리 몫이 아니다.
//

import Foundation

enum AllergenGroup: String, Codable, CaseIterable {
    case legal          // 법정 22종 — 표시 의무
    case common         // 자주 걸러내는 것 (22종 밖)
    case additive       // 첨가물 계열

    var title: String {
        switch self {
        case .legal:    return String(localized: "법정 표시 대상 22종")
        case .common:   return String(localized: "자주 걸러내는 것")
        case .additive: return String(localized: "첨가물")
        }
    }

    var note: String {
        switch self {
        case .legal:
            return String(localized: "제조사가 포장에 반드시 표시해야 하는 항목입니다. 판정이 가장 정확합니다.")
        case .common:
            return String(localized: "표시 의무가 없어 원재료명에서 찾습니다. 표기가 없으면 확인되지 않습니다.")
        case .additive:
            return String(localized: "원재료명에서 찾습니다. 제품마다 표기가 달라 놓칠 수 있습니다.")
        }
    }
}

struct Allergen: Identifiable, Codable, Hashable {
    let id: String
    let name: String            // 한국어 기준어 (= 로컬라이즈 키)
    let group: AllergenGroup
    /// 원재료명·표시란에 등장하는 표기들. 짧은 것부터가 아니라 긴 것부터 매칭한다.
    let terms: [String]
    /// 켜 두면 온보딩에서 기본 선택된다 (우유·밀)
    var defaultOn: Bool = false

    /// 2글자 미만 표기는 본문 매칭에서 제외한다 (오탐 방지). 표시란 안에서는 허용.
    var safeTerms: [String] { terms.filter { $0.count >= 2 } }
}

enum AllergenDB {

    // MARK: - 법정 22종
    // 조개류는 굴·전복·홍합을 포함해 22종으로 센다.
    static let legal: [Allergen] = [
        Allergen(id: "egg", name: "알류(가금류)", group: .legal, terms: [
            "알류", "계란", "달걀", "난백", "난황", "전란액", "난백분", "난황분",
            "난가공품", "메추리알", "egg", "albumen"
        ]),
        Allergen(id: "milk", name: "우유", group: .legal, terms: [
            "우유", "탈지분유", "전지분유", "혼합분유", "조제분유", "유청단백", "유청분말", "유청",
            "카제인나트륨", "카제인", "유당", "버터밀크", "버터", "생크림", "유크림", "크림",
            "치즈", "연유", "가당연유", "발효유", "유단백", "유고형분", "밀크",
            "milk", "casein", "whey", "lactose", "butter", "cheese"
        ], defaultOn: true),
        Allergen(id: "buckwheat", name: "메밀", group: .legal, terms: ["메밀", "buckwheat"]),
        Allergen(id: "peanut", name: "땅콩", group: .legal, terms: ["땅콩", "낙화생", "피넛", "peanut"]),
        Allergen(id: "soy", name: "대두", group: .legal, terms: [
            "대두", "분리대두단백", "농축대두단백", "대두유", "대두레시틴", "탈지대두",
            "간장", "된장", "두부", "두유", "콩기름", "소이", "soy", "soya", "lecithin"
        ]),
        Allergen(id: "wheat", name: "밀", group: .legal, terms: [
            "소맥분", "정제소맥분", "소맥전분", "소맥", "밀가루", "통밀", "듀럼밀", "세몰리나",
            "밀글루텐", "글루텐", "밀단백", "밀전분", "밀배아", "wheat", "gluten", "semolina"
        ], defaultOn: true),
        Allergen(id: "mackerel", name: "고등어", group: .legal, terms: ["고등어", "mackerel"]),
        Allergen(id: "crab", name: "게", group: .legal, terms: ["게살", "꽃게", "대게", "홍게", "게엑기스", "게추출물", "게", "crab"]),
        Allergen(id: "shrimp", name: "새우", group: .legal, terms: ["새우", "건새우", "새우분말", "새우추출물", "shrimp", "prawn"]),
        Allergen(id: "pork", name: "돼지고기", group: .legal, terms: [
            "돼지고기", "돈육", "돈지", "라드", "베이컨", "삼겹살", "돈피", "pork", "lard"
        ]),
        Allergen(id: "peach", name: "복숭아", group: .legal, terms: ["복숭아", "peach"]),
        Allergen(id: "tomato", name: "토마토", group: .legal, terms: ["토마토", "토마토페이스트", "케첩", "tomato"]),
        Allergen(id: "sulfite", name: "아황산류", group: .legal, terms: [
            "아황산나트륨", "산성아황산나트륨", "메타중아황산나트륨", "메타중아황산칼륨",
            "무수아황산", "이산화황", "아황산", "sulfite", "sulphite"
        ]),
        Allergen(id: "walnut", name: "호두", group: .legal, terms: ["호두", "walnut"]),
        Allergen(id: "chicken", name: "닭고기", group: .legal, terms: ["닭고기", "계육", "닭가슴살", "치킨", "chicken"]),
        Allergen(id: "beef", name: "쇠고기", group: .legal, terms: [
            "쇠고기", "소고기", "우육", "우지", "사골", "beef", "tallow"
        ]),
        Allergen(id: "squid", name: "오징어", group: .legal, terms: ["오징어", "squid", "calamari"]),
        Allergen(id: "shellfish", name: "조개류", group: .legal, terms: [
            "조개", "바지락", "가리비", "모시조개", "shellfish", "clam", "scallop"
        ]),
        Allergen(id: "oyster", name: "굴", group: .legal, terms: ["굴", "굴엑기스", "oyster"]),
        Allergen(id: "abalone", name: "전복", group: .legal, terms: ["전복", "abalone"]),
        Allergen(id: "mussel", name: "홍합", group: .legal, terms: ["홍합", "mussel"]),
        Allergen(id: "pinenut", name: "잣", group: .legal, terms: ["잣", "pine nut", "pinenut"])
    ]

    // MARK: - 자주 걸러내는 것 (법정 22종 밖 · 원재료명에서 찾는다)
    static let common: [Allergen] = [
        Allergen(id: "sesame", name: "참깨", group: .common, terms: ["참깨", "깨", "참기름", "sesame"]),
        Allergen(id: "almond", name: "아몬드", group: .common, terms: ["아몬드", "almond"]),
        Allergen(id: "cashew", name: "캐슈넛", group: .common, terms: ["캐슈넛", "캐슈", "cashew"]),
        Allergen(id: "pistachio", name: "피스타치오", group: .common, terms: ["피스타치오", "pistachio"]),
        Allergen(id: "hazelnut", name: "헤이즐넛", group: .common, terms: ["헤이즐넛", "개암", "hazelnut"]),
        Allergen(id: "macadamia", name: "마카다미아", group: .common, terms: ["마카다미아", "macadamia"]),
        Allergen(id: "kiwi", name: "키위", group: .common, terms: ["키위", "kiwi"]),
        Allergen(id: "banana", name: "바나나", group: .common, terms: ["바나나", "banana"]),
        Allergen(id: "mango", name: "망고", group: .common, terms: ["망고", "mango"]),
        Allergen(id: "strawberry", name: "딸기", group: .common, terms: ["딸기", "strawberry"]),
        Allergen(id: "corn", name: "옥수수", group: .common, terms: ["옥수수", "콘시럽", "corn"]),
        Allergen(id: "palmoil", name: "팜유", group: .common, terms: ["팜유", "팜올레인", "팜핵유", "palm oil"]),
        Allergen(id: "gelatin", name: "젤라틴", group: .common, terms: ["젤라틴", "gelatin", "gelatine"]),
        Allergen(id: "cocoa", name: "카카오", group: .common, terms: ["카카오", "코코아", "초콜릿", "cocoa", "chocolate"])
    ]

    // MARK: - 첨가물
    static let additive: [Allergen] = [
        Allergen(id: "tarcolor", name: "타르색소", group: .additive, terms: [
            "황색4호", "황색5호", "적색2호", "적색3호", "적색40호", "적색102호",
            "청색1호", "청색2호", "녹색3호", "타르색소", "합성착색료"
        ]),
        Allergen(id: "preserv", name: "합성보존료", group: .additive, terms: [
            "안식향산나트륨", "안식향산", "소브산칼륨", "소브산", "데히드로초산나트륨",
            "파라옥시안식향산", "프로피온산"
        ]),
        Allergen(id: "sweetener", name: "인공감미료", group: .additive, terms: [
            "아스파탐", "수크랄로스", "아세설팜칼륨", "사카린나트륨", "삭카린"
        ]),
        Allergen(id: "msg", name: "L-글루탐산나트륨", group: .additive, terms: [
            "L-글루탐산나트륨", "글루탐산나트륨", "향미증진제"
        ]),
        Allergen(id: "flavor", name: "합성착향료", group: .additive, terms: ["합성착향료", "합성향료"])
    ]

    static let all: [Allergen] = legal + common + additive
    static func find(_ id: String) -> Allergen? { all.first { $0.id == id } }
    static var defaultOnIDs: Set<String> { Set(all.filter(\.defaultOn).map(\.id)) }
}
