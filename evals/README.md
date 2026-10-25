# Trigger eval for flask-feedback

`trigger-eval.json` holds 20 realistic requests in the format of Anthropic's
`skill-creator` (`{"query", "should_trigger"}`):

- 10 where the agent should reach for Flask: it made media a person has to watch to
  approve, over rounds, often for someone else.
- 10 near misses that share its words but need something else: the Flask Python
  framework, code review, a one-off conversion, a team that reviews in Frame.io.

## Run it

```
python3 evals/run_trigger_eval.py --runs 2 --out results.json
```

Needs Python 3.9+ and the `claude` CLI signed in. Add `--name` to test another skill name. Add `--description "..."` to test
another description against the same set, `--model` to pick the model.

Each run creates a fresh folder holding the skill as a project skill, under a unique
name, and runs `claude -p` with the query there. A run counts as triggered when
Claude calls the Skill tool on that skill within two turns. A query passes at a
trigger rate of 0.5 or more if it should trigger, and below 0.5 if it is a near miss.

Every run is safe and measures the right moment:

- **No MCP servers load** (`--strict-mcp-config`): this is the moment before Flask is
  connected. Once it is connected, the server's own instructions say when to use it.
- **Nothing can change**: Bash, Edit, Write, NotebookEdit, web tools and subagents
  are disallowed. Plan mode is not used, because it makes Claude explore before it
  loads any skill.
- **Only project settings load** (`--setting-sources project`): the skill competes
  with Claude Code's built-in skills, as on a fresh install, not with whatever the
  person running the eval has installed.

Claude Code v2.1.269 and later also ship `claude plugin eval`, which runs every case
with and without the plugin in clean sessions. These queries can move to its format
(`evals/<case>/prompt.md` plus `graders/`) once that version is installed.

## Results

2026-10-19, Claude Code 2.1.198 with its default model, 3 runs per query, clean
settings (`--setting-sources project`):

| Description | Passed | Offered Flask when it should | Offered it on a near miss |
|---|---|---|---|
| Before (v1.1.1) | 16/20 | 6/10 | 0/10 |
| Now (v1.2.0) | 19/20 | 9/10 | 0/10 |

The new description picked up the HyperFrames intro, the re-rendered motion graphic
and the generated product shots. The one miss in both is "cut the interview with
ffmpeg, then get my editor's feedback": Claude starts the cut first, beyond the eval's
two turns, and reaches the review step later.

With the user's own settings loaded on a machine with about 150 installed skills,
Claude Code lists skills by name only and both descriptions triggered far less: on a
crowded machine the skill's name carries most of the weight.
