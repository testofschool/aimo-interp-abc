#!/usr/bin/env python3
"""Validate flat note content against the supplied/live Submission invitation.

Usage: python3 -I tools/or_payload_gate.py PAYLOAD.json [--inv INVITATION.json]
       [--snapshot OLD_INV.json] [--pdf FILE]
Exit 0: syntax/PDF-file checks pass; 1: violations; 2: unreadable inputs.
Single-choice acknowledgements are copied exactly from the form. This checks
syntax, not their factual truth or human approval. Only PASS writes .filled.json.
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

INV_ID = "NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission"
URL = "https://api2.openreview.net/invitations?id=" + INV_ID
KINDS = {"string", "string[]", "profile[]", "author{}", "object{}", "file"}
LAST_FETCH_ROUTE = None


class FetchFailure(ValueError): pass


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def invitation_object(data):
    if not isinstance(data, dict):
        raise ValueError("invitation must be an object")
    if "edit" not in data:
        rows = data.get("invitations")
        if not isinstance(rows, list) or len(rows) != 1 or data.get("count", 1) != 1:
            raise ValueError("expected one invitation")
        data = rows[0]
    if not isinstance(data, dict) or data.get("id") != INV_ID:
        raise ValueError("unexpected invitation ID")
    fields = data.get("edit", {}).get("note", {}).get("content")
    if not isinstance(fields, dict) or not fields:
        raise ValueError("missing content schema")
    return data


def fetch_inv(path=None):
    global LAST_FETCH_ROUTE
    if path:
        LAST_FETCH_ROUTE = "saved_invitation"
        return invitation_object(json.loads(Path(path).read_text()))
    try:
        with urllib.request.urlopen(URL, timeout=30) as response:
            data = response.read()
        LAST_FETCH_ROUTE = "urllib_verified_tls"
    except urllib.error.URLError as error:
        if not isinstance(error.reason, ssl.SSLError):
            raise FetchFailure("live invitation fetch unavailable") from None
        # curl uses the system trust route on this Mac. Verification stays on;
        # --disable first prevents a user's curlrc from adding unsafe options.
        try:
            result = subprocess.run(["/usr/bin/curl", "--disable", "--fail", "--silent", "--show-error", "--connect-timeout", "10", "--max-time", "25", "--max-filesize", "1048576", URL], capture_output=True, timeout=30, check=False)
        except (OSError, subprocess.TimeoutExpired):
            raise FetchFailure("verified curl fallback unavailable after urllib TLS failure") from None
        if result.returncode:
            raise FetchFailure("verified curl fallback failed after urllib TLS failure") from None
        data = result.stdout
        LAST_FETCH_ROUTE = "curl_verified_after_urllib_tls_failure"
    return invitation_object(json.loads(data))


def field_diff(old, new):
    oc, nc = old["edit"]["note"]["content"], new["edit"]["note"]["content"]
    return {"added": sorted(set(nc)-set(oc)), "removed": sorted(set(oc)-set(nc)),
            "changed": [key for key in sorted(set(oc)&set(nc)) if oc[key] != nc[key]]}


def param_of(spec):
    if not isinstance(spec, dict) or not isinstance(spec.get("value"), dict) or not isinstance(spec["value"].get("param"), dict):
        raise ValueError("malformed field parameter")
    return spec["value"]["param"]


def choices(param, key):
    rows = param[key]
    if not isinstance(rows, list) or not rows:
        raise ValueError("malformed choices")
    values = [row.get("value") if isinstance(row, dict) else row for row in rows]
    if not all(isinstance(value, str) for value in values):
        raise ValueError("unsupported choices")
    return values


def schema_errors(param, label):
    errors = []
    if not isinstance(param, dict):
        return [f"{label}: malformed parameter"]
    if "optional" in param and not isinstance(param["optional"], bool):
        errors.append(f"{label}: optional must be boolean")
    if "const" in param:
        return errors
    kind = param.get("type")
    if not isinstance(kind, str) or kind not in KINDS:
        return errors + [f"{label}: unsupported or missing type"]
    for key in ("minLength", "maxLength", "minItems", "maxItems", "maxSize"):
        value = param.get(key)
        if key in param and (isinstance(value, bool) or not isinstance(value, (int,float)) or not math.isfinite(value) or value < 0):
            errors.append(f"{label}: invalid {key}")
    if "regex" in param:
        try:
            re.compile(param["regex"])
        except (TypeError, re.error):
            errors.append(f"{label}: malformed or unsupported regex")
    for key in ("enum", "items"):
        if key in param:
            try:
                choices(param, key)
            except ValueError:
                errors.append(f"{label}: malformed {key}")
    if kind in ("author{}", "object{}"):
        props = param.get("properties")
        if not isinstance(props, dict) or not props:
            errors.append(f"{label}: missing object properties")
        else:
            for key, spec in props.items():
                child = spec.get("param") if isinstance(spec, dict) else None
                errors.extend(schema_errors(child, label+"."+key))
    if kind == "file" and (not isinstance(param.get("extensions"), list) or not param["extensions"] or not all(isinstance(x,str) and x for x in param["extensions"])):
        errors.append(f"{label}: malformed file extensions")
    return errors


def empty(value):
    return value is None or value == [] or (isinstance(value, str) and not value.strip())


def value_errors(value, param, label, directory, file_override=None):
    errors = []
    if "const" in param:
        return [] if value == param["const"] else [f"{label}: does not match constant"]
    kind = param["type"]
    if kind in ("author{}", "object{}"):
        if not isinstance(value, list) or not value:
            return [f"{label}: expected nonempty object list"]
        for index, obj in enumerate(value):
            at = f"{label}[{index}]"
            if not isinstance(obj, dict):
                errors.append(f"{at}: expected object"); continue
            props = param["properties"]
            if set(obj)-set(props):
                errors.append(f"{at}: unknown object properties")
            for key, spec in props.items():
                child = spec["param"]
                if key not in obj or empty(obj[key]):
                    if not child.get("optional", False): errors.append(f"{at}.{key}: missing required value")
                else:
                    errors.extend(value_errors(obj[key], child, at+"."+key, directory))
        return errors
    if kind == "file":
        path = file_override if file_override is not None else value
        if not isinstance(path, str) or not path:
            return [f"{label}: expected local file path"]
        path = Path(path)
        if not path.is_absolute(): path = directory/path
        if not path.is_file() or path.suffix[1:].lower() not in [x.lower() for x in param["extensions"]]:
            return [f"{label}: file missing or extension invalid"]
        if path.stat().st_size > param.get("maxSize",50)*1024*1024:
            errors.append(f"{label}: file exceeds maximum size")
        if path.suffix.lower() == ".pdf":
            with path.open("rb") as stream:
                if stream.read(5) != b"%PDF-": errors.append(f"{label}: invalid PDF signature")
        return errors
    multiple = kind.endswith("[]")
    if (multiple and not isinstance(value,list)) or (not multiple and not isinstance(value,str)):
        return [f"{label}: expected {kind}"]
    values = value if multiple else [value]
    if multiple:
        for key, failed in (("minItems",len(values)<param.get("minItems",0)), ("maxItems",len(values)>param.get("maxItems",float('inf')))):
            if failed: errors.append(f"{label}: violates {key}")
    for item in values:
        if not isinstance(item,str) or not item.strip():
            errors.append(f"{label}: expected nonempty strings"); continue
        if param.get("regex") and re.fullmatch(param["regex"],item) is None: errors.append(f"{label}: regex mismatch")
        if kind == "profile[]" and re.fullmatch(r"~\S+",item) is None: errors.append(f"{label}: invalid profile ID")
        if len(item)<param.get("minLength",0) or len(item)>param.get("maxLength",float('inf')): errors.append(f"{label}: string length outside bounds")
        for key in ("enum","items"):
            if key in param and item not in choices(param,key): errors.append(f"{label}: value not in exact choices")
    return errors


def validate(inv, payload, directory, pdf_override=None, now_ms=None):
    """Return report and filled content, without network, SDK, or file writes."""
    inv = invitation_object(inv)
    fields = inv["edit"]["note"]["content"]
    errors, notes, params = [], [], {}
    if not isinstance(payload,dict): raise ValueError("payload must be object")
    for name,spec in fields.items():
        try:
            params[name]=param_of(spec); errors.extend(schema_errors(params[name],name))
        except ValueError:
            errors.append(f"{name}: malformed schema")
    if "pdf" not in params or params["pdf"].get("type") != "file": errors.append("pdf: missing file schema")
    clock=time.time()*1000 if now_ms is None else now_ms
    dates=[inv.get(key) for key in ("cdate","duedate","expdate")]
    if any(isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) for value in dates):
        errors.append("invitation: missing or malformed opening/deadline dates")
    elif not dates[0] <= clock < min(dates[1:]):
        errors.append("invitation: form not open or due date passed")
    filled=copy.deepcopy(payload)
    for key in set(payload)-set(fields): errors.append(f"{key}: field not in live invitation")
    if not errors:
        for name,param in params.items():
            if "const" in param:
                if name in payload: errors.extend(value_errors(payload[name],param,name,directory))
                continue
            if name not in filled and "enum" in param and len(choices(param,"enum"))==1:
                filled[name]=choices(param,"enum")[0]; notes.append(f"auto-filled {name} from live enum (truth not verified)")
            value=filled.get(name)
            if name not in filled or empty(value):
                if not param.get("optional",False): errors.append(f"{name}: missing required value")
                continue
            errors.extend(value_errors(value,param,name,Path(directory),pdf_override if name=="pdf" else None))
            if param["type"]=="file" and not errors:
                path=Path(pdf_override if name=="pdf" and pdf_override else value)
                filled[name]=str(path if path.is_absolute() else Path(directory)/path)
    authors=filled.get("authors",[]); reviewers=filled.get("reciprocal_reviewers",[])
    author_ids=[a.get("username") for a in authors if isinstance(a,dict)] if isinstance(authors,list) else []
    if author_ids and len(set(x for x in author_ids if isinstance(x,str))) != len(author_ids): errors.append("authors: invalid or duplicate profile IDs")
    if isinstance(reviewers,list) and any(r not in author_ids for r in reviewers): errors.append("reciprocal_reviewers: reviewer not in authors")
    if isinstance(reviewers,list) and len(set(x for x in reviewers if isinstance(x,str)))!=len(reviewers): errors.append("reciprocal_reviewers: invalid or duplicate reviewers")
    ai=filled.get("ai_assistance",[])
    if isinstance(ai,list) and "No AI assistance was used" in ai and len(ai)>1: errors.append("ai_assistance: contradictory selections")
    ids=filled.get("leaderboard_submission_ids")
    if isinstance(ids,str) and re.fullmatch(r"\s*\d+\s*(,\s*\d+\s*)?",ids) is None: errors.append("leaderboard_submission_ids: expected one or two numeric IDs")
    names=[]
    for author in authors if isinstance(authors,list) else []:
        if isinstance(author,dict) and isinstance(author.get("fullname"),str): names+=author['fullname'].split()
    for field in ("title","abstract","TLDR"):
        text=filled.get(field,"")
        if not isinstance(text,str): continue
        if (field=="title" and "\n" in text) or any(len(n)>2 and re.search(r"\b"+re.escape(n)+r"\b",text) for n in names) or re.search(r"[\w.+-]+@[\w-]+\.[\w.]+|github\.com/",text): errors.append(f"{field}: identity/newline check failed (content omitted)")
    for key in ("venue","venueid"): filled.pop(key,None)
    report={"result":"FAIL" if errors else "PASS","invitation_tmdate":inv.get("tmdate"),"invitation_sha256":canonical_hash(inv),"payload_sha256":canonical_hash(filled),"duedate":inv.get("duedate"),"expdate":inv.get("expdate"),"errors":errors,"notes":notes,"scope":"schema/file syntax only; factual attestations and human review not verified"}
    if not errors:
        report['pdf_sha256']=hashlib.sha256(Path(filled['pdf']).read_bytes()).hexdigest()
    return report,filled


def main(args=None):
    args=sys.argv[1:] if args is None else args
    if not args: print(__doc__); return 2
    try:
        options={};i=1
        while i<len(args):
            if args[i] not in {"--inv","--snapshot","--pdf"} or i+1>=len(args): raise ValueError("invalid options")
            options[args[i]]=args[i+1];i+=2
        path=Path(args[0]).absolute();inv=fetch_inv(options.get('--inv'));fetch_route=LAST_FETCH_ROUTE
        report,filled=validate(inv,json.loads(path.read_text()),path.parent,options.get('--pdf'))
        report['invitation_fetch_route']=fetch_route
        if '--snapshot' in options: report['diff_vs_snapshot']=field_diff(fetch_inv(options['--snapshot']),inv)
        output=Path(str(path)+'.filled.json')
        if report['result']=='PASS':
            output.write_text(json.dumps(filled,indent=1,ensure_ascii=False)+'\n');report['filled_payload']=str(output)
        else: report['filled_payload']=None
        print(json.dumps(report,indent=1,ensure_ascii=False));return 0 if report['result']=='PASS' else 1
    except (OSError,ValueError,TypeError,KeyError,AttributeError,re.error) as error:
        print(json.dumps({'result':'UNREADABLE','error_type':type(error).__name__,'errors':[str(error) if isinstance(error,FetchFailure) else 'invalid inputs or unavailable invitation; no payload approved']}));return 2


if __name__=='__main__':sys.exit(main())
