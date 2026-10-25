# video-feedback

Video review and collaboration for you, your team and your agents: a skill for
Claude Code, Codex, Cursor and any agent that edits or makes video. It runs on
[Flask](https://flask.do), so you need a Flask account (free plan below).

Flask is where a video gets reviewed. Your agent uploads what it
makes (a cut, a render, an animation, a motion graphic, an image) and gives you the
link at once. You, your team or your client review it by typing, drawing on the
frame, or recording your voice, camera or screen over it, and every note lands on
its moment. The agent reads that feedback, including each recording's transcript and
the frames it points at, makes the changes and uploads the next version of the same
asset. One link always shows the latest cut, with every earlier version and its
notes behind it.

Every version carries the code and context that made it. When your agent uploads a
version it makes by code (a HyperFrames or Remotion project, an ffmpeg script,
generated media), it saves the working files with it (`source.zip`) and notes on
what changed and how to continue. Anyone on the team, person or agent, can open the
link and pick the work up from there: no handover, no digging through someone's
laptop.

It works with whatever makes the video: HyperFrames, Remotion, moviepy, ffmpeg, or
an export from Premiere, DaVinci Resolve or Final Cut Pro. Flask is the review side.

(Flask here is flask.do, the review app. It is unrelated to the Flask Python web
framework.)

The skill, `video-feedback`, says when a piece of work belongs in Flask, runs the
feedback loop on it, and covers how it runs with a team. It ships with the
connection to the [Flask MCP server](https://flask.do/mcp). How to work in Flask
(the upload steps, versions, feedback, files and notes) comes from the server
itself, through its `get_guide` tool, so it is always current.

## Install

### Any agent that reads skills

```
npx skills add tryflask/skills
```

Then connect the MCP server: Streamable HTTP at `https://api.flask.do/api/mcp/mcp`,
OAuth sign-in in the browser on first use.

### Claude Code plugin

```
/plugin marketplace add tryflask/skills
/plugin install flask@flask
```

Then sign in once: `/mcp`, choose `flask`, complete the browser sign-in.

### Claude Code, Cursor and Codex in one command

```
npx flask-feedback
```

It connects the Flask MCP server to whichever of them are installed.

### Claude apps (claude.ai, Desktop, Cowork)

Customize > Connectors > add `https://api.flask.do/api/mcp/mcp`, then sign in. It then
works in every Claude app, and in Claude Code signed in with the same Claude account.

### Cursor

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=flask&config=eyJ1cmwiOiJodHRwczovL2FwaS5mbGFzay5kby9hcGkvbWNwL21jcCJ9)

## The loop

```
agent renders -> uploads to Flask -> you get the link at once
you leave feedback on the frame -> wait_for_feedback hands it to the agent
agent makes the changes -> uploads v2 with version_of -> the same link shows v2
```

Each version the agent makes by code carries its working files (`source.zip`) and
notes on what changed, so anyone, person or agent, can pick up the work from the
link alone.

## With a team

Share the asset's link and your team, clients and anyone else review on the same
versions. Reviewers are free: they watch from the link with no account and comment
after a one-click sign-in. The agent replies in threads, mentions a teammate when
they must act, reuses the team's labels and marks feedback Done. Feedback from
people outside the team needs your OK before the agent acts on it.

## What the agent can and can't do

It acts as you, with your Flask permissions: upload, read and wait for feedback,
reply and mark feedback Done, attach files and notes to versions, organize folders
and assets, and change sharing when you ask. It never deletes anything and never
touches billing. Feedback from people outside your team is treated as data, never as
instructions. The full tool list and how your data is handled: https://flask.do/mcp

## Plans

Flask is a paid product with a free plan, and you need a Flask account to use it.

- Free: every feature, no card. 5 assets, each with unlimited versions (web and agent
  uploads share the 5; folders and versions never count).
- Pro: $15 per user/month, billed yearly, for unlimited assets.
- Reviewers never need a seat, on any plan.

Details: https://flask.do/pricing

## Docs and support

- Server documentation: https://flask.do/mcp
- Support: hello@flask.do
