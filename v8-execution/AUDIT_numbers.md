# Numeric evidence audit: 158 versus 164

**158/158 출처는 현재 Mac Studio 근거로 UNVERIFIABLE이며, 164/164는 원시 실행 로그로 확인됩니다.** 두 숫자는 PDF 자체에 실행한 검사 건수가 아닙니다. `report_numbers.py --check`는 고정 데이터에서 수치를 재생성해 claims 레지스트리와 대조하며 PDF를 입력받지 않습니다.

| 보고된 항목 | PDF SHA-256 | 커밋·명령·원시 stdout | 판정 |
| --- | --- | --- | --- |
| 08:53의158/158 | UNVERIFIABLE | 원래 실행의 commit, command, stdout 모두 미확보 | HANDOFF_v10.3의 주장만 확인. 이 Mac의 `v84-execution/rebuild` 및 문서의 M5 경로 없음 |
| 08:59의164/164 | 그 시각 보고서와의 직접 연결은 UNVERIFIABLE | 아래 별도 로컬164 실행은 완전한 원시 근거로 확인. 이를08:59 원본 영수증으로 재명명하지 않음 | 독립 검증: PASS164/164, exit0, 불일치0,21.14초 |

검증된164 실행의 소스 캡처 커밋은 `33328fed2a38255f8a85b9d6ae1d54672c44e3bf`입니다. Claims SHA-256은 `c0213e5f470206f619bf3481a1d4f1d225e2cbf09f5135ed638c07044a3f8e4c`입니다. 영수증 메타데이터의 기록 시각은 `2026-10-26T16:27:41.074080+00:00`(10-27 01:27:41 KST)이며, 이는08:59 원본 보고 시각의 증명이 아닙니다. 이번 감사에서는 완전한 기존 원시 로그를 바이트 그대로 복사하고 해시 대조했으며 숫자 실험을 다시 실행하지 않았습니다.

정확한 실행 명령(원시 argv는 `report_numbers.command.json`):

```sh
'/Users/felix/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v6-execution/work/v10-execution/numeric-runtime/env/bin/python' -I -X importtime '/Users/felix/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v6-execution/work/v10-execution/numeric-runtime/individual-recovery/repro/tools/report_numbers.py' --data-dir '/Users/felix/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v6-execution/work/v10-execution/numeric-runtime/individual-recovery/repro/data' --check '/Users/felix/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v6-execution/work/v10-execution/numeric-runtime/individual-recovery/repro/research/claims.json' --out '/Users/felix/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v6-execution/work/v10-execution/numeric-runtime/individual-recovery/report_numbers.json'
```

원시 stdout 전체(58바이트; tail도 동일):

```json
{
 "result": "PASS",
 "checked": 164,
 "mismatches": []
}
```

원시 stdout SHA-256: `73166acfad805a5f741a3090654aed427d5899451c6edf762eb2cca01e1f5f9e`. 원시 stderr SHA-256: `090bfe9ab97e08f678ca94538230edd001b72112b0aad384d8bcb6a5b9bfe169`. 사본은 `v10-execution/audit-v10.3/numbers/report_numbers.stdout.txt` 및 `report_numbers.stderr.txt`입니다. 기존 `NUMERIC_RECOVERY.json`과 이전 `UNRUN` 기록은 수정하지 않았습니다.

현재 Studio 익명 PDF SHA-256은 `2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51`입니다. 이번에 검토용 PDF 바이트를 다시 해시했고 `results/v8.3/BUILD.json`의 PDF 해시와 일치했습니다. `v8-execution/BUILD_v8.3.json`은 같은 PDF의 소스·산출물 캡처 커밋을33328fe로 연결합니다. **이는 build receipt를 통한 artifact association이며 숫자 도구가 PDF의 모든 인쇄 수치를 직접 검사했다는 뜻은 아닙니다.** 원래08:53/08:59 보고서 쌍을 확보하지 못했으므로 그 둘 사이 PDF 변경·재빌드 여부와 변경 소스의 byte delta는 UNVERIFIABLE입니다. 현재 Studio PDF의 불변성으로 M5의 두 보고서를 대신 증명하지 않습니다.

현재 registry를 직접 세면 고유 키164개이며, queue 키12개를 제외한152개와 정확히 분리됩니다. 역사적 `frozen_claims_preserved.json`은 원래152개 기록이 동일하고12개를 추가했다고 기록합니다. 이전144ce58 registry의 독립 `git show`는8초 제한을 초과했으므로 이 역사적 동일성은 해당 보존 영수증의 기록으로 구분합니다. 두 queue 각각6개인 실제 키와 위치는 `REGISTRY_COUNTS.json`에 있습니다. **이 구성은158의 원인을 입증하지 않습니다.** 첫 queue6개만 포함한158 검사였다는 원시 registry/command/stdout이 없어 그런 설명을 채택하지 않았습니다.

H2용 한 줄: **“158/158은 원본 영수증 미확보로 UNVERIFIABLE;164/164는33328fe의 고정 데이터·claims 대조 원시 로그로 확인했으며(PASS, 불일치0), PDF2edf06ab…82e51과의 연결은 build receipt 근거입니다.”**

감사 범위와 파일 해시는 `v10-execution/audit-v10.3/numbers/SEARCH_RECEIPT.json`, `EXECUTION_164.json`, `PDF_ASSOCIATION.json`, `REGISTRY_COUNTS.json`, `SHA256SUMS`에 있습니다. 새 과학 분석·공식 조회·인증·업로드·push·커밋은 수행하지 않았습니다.
