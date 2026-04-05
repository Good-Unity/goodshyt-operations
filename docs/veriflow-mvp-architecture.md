# Veriflow MVP architecture

Veriflow should be built as a mathematical knowledge-to-equation agent.

## Goal

Transform natural-language questions, formal rules, and datasets into:
- formal equations
- generated data
- formula-based answers
- validation records
- provenance

## Why this repo

`goodshyt-operations` already implements a typed request -> plan -> execute loop. That makes it the best initial home for the orchestration layer of a Veriflow MVP.

## MVP task types

1. equation_creation
2. data_generation
3. formula_question_answering

## Core loop

1. receive request
2. classify task
3. retrieve rules and context
4. call the right tool
5. validate result
6. return answer with trace

## Proposed modules

```text
src/goodshyt_operations/veriflow/
  models.py
  planner.py
  tools.py
  validator.py
  service.py
```

## Suggested API additions

- `POST /veriflow/parse`
- `POST /veriflow/generate-data`
- `POST /veriflow/answer`

## Data model sketch

- VeriflowRequest
- VeriflowTask
- FormalModel
- ToolTrace
- ValidationResult
- VeriflowResponse

## Repo boundaries

- `goodshyt-operations`: orchestration, tool routing, API endpoints
- `goodshyt-core`: reusable formal rules, scoring, shared primitives
- `goodshyt-synthesis-network`: later observability and cross-run evaluation

## First implementation target

Add one deterministic path:
- parse a request for a simple linear model
- generate rows from `y = m*x + b`
- answer a value query from that formula
- return steps and validation

## Notes

Start with strict tool schemas, bounded retries, and explicit validation before adding more task families.
