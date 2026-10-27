# AI disclosure scoped audit — current checkpoint

AI 고지 예외 보완판을 직접 승인된 범위로 적용했습니다. 유일하고 순서가 맞는 AI Use Statement → References 구간의 Codex만 예외로 처리합니다. 제목 경계 누락·중복·역전, 본문·부록·참고문헌 Codex, 나머지 전역 금지어는 계속 차단합니다. 원본 375 스크립트와 기존 Codex:1 FAIL 영수증은 그대로 보존했습니다.

현재 익명 PDF SHA256: `8c78e829da9988fc2ef37532c8880f9ee031812382a2de6017dcf46b470b98aa`. 본문 5쪽 / 전체 10쪽. Anthropic Claude와 OpenAI Codex가 이미 고지돼 있어 이 단계의 원고·PDF 수정 및 재빌드는 0건입니다. 이전에 승인된 정확한 두 문구 수정만 유지됩니다.

새 보완판 SHA256: `a1c05d7722dddf4b345ef82f8fe167cac52d6ff0b64c79c7a0e3d07527527645`. 실제 PDF 감사 PASS; 요청 대조는 본문 Codex FAIL / AI Use Statement 내 Codex PASS. 전체 합성 텍스트 대조 13/13 기대값 충족(PDF 변경 없음). v3 일반모드 19/19 PASS, 숫자 재검증 164/164 PASS·불일치 0. 기존 동일 바이트 PDF의 fidelity 21/21 및 익명·기명 전쪽 시각검사 PASS는 계속 유효합니다.

H2는 요청 준비 상태이며 승인되지 않았습니다. 현재 PDF를 직접 확인한 뒤 `v8.3 PDF 확인`을 입력해야 합니다. 기존 f의 네 가지 어휘 차이 공시는 H2_CHECKS에 유지했고, e의 옛 §5는 무번호 Limitations로 이동한 상태입니다. H3 미러 성공은 아직 확인되지 않았습니다. H1 비밀번호 대기는 유지하며 push·OpenReview 작업은 수행하지 않았습니다.

push 직전에 실제 hostname·저장소 절대경로·HEAD를 다시 보고합니다. 허용 기계는 Jungs-Mac-Studio.local, 저장소는 `/Users/felix/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v6-execution/work` 하나입니다.
