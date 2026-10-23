# v8.1 G-AUTHOR 확인 반영

2026-10-24 KST. 사용자가 현재 채팅에서 최종 기명 PDF와 AI 보조 작업의 검토·책임, ~Jung_Min_Kang1 상호 심사 3건, 규정 준수, CC BY-SA 4.0을 직접 확인했다. 필수 실행 조건 충족 후 GitHub push 및 OpenReview 제출·시험 수정·원복을 승인했고, 기존 Codabench 동결 2건 승인을 유지했다. 원문과 승인 대상 PDF 해시는 `research/AUTHOR_APPROVAL_v8.1.json`에 기록했다.

이로써 G-AUTHOR는 확인 완료다. 제출·공개 자체의 완료나 실행 조건 면제로 기록하지 않는다. 동일 범위 승인을 다시 요청하지 않는다.

## 반영한 변경과 검증

AI Use Statement의 마지막 한 문장만 다음과 같이 바꿨다.

> The author has reviewed all AI-assisted work and takes full responsibility for the final content, including AI-assisted text, claims, code, reported statistics and other artifacts.

AI 사용 분야·도구·제외 사용·원천 관측과 파생 계산의 구별은 유지했다. 별도로 수치를 직접 재계산했다는 주장을 저자에게 추가하지 않았다. 본문·분석·참고문헌·수치 파일·152개 claim·생성기·스타일·preamble은 그대로다. 두 TeX와 PDF를 다시 만들었고 submission_text_gate는 통과했다.

| 축 | 차이 | 분류·근거 |
|---|---|---|
| AI 공개문 마지막 문장 | 검토 책임에서 완료된 검토·책임으로 갱신 | 직접 사용자 확인 반영 |
| 과학 본문·등록 수치·계산 출력·생성기 | 동일 | SOURCE_CHECKS.json의 바이트·단일 치환 검사 |
| 스타일·글꼴·쪽수 | 동일 | 글꼴 표 동일, 두 PDF 모두 9쪽·Type3=0 |
| PDF 8쪽 | 공개문 마지막 문장 재흐름 | 두 변형 직접 시각 검토; 잘림·겹침·문자 누락 없음 |
| 나머지 16쪽 | 픽셀 동일 | 승인 대상 정본의 검증 렌더와 직접 비교 |
| 제출 메타데이터·현재 README | 승인 상태로 갱신 | 과거 실행 기록은 당시 기록으로 보존 |

미보고 내용·서식 차이 0. 재생성 충실도 PASS.

현재 기명 PDF SHA256은 `31c5ee0c79278c7b31a038acde4ed3f6ff61fbc2dbc361280000fc485b512c95`, 저자명 제거본은 `b6c3fc29778c622b1476186e1ba0406126643516ed851c37ce3e90062e605bd8`이다. 본문 부정어 수는 각각 40이다.

## 게이트와 남은 조건

직접 확인 기록을 근거로 strict preflight에 `--author-review-confirmed`를 사용했다. 두 변형 모두 `author_review_and_attestations=CONFIRMED_BY_CALLER`, `completed_review_wording=PRESENT`다. 독립 에이전트도 두 TeX와 PDF 공개문을 검사해 오류 없음과 완료 검토 문구를 확인했다.

상금 게이트는 여전히 15/17이고 ID_FIELD·OWN_SCORE만 실패한다. Payload gate와 strict preflight의 남은 오류는 실제 leaderboard_submission_ids 누락이다. 없는 점수·접수번호를 작성하지 않았고, 게이트 코드를 바꾸지 않았다.

T2는 Felix가 06:00 KST에 확인한 외부 장애 상태를 유지한다. 실제 평가 경로와 인증 세션, 현재 phase·계정·한도 확인이 있어야 승인된 2건을 제출할 수 있다. 공개 push와 OpenReview 제출·시험 수정·원복은 아직 실행하지 않았다. 이번 직접 승인은 필수 실행 조건 충족을 전제로 하므로, 조건 미충족 상태에서 원래 핸드오프의 10분 내 push 문구만으로 공개하지 않는다.

11월 3일 12:00 KST의 현재 채팅 1회 fallback 확인 예약은 유지했고, 이번 직접 승인 기록을 이어받아 같은 승인을 다시 요청하지 않도록 prompt를 갱신했다. 평가 경로가 없을 때의 `none`·planned-not-run·보류 메일 조건을 유지한다. 예약만으로 Gmail 발송 권한을 추가하지 않았으며 발송자는 핸드오프대로 Felix다.

증거: `results/v8.1/author-approved-2026-10-24/`, `research/AUTHOR_APPROVAL_v8.1.json`. 전체 목표는 외부 평가 경로·영수증이 없어 미완료이며, 인간 승인 항목은 더 이상 차단 사유가 아니다.
