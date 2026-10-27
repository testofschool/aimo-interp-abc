#!/usr/bin/env python3
"""Validate own native outputs and publish aggregate preregistered analysis only.

No network, authentication, uploads, gold-label reads or model execution. Private
item identifiers and predictions stay in process memory and the external cache.
"""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'v9-execution/official-analysis'
CACHE = Path.home() / '.cache/aimo-official-outputs'
EXPECTED = [
    (1012526, 'solution-always-true-small.zip', '4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a'),
    (1012549, 'solution-text-length-control-small.zip', '30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd'),
    (1012564, 'bundle3-trained-probe-small.zip', '852fff17372ebdcf967549a4270339a2e792372c1b5496da968b2df884ccc67b'),
]
PROTOCOL_SHA = '1fade7edee89a5086766afdf1ebe8cfb61ea6e5f53e3d4adbeb91bbc5d5dbad5'
PREREG_SHA = 'c8f4d89a0a4efca1f458e65c61167551056bd34ade8d542db5682a56545d3ddc'
SCORER_SHA = 'df10d76c79129220aba37f0a23300df8d220c46af5dabec4dd20ad09fdda6191'
ORGANIZER_REV = 'de794053debe75a711400696e66b60937cebbb1b'
KST = timezone(timedelta(hours=9))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, code):
    if not condition:
        raise ValueError(code)


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.utcoffset() is not None, 'TIMEZONE_REQUIRED')
    return parsed


def number(value):
    require(type(value) in (str, int, float, Decimal), 'INVALID_NUMERIC_TYPE')
    result = Decimal(str(value))
    require(result.is_finite(), 'NONFINITE_NUMBER')
    return result


def zip_check(path):
    raw = path.read_bytes()
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), 'DUPLICATE_ZIP_MEMBER')
        for info in infos:
            name = info.filename
            require(name and not name.startswith('/') and '\\' not in name and ':' not in name,
                    'UNSAFE_ZIP_PATH')
            require('..' not in PurePosixPath(name).parts, 'UNSAFE_ZIP_PATH')
            require(not stat.S_ISLNK(info.external_attr >> 16), 'ZIP_SYMLINK')
            require(not info.flag_bits & 1, 'ENCRYPTED_ZIP')
        require(archive.testzip() is None, 'ZIP_CRC_FAILURE')
    return {'sha256': sha(raw), 'bytes': len(raw), 'member_count': len(names),
            'crc_ok': True, 'unique_safe_paths': True}


def read_member(path, basename):
    with ZipFile(path) as archive:
        names = [n for n in archive.namelist() if PurePosixPath(n).name == basename]
        require(len(names) == 1, 'REQUIRED_MEMBER_NOT_UNIQUE')
        return archive.read(names[0])


def api_scores(receipt):
    require(receipt.get('owner') == 'testofschool' and receipt.get('status') == 'Finished',
            'NATIVE_OWNER_OR_STATUS_MISMATCH')
    require(receipt.get('phase') == 30038 and receipt.get('task', {}).get('id') == 36241,
            'NATIVE_SMALL_TASK_MISMATCH')
    result = {}
    for row in receipt['scores']:
        key = row.get('column_key')
        if key in {'accuracy', 'coverage', 'invalid_predictions'}:
            require(key not in result, 'DUPLICATE_NATIVE_SCORE_KEY')
            result[key] = number(row['score'])
    require(set(result) == {'accuracy', 'coverage', 'invalid_predictions'}, 'MISSING_NATIVE_SCORE_KEY')
    return result


def run():
    OUT.mkdir(exist_ok=True)
    score_path = ROOT / 'v9-execution/SCORES.json'
    journal_path = ROOT / 'v9-execution/official-upload-journal.json'
    score_raw, journal_raw = score_path.read_bytes(), journal_path.read_bytes()
    scores, journal = json.loads(score_raw), json.loads(journal_raw)
    prereg_path = ROOT / 'v9-execution/PREREG.md'
    protocol_path = ROOT / 'v9-execution/paired_protocol.py'
    require(sha(prereg_path.read_bytes()) == PREREG_SHA, 'PREREG_BYTES_CHANGED')
    require(sha(protocol_path.read_bytes()) == PROTOCOL_SHA, 'PROTOCOL_BYTES_CHANGED')
    prereg_receipt = json.loads((ROOT / 'v9-execution/PREREG_COMMIT.json').read_text())
    require(prereg_receipt['prereg_sha256'] == PREREG_SHA, 'PREREG_RECEIPT_HASH_MISMATCH')
    prereg_time = timestamp(prereg_receipt['commit_time_KST'])
    commit_recheck = {'status': 'PRIOR_GIT_COMMIT_RECEIPT_USED'}
    try:
        result = subprocess.run(['git', 'show', '-s', '--format=%H%n%cI', prereg_receipt['commit']],
                                cwd=ROOT, capture_output=True, text=True, timeout=5, check=True)
        lines = result.stdout.splitlines()
        require(lines[0] == prereg_receipt['commit'] and timestamp(lines[1]) == prereg_time,
                'GIT_PREREG_TIME_MISMATCH')
        commit_recheck = {'status': 'CURRENT_GIT_METADATA_RECHECK_MATCH', 'commit_time': lines[1]}
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        commit_recheck['current_git_read'] = 'UNAVAILABLE_BOUNDED_READ; prior actual-Git receipt preserved'
    scorer_path = ROOT / 'v9-execution/gs/components/scoring_program/scoring.py'
    scorer_raw = scorer_path.read_bytes()
    require(sha(scorer_raw) == SCORER_SHA, 'SCORER_BYTES_CHANGED')
    frozen = subprocess.run(['git', 'show', ORGANIZER_REV + ':components/scoring_program/scoring.py'],
                            cwd=ROOT / 'v9-execution/gs', capture_output=True, timeout=5, check=True)
    require(frozen.stdout == scorer_raw, 'FROZEN_SCORER_SOURCE_MISMATCH')
    for fragment in [b'total = len(labels)', b'accuracy = correct / total',
                     b'coverage = covered / total',
                     b'invalid_predictions = (total - covered) + structural_errors']:
        require(fragment in scorer_raw, 'UNWEIGHTED_BINARY_CONTRACT_NOT_ESTABLISHED')
    require(len(scores['runs']) == len(journal['bundles']) == 3, 'EXACT_THREE_RUNS_REQUIRED')
    rows, maps, raw_sources = [], [], []
    for order, (submission_id, filename, expected_sha) in enumerate(EXPECTED, 1):
        row = scores['runs'][order - 1]
        entry = journal['bundles'][order - 1]
        require(row['submission_id'] == entry['submission_id'] == submission_id, 'RUN_BINDING_MISMATCH')
        require(row['name'] == entry['name'] == filename and row['sha256'] == entry['sha256'] == expected_sha,
                'FROZEN_BUNDLE_REGISTRY_MISMATCH')
        require(row['state'] == entry['state'] == 'ACCEPTED_FINISHED', 'RUN_NOT_NATIVE_FINISHED')
        require(entry.get('upload_attempts') == 1, 'UPLOAD_ATTEMPT_COUNT_NOT_ONE')
        paths = {kind: CACHE / str(submission_id) / kind for kind in
                 ('submitted-bundle.zip', 'prediction_result.zip', 'scoring_result.zip')}
        zips = {kind: zip_check(path) for kind, path in paths.items()}
        require(zips['submitted-bundle.zip']['sha256'] == expected_sha, 'SERVER_BUNDLE_BYTES_MISMATCH')
        prediction_raw = read_member(paths['prediction_result.zip'], 'predictions.jsonl')
        summary_raw = read_member(paths['prediction_result.zip'], 'ingestion_summary.json')
        scoring_raw = read_member(paths['scoring_result.zip'], 'scores.json')
        predictions = [json.loads(line) for line in prediction_raw.decode('utf-8').splitlines() if line.strip()]
        summary = json.loads(summary_raw)
        scored = json.loads(scoring_raw, parse_float=Decimal)
        require(predictions and all(isinstance(r, dict) for r in predictions), 'PREDICTION_SCHEMA_INVALID')
        require(all(set(r) == {'id', 'is_robust', 'valid'} for r in predictions), 'UNEXPECTED_PREDICTION_FIELDS')
        require(all(isinstance(r['id'], str) and r['id'] for r in predictions), 'UNSTABLE_ITEM_ID')
        require(len({r['id'] for r in predictions}) == len(predictions), 'DUPLICATE_ITEM_ID')
        require(all(type(r['is_robust']) is bool and type(r['valid']) is bool and r['valid'] for r in predictions),
                'PREDICTIONS_NOT_COMPLETE_VALID_BINARY')
        require(type(summary.get('cases')) is int and summary['cases'] == len(predictions), 'SUMMARY_CASE_COUNT_MISMATCH')
        for key in ('invalid_predictions', 'timeouts', 'skipped_for_deadline'):
            require(type(summary.get(key)) is int and summary[key] == 0, 'INGESTION_INVALID_OR_SKIPPED')
        native = api_scores(row['native_receipt'])
        small = api_scores(row['small_score_receipt'])
        require(row['native_receipt']['id'] == row['small_score_receipt']['id'] == submission_id,
                'NATIVE_RECEIPT_BINDING_MISMATCH')
        require(set(scored) == set(native) and all(number(scored[k]) == native[k] == small[k] for k in native),
                'SCORING_JSON_NATIVE_API_MISMATCH')
        require(all(number(row['native_score_values'][k]) == native[k] == number(row[k]) for k in native),
                'SAVED_RAW_SCORE_MISMATCH')
        require(native['coverage'] == 1 and native['invalid_predictions'] == 0 and 0 <= native['accuracy'] <= 1,
                'COMPLETE_UNWEIGHTED_SCORE_PRECONDITION_FAILED')
        n = len(predictions)
        k_exact = native['accuracy'] * n
        require(k_exact == k_exact.to_integral_value(), 'ACCURACY_NOT_EXACT_INTEGER_COUNT')
        created = timestamp(row['native_receipt']['created_when'])
        require(created > prereg_time, 'SUBMISSION_PRECEDES_PREREG')
        require(row.get('finished_time_KST') is None, 'DO_NOT_REINTERPRET_EXACT_FINISH_TIME')
        maps.append({r['id']: r['is_robust'] for r in predictions})
        raw_sources.append({'run_order': order, 'prediction_member_sha256': sha(prediction_raw),
                            'ingestion_summary_sha256': sha(summary_raw), 'scores_member_sha256': sha(scoring_raw)})
        rows.append({'run_order': order, 'bundle': filename, 'native_submission_id': submission_id,
                     'native_small_task': 36241, 'native_phase': 30038, 'status': 'Finished',
                     'zips': zips, 'prediction_rows': n, 'unique_ids': n,
                     'all_prediction_rows_valid_binary': True, 'summary_cases': summary['cases'],
                     'summary_invalid_predictions': 0, 'summary_timeouts': 0, 'summary_skipped': 0,
                     'native_scoring_json_matches_api': True,
                     'accuracy_native_raw': str(native['accuracy']), 'coverage_native_raw': str(native['coverage']),
                     'invalid_predictions_native_raw': str(native['invalid_predictions']), 'N': n, 'k': int(k_exact),
                     'count_identification': 'public unweighted binary scorer + native full coverage/zero structural invalid + unique valid predictions count',
                     'native_created_when': row['native_receipt']['created_when'],
                     'native_created_KST': created.astimezone(KST).isoformat(),
                     'native_exact_finished_time': None,
                     'native_exact_finished_time_status': 'NOT_EXPOSED_BY_SAVED_NATIVE_API',
                     'observed_finished_KST': row['observed_finished_KST']})
    require(all(len(m) == 14 for m in maps), 'EXPECTED_14_ITEM_CONTRACT_MISMATCH')
    all_same_ids = all(set(m) == set(maps[0]) for m in maps[1:])
    require(all_same_ids, 'REAL_ITEM_ID_SETS_DIFFER')
    spec = importlib.util.spec_from_file_location('unchanged_paired_protocol', protocol_path)
    protocol = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(protocol)
    contract = {'same_evaluation_items': True, 'unweighted_binary_accuracy': True,
                'probe_coverage': 1.0, 'control_coverage': 1.0,
                'probe_invalid_predictions': 0, 'control_invalid_predictions': 0}
    paired = protocol.from_binary_predictions(maps[2], maps[1], rows[2]['k'], rows[1]['k'],
                                              alpha=0.05, validated_contract=contract)
    analysis = protocol.analyze(14, rows[2]['k'], rows[1]['k'], joint=paired['table'], alpha=0.05)
    chronology = {'prereg_commit': prereg_receipt['commit'], 'prereg_commit_time_KST': prereg_time.astimezone(KST).isoformat(),
                  'prereg_sha256': PREREG_SHA, 'current_git_metadata_recheck': commit_recheck,
                  'native_probe_created_KST': rows[2]['native_created_KST'],
                  'seconds_prereg_to_probe_submission': (timestamp(rows[2]['native_created_when']) - prereg_time).total_seconds(),
                  'status': 'PREREG_PRECEDES_NATIVE_PROBE_SUBMISSION',
                  'prior_official_results_seen': scores['exploratory'],
                  'scope': 'Local actual-Git prereg receipt and native server submission creation; not a fabricated server finish time'}
    recorded = datetime.now(timezone.utc).isoformat()
    native_check = {'schema_version': 1, 'recorded_at_utc': recorded, 'status': 'PASS',
                    'scope': 'Own native Small outputs; aggregate-only verification; no gold-label access',
                    'scorer_contract': {'organizer_commit': ORGANIZER_REV, 'source_sha256': SCORER_SHA,
                        'frozen_git_source_match': True, 'unweighted_binary_accuracy': True,
                        'denominator_proof': 'coverage=covered/total=1 and invalid=(total-covered)+malformed+duplicate+extra=0; all unique valid predictions therefore cover exactly the reference cases; count14 and accuracy0.5 give k7',
                        'server_deployment_source_hash_authenticated': False,
                        'deployment_limit': 'Frozen official source and native schema/values establish the declared reference contract; server deployment bytes and private reference hash are not exposed.'},
                    'runs': rows, 'same_real_item_id_sets_all_three': all_same_ids,
                    'individual_item_ids_or_prediction_rows_published': False,
                    'raw_native_outputs_remain_outside_git': True, 'raw_member_sha256': raw_sources,
                    'prereg_chronology': chronology,
                    'input_receipts': {'SCORES_sha256': sha(score_raw), 'journal_sha256': sha(journal_raw)},
                    'source_receipts_unchanged_during_analysis': sha(score_path.read_bytes()) == sha(score_raw) and sha(journal_path.read_bytes()) == sha(journal_raw),
                    'no_signed_urls_in_outputs': True}
    ablation = {'schema_version': 1, 'recorded_at_utc': recorded, 'status': 'MEASURED_PREREGISTERED_COMPARATIVE_CONTROL',
                'comparison': 'organizer trained probe bundle3 minus frozen length-and-digit control bundle2',
                'label': 'comparative control, not causal white-box signal ablation',
                'scope': 'Official Small validation task36241, same14 native stable item IDs; conditional iid paired reference only',
                'preregistered': True, 'exploratory': scores['exploratory'], 'prereg_chronology': chronology,
                'pairing_route': paired['pairing_source'], 'validated_score_contract': contract,
                'native_validation': 'v9-execution/NATIVE_OUTPUT_CHECK.json',
                'paired_protocol_sha256': PROTOCOL_SHA, 'primary': analysis['primary'],
                'secondary_paired_n80': analysis['secondary'], 'pvalue': analysis['primary']['pvalue'],
                'N80': analysis['secondary']['first_n'],
                'reporting': {'equivalence_claim_allowed': False, 'black_box_sufficiency_claim_allowed': False,
                    'absence_of_white_box_benefit_claim_allowed': False, 'causal_signal_ablation_claim_allowed': False,
                    'final_test_ranking_claim_allowed': False,
                    'problem_cluster_structure': 'UNMEASURED; iid conditional reference, not cluster-robust inference',
                    'reference_label_stability': 'Same native task/phase and stable matched case IDs; private reference hash not exposed; no individual labels reconstructed'},
                'sources': analysis['sources']}
    (ROOT / 'v9-execution/NATIVE_OUTPUT_CHECK.json').write_text(json.dumps(native_check, indent=2) + '\n')
    (ROOT / 'v9-execution/ABLATION.json').write_text(json.dumps(ablation, indent=2) + '\n')
    receipt = {'schema_version': 1, 'recorded_at_utc': recorded, 'status': 'PASS',
               'script_sha256': sha(Path(__file__).read_bytes()), 'protocol_sha256': PROTOCOL_SHA,
               'outputs': {name: sha((ROOT / 'v9-execution' / name).read_bytes()) for name in
                           ['NATIVE_OUTPUT_CHECK.json', 'ABLATION.json']},
               'private_cache_read_only': True, 'raw_output_files_copied_into_git': 0,
               'network_requests': 0, 'auth_requests': 0, 'uploads': 0,
               'paper_or_gate_edits': 0, 'SCORES_or_journal_edits': 0, 'git_commits': 0}
    (OUT / 'EXECUTION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'result': 'PASS', 'native_runs_verified': 3,
                      'counts': [{'order': r['run_order'], 'k': r['k'], 'N': r['N']} for r in rows],
                      'primary': analysis['primary'], 'secondary_paired_n80': analysis['secondary'],
                      'prereg_precedes_probe': True}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(run())
    except Exception as error:
        # Never print row values, item IDs, private text, paths from ZIP errors,
        # or arbitrary exception messages into logs or published receipts.
        OUT.mkdir(exist_ok=True)
        failure = {'status': 'UNUSABLE', 'error_type': type(error).__name__,
                   'raw_error_text_withheld_for_private_item_safety': True}
        (OUT / 'FAILED_EXECUTION.json').write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure))
        sys.exit(2)
