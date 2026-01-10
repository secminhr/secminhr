---
title: "test draft"
date: 2025-11-27T21:32:34+0800
categories: ["Draft"]
tags: ["test"]
---

This is a test draft.

Testing typst formula.
```typst
#import "@preview/curryst:0.6.0": rule, prooftree, rule-set
#let tree = rule(
  label: [Label],
  name: [Rule name],
  [Premise 1],
  [Premise 2],
  [Premise 3],
  [Conclusion],
)
#prooftree(tree)
```