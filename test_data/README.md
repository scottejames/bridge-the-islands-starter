# Test data

Every case for Bridge the Islands lives here as a plain text file,
grouped into three difficulty tiers. Both `python/run_tests.py` and
`java/src/TestRunner.java` load directly from this directory — nothing is
duplicated in code.

## File format

```
name=<case name>
n=<int>
expected=<int>
events=
<event 0>
<event 1>
...
```

Everything from the line after `events=` to the end of the file is the
event list, one event per line, each either `U u v` (build a bridge) or
`Q u v` (query). Filenames are numbered (`01_...`, `02_...`) purely so
both loaders sort them into a stable, predictable order when they list a
directory — the number carries no other meaning.

`expected` was never computed by hand — it comes from a working reference
implementation kept outside this repository, checked once and then
treated as ground truth. Take it as correct.

## Simple — `simple/`

Tiny event sequences. Each one isolates a single mechanic rather than
combining several, so a failure here points at a specific piece of
missing logic rather than "something is wrong somewhere."

| Case | Islands | Events | Expected | Tests |
|---|---|---|---|---|
| `01_single_bridge` | 2 | `U 0 1`, `Q 0 1` | 1 | The most basic case: build one bridge, ask if it connects what it should. |
| `02_query_before_bridge` | 2 | `Q 0 1` | 0 | A query with no bridges built yet. Checks that the starting state is "nothing is connected to anything else," not some other default. |
| `03_self_query` | 1 | `Q 0 0` | 1 | An island can always reach itself, with zero bridges involved. |
| `04_transitive_chain` | 3 | `U 0 1`, `U 1 2`, `Q 0 2` | 1 | Islands 0 and 2 are never bridged directly — only through island 1. Checks that "connected" means "connected via any sequence of bridges," not just "directly bridged." |
| `05_separate_components` | 4 | `U 0 1`, `U 2 3`, `Q 0 2` | 0 | Two separate pairs of islands, each internally connected, but never connected to each other. |
| `06_mixed_queries` | 4 | `U 0 1`, `Q 0 1`, `Q 0 2`, `U 1 2`, `Q 0 2` | 2 | The same pair of islands (0 and 2) is queried twice, with a bridge built in between — and gets a different answer each time. Checks that a query reflects the state at that exact point in the sequence, not the final state. |
| `07_redundant_bridge` | 2 | `U 0 1`, `U 0 1`, `Q 0 1` | 1 | The same bridge is "built" twice. Checks that building a bridge that already exists doesn't cause an error or a miscount. |
| `08_five_islands_merge` | 5 | `U 0 1`, `U 2 3`, `U 1 2`, `U 3 4`, `Q 0 4` | 1 | Two separate pairs get stitched into one group by later bridges. By the final query, everything is connected to everything. |

## Medium — `medium/`

Still small enough to work out with pencil and paper, but big enough that
the interesting behaviour is a genuine correctness question, not a
one-glance inspection.

| Case | Islands | Expected | Tests |
|---|---|---|---|
| `01_long_chain_trap` | 8 | 4 | **The trap.** A long run of bridges built one at a time (0–1, 1–2, 2–3, …) with queries checking connectivity along the way. A solution that tracks each island's group using a direct pointer — updated only for the two islands directly involved in each new bridge, without accounting for anything that was already pointing through one of them — will get the first bridge or two right and then start silently giving wrong answers as the chain grows. This is the single highest-signal case in the whole suite. |
| `02_two_chains_never_meet` | 6 | 2 | Two separate chains of bridges, never connected to each other. Checks that a solution correctly says "no" across components just as reliably as it says "yes" within one. |
| `03_redundant_unions` | 5 | 3 | Several bridges are built more than once (in both directions, `U 0 1` and `U 1 0`), interleaved with real new bridges and queries. Checks that repeatedly "building" an existing bridge never corrupts what's already been tracked. |
| `04_star_topology` | 6 | 5 | One hub island bridged directly to five others, one at a time. The leaf islands are never bridged to each other directly — only through the hub. Checks that a solution handles this shape as comfortably as a straight chain; some approaches quietly assume connections only ever form in a line. |
| `05_temporal_ordering` | 4 | 2 | The same two pairs of islands are each queried once before their bridge is built and once after. Checks — like `06_mixed_queries` in the simple tier, but with two independent pairs instead of one — that ordering is respected throughout, not just in a single lucky case. |

## Hard — `hard/`

Two different kinds of case, both too large to work out by hand.

**Long chains (`01`–`03`).** Islands are bridged into one long chain,
0–1–2–…, with a query back to island 0 injected after every single
bridge. Building the chain itself is cheap. What's expensive is
repeatedly asking "is island 0 still connected to the far end?" as that
far end keeps getting further away — an approach that re-derives an
island's current group from scratch every time, without keeping account
of anything it already worked out, will find each successive query more
expensive than the last. The costs compound fast, even though these
chains only reach into the tens of thousands of islands.

**Random workloads (`04`–`06`).** Large numbers of islands with bridges
and queries in random order — no adversarial structure, just realistic
scale. These exist to check whether a solution tracks connectivity
directly at all, versus re-exploring the whole map of bridges built so
far on every single query. The latter works fine on the simple and
medium tiers and becomes unusable here.

| Case | Islands | Events | Expected | Tests |
|---|---|---|---|---|
| `01_chain_n15000` | 15,000 | 29,998 | 14,999 | Smallest of the three chains — confirms the basic behaviour before scaling up. |
| `02_chain_n25000` | 25,000 | 49,998 | 24,999 | A longer chain, same shape. |
| `03_chain_n35000` | 35,000 | 69,998 | 34,999 | The longest chain in the suite — the heaviest version of the "repeatedly ask about a moving target" cost. |
| `04_random_workload_n20000` | 20,000 | 39,997 | 4,162 | A large, unstructured mix of bridges and queries. Mostly a scale and performance check. |
| `05_random_workload_n45000` | 45,000 | 89,996 | 9,156 | Roughly double the scale of `04` — the heaviest general-purpose scale check in the suite. |
| `06_mostly_disconnected_n30000` | 30,000 | 65,000 | 8 | Thousands of small, separate groups of islands, queried heavily and mostly asking about pairs in *different* groups. Checks that correctly saying "no" stays fast too — it isn't only the "yes" answers that need to scale. |
