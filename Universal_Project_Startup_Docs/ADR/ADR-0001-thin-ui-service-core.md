# ADR-0001 — Thin UI With Service/Domain Core

## Status
Template seed / Usually recommended, confirm per project

## Decision
Business rules, validation, workflow transitions, permissions, parsing, persistence, and audit behavior should live outside the UI layer. UI files should render, collect input, and call services.

## Context
Prior projects showed that UI-owned business logic creates fragile rerun behavior, weak testing, and poor portability.

## Alternatives considered
- UI-heavy implementation: fast early build, poor long-term maintainability.
- Service/domain core with thin UI: more structure early, stronger testing and future portability.

## Why chosen
This pattern prevents spaghetti code and allows future UI replacement without rewriting the application core.

## Consequences
Easier testing, cleaner architecture, clearer ownership. Requires discipline and up-front module planning.

## Review trigger
Revisit only for tiny throwaway tools with no persistence, review, audit, or long-term maintenance expectations.
