# Third-Party Model Review Standard

**Document ID:** DEMO-TPM-003  
**Version:** 1.0  
**Status:** Synthetic demonstration document  
**Policy owner:** Third-Party Risk and Enterprise Security

> This document is fictional content created for a technical demonstration. It is not a vendor contract or formal third-party risk assessment.

## A. Review Applicability

### A.1 When Review Is Required

A third-party model review is required before an application sends Internal, Confidential, or Restricted information to a provider outside the approved enterprise model boundary.

Review is also required when a provider:

- Stores prompts or responses.
- Uses customer content for service improvement or training.
- Routes data through an unapproved region.
- Uses subcontractors to process model requests.
- Provides tool calling or retrieval against external systems.
- Changes the model, hosting location, terms, or retention behavior materially.

## B. Required Evidence

### B.1 Provider and Data Evidence

The request owner must collect:

1. Provider name, service name, model name, and deployment region.
2. Data categories and example fields sent to the provider.
3. Retention period for prompts, responses, files, and telemetry.
4. Whether customer content is used for training or product improvement.
5. Encryption details in transit and at rest.
6. Identity and access-control options.
7. Subprocessor and cross-border processing information.
8. Security incident notification commitment.
9. Service availability, support, and deletion process.
10. Exit plan and an alternative provider or operating mode.

## C. Network and Application Controls

### C.1 Minimum Technical Controls

The application must use a controlled outbound path. At minimum, the design must include:

- An allow-list for approved provider destinations.
- A firewall, proxy, or API gateway that can block outbound requests.
- Secrets stored outside browser code and source control.
- Request size, rate, and cost limits.
- DLP or equivalent inspection where required by data classification.
- Safe telemetry that excludes secrets and sensitive prompt content.
- A kill switch or configuration change that disables the provider route.

A private endpoint to the internal Azure service does not automatically make the third-party provider private. The external hop requires its own approved network and data-transfer controls.

## D. Approval Outcomes

### D.1 Approved

The provider and model may be used for the documented data classes and purpose, subject to the listed controls and expiration or review date.

### D.2 Approved with Conditions

Use is allowed only after named compensating controls are implemented. Conditions must identify the owner, evidence, due date, and verification method.

### D.3 Rejected

The provider may not process the proposed data or support the proposed use case. The requester must use an approved provider or redesign the workflow.

## E. Assistant Review Questions

### E.1 Required Clarifying Questions

When asked whether an external model may be used, the assistant should identify the missing facts instead of giving an unconditional approval:

- What data classification is involved?
- Is personal or regulated information present?
- Which provider and model are being used?
- Where is the provider processing the request?
- What are the retention and training-use terms?
- Has Security, Privacy, and Third-Party Risk review been completed?
