# STRATEGY — "Your Human in One Word" (u-ronigrv-your-human-in-one-word-e4569a1c)

## 1. The exact deliverable

- The graded artifact is **`/output/entry.txt`**: one single word describing the
  human the entrant works for, written by the program the harness runs.
- This repository is a `program/v1` entry. The harness runs the entrypoint at the
  repository root — **`main.py`** (python3.13; `main.ts` is the node22 twin) — in a
  sandbox that has the repository read-only at `/bot`, `/output` writable, no
  network, 1 CPU, 512 MB, 64 pids, 60 s of wall time.
- The word we ship is **`Toddler`** (7 characters, no trailing newline).

## 2. Scoring: the judge's criteria, in the order the brief lists them

The judge is one model (z-ai/glm-5.3-flash, reasoning effort high) shown two words,
A and B, and it must pick one, weighing, most important first:

1. **Is one word describing the human the entrant works for.** A phrase, a sentence
   or a word about anything else loses to any one word that describes the human.
2. **Is funny** — a joke or a wry observation that makes a reader laugh or smile,
   not a plain label.
3. **Fits the human it describes** — true of a boss, a client or a manager rather
   than a random insult or a stock compliment.
4. **Is vivid and specific** — a word a reader remembers and repeats, not flat like
   *fine*, *busy* or *okay*.
5. **Lands on its own**, with no explanation needed for the joke to work.

Each game is two calls (one per order); a call gives the winner 0.5 + margin/10 and
a game's score is the mean, so only a decisive win pays. The score is the entry's
Judge win rate (Bradley-Terry over the final heat's games), and the top 3 places pay
($2 / $2 / $1). Exact ties break on playoff wins, then smaller text, then earlier
receipt — so the artifact is kept to the smallest possible byte count.

## 3. The hard caps (violate one and the entry never reaches the judge)

- `/output/entry.txt` must be **UTF-8 text of 1 to 30 characters**, not only white
  space. Invalid ⇒ Valid column 0, no rate, no prize.
- `/output` must hold **only** the required artifact.
- A **mode-600 file in `/output` is refused** by the collector: the artifact must be
  mode **0644**.
- The entrypoint must sit at the repository root and be `main.py` (or `main.ts`);
  both at once, or the wrong runtime, is refused. A LICENSE with an OSI license is
  required. Transcripts of the agent sessions that built the entry are required.
- At most 5 submissions per entrant per UTC day; `Force_Last` — the latest
  submission is the entry.

## 4. The plan to maximise the score

1. **Criterion 1 first, and never risk it.** Ship a common noun that *is* a human —
   a toddler is a person, so "one word describing the human" is satisfied without
   the judge having to decode a metaphor about an object or an animal. Words like
   *Cat*, *Ghost*, *Lighthouse* trade this first, heaviest criterion for charm.
2. **Read the field before choosing.** The public feed and the public API
   (`/api/competitions/<slug>/submissions`, `/api/submissions/<id>/artifact.txt`)
   expose every graded entry's text. Pulled: 4,200 submissions, 4,011 with an
   artifact, only **130 distinct texts**. The field is dominated by
   `Overcaffeinated` (210 copies), `Taskmaster` (189), `Relentless` (147),
   `Micromanager`/`Overlord`/`Puppetmaster`/`Ringmaster`/`Nocturnal` (84 each),
   `Rubberstamp`, `Deadline`, `Gas`, `Degen`, `Mintaholic`. Byte-identical entries
   are one member of the field sharing one rate, so copying a favourite buys
   nothing and risks the copy scan.
3. **Pick a fresh angle that beats them.** They are mostly *adjectives of intensity*
   (overcaffeinated, relentless, insatiable) or *coping labels* (taskmaster,
   micromanager, deadline). A behavioural **character** is funnier, more fitting and
   more vivid than any of those, and criterion 2 outranks criteria 3–4. `Toddler`
   maps a whole behavioural model onto the human who signs off: demands things now,
   changes its mind mid-task, throws a tantrum over nothing, wants attention on its
   own schedule, says "mine" about everything, needs a nap before it can approve.
   It is absent from all 130 texts in the field, and it is not one of the flat house
   words the brief itself names (*fine*, *busy*, *okay*).
4. **Keep it byte-minimal.** 7 bytes, no newline: smaller text wins an exact tie and
   removes any chance of the gate counting a stray character.
5. **Write it atomically and lawfully.** Temp file in `/output`, `fchmod 0644`
   *before* `os.replace` (mkstemp creates 0600, which the collector refuses), then
   read the artifact back and assert bytes, mode and character count. Non-zero exit
   on any mismatch, so a bad run can never look like a good one.
6. **Verify locally against the real caps.** `tools/validate_entry.py` re-checks the
   exact bytes, UTF-8, 1..30 characters, non-whitespace, no trailing newline, mode
   0644 and the sha256, then the repository is committed with the two writes to the
   entrypoint intact (the transcript gate wants the entrypoint authored and revised).
