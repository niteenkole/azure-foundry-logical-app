# AI Model Governance Policy

**Document ID:** DEMO-AI-GOV-001  
**Version:** 1.4  
**Status:** Synthetic demonstration document  
**Policy owner:** Enterprise Technology Risk  
**Review cycle:** Annual and whenever a material model, provider, or regulatory change occurs

> This document is fictional content created for a technical demonstration. It is not legal, security, privacy, procurement, or compliance advice.

## A. Policy Purpose and Scope

### A.1 Purpose

This policy defines the minimum governance requirements for evaluating, approving, deploying, and monitoring generative AI models used to support business processes.

The policy applies to:

- Foundation models accessed through a cloud provider.
- Models hosted by a third-party provider.
- Fine-tuned or adapted models used with enterprise data.
- AI agents that call models, tools, search indexes, or business systems.
- Internal prototypes when they process non-public enterprise information.

### A.2 Scope

This policy applies to foundation models, third-party models, adapted models, AI agents, retrieval systems, and prototypes that process non-public enterprise information.

## B. Core Principles

### B.1 Approved Use Only

A model may be used only for a documented business purpose with a named business owner. The owner is accountable for the intended use, user population, data types, and operational outcome.

### B.2 Minimum Necessary Data

Applications must send only the data needed for the approved task. Personal information, confidential business information, credentials, access tokens, and production secrets must not be included unless the use case has explicit approval and technical controls.

### B.3 Human Accountability

A model output is decision support, not an approval or authoritative business decision, unless a separate control owner has approved the use case and defined human review requirements.

### B.4 Explainable Boundaries

The application must document what the model can answer, what sources it may use, what it must refuse, and when a human must review the output.

## C. Risk Tiers

### C.1 Tier 1: Low-Risk Assistance

Examples include drafting, reformatting, summarizing public information, and generating non-sensitive test content.

Required controls:

- Named business owner.
- Basic application testing.
- User notice that content is AI-generated.
- No confidential or personal data unless separately approved.

### C.2 Tier 2: Controlled Enterprise Assistance

Examples include searching internal policy documents, preparing internal summaries, and assisting employees with approved procedures.

Required controls:

- Security review.
- Privacy review when personal information may be processed.
- Approved knowledge sources with document ownership.
- Access control based on the user's business need.
- Logging of safe operational metadata.
- Human escalation when the source does not answer the question.

### C.3 Tier 3: High-Impact or Regulated Use

Examples include automated decisions affecting customers, employees, eligibility, claims, underwriting, legal outcomes, financial actions, or access to critical services.

Required controls:

- Formal risk assessment.
- Executive or delegated risk approval.
- Legal and privacy review.
- Documented human-in-the-loop decision.
- Monitoring for accuracy, drift, unfair outcomes, and harmful responses.
- Tested rollback and incident response procedures.

## D. Model and Provider Approval

### D.1 Required Approval Record

Before production use, the requester must record:

1. Business purpose and named owner.
2. Model provider and deployment name.
3. Model region and service boundary.
4. Data categories sent to the model.
5. Provider retention and training-use terms.
6. Identity, access, and secret-management design.
7. Logging, monitoring, and incident response design.
8. Human review and escalation process.
9. Expected cost and usage limits.
10. Exit plan if the provider or model is no longer approved.

An external model provider requires the third-party review described in `third-party-model-review-standard.md`.

## E. Prompt and Response Handling

### E.1 Input and Instruction Handling

The application must validate user input before the model request. It must apply an approved system instruction and must not rely on the model alone to enforce deterministic limits.

Responses must be treated as untrusted generated content. The application must:

- Identify when an answer is based on retrieved policy content.
- Say when the approved source does not contain an answer.
- Avoid presenting generated text as a binding approval.
- Apply output handling before displaying or sending content to another system.
- Escalate high-impact decisions to an accountable human.

### E.2 Response Handling

## F. Monitoring and Review

The service owner must review operational telemetry at a defined interval. Safe telemetry may include trace ID, deployment name, latency, status, error category, and usage counters.

Ordinary application logs must not contain API keys, access tokens, full sensitive prompts, or sensitive retrieved documents unless a separate controlled logging design has been approved.

### F.1 Safe Operational Telemetry

## G. Exceptions

### G.1 Exception Requirements

An exception must identify the control being waived, business justification, data involved, compensating controls, approving authority, expiration date, and review date. Exceptions are time-limited and must not become a permanent substitute for the standard control.
