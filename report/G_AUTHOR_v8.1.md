# v8.1 저자 검토 자료

2026-10-24 재빌드본. 상태: **G-AUTHOR 준비 완료 · 최종 저자 확인 전**.

## 검토할 파일

제출 대상은 `aimo-interp-report-v8-named.pdf`이며 Jung Min Kang / Independent로 표시된다. `aimo-interp-report-v8-anonymous.pdf`는 저자명 제거 비교본이다. 공통 저장소 URL이 신원을 드러내므로 완전한 익명본으로 보지 않는다. 두 PDF는 각각 9쪽이며 본문·글꼴·페이지의 모든 픽셀이 직전 검증본과 같다. 재빌드 메타데이터로 파일 해시만 바뀌었다.

| 파일 | 이번 SHA256 |
|---|---|
| 기명 | 4cf4e1acc585e33ae27bf9484b6e1f7d1df75f2a887edc56cabef96743eb1639 |
| 저자명 제거 | a290cac61a5dbf98c65f91e0f8f44ec350dc973b2ee81c568ce9ecf5199a1542 |

## 본문에서 확인할 핵심

- 선언한 독립 fair-coin 귀무모형, 소유자별 선택 보정과 소유자 간 BH 보정 아래에서 Small 59/61, Main 40/41 소유자가 기각되지 않는다는 결과다. 비기각은 우연과 동등함 또는 두 방법 간 차이가 없다는 증명이 아니다.
- 76/169는 정해진 효과에 대한 단일 예측기의 독립 정답 항목 기준 설계 목표다. paired·problem-clustered 비교의 표본 수는 별도로 산정해야 한다.
- 스냅샷은 10월 21일 삭제 공지 전 자료다. 삭제된 두 제출을 특정 소유자와 연결하거나 해당 통계로 부정행위를 판정하지 않는다.
- 두 동결 기준선의 비공개 평가는 UNMEASURED다. 접수번호·점수·최종 테스트 결과를 작성하지 않았다.
- 공개 데이터, 고정 입력과 계산에 관한 152개 수치는 재검증됐다. AI Use Statement와 수치·본문·서식은 변경하지 않았다.

## 저자가 최종 확인할 사항

- [ ] 최종 제출할 기명 PDF와 AI 보조 작업을 검토하고, 본문·주장·코드·통계 및 AI 보조 내용에 책임진다.
- [ ] AI 사용 분야는 Ideation, Coding, Analysis, Writing이며, Claude와 Codex 사용을 밝힌 현 AI Use Statement와 일치한다.
- [ ] 저자이자 상호 심사자 `~Jung_Min_Kang1`으로 배정되는 3건의 심사를 기한 내 직접 작성한다. 심사 마감은 주최 측 공지 기준 2026-11-13 20:59 KST다. 미제출·지연·저품질·미공개 AI 심사는 desk reject 또는 수상 제외 사유가 된다.
- [ ] 규정 준수, CC BY-SA 4.0, Small models track 및 white-box award 미신청을 확인한다.
- [ ] 필수 실행 조건이 충족된 최종본에 대해 GitHub 공개 push와 OpenReview 제출, 시험 수정 및 TLDR 원복을 승인한다.

기존 Codabench 동결 Small 번들 2건 승인은 유효하다. 이 검토 자료의 생성, PDF 탭 열기, 준비된 확인 문구, AI 점검은 실제 저자 확인으로 기록되지 않는다.

## 최종 승인 문구 예시

아래 문구는 T2 영수증 반영 또는 기한 fallback 후의 **최종 제출본을 실제 검토한 뒤** 사용할 수 있다. 현재 재빌드본의 내용 검토를 먼저 할 수 있으며, 이후 본문이 바뀌면 그 최종본에 대한 확인을 받는다.

> v8.1 최종 기명 PDF와 AI 보조 작업을 검토했고 최종 내용에 책임집니다. ~Jung_Min_Kang1 상호 심사 3건 참여와 규정 준수, CC BY-SA 4.0에 동의합니다. 필수 실행 조건이 충족된 이 최종본의 GitHub push와 OpenReview 제출·시험 수정·원복을 승인합니다. Codabench 동결 2건 승인은 유지합니다.

G-AUTHOR 근거는 핸드오프 §1의 “Felix types ... after opening the v8 PDF”와 “none — no document substitutes for it”이다. 정확한 한 문장 암기보다 실제 검토·책임·의무·실행 범위에 대한 직접 확인을 기록한다.

## 현재 실행 상태와 11월 3일 조건

수치·렌더링·제출 문구 검사는 통과했다. 상금 게이트는 15/17이며 ID_FIELD와 OWN_SCORE가 실패다. OpenReview 기술 검사는 실제 leaderboard_submission_ids 미입력으로 차단돼 있고, 저자 검토·확약도 미확인 상태다. 공개 push와 OpenReview 제출은 실행하지 않았다.

Felix의 10월 24일 06:00 KST 확인에 따라 T2는 외부 원인으로 blocked다. URL은 Felix가 Discord에서 확인하면 이 채팅에 전달한다. 2026-11-03 12:00 KST까지 경로가 없으면 `leaderboard_submission_ids: ["none"]`과 planned-not-run 설명, 보류 문의 메일의 fallback을 적용하는 조건을 기록했다. 해당 시각에 같은 채팅을 한 번 깨워 상태를 확인하도록 예약했다. 핸드오프상 보류 메일 발송자는 Felix다.

`none`의 문법 적합성과 주최 측 수락은 구별한다. 원래 17항목 게이트가 실제 ID·점수를 요구한다는 충돌도 기록하며, 실패를 PASS로 바꾸거나 실측을 만들어내지 않는다. 기한 fallback과 최종 제출 실행의 조건은 당시 사용자 지시 및 직접 승인 범위에 따라 판단한다.
