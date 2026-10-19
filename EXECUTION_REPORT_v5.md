# v5 실행 보고 — 공개 재현 완료, 소유자 제출 대기

2026-10-20 KST: 소유자의 직접 공개 승인 후 저장소를 게시했다.
https://github.com/testofschool/aimo-interp-abc

공개 commit `6fef8753b2e21b0c53098e77fdbc6e72ad4d4251`를 인증 없이 새로 복제하고
별도 venv와 실제 HF download로 V1-V4를 검증했다. 원본 V1 13/13, 원본 V2 17,
최종 V1 87/87, 최종 V2 89, V3 12개 값, V4 CLOSED/exit1이 모두 기대값대로다.
ZIP 재빌드와 TeX 재생성도 byte-identical이다. 보고서 PDF는 동일한 5쪽/SHA256을
유지했다. 원문 공개-clone 출력과 영수증은 `PUBLICATION.md` 및
`results/v5/publication/`에 있다. 추가 GPU job/지출은 0이다.

R3와 acceptance1의 공개-repo clone 부분은 완료됐다. 소유자 Codabench 업로드,
점수·screenshot/time·nomination, author review, OpenReview 최종 form/rules·receipt는
남아 있다. private validation/test는 UNMEASURED이며 전체 목표 완료를 주장하지 않는다.
아래 내용은 공개 이전의 실행·검증 기록으로 보존한 역사적 snapshot이다.

---

# v5 실행 보고 — 로컬 보고서 준비 완료, 외부 게시·제출 미완료

직접 요청 `/goal run`과 제공된 v5 파일을 바탕으로 CPU 보고서 작업을 진행했다.
첨부 문서의 과거 소유자 발언, 외부 게시 요청, 계정 작업을 독립적인 직접 지시로
승격하지 않았다. 원본 작업 상태를 `../v5-execution/pre-v5-checkpoint.tar.gz`와
파일별 SHA256 목록으로 먼저 보존했다. 원본 ZIP SHA256은
`b244a735770b024dc7302ad9a2098ba71c06aac7c14f09393ffc93c3bd6ebc0a`다.
독립 HANDOFF_v5.md와 ZIP 내부 파일은 byte-identical이다.

## 검증 결과

| 검증 | 결과 | 실제 exit | 범위 |
|---|---|---:|---|
| 원본 V1 | PASS, 13/13 | 0 | 제공된 원래 claims |
| 원본 V2 | PASS, 17 placeholders | 0 | 제공된 원래 outline |
| V3 | PASS, 등록값 12개 일치 | 0 (runner) | 표의 중첩 key를 포함한 주요 값 |
| V4 | CLOSED | 1 | 기대된 방법 재개 중단 상태 |
| 최종 V1 | PASS, 87/87 | 0 | 확장한 모든 scalar numeric keys |
| 최종 V2 | PASS, 89 placeholders | 0 | 현재 본문, registry 값 대조 포함 |
| PDF | PASS, 5쪽 | 0 | 4쪽 본문 + 1쪽 references |
| PDF 렌더·폰트·숫자 | PASS | 0 | 전 5쪽 시각 확인, Type-3 0, 미해결 참조 0, 35개 decimal token 존재 |
| 새 로컬 clone | PASS | 0 | 별도 venv/실제 pinned download/전체 CPU gate/ZIP/TeX 재생성 |

원본 검증 stdout/stderr: `results/v5/{V1,V2,V4}.{stdout,stderr}` 및
`preregistered_receipt.json`. 현재 저장소 전체 재현 출력은
`results/v5/repository_reproduction.stdout`, 구조화 영수증은
`repository_reproduction.json`이다. 아래는 실제 stdout 일부이며, 전체 출력은
파일에 보존했다.

```text
V1_original actual exit 0
{
 "result": "PASS",
 "checked": 13,
 "mismatches": []
}
V1_final actual exit 0
{
 "result": "PASS",
 "checked": 87,
 "mismatches": []
}
V3 PASS: 12 registered values
V4 actual exit 1
{"result": "CLOSED", "reason": "no self-made labels supplied; method track stays folded"}
ALL_CPU_GATES_PASS; V4_CLOSED_EXPECTED
```

## 핵심 claims

| Key / 정의 | 재현값 | 해석 |
|---|---:|---|
| r2_problem_train_multi | 0.7822 (76행/18문제) | 동일 관측행의 문제평균 분산분해, multi-configuration |
| r2_problem_train_true_multi | 0.7369 (70행/15문제) | 실제 multi-checkpoint 문제만; effort행 유지 |
| r2_problem_small_multi | 0.7811 (39행/14문제) | Small만 포함한 분산분해 |
| r2_problem_sample_full | 0.1813 | 다른 panel/configuration/coverage, 통제된 일반화 비교 아님 |
| Small concordance | 11/11, Bernoulli reference 4.89 | p-value나 인과적 null 검정 아님 |
| no-gap concordance | 10/15, reference 3.59 | 모든행 threshold + gpt-oss worst-effort collapse |
| control Small LOPO | bacc 0.6855; acc 0.7674 | 전체 labelled80에서 문제 제외 학습, Small43 평가 |
| always robust Small | bacc 0.5000; acc 0.7209 | 맞힌 행 31/43; control은 33/43 |
| control bacc CI95 | [0.4759, 0.9378] | 22문제, fixed OOF, 정렬 cluster, RNG seed0, 4000회 |
| paired delta CI95 | [-0.0241, 0.4378] | 0 포함; 정식 검정력/MDE 결과 아님 |
| agg format flag | bacc/acc 1.0 | 141개 관측행의 완벽한 연관, 구성 원인의 증명 아님 |
| agg majority | acc 0.7447 | sample 개발자료 caveat |

전체 87개 값은 `report/CLAIMS_TABLE.md`, 숫자 원장은 `research/claims.json`,
계산 결과는 `results/report_numbers.json`에 있다. 고정된 외부 인용값과 protocol
literal의 출처는 `report/ALLOWED_LITERALS.txt`에 있다. 원래 13개 수치는 그대로
통과했다. `tools/report_numbers.py`는 데이터 해시가 다르면 계산 전에 STOP한다.
잘못된 literal/미등록 key/불일치 값/없는 key를 렌더러가 거부하는 것도 확인했다.
합성 guard 테스트는 과학적 실험 결과로 집계하지 않는다.

## PDF와 과학적 수정

`report/aimo-interp-report-v5.pdf` SHA256:
`1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf`.
공식 NeurIPS 스타일을 수정 없이 포함한 standalone source를 만들었고 desktop
compiler와 pdfTeX 두 경로가 성공했다. Inline bibliography이므로 BibTeX를 실행하지
않았다. 최종 5쪽 PNG를 실제로 확인했다. exact source/kit/style hashes와 build
영수증, page renders는 `report/source_provenance.json`, `render_qa_v5.json`,
`report/qa_v5/`에 있다. PDF binary의 다른 환경 byte 재현은 주장하지 않는다.

v5 숫자는 맞았지만 문서 해석에 다음 수정이 필요했다. 문제별 평균의 R²를
미지 문제 예측 성능으로 표현하지 않았다. 다른 행/metric의 organizer probe와
control이 일치하거나 우월하다는 문구를 삭제했다. 76행 중 effort 반복만 있는
문제 3개를 명시하고 별도 checkpoint sensitivity를 계산했다. sample identifiers는
일부 기반 checkpoint가 겹치므로 전부 다른 모델이라고 하지 않았다. 기존
unscripted power note의 CI/MDE를 현재 결과로 사용하지 않고 완전히 명시한 bootstrap을
추가했다. Omni-MATH/Monte Carlo raw source가 없어 외부 시도 수치는 싣지 않았다.
관측되지 않은 white-box 효과를 과학적 음성 결과로 바꾸지 않았다.

주최 측 primary sources와 경쟁 참가자의 공개 결과를 확인하고 겹치는 선행작업을
인용했다. exhaustive novelty 주장은 삭제했다. raw source cache 43개는 별도
`../v5-execution/sources/`에 있으며 출처·byte·hash·검증등급 ledger만 공개 export에
포함했다. 외부 연구 결과는 저자의 보고를 확인한 것이며 직접 GPU 재실행한 것은
아니다. 공개 train label rule과 공개되지 않은 private label rule도 구분했다.

## 번들·비용·계정 상태

원본 control Small ZIP은 변경하지 않았다:
`30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`.
공식 pinned builder로 always-true Small ZIP을 새로 만들었다:
`4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` (519 bytes).
Pinned host harness에서 후자는 coverage 1.0, invalid 0, public-sample accuracy
0.375를 보였고 exit0이다. GPU image parity나 private evaluation은 아니다.

사용자가 현재 대화에서 Codabench 계정은 `testofschool`, 아직 제출 전이라고
확인했다. `kangmin` 행은 우리 결과로 쓰지 않았다. 보고서 section4에 control과
always-true private validation/test UNMEASURED 및 필요한 limitation을 넣었다.

추가 GPU job 0, 추가 지출 $0. 기존 J0 누적 $0.412497는 이전 영수증의 역사적
값이며 이번에 청구 계정을 다시 조회하지 않았다. 방법 트랙 FOLDED, White-Box
Award OUT, V4 CLOSED를 유지했다.

## 공개 준비와 남은 수락 조건

공개용 export는 `../v5-execution/public-release/`에 별도 Git 저장소로 준비했다.
Git author는 `felix <gangjeongmin23@gmail.com>`이다. 원본 repo의 v4 미커밋 변경과
history는 강제로 정리하거나 public history로 전송하지 않았다. 공개 export는
parquet·변환된 sample/reference·이전 GPU launcher/log를 포함하지 않는다.
해시 고정 HF fetcher는 네 파일의 fresh download, offline verify, mismatch STOP을
통과했다. 데이터 원장과 파일별 release inventory를 함께 제공한다.

**외부 작업 미완료:** GitHub 저장소 생성/push 및 public HEAD/fresh-clone 영수증,
Codabench 업로드·private점수·owner screenshot/time, Discord final-test nomination,
human author review, actual OpenReview form 확인·제출·receipt. 로컬 검증을 public
검증이나 제출로 올려 표시하지 않았다. 첨부문서 R3만을 외부 공개 확정 권한으로
간주하지 않았고, 구체적인 공개 artifact 준비를 마친 후 소유자에게 넘긴다.

`OWNER_CHECKLIST_v5.md`에 정확한 bundle 두 개와 다음 owner action을 기재했다.
Codabench close는 2026-11-01 11:55Z이고, website의 report due는 November15다.
정확한 report cutoff hour/timezone과 최종 portal rules는 미확인이다. November15-30에
최대 세 편 peer-review 의무를 report/checklist에 명시했다.

전체 목표는 외부 수락 조건이 남아 있으므로 완료 처리하지 않았다. 파일별
build-input 변경과 해시는 `BUILD_INPUT_CHANGES_v5.md` / `results/v5/working_tree_changes.json`에
기록한다. 기존 네 parquet와 강화된 grouped_eval/submit_gate, original kill_reports는
변경하지 않았음을 pre-v5 해시와 대조했다.

## 새 로컬 clone readback

검증한 코드 commit은 `6e9003b47ab624310f08a4a78192046da9671370`이다.
별도 venv에 고정 dependencies를 설치하고 HF에서 네 파일을 실제로 내려받아
V1 13/13, V2 17, 최종 V1 87/87, 최종 V2 89, V3 12개, V4 CLOSED/exit1을
확인했다. 원본 control ZIP 두 버전은 byte-identical로 재빌드했고 standalone
TeX SHA256도 `95e9dde2250115e4a2475325a8719aa29527ac0992305257ab5ee2d1f3fa242b`로
일치했다. 영수증과 명령별 원문 출력은 `results/v5/fresh_local_clone/`에 있다.

```text
V1_original actual exit 0
{
 "result": "PASS",
 "checked": 13,
 "mismatches": []
}
V2_original actual exit 0
{"result": "PASS", "placeholders": 17, "out": "/var/folders/14/76vt1lk92056gjht3hr6xwq00000gn/T/aimo-report-plewlrqd/original.md"}
V1_final actual exit 0
{
 "result": "PASS",
 "checked": 87,
 "mismatches": []
}
V3 PASS: 12 registered values
V2_final actual exit 0
{"result": "PASS", "placeholders": 89, "out": "/var/folders/14/76vt1lk92056gjht3hr6xwq00000gn/T/aimo-report-plewlrqd/final.md"}
V4 actual exit 1
{"result": "CLOSED", "reason": "no self-made labels supplied; method track stays folded"}
ALL_CPU_GATES_PASS; V4_CLOSED_EXPECTED
```

이 검증은 local repository를 source로 한 fresh clone이다. public remote의
HEAD 확인이나 public fresh-clone acceptance를 대체하지 않는다. 테스트 이후
추가되는 실행보고/receipt/inventory 문서만 별도 export commit에 기록하며
계산·렌더·fetch·source 생성 코드와 scientific manuscript/PDF는 변경하지 않는다.
