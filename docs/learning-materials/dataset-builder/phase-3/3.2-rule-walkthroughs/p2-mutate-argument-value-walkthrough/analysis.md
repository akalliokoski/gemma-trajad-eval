# Infographic analysis — P2 mutate_argument_value walkthrough

## Topic
P2 mutate_argument_value: how argument-level perturbations create `bad_tool_arguments` anomalies, what real samples look like, and what implementation cleanup made the rule more believable.

## Audience
A technically curious learner reading the repo after the earlier P1 walkthrough.

## Content shape
This is not a metrics dashboard. It is a technical debrief with:
- one compact rule definition
- one design problem (`_CORRUPTED` strings + bool/int bug)
- one bounded implementation fix
- three to four concrete before/after examples
- one verification block

## Most important learning objectives
1. Understand how P2 differs from P1: same tool, wrong argument.
2. See why mutation realism depends on argument type.
3. Remember the bug: Python `bool` is a subclass of `int`.
4. Remember the fix: flip booleans, use typo/path-like string corruption, keep tests tight.

## Recommended layout × style
- Layout: `dense-modules`
- Style: `pop-laboratory`
- Aspect: `portrait`

Why:
- the content is a high-density technical guide with several small example cards
- the visual should feel precise and repo-engineering oriented rather than playful
- portrait works well for stacked modules: rule summary, real examples, bug/fix, verification, takeaway

## Information modules to show
1. Rule contract
2. Real string example
3. Real integer example
4. Boolean bug and fix
5. Verification summary
6. Design takeaway

## Text-density guidance
Prefer large readable headings, short labels, and tiny code-like chips instead of long paragraphs. Use arrows for before/after examples.
