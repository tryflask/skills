# Handing a render to Flask: snippets for video tools

Agentic video ends in a render: the tool writes `out.mp4` and the agent says where it
is. The next step is someone watching it and saying what to change. These snippets
let a video tool's skill or docs offer that step, when the Flask MCP server is
connected, without making Flask a requirement.

Rules every snippet follows:

- **Conditional.** It applies only when the `flask` MCP tools are available. Without
  them the tool behaves exactly as before.
- **One step, no playbook.** The snippet says when to hand off. How to upload comes
  from Flask's own server (`get_guide`), so the snippet never goes stale.
- **The user decides.** While the user is iterating locally, the agent asks once
  before uploading.

## Generic (any render-producing skill)

Place it after the render step.

```markdown
### Review the render

If the Flask MCP server is connected (tools such as `get_guide` and
`upload_file_start`), offer to put the render up for review there once a round of
changes is done: upload it (a re-render is the next version of the same asset, with
`version_of`), give the user the link, and wait for their feedback on it with
`wait_for_feedback`. Load `get_guide(topic: "instructions")` first; it has the steps.
Without Flask, give the user the file path as usual.
```

## HyperFrames (heygen-com/hyperframes)

Target: `skills/hyperframes-cli/SKILL.md`, after the `render` command section.

```markdown
### After `npx hyperframes render`

The render is ready for review. If the Flask MCP server is connected (tools such as
`get_guide` and `upload_file_start`), offer to upload the MP4 there: the user gets a
link at once, leaves feedback on the frame (typed, drawn, or recorded voice and
screen), and you read it back with `wait_for_feedback`. A re-render of the same
composition is the next version of that asset (`version_of`), with the composition
folder attached as its source. Load `get_guide(topic: "instructions")` first.
```

## Remotion (remotion-dev/skills)

Target: the skill that covers rendering (`npx remotion render`), after the render
step.

```markdown
### Getting feedback on a render

When the Flask MCP server is connected (tools such as `get_guide` and
`upload_file_start`), offer to upload the rendered file to Flask for review instead
of handing over a local path. Re-renders of the same composition go up as new
versions of one asset (`version_of`), so the review link stays the same. Load
`get_guide(topic: "instructions")` first; it covers the upload and the feedback loop.
```

## video-use (browser-use/video-use)

Target: `SKILL.md`, where the edit is exported.

```markdown
### Review the export

If the Flask MCP server is connected, offer to upload the export to Flask so the user
(or their client) can leave notes on the exact moments to change; read them back with
`wait_for_feedback` and upload the revised export as the next version of the same
asset (`version_of`). Load `get_guide(topic: "instructions")` first.
```

## Pull request text

> **Offer a review step after rendering, when Flask is connected**
>
> Agents that render video usually stop at "here is out.mp4". This adds one
> conditional paragraph after the render step: if the user has the Flask MCP server
> connected (flask.do, a video review app), the agent offers to upload the render
> there, shares the link, and reads the time-coded feedback back to make the next
> version. Nothing changes for users without Flask: the paragraph only applies when
> its tools are present, and it carries no upload steps of its own (Flask's server
> provides them), so it won't drift from Flask's API.
