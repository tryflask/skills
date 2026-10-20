#!/usr/bin/env python3
"""Trigger eval for the flask-review skill: does Claude open the skill for a request?

For each query in trigger-eval.json, and each run, a fresh folder gets the skill as a
project skill under a unique name, and `claude -p` answers the query there. A run
counts as triggered when Claude calls the Skill tool on that skill within two turns.
A query passes when its trigger rate is at least 0.5 for a should-trigger query, and
below 0.5 for a near miss.

The runs are safe and clean: only project settings load (--setting-sources project),
so the user's own skills don't crowd the listing; no MCP servers load
(--strict-mcp-config), so it measures the moment before Flask is connected; and the
tools that change anything (Bash, Edit, Write, NotebookEdit, web, subagents) are
disallowed.

usage: run_trigger_eval.py [--description TEXT] [--name NAME] [--runs 2] [--workers 6] [--timeout 45]
                           [--model MODEL] [--out results.json]
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "plugins" / "flask" / "skills" / "flask-review" / "SKILL.md"
BLOCKED = ["Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch", "Agent"]


def skill_parts(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    front, body = m.group(1), m.group(2)
    desc = re.search(r"^description: (.*)$", front, re.M).group(1)
    return desc, body


def one_run(query, description, body, timeout, model, prefix="flask-review"):
    name = f"{prefix}-{uuid.uuid4().hex[:8]}"
    root = Path(tempfile.mkdtemp(prefix="flask-trigger-"))
    try:
        skill = root / ".claude" / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {json.dumps(description)}\n---\n{body}")
        cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose",
               "--strict-mcp-config", "--setting-sources", "project",
               "--max-turns", "2", "--disallowedTools", *BLOCKED]
        if model:
            cmd += ["--model", model]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        proc = subprocess.Popen(cmd, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True)
        start = time.time()
        try:
            for line in proc.stdout:
                if time.time() - start > timeout:
                    return False
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "assistant":
                    for c in event["message"].get("content", []):
                        if c.get("type") == "tool_use" and c.get("name") == "Skill" and name in json.dumps(c.get("input", {})):
                            return True
                if event.get("type") == "result":
                    return False
            return False
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-set", default=str(HERE / "trigger-eval.json"))
    ap.add_argument("--description", help="test this description instead of the skill's own")
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=45)
    ap.add_argument("--model")
    ap.add_argument("--name", default="flask-review", help="skill name to test (a unique suffix is added)")
    ap.add_argument("--out")
    a = ap.parse_args()
    desc, body = skill_parts(SKILL.read_text())
    desc = a.description or desc
    items = json.load(open(a.eval_set))
    jobs = [(i, it["query"]) for i, it in enumerate(items) for _ in range(a.runs)]
    with ThreadPoolExecutor(a.workers) as pool:
        hits = list(pool.map(lambda j: (j[0], one_run(j[1], desc, body, a.timeout, a.model, a.name)), jobs))
    results = []
    for i, it in enumerate(items):
        got = [h for k, h in hits if k == i]
        rate = sum(got) / len(got)
        ok = rate >= 0.5 if it["should_trigger"] else rate < 0.5
        results.append({**it, "triggers": sum(got), "runs": len(got), "pass": ok})
        print(f"{'PASS' if ok else 'FAIL'}  {'should' if it['should_trigger'] else 'not   '}  {sum(got)}/{len(got)}  {it['query'][:90]}")
    passed = sum(r["pass"] for r in results)
    print(f"\n{passed}/{len(results)} passed")
    if a.out:
        json.dump({"description": desc, "passed": passed, "total": len(results), "results": results}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
