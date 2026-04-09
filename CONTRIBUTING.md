# Contributing Guide

This repository is used as a student-facing learning companion. Contributions should optimize for clarity, reproducibility, and teaching value, not only for technical correctness.

## Goals

- keep demos easy for students to run
- make the business context explicit
- prefer synthetic data when real data is unavailable or sensitive
- leave a clear path for extension exercises

## Preferred Demo Structure

For a new demo folder, please include:

- `README.md`
- `requirements.txt` or `pyproject.toml`
- a synthetic data generator if needed
- one main runnable script
- optional notebook for interactive exploration
- optional screenshots or output artifacts

## README Template Expectations

Each demo README should cover:

- what the demo does
- why it matters in BFSI or analytics
- files in the folder
- setup steps
- how to run the demo
- expected outputs
- ideas for student extensions

## Naming and Organization

- prefer descriptive folder names over cryptic names
- keep business use cases under `DomainUseCaseDemos`
- keep technique-first examples under `TechUseCaseDemos`
- use consistent naming for `README.md`

## Testing

Where practical, add at least a smoke test that verifies:

- synthetic data generation runs
- key scripts execute without crashing
- expected output files or columns are created

## Documentation Style

- explain both the technical method and the business meaning
- write for students who may be seeing the topic for the first time
- keep setup instructions explicit

## Safe Data Practices

- do not commit sensitive or private real-world data
- prefer synthetic datasets for teaching examples
- call out any assumptions used to generate synthetic data
