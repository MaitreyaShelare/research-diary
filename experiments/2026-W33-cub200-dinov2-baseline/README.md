---
type: experiment
experiment_id: 2026-W33-cub200-dinov2-baseline
week: 2026-W33
status: completed
project: cub200
dataset: cub-200-2011
tags: [baseline, dinov2]
---

# Experiment: 2026-W33-cub200-dinov2-baseline

## Goal
Create a reproducible frozen-feature baseline for CUB-200 classification using DINOv2 embeddings.

## Context
This baseline anchors future augmentation and classifier-head ablations for the cub200 project.

## External Links
- Code repository: https://github.com/example/research-cub200
- W&B run/group: https://wandb.ai/example/cub200/runs/placeholder

## Setup Summary
- Model: Frozen DINOv2 backbone + linear classifier head.
- Data: CUB-200-2011 standard split.
- Training protocol: Fixed seed, standard augmentations, early stopping on validation loss.

## Results Snapshot
- Primary metric(s): Placeholder top-1 accuracy and validation loss.
- Secondary notes: Stable convergence with no anomalous run behavior.

## Interpretation
The setup is stable enough to use as a baseline reference, but deeper class-wise analysis is needed.

## Decision
Keep this baseline unchanged and build targeted ablations on top.

## Next Step
Run augmentation variants and compare class-level confusion changes.
