# v8.3 H2 사전검사 — 사용자 PDF 확인 대기

**H2/G-LOOK: PENDING.** 이 검사는 `v8.3 PDF 확인`이라는 사용자 답을 대신하지 않습니다. PDF·소스·게이트를 수정/재빌드하지 않았고 커밋·업로드도 하지 않았습니다.

검사 PDF: `v10-execution/review/aimo-interp-report-v8.3-anonymous.pdf`
SHA-256: `2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51`

| 항목 | 판정 | 이번에 직접 확인한 내용 |
| --- | --- | --- |
| a 해시·소스 시각 | **FAIL(시각 조건)** | 해시는 exact. 원본 mtime 10-25 13:20:19 KST / PDF 생성 13:20:18은 마지막 원고 소스 커밋 `33328fe` 13:26:39보다 앞섬. 검토용 복사본 mtime 10-27 00:55:32는 후지만 재빌드 증거가 아님. 동일 TeX/PDF가 `33328fe`에 함께 포착된 정상적인 build→commit 순서이며, 새 소스 비교 14/14 일치. bookkeeping HEAD `e920ae`와 구분. |
| b v3 일반 게이트 | PASS **19/19, exit 0** | SHA `152e2a48…c7630` 바이트를 `git show 33328fe`로 회수해 같은 PDF에 신규 실행. fallback/test 옵션 없음. |
| c 본문 경계 | PASS | 총 10쪽. 본문 5쪽에서 종료, 6쪽 첫 줄 `Limitations and sensitivity directions`. p1·p5·p6 새 렌더로 확인. |
| d 익명성 | PASS | 지정 7개 토큰 각각 본문/metadata/7개 URI에서 대소문자 무시 0건. Author=`Anonymous Author(s)`. |
| e E4 위치·내용 | **FAIL(문자 그대로의 §5 없음)** | 현재 번호 본문은 §§1–3. old §5의 실제 대응은 p6 **무번호 Limitations**. 그곳과 abstract 모두 두 UUID·각 7/14·fair-coin expectation·queue/leaderboard 구분 있음. `strongest non-perfect owner` 0건. 대응 위치의 내용 검사는 PASS. |
| f R1 충실도 | **공개된 추가 문구를 포함한 조건부 PASS** | R1 PDF/text SHA exact; 신규 공백 정규화 diff 36블록과 전체 diff 보관. 새 소스 비교 14/14 일치. 아래 문구를 포함하므로 좁은 네 항목만의 변경이라고 생략하지 않음. |
| g 글꼴 | PASS | 신규 `pdffonts`: Type 3 **0**, 글꼴 11개. |
| h 저장소 URL | PASS | `https://anonymous.4open.science/r/aimo-identifiability` 본문에 exact 2회. 문자 URL이며 URI annotation은 아님. 미러 접속/익명화 상태는 이번에 확인하지 않음. |

**R1과의 차이에서 생략하면 안 되는 기공개 원문:**

- Abstract: “We provide CPU reproduction rather than additional model runs.”
- [11] 추가: “The 24 October temporary-evaluation-queue notice is documented in the supplied v8.3 handoff; the recorded queue responses accompany the archive.”
- 익명 self-source 표시: `6f81bc3b31472dfeb1179b25c31fd7bb128dd19f` → `[withheld for anonymous review]`.
- E4의 pending 정리: “The recorded queue receipt JSONs accompany the reproduction archive.”

**p1 원문 발췌** — 제목: “Can a small validation leaderboard rank robustness predictors? Identifiability limits in AIMO-Interp”; 저자: “Anonymous Author(s)”. Abstract 마지막 두 문장은 아래와 같습니다(줄바꿈만 펼침; `2026- 10-24`는 PDF 줄바꿈 지점).

> Both reference baselines were scored once each through the organizers’ temporary evaluation queue during the Codabench outage [11]; these runs are not on the leaderboard. The always-robust rule scored 7/14 (submission id bde5e370-4dba-4f19-8291-4a998bfecdcd, 2026- 10-24 19:01:28 KST) and the length-and-digit control scored 7/14 (submission id 0c736e59-8248-4dee-8e4f-2df037c552d7, 2026-10-24 19:03:37 KST); each equals the fair-coin expectation and is not separable from it under the declared null.

**p5 원문 마지막 본문 줄:** `validation grid.` / 마지막 인쇄 줄(footer): `5`.

상세 수치·원문 줄바꿈·a–h 결과: `v8-execution/H2_CHECKS.json`. 신규 근거: `report/build/h2-precheck-2026-10-27/`(Git 제외). 기존 10쪽 전체 시각 검토와 `FIDELITY_REVIEW.md`는 **이전 증거**로 구분했으며, 이번 시각 재검사는 p1·p5·p6만입니다. a/e 불일치를 숨기거나 해소하기 위한 PDF 편집은 하지 않았습니다.
