# 기존 노트의 새 양식 입력 후보 — v8.3

이 패킷은 **이미 접수된 note `kPRRCYEOG1`의 양식 필드 보완용 로컬 후보**입니다. 새 게시나 v8.4 원고가 아닙니다. 원본 제출 영수증과 원본 payload를 보존했습니다.

## 현재 공식 변경

- OpenReview invitation `tmdate=1793515755843`: `submission_1_id`와 `submission_1_track`이 새 필수 항목입니다. 두 번째 ID/track은 선택 항목입니다.
- 기존 `leaderboard_submission_ids`도 남아 있습니다. 한 노트의 같은 두 접수를 다음처럼 일치시킵니다.

| 항목 | 값 |
| --- | --- |
| leaderboard_submission_ids | `1012526, 1012549` |
| submission_1_id | `1012526` |
| submission_1_track | `Small models track` 하나 |
| submission_2_id | `1012549` |
| submission_2_track | `Small models track` 하나 |

첫 ID/track 두 항목만 필수라는 뜻이며, 위 패킷은 이미 기록된 두 Small 접수를 모두 명시합니다. 새 사실 확약 enum은 추가되지 않았습니다. 기존 AI·심사·규정·중복 보고서 관련 동의의 사실성은 저자가 확인하며, syntax PASS가 대신 입증하지 않습니다.

## 검증 범위

- `OLD_PAYLOAD_GATE.json`: 원래 payload는 새 필수 두 항목 누락으로 실제 FAIL.
- `CANDIDATE_GATE.json`: 새 후보는 저장된 공식 원문에 대한 실제 PASS.
- `DRY_RUN.json`: 인증·SDK·서비스 쓰기 없는 실제 dry-run.
- `ID_TRACK_CONSISTENCY.json`: 기존 통합 ID 순서와 새 ID/track 쌍 일치.
- 제목·초록·TLDR·저자·기존 동의 문구·PDF는 바꾸지 않았습니다.
- PDF SHA256: `944693b7138f0cfc51e254b7c37284806336044ed06722d2e09905714c6f55ae`.

이 변경만으로 이전 접수의 거절·소멸을 추정하지 않습니다. 현재 서버 새 필드 상태는 owner 인증 조회 전에는 미확인입니다.

## Felix가 기존 노트를 수정할 때

현재 v8.3의 양식 필드만 보완하려는 경우, 본인 Terminal에서 아래 명령을 사용합니다. v8.4 PDF가 준비되면 H2b에 별도 payload와 명령을 다시 제공합니다.

```zsh
cd /Users/felix/aimo-v12
/Users/felix/orvenv/bin/python -I tools/or_post.py v12-execution/form-updates/20261101T2038KST/payload_v83_schema_1793515755843.json.filled.json --revise kPRRCYEOG1 --out v12-execution/form-updates/20261101T2038KST/REVISE.json
```

인증정보는 본인 Terminal에만 입력합니다. 명령은 쓰기 직전에 live 양식을 다시 검사합니다. 새 노트 생성 경로는 사용하지 않습니다. 결과가 불명확하면 기존 노트와 영수증을 조정하기 전 재시도하지 않습니다.

수정 뒤에는 같은 note.id, 통합 ID 순서, 새 두 ID/track 쌍, 첨부 PDF SHA를 실제 readback으로 확인합니다. 다른 PDF로 바꾸려면 해당 PDF의 인간 확인 조건을 먼저 충족합니다.

## 재생성 시점

공식 phase30038 종료는 `2026-11-02T12:00:00Z` (**11월 2일 21:00 KST**)로 연장됐고 현재 Current입니다. 최종 board 동결·T-REGEN은 실제 종료 확인 후 진행합니다. 11월 2일 21:01 KST에 단발 확인을 예약했습니다. 다시 연장되거나 상태를 읽을 수 없으면 mutable board를 final로 취급하지 않습니다.

내용 동결 **11월 4일 20:00 KST**, 제출·수정 운영 cutoff **11월 6일 20:00 KST**는 유지합니다.

새 필드 readback 대조를 포함한 로컬 도구 검증: `HELPER_COMPATIBILITY.json` (55개 오프라인 시험 PASS). 의미상 통합 ID/쌍 일치는 별도 `ID_TRACK_CONSISTENCY.json`으로 확인했습니다. 재검증용 공개 양식 원문은 `LIVE_INVITATION.json`입니다.
