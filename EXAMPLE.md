# Worked example, step by step

This walks through the problem by hand, tracking state one event at a
time, using a real example (it's the same case as
`test_data/medium/01_long_chain_trap.txt`, so you can cross-check the
final answer against that file). The goal here is to make sure the
*rules* of the problem are completely clear before you write any code —
it deliberately stops short of showing you an efficient way to track
this as the event list gets large. See [README.md](README.md) for the
full problem statement and constraints.

## The setup

```
n = 8 islands: 0, 1, 2, 3, 4, 5, 6, 7
```

Think of the islands as sitting in **groups** — sets of islands that can
currently reach one another via some sequence of bridges, however
roundabout. At the start, before any bridges exist, every island is
alone in its own group:

```
{0} {1} {2} {3} {4} {5} {6} {7}
```

A `U u v` event **merges** the group containing `u` with the group
containing `v` into one bigger group (if they're already in the same
group, nothing changes). A `Q u v` event asks: right now, at this exact
point in the sequence, are `u` and `v` in the same group? Bridges are
never removed, so groups only ever merge — they never split back apart.

## Stage by stage

Process the events in order, updating the groups, and answering each
query against the groups *as they stand at that moment*.

| Event | What happens | Groups after |
|---|---|---|
| `U 0 1` | merge `{0}` and `{1}` | `{0,1} {2} {3} {4} {5} {6} {7}` |
| `U 1 2` | merge `{0,1}` and `{2}` | `{0,1,2} {3} {4} {5} {6} {7}` |
| `Q 0 2` | 0 and 2 are both in `{0,1,2}` → **yes** | *(unchanged)* |
| `U 2 3` | merge `{0,1,2}` and `{3}` | `{0,1,2,3} {4} {5} {6} {7}` |
| `U 3 4` | merge `{0,1,2,3}` and `{4}` | `{0,1,2,3,4} {5} {6} {7}` |
| `Q 0 4` | 0 and 4 both in `{0,1,2,3,4}` → **yes** | *(unchanged)* |
| `U 4 5` | merge in `{5}` | `{0,1,2,3,4,5} {6} {7}` |
| `U 5 6` | merge in `{6}` | `{0,1,2,3,4,5,6} {7}` |
| `U 6 7` | merge in `{7}` | `{0,1,2,3,4,5,6,7}` |
| `Q 0 7` | 0 and 7 both in the one big group → **yes** | *(unchanged)* |
| `Q 1 6` | 1 and 6 both in the one big group → **yes** | *(unchanged)* |

Four `Q` events, all four answered "yes."

**Answer: `count_reachable_queries(8, events)` = `4`.**

The thing worth noticing: **island 0 and island 2 are never bridged
directly** — the only bridge touching island 0 is `U 0 1`, and the only
bridges touching island 2 are `U 1 2` and `U 2 3`. They're connected
purely because the group they both ended up in grew to include them
both, one merge at a time. By the last query, `Q 1 6`, the entire
archipelago has folded into a single group through a long chain of
individually small merges — nothing in the event list ever mentions
island 1 and island 6 together directly.

---

## A second wrinkle: the same pair can answer differently at different times

Different example (same as `test_data/simple/06_mixed_queries.txt`):

```
n = 4 islands: 0, 1, 2, 3
events:
  U 0 1
  Q 0 1
  Q 0 2
  U 1 2
  Q 0 2
```

Walking through it:

| Event | Groups after | Query answer |
|---|---|---|
| `U 0 1` | `{0,1} {2} {3}` | — |
| `Q 0 1` | *(unchanged)* | 0 and 1 same group → **yes** |
| `Q 0 2` | *(unchanged)* | 0 and 2 different groups → **no** |
| `U 1 2` | `{0,1,2} {3}` | — |
| `Q 0 2` | *(unchanged)* | 0 and 2 now same group → **yes** |

The *exact same pair*, `0` and `2`, is asked about twice and gets a
different answer each time, because a bridge was built in between. A
query only ever reflects the state of the archipelago at that precise
point in the event list — not what the archipelago eventually becomes.

**Answer: `count_reachable_queries(4, events)` = `2`.**
