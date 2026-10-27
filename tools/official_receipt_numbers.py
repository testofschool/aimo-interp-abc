#!/usr/bin/env python3
"""Regenerate official-run numbers from committed aggregate receipts only.

Private native item rows are inputs to the earlier, separately recorded native
validation. This reproduction uses its pinned aggregate table, verifies native
API marginals/provenance, and recomputes exact paired inference. It never opens
the private cache, reconstructs labels, or authenticates server deployment code.
"""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = {
    'v9-execution/SCORES.json': 'f5cd2423cc88236c350ae2abecb7b1785075a21fc152d32e3f0ab56c238e0b94',
    'v9-execution/NATIVE_OUTPUT_CHECK.json': '8ea086829b9e6f0defaab7d477842a22357b757c9c6931f286fb92334c555839',
    'v9-execution/ABLATION.json': 'af0e3f3605312e717461f2aa8d3326337a773cd0d36ab9fe18a3dd1d17d77e2c',
    'v9-execution/paired_protocol.py': '1fade7edee89a5086766afdf1ebe8cfb61ea6e5f53e3d4adbeb91bbc5d5dbad5',
    'v9-execution/PREREG.md': 'c8f4d89a0a4efca1f458e65c61167551056bd34ade8d542db5682a56545d3ddc',
}
BUNDLES = [
    ('always_true', 'solution-always-true-small.zip', '4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a'),
    ('text_length_control', 'solution-text-length-control-small.zip', '30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd'),
    ('trained_probe', 'bundle3-trained-probe-small.zip', '852fff17372ebdcf967549a4270339a2e792372c1b5496da968b2df884ccc67b'),
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dec(value):
    require(type(value) in (str, int, float, Decimal), 'invalid numeric type')
    result = Decimal(str(value))
    require(result.is_finite(), 'nonfinite receipt value')
    return result


def integer(value):
    require(type(value) is int and value >= 0, 'invalid nonnegative count')
    return value


def stamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.utcoffset() is not None, 'receipt timestamp lacks timezone')
    return result


def native_values(receipt):
    require(receipt['owner'] == 'testofschool' and receipt['status'] == 'Finished', 'native owner/status mismatch')
    require(receipt['phase'] == 30038 and receipt['task']['id'] == 36241, 'native Small track mismatch')
    result = {}
    for row in receipt['scores']:
        key = row['column_key']
        if key in ('accuracy', 'coverage', 'invalid_predictions'):
            require(key not in result, 'duplicate native score key')
            result[key] = dec(row['score'])
    require(set(result) == {'accuracy', 'coverage', 'invalid_predictions'}, 'missing native score')
    return result


def validate_records(scores, native, ablation, previous_scores, protocol):
    """Check aggregate provenance/arithmetic and return manuscript scalar keys."""
    require(scores['competition_id'] == 16180 and scores['phase_id'] == 30038 and
            scores['task_id'] == 36241, 'official score registry scope mismatch')
    require(previous_scores['competition_id'] == 16180 and previous_scores['phase_id'] == 30038 and
            previous_scores['task_id'] == 36241, 'prior score snapshot scope mismatch')
    require(native['status'] == 'PASS', 'native validation did not pass')
    require(native['same_real_item_id_sets_all_three'] is True, 'unmatched native item sets')
    require(native['individual_item_ids_or_prediction_rows_published'] is False and
            native['raw_native_outputs_remain_outside_git'] is True, 'private-row publication boundary failed')
    require(native['scorer_contract']['unweighted_binary_accuracy'] is True, 'unweighted score contract absent')
    require(native['scorer_contract']['server_deployment_source_hash_authenticated'] is False,
            'server deployment attestation must not be invented')
    require(len(scores['runs']) == len(native['runs']) == len(previous_scores['runs']) == 3, 'exactly three official runs required')
    require(scores['exploratory'] is False and ablation['exploratory'] is False and ablation['preregistered'] is True,
            'preregistration classification mismatch')
    out = {}
    for i, (prefix, filename, bundle_sha) in enumerate(BUNDLES):
        s, n, prior = scores['runs'][i], native['runs'][i], previous_scores['runs'][i]
        require(n['native_small_task'] == 36241 and n['native_phase'] == 30038,
                'native aggregate scope mismatch')
        require(n['native_scoring_json_matches_api'] is True, 'native scoring/API validation missing')
        require(s['name'] == n['bundle'] == filename and s['sha256'] == bundle_sha, 'bundle identity mismatch')
        require(s['native_receipt'] == prior['native_receipt'] and
                s['small_score_receipt'] == prior['small_score_receipt'], 'native API receipt changed after count enrichment')
        sid = integer(s['submission_id'])
        require(sid == n['native_submission_id'] == s['native_receipt']['id'] == s['small_score_receipt']['id'],
                'native submission binding mismatch')
        require(s['state'] == 'ACCEPTED_FINISHED' and n['status'] == 'Finished', 'official run not finished')
        values = native_values(s['native_receipt'])
        require(values == native_values(s['small_score_receipt']), 'native score receipt mismatch')
        require(values['coverage'] == 1 and values['invalid_predictions'] == 0, 'coverage/invalid contract mismatch')
        total = integer(n['N'])
        require(total == 14 and total == n['prediction_rows'] == n['unique_ids'] == n['summary_cases'], 'count denominator mismatch')
        require(n['all_prediction_rows_valid_binary'] is True and
                n['summary_invalid_predictions'] == n['summary_timeouts'] == n['summary_skipped'] == 0,
                'native output validity mismatch')
        correct = integer(n['k'])
        require(0 <= values['accuracy'] <= 1 and values['accuracy'] * total == correct, 'native accuracy/count mismatch')
        require(s['N'] == total and s['k'] == correct, 'enriched score marginals mismatch')
        for key in values:
            require(dec(s[key]) == dec(s['native_score_values'][key]) == values[key], 'saved score value mismatch')
            require(dec(n[key + '_native_raw']) == values[key], 'native validation score mismatch')
        require(n['zips']['submitted-bundle.zip']['sha256'] == bundle_sha, 'server ZIP hash mismatch')
        require(all(z['crc_ok'] is True and z['unique_safe_paths'] is True for z in n['zips'].values()),
                'native ZIP validation missing')
        require(n['native_exact_finished_time'] is None and s['finished_time_KST'] is None, 'exact server finish time fabricated')
        created = stamp(s['native_receipt']['created_when'])
        require(created == stamp(n['native_created_when']) == stamp(n['native_created_KST']), 'submission creation timestamp mismatch')
        kst = created.astimezone(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
        for suffix, value in [('submission_id', sid), ('k', correct), ('n', total),
                              ('accuracy', float(values['accuracy'])), ('coverage', float(values['coverage'])),
                              ('invalid_predictions', int(values['invalid_predictions'])), ('submitted_at_kst', kst)]:
            out['official_' + prefix + '_' + suffix] = value
    require(ablation['paired_protocol_sha256'] == SOURCE_SHA256['v9-execution/paired_protocol.py'], 'paired helper provenance mismatch')
    require(ablation['validated_score_contract'] == {
        'same_evaluation_items': True, 'unweighted_binary_accuracy': True,
        'probe_coverage': 1.0, 'control_coverage': 1.0,
        'probe_invalid_predictions': 0, 'control_invalid_predictions': 0}, 'paired score contract mismatch')
    chronology = ablation['prereg_chronology']
    require(chronology == native['prereg_chronology'] and
            scores['prereg_commit'] == chronology['prereg_commit'], 'preregistration provenance mismatch')
    require(chronology['prereg_sha256'] == SOURCE_SHA256['v9-execution/PREREG.md'] and
            stamp(chronology['prereg_commit_time_KST']) < stamp(chronology['native_probe_created_KST']) ==
            stamp(scores['runs'][2]['native_receipt']['created_when']), 'preregistration chronology failed')
    primary = ablation['primary']
    table = primary['table']
    require(set(table) == {'both_correct', 'probe_only', 'control_only', 'both_wrong'}, 'invalid joint-table keys')
    actual = protocol.from_joint_counts(**table, alpha=0.05)
    require(actual == primary, 'stored paired statistics disagree with aggregate table')
    require(actual['n'] == out['official_trained_probe_n'] == out['official_text_length_control_n'] and
            actual['probe_correct'] == out['official_trained_probe_k'] and
            actual['control_correct'] == out['official_text_length_control_k'], 'joint table disagrees with native marginals')
    secondary = protocol.first_n_for_power(table['probe_only'] / actual['n'], table['control_only'] / actual['n'])
    recorded_secondary = dict(ablation['secondary_paired_n80'])
    recorded_secondary.pop('status_qualification', None)
    require(secondary == recorded_secondary and ablation['N80'] == secondary['first_n'] and
            ablation['pvalue'] == actual['pvalue'], 'paired power or exact p provenance mismatch')
    for key in ['equivalence_claim_allowed', 'black_box_sufficiency_claim_allowed',
                'absence_of_white_box_benefit_claim_allowed', 'causal_signal_ablation_claim_allowed',
                'final_test_ranking_claim_allowed']:
        require(ablation['reporting'][key] is False, 'unsupported scientific conclusion permitted')
    values = {'n': actual['n'], **table, 'discordant': actual['discordant_items'],
              'accuracy_difference': actual['accuracy_difference_probe_minus_control'],
              'exact_p': actual['pvalue'], 'alpha': actual['alpha'],
              'reject_reference': actual['reject_reference_null'],
              'n80': secondary['first_n'], 'n80_status': secondary['status']}
    out.update({'official_probe_control_' + key: value for key, value in values.items()})
    return out


def inspect(root=ROOT):
    root = Path(root)
    state = {'measurement_status': 'UNMEASURED', 'measured_score_statements_allowed': False,
             'source': 'PINNED_NATIVE_OFFICIAL_AGGREGATE_RECEIPTS',
             'native_owner_receipt_verified': False, 'errors': [], 'numbers': {}}
    try:
        raw = {}
        for name, expected in SOURCE_SHA256.items():
            raw[name] = (root / name).read_bytes()
            require(hashlib.sha256(raw[name]).hexdigest() == expected, 'official source hash mismatch: ' + name)
        scores = json.loads(raw['v9-execution/SCORES.json'])
        native = json.loads(raw['v9-execution/NATIVE_OUTPUT_CHECK.json'])
        ablation = json.loads(raw['v9-execution/ABLATION.json'])
        previous_scores = None
        for name, item in native['input_receipts_snapshots'].items():
            path = (root / item['snapshot']).resolve()
            require(path.is_relative_to(root.resolve()), 'snapshot path outside reproduction root')
            value = path.read_bytes()
            key = 'SCORES_sha256' if name.endswith('SCORES.json') else 'journal_sha256'
            require(hashlib.sha256(value).hexdigest() == item['sha256'] == native['input_receipts'][key],
                    'native input snapshot hash mismatch')
            if name == 'v9-execution/SCORES.json':
                previous_scores = json.loads(value)
        require(previous_scores is not None, 'native source score snapshot missing')
        spec = importlib.util.spec_from_file_location('official_unchanged_paired_protocol', root / 'v9-execution/paired_protocol.py')
        protocol = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(protocol)
        state['numbers'] = validate_records(scores, native, ablation, previous_scores, protocol)
        state.update({'measurement_status': 'NATIVE_OFFICIAL_SMALL_AGGREGATES_VERIFIED',
                      'measured_score_statements_allowed': True, 'native_owner_receipt_verified': True,
                      'association_basis': 'native authenticated API receipts plus prior native-output aggregate verification',
                      'source_sha256': dict(SOURCE_SHA256),
                      'raw_private_case_rows_required_for_reproduction': False,
                      'server_deployment_hash_authenticated': False})
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError) as error:
        state['errors'].append(str(error))
    return state


def numbers(state):
    if not state['measured_score_statements_allowed']:
        raise ValueError('official aggregate source invalid: ' + '; '.join(state['errors']))
    return state['numbers']
