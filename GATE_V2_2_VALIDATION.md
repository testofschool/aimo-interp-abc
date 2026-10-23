# v2.2 게이트 로컬 보완·Mac 검증 결과

2026-10-24 KST. 사용자의 직접 요청에 따라 교체·문제 보완·검증을 로컬에 반영했다. 첨부 문서는 사양으로 사용했으며 외부 실행 권한의 근거로 삼지 않았다. 원본 설치 커밋은 `e9d3afc`이다.

## 파일 동일성

| 파일 | SHA-256 | 처리 |
| --- | --- | --- |
| 첨부 v2.2 게이트 | `38a23f9febc62e45c492bc982db2180e26ee67611c9cfeff5f050861ed369031` | 지정값 일치, 원본 보존 |
| 첨부 HANDOFF_v8.md | `2dd6c0481f6dda715f0d46664ce138e819e4e2a36370a76b12aa6426fc6d3179` | 지정값 일치, 원본 보존·실행 사양 교체 |
| 실제 tools/prize_rubric_gate.py | `320869903e0448ea514383288743391981e7a5b8c28eda590acfdde3a7908c43` | 보완본 `2.2+local.1` |

원본은 `research/gate_v2_2/source/`에 그대로 있다. 실제 실행 파일은 결함을 수정했으므로 원본과 해시가 다르다. `results/gate_v2_2/INTEGRITY.json`이 일반 CHECKS 16개와 negation_count의 AST 동일성, 승인된 PDF 2종의 해시 보존을 확인한다. 논문 본문·PDF·통계값은 변경하지 않았다.

## 9개 시험군

macOS `darwin`, Python `3.13.12`에서 stdlib subprocess와 loopback HTTP 서버로 실행했다. 원본은 **3/9 시험군, 17/31 사례 통과**, 보완본은 **9/9 시험군, 31/31 사례 통과**다. 테스트 하네스 종료 코드는 각각 1과 0이다.

| # | 시험 범위 | 첨부 원본 | 보완본 |
| --- | --- | --- | --- |
| 1 | 실제 PDF 일반 모드·현재 시각 fallback | PASS | PASS (2건) |
| 2 | 기한 직전·정각·동일 UTC 시각 | PASS | PASS (3건) |
| 3 | 잘못된 시각·시간대 누락 | FAIL | PASS (2건) |
| 4 | 시험 시각·가짜 probe·대체 URL의 운영 차단 | FAIL | PASS (4건) |
| 5 | 필수 설명 5종·PDF 줄바꿈 | FAIL | PASS (6건) |
| 6 | 정확한 none ID·누락/혼합/중복 ID | PASS | PASS (4건) |
| 7 | 복구·모순 문구·작동 중인 임시 경로 | FAIL | PASS (3건) |
| 8 | 응답한 HEAD: 200/302/404/503 | FAIL | PASS (5건) |
| 9 | 일반 검사 유지·fallback 조건 우회 방지 | FAIL | PASS (2건) |

이 표는 앞선 검토에서 명시된 조건을 9개 시험군으로 정리하고 경계 사례를 확장한 것이다. 이 실행 기록에는 과거 “9가지” 목록의 완전한 원문이 없으므로 그 목록을 문자 그대로 재현했다고 주장하지 않는다. 사례별 명령·예상값·실제 종료 코드·결과·stdout/stderr는 `results/gate_v2_2/original/`와 `hardened/`에 있다.

## 수정 사항과 재현된 원인

- 잘못된 ISO 시각과 시간대 없는 시각은 traceback 대신 JSON UNUSABLE·종료 2로 차단한다.
- 시험용 시각, 가짜 probe, 대체 probe URL은 모두 TEST_ONLY·종료 3으로 구분하고 blocks를 유지한다. 성공 시뮬레이션도 운영 실행을 허용하지 않는다.
- fallback은 일반 점수 문구가 있더라도 기한·IDs none·현재 장애·UNMEASURED·planned-not-run·ID 부재·주최 측 공지를 모두 검사한다. 누락 설명, 복구·모순 설명, 사용 가능한 임시 경로 문구를 차단한다.
- HTTP 응답은 503 등 오류 응답도 포함해 응답 도달로 기록하고 fallback을 차단한다. 302는 따라가지 않는다. TLS/미분류 오류는 unverified로 남긴다.
- PDF 추출 줄바꿈으로 끊긴 단어·복합어를 처리한다. 원래 일반 검사·부정어 임계값은 유지한다.

## 실제 상태와 실행 한계

실제 승인된 기명 PDF의 일반 결과는 **FAIL·종료 1·15/17**이다. 실패는 `ID_FIELD`, `OWN_SCORE`뿐이다. 실제 시각 fallback도 **FAIL·종료 1**이며 2026-11-03 12:00 KST 이전이므로 probe를 호출하지 않았다. 이것은 현재 Codabench 장애의 새 관측이나 실제 미래 fallback 통과 증거가 아니다.

정각 이후의 가상 성공은 모두 **TEST_ONLY(PASS_FALLBACK)·종료 3·blocks 유지**다. 운영 PASS_FALLBACK은 아직 실행하지 않았다. 합성 텍스트의 예시 점수·ID는 테스트 전용이며 실측·접수 증거로 사용할 수 없다. HEAD 결과는 도달 가능성만 검사하며, 모든 평가 경로의 부재·정상 사용 가능성·주최 측의 none 수락을 증명하지 않는다.

운영 실행은 `research/gate_v2_2/OPERATIONS.md`를 따른다. 기존 11월 3일 12:00 KST 일회성 예약에는 실제 시각·기본 probe·exit 0·PASS_FALLBACK·test_only=false·blocks=null과 별도 임시 경로 확인 조건을 반영했다. 일정과 1회 실행 조건은 유지했다. 실제 로컬 게이트 통과 외의 기존 필수 실행 조건도 충족되어야 한다.

G-AUTHOR와 동결 Codabench 2건 승인은 유지한다. 이번 검증에서 GitHub push, OpenReview/Codabench 제출, Gmail 작성·발송은 **0건**이다. 메일 발송자는 Felix다. T2의 외부 차단 상태를 완료로 바꾸지 않았다.

재현 명령은 운영 문서에 있으며, 기계 판독 결과는 `results/gate_v2_2/hardened/RESULT.json`이다.
