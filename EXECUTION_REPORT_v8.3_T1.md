# v8.3 T1 실행 결과 — 익명 PDF 확인 대기

사용자의 직접 요청에 따라 이 Mac Studio에서 T0 이전을 건너뛰고 `git switch -c v8.3 144ce58`로 시작했다. 수행 범위는 T1이며 새 PDF 확인 전에는 T3·T4를 실행하지 않는다.

## 입력·브랜치 검증

- ZIP: `a5b0e1f8feaf1ac0742dd8b14ad90d6935dd8cf363470ff330654552635a52a0`, 지정값 일치.
- SHA256SUMS: HANDOFF, v3 게이트, 영수증2건의 **4/4 일치**. 원본은 `research/v8_3_sources/`에 보존했고 영수증2건은 요청한 `v8-execution/queue/`에도 배치했다.
- 시작 정본: `144ce584548512cf903afe2b5486b35aac1f4cc9`. 설치 커밋 `3912328`에서 정확한 v3를 먼저 설치했다.
- v3 SHA: `152e2a488eb0c3cdeadbe4195bb09ac90acab464df4326a612098dc63f5c7630`, 변경 없음.
- 이전32086990게이트는 diff 비교만 하고 실행하지 않았다. 비교 보고서는 `results/v8.3/gate_controls/GATE_DIFF.md`, 전체diff는 `v8-execution/v8.3-input/gate_32086990_to_v3.diff`다.

R1의 정본 기명PDF31c5ee0c…2c95는 일치했다. 정본 익명PDF의 실제값은 b6c3fc29…05bd8이며, 핸드오프의 오래된 a290cac6…와 구분해 기록했다. 이전 게이트 실제값32086990…과 R1의38a23f9f… 차이도 기록했다. 현재 직접 지시대로 정본144ce58은 유지하고 게이트만 지정v3로 교체했다.

## 동결 번들·기존 T2

| 번들 | 크기 | 이 Mac의 SHA-256 | 기존 큐 UUID / 결과 / KST |
| --- | --- | --- | --- |
| Always robust |519 B|`4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a`|`bde5e370-4dba-4f19-8291-4a998bfecdcd`,7/14,10-24 19:01:28 |
| Length/digit |1387 B|`30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`|`0c736e59-8248-4dee-8e4f-2df037c552d7`,7/14,10-24 19:03:37 |

두 번들 모두 root small.txt, CRC 정상이며 기대 해시와 일치한다. 이번 실행의 큐·공식 Codabench 재제출은0건이다. 영수증은 hash-verified 공개API뷰이고 UUID→번들 연결은 직접 사용자/핸드오프에 따른다. M5 native owner 영수증이나 복구키를 회수했다고 표시하지 않았다. 최종 테스트 결과는 여전히 미측정이다.

## PDF 및 검증

| 변형 | 본문/전체 | Type3 | v3 일반 모드 | SHA-256 |
| --- | --- | --- | --- | --- |
| **익명 제출 후보** |5/10쪽|0|**PASS19/19,exit0**|`2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51` |
| 기명 보관용 |5/10쪽|0|18/19,익명화만 의도된FAIL|`c8be7a4f3c4fac8da00d1c7c05f6edef9e17f2e974e97b8a190c371eb9927cc0` |

숫자 재생성·registry check는 **164/164,exit0**이며 기존152개 claim 레코드와 기존 number 값 전부 동일하다. 원본 영수증에서 결과·UUID·KST시각·fair-coin p값12개 키만 추가했다. 원본SHA변조·누락·잘못된상태 등 새 경계시험15개와 source-aware 렌더가 통과했다. `submission_text_gate.py`는 CLEAN·exit0. 독립 기계 fidelity는27/27, 미보고 차이0. 두 PDF 전체20쪽을 렌더 검토했다. 익명본은 텍스트·metadata·실제 링크URI의 식별 문자열 검출0건이다.

본문은 실제5쪽에서 끝나고6쪽은 Limitations로 시작한다. 게이트의3줄 허용 오차를 이용하지 않았다. Limitations+AI는6쪽,References7쪽,AppendixA8–9쪽,B9–10쪽이다. 전체9→10쪽 증가는 E11의 명시적 구분·부록 재배치에 따른 의도된 변경이며, 본문 한도는5쪽이다.

## 텍스트·형식 변경

- E4: 초록, 옛§4.1, Limitations의 미측정/예정/대기 baseline 설명을 영수증 기반7/14 관측으로 바꾸고 fair-coin 비교만 사용했다. 다른 owner와의 paired 비분리 결론은 넣지 않았다. 최종 테스트 미측정 한계는 보존했다.
- E11: §1–§3 본문, Limitations, AI, References, AppendixA(옛§4), B(옛§6)로 재배치했다. 표6개 내용과 선언된 가정은 그대로이며 **§2.3 축약도 필요 없었다**.
- E12: Korea 위치 문구를 KST로 정리하고 익명본의 저장소URL2건을 지정 mirror URL로 바꿨다. 익명 metadata를 유지하고 검색 가능한 자기 source commit은 익명본에서만 마스킹했다. 기명본 URL·source commit은 그대로다. 초록[11]은 removal 문장 뒤로 옮겼다.
- 잠긴 v3와의 문법 정규화: E4 UUID마다 단수형 `submission id`를 사용했다. 부록 이동으로 범위 밖이 되는 CPU 비용 설명은 초록에 사실 그대로 남겼다. 게이트 바이트는 바꾸지 않았다.
- 공식 NeurIPS style·폰트·여백·표 caption은 유지했다. 전체 pdftotext diff와 이동 블록 검증 결과는 `results/v8.3/fidelity/`에 있다.

원고값은 공개API 출처와 직접 제공된 연결을 명시적으로 구분하는 별도 queue guard를 통과한다. 기존 숫자 Codabench guard·PREREG·canonical UNMEASURED 파일은 바이트 단위로 보존했다. 잘못된 queue source는 초록/Limitations의 stale 숫자도 출력하지 못하도록 전체 렌더를 차단한다.

## 대기 상태

**G-LOOK 대기**: 실제 익명 PDF를 연 뒤 `v8.3 PDF 확인` 메시지가 필요하다. 그 전에는 `AUTHOR_APPROVAL_v8.3.json`을 만들지 않는다. 기존 v8.1 G-AUTHOR는 보존했다.

T3 push, G-MIRROR 생성·검증, OpenReview 인증/업로드/노트 생성/수정은 미실행이다. PDF의 mirror URL 표기는 실제 mirror 준비를 뜻하지 않는다. 이후 OpenReview는 제1저자당 최초 노트1건만 만들고 모든 후속 변경은 동일 note.id의 수정본으로 처리한다. 기존 예약도 새 PDF 확인 전에는 POST/push/업로드를 하지 않도록 정리했다.

현재 요청된 범위는 **T1 완료 → PDF 확인 대기**다. 메일·Discord 발송0건. 빌드 JSON은 `results/v8.3/BUILD.json`과 `v8-execution/BUILD_v8.3.json`에 있다.
