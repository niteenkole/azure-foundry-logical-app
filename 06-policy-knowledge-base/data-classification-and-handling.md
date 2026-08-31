# Data Classification and AI Handling Standard

**Document ID:** DEMO-DATA-AI-002  
**Version:** 2.1  
**Status:** Synthetic demonstration document  
**Policy owner:** Information Protection and Privacy

> This document is fictional content created for a technical demonstration. It is not an organizational data-classification policy.

## A. Purpose and Classification Model

### A.1 Purpose

This standard defines which information may be sent to an AI model and which protections are required before processing.

## B. Data Classes

### B.1 Public

Information approved for public distribution, such as published product information, public web content, public reports, and approved marketing material.

AI use:

- May be used with an approved model for drafting, summarization, classification, and translation.
- The business owner remains responsible for accuracy and publication approval.

### B.2 Internal

Routine business information that is not intended for public release but whose disclosure would cause limited harm. Examples include internal procedures, general operating guidance, and non-sensitive project information.

AI use:

- May be processed by an approved enterprise model.
- Access must be limited to authorized users.
- The application should use approved enterprise knowledge sources.
- Prompts and responses must not be exposed through ordinary public sharing.

### B.3 Confidential

Information that could cause material business, contractual, competitive, or operational harm if disclosed. Examples include non-public financial information, supplier terms, security architecture, internal investigations, and customer or partner information.

AI use:

- Requires documented business purpose and owner.
- Requires Security review before production use.
- Requires Privacy review when personal information is present.
- Must use approved provider terms, region, access controls, and retention settings.
- Must not be sent to an external model provider without third-party approval.

### B.4 Restricted

Information requiring the highest level of protection. Examples include credentials, private keys, access tokens, regulated records, highly sensitive personal information, authentication data, and information subject to legal hold.

AI use:

- Must not be sent to a model through a general-purpose prompt interface.
- Must not be placed in prompts, logs, source code, browser storage, or client-side telemetry.
- A specific approved architecture and risk assessment are required for any exceptional processing.

## C. Handling Rules

### C.1 Required Handling Controls

1. Classify the data before designing the model interaction.
2. Remove unnecessary names, identifiers, secrets, and fields.
3. Use masking or tokenization where the task does not require direct identifiers.
4. Confirm that the model provider's retention and training-use terms match the approved use case.
5. Restrict retrieved documents according to user authorization.
6. Treat model output as generated content until reviewed or verified.
7. Report suspected disclosure or unintended processing through the incident process.

## D. Example Decisions

### D.1 Internal Procedure Summary

Question: "Can the assistant summarize an internal procedure?"

Decision: Yes, if the procedure is classified Internal, the user is authorized, the document is an approved knowledge source, and the model deployment is approved for Internal data.

### D.2 Access Token Troubleshooting

Question: "Can I paste an access token so the assistant can troubleshoot it?"

Decision: No. Access tokens are Restricted and must never be placed in a prompt. Revoke or rotate the token through the approved operational process and provide sanitized diagnostic information instead.
