# Formal or_watch.py hardening

Supplied original SHA-256: `0f6e62c18896e57d2b6fa18c751e47e7a4f663f4dee5c588a6928b9495874df1`. Preserved at `v12-execution/audit/or_watch.original.py`; pre-execution defect/change plan is `OR_WATCH_CHANGEPLAN.json`. Patched SHA-256: `c87a5b708ce3067b81eca8ff0bf581040becc53ef6765d22bc2f0401c53fe94e`. The SCR mismatch is intentional and recorded in `OR_WATCH_PREREG_MISMATCH.json` before final tests or live execution. The supplied source is not represented as having passed these repaired checks.

Confirmed defects in the supplied source: invitation failure returned before the remaining sources; failed git acquisition could still report NO_CHANGE; Codabench errors replaced a successful phase baseline; clone/fetch/diff nonzero statuses could become empty successful patches; optional-to-required and type changes lacked explicit classification; malformed baseline JSON/snapshot content could abort all tracks; state writes were not atomic.

The formal operator filename remains `tools/or_watch.py`. Public invitation, SITE, BY and phase reads run independently. An error produces PARTIAL_ERROR (exit 2), retains healthy changes/evidence, and preserves the previous complete baseline and its raw invitation snapshot. Successful invitation snapshots use immutable hash-qualified filenames under the configured root. Each run has a separate audit result. The baseline is atomically replaced only when all acquisition, baseline parsing and required SITE diff work succeeds.

Drift output distinguishes required additions, required-field changes, optional-to-required transitions, type changes, field removal, dates and license. New facts are marked for payload review; the watcher never declares them true or edits a note. SITE patches use the exact old/new commits, checked clone/fetch/diff statuses, no external diff/textconv, and full untruncated index.html output. An empty successful patch is explicitly different from a failed patch.

The script uses TLS verification, bounded HTTPS/git calls, a verified curl fallback for local certificate failures, disabled git credentials/prompts, and no scheduler. A fixed cutoff at 2026-11-06 20:00 KST stops network and baseline writes; tests inject time in the Python function and the operator CLI has no fake-clock option. The legacy successful phase-end baseline is supported; error/malformed phase observations are not adopted as successes.

Offline validation: 25 tests, PASS, exit 0. Exact command:

```sh
/Users/felix/orvenv/bin/python -B -I -m unittest discover -s tests -p test_or_watch.py -v
```

Coverage includes HTTP503, git timeout, independent healthy-track changes, all-source outage, malformed baseline/snapshot, same-tmdate schema drift without raw-baseline overwrite, required/optional/const/type/enum drift, failed/empty/large SITE patches, atomic replacement failure, cutoff side effects, verified TLS fallback, and disabled credential/process side effects. Public network responses remain for the root agent's live run; this agent ran no live watcher and made no authentication, service, scheduler, report/PDF, payload-gate or submitter change.

Only watcher source, its focused tests and watcher-specific audit files were written by this task. Future E14 must continue to distinguish eighty labelled fit rows from the ninety-four total public rows; this watcher does not modify those facts.
