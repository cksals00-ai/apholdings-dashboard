//
//  Matcher.swift
//  세이프리스트 — 판정 엔진
//
//  설계 원칙 하나만 기억한다.
//  ── 초록불(안전)은 만들지 않는다. ──
//  "회피 항목이 발견되지 않았다"와 "안전하다"는 전혀 다른 말이고,
//  그 둘을 같은 색으로 칠하는 순간 이 앱은 사고를 낸다.
//

import Foundation

// MARK: - 결과 모델

enum Verdict {
    case hit            // 🔴 회피 항목 발견
    case notFound       // ⚪ 표시란을 읽었고, 회피 항목은 없었다
    case unreadable     // ⚪ 표시란을 찾지 못했다 (판단 불가)
}

struct Finding: Identifiable, Hashable {
    var id: String { allergen.id + matched }
    let allergen: Allergen
    let matched: String         // 실제로 걸린 표기
    let fromBox: Bool           // 알레르기 표시란에서 나왔는가
}

struct Analysis {
    var verdict: Verdict
    var findings: [Finding] = []
    var boxText: String? = nil          // 찾아낸 알레르기 표시란 원문
    var gelatinAmbiguous = false        // 젤라틴인데 원료(돼지/소) 미상
    var crossContact: String? = nil     // "같은 제조시설" 혼입 문구

    var legalFindings: [Finding] { findings.filter { $0.allergen.group == .legal } }
    var otherFindings: [Finding] { findings.filter { $0.allergen.group != .legal } }
}

// MARK: - 엔진

enum Matcher {

    /// 알레르기 표시란을 여는 말들. 제조사마다 조금씩 다르다.
    private static let boxAnchors = [
        "알레르기유발물질", "알레르기유발성분", "알레르기성분", "알레르기물질", "알레르기",
        "allergen", "contains"
    ]

    /// 표시란이 끝났다고 볼 만한 말들
    private static let boxStoppers = [
        "보관방법", "유통기한", "소비기한", "품목보고", "제조원", "판매원", "수입원",
        "반품", "고객상담", "영양정보", "내용량", "포장재질", "식품유형", "원산지",
        "부정불량", "교환", "총내용량"
    ]

    /// 혼입 가능성 문구
    private static let crossHints = ["같은제조시설", "같은생산시설", "혼입가능", "혼입될수있", "제조하고있습니다"]

    // MARK: 정규화
    /// 공백·구두점을 걷어내 표기 흔들림을 흡수한다. 한글/영문/숫자만 남긴다.
    static func normalize(_ s: String) -> String {
        let lowered = s.lowercased()
        var out = ""
        out.reserveCapacity(lowered.count)
        for ch in lowered.unicodeScalars {
            if CharacterSet.alphanumerics.contains(ch) || (ch.value >= 0xAC00 && ch.value <= 0xD7A3) {
                out.unicodeScalars.append(ch)
            }
        }
        return out
    }

    // MARK: 표시란 잘라내기
    /// "알레르기…" 뒤부터 다음 섹션 머리말 전까지를 표시란으로 본다.
    static func extractBox(_ normalized: String) -> String? {
        for anchor in boxAnchors {
            guard let r = normalized.range(of: anchor) else { continue }
            var tail = String(normalized[r.upperBound...])
            // 다음 섹션에서 끊는다
            var cut = tail.count
            for stopper in boxStoppers {
                if let sr = tail.range(of: stopper) {
                    cut = min(cut, tail.distance(from: tail.startIndex, to: sr.lowerBound))
                }
            }
            tail = String(tail.prefix(min(cut, 160)))   // 표시란은 길지 않다
            if tail.count >= 2 { return tail }
        }
        return nil
    }

    // MARK: 판정
    static func analyze(_ raw: String, avoiding selectedIDs: Set<String>) -> Analysis {
        let text = normalize(raw)
        guard !text.isEmpty else { return Analysis(verdict: .unreadable) }

        let box = extractBox(text)
        var result = Analysis(verdict: .unreadable, boxText: box)

        let watched = AllergenDB.all.filter { selectedIDs.contains($0.id) }
        var seen = Set<String>()

        // ① 알레르기 표시란 — 법이 표준 용어로 찍어주는 곳. 여기가 가장 정확하다.
        //    표시란 안에서는 기준어("밀", "게" 같은 짧은 말)도 인정한다.
        if let box {
            for a in watched {
                let boxTerms = ([normalize(a.name)] + a.terms.map(normalize))
                    .filter { !$0.isEmpty }
                    .sorted { $0.count > $1.count }
                for t in boxTerms where box.contains(t) {
                    if seen.insert(a.id).inserted {
                        result.findings.append(Finding(allergen: a, matched: t, fromBox: true))
                    }
                    break
                }
            }
        }

        // ② 원재료 본문 — 표시 의무가 없는 항목은 여기서만 찾을 수 있다.
        //    오탐을 막기 위해 두 글자 이상 표기만 쓴다.
        //
        //    ★ 법정 22종은 표시란이 있으면 본문을 뒤지지 않는다.
        //      제조사가 표시란에 적을 법적 의무를 지므로, 거기 없으면 없는 것이다.
        //      본문까지 뒤지면 「아몬드밀크」의 "밀크칼슘" 같은 표기가 우유로 걸려
        //      모든 제품이 빨간불이 된다. 빨간불만 뜨는 앱은 아무도 안 본다.
        let boxExists = (box != nil)
        for a in watched where !seen.contains(a.id) {
            if boxExists && a.group == .legal { continue }
            let terms = a.safeTerms.map(normalize).filter { $0.count >= 2 }
                .sorted { $0.count > $1.count }
            for t in terms where text.contains(t) {
                result.findings.append(Finding(allergen: a, matched: t, fromBox: false))
                seen.insert(a.id)
                break
            }
        }

        // ③ 젤라틴 — 원료가 돼지인지 소인지 표기되지 않는 경우가 많다.
        if text.contains("젤라틴") || text.contains("gelatin") {
            let origins = ["돈피", "돼지", "우피", "쇠고기", "소고기", "어류", "생선", "pork", "beef", "fish"]
            result.gelatinAmbiguous = !origins.contains { text.contains($0) }
        }

        // ④ 혼입 가능성 문구
        if let hint = crossHints.first(where: { text.contains($0) }) {
            result.crossContact = hint
        }

        // ⑤ 최종 판정
        if !result.findings.isEmpty {
            result.verdict = .hit
        } else if box != nil {
            result.verdict = .notFound
        } else {
            result.verdict = .unreadable
        }
        return result
    }
}
