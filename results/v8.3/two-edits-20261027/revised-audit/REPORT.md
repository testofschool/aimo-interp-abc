# 수정판 감사 실행 결과

주신patch는exit0으로 적용됐고 파일SHA256은 기대값 `375a982380f2e0eb43bfe9d85b1c91d1cf0fade81c02613bf0fb902ba46b582c`와 exact 일치합니다. 구판과 수정판의 diff 및 patch stdout/stderr를 보존했습니다.

실제 실행은 **FAIL / exit1 / FORBIDDEN_0 = {"Codex":1}**입니다. 새PDF SHA `8c78e829da9988fc2ef37532c8880f9ee031812382a2de6017dcf46b470b98aa`는 검사 전후 변경되지 않았습니다. 다른 검사 항목은 통과했습니다.

해당1건은6쪽 AI Use Statement의 원문입니다: “The tools were Anthropic Claude and OpenAI Codex, including independent AI agents used for cross-checks.” 원고의 이 고지는 사용자가 허용한 두 문구 수정 범위 밖이며 그대로 유지했습니다. handoff0건, 본문 UNMEASURED0건입니다.

검사 정책 보완안(PROPOSED_POLICY.json)은 **Codex 금지에서 명확히 구분된 AI Use Statement 구간만 제외**하고, 다른 영역의 Codex와 모든 다른 금지어·본문 UNMEASURED 규칙은 유지하는 것입니다. 이는 새 해시를 갖는 별도 검사 정책이므로 현재375 파일을 몰래 바꾸거나 PASS로 재분류하지 않았습니다.

H2는 감사PASS 전제조건 때문에 계속 보류입니다. 원고 추가 변경·push·OpenReview 수정은 없으며 H1 비밀번호 대기는 유지합니다.
