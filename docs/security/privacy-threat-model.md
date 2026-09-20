# Threat Model & Privacy Preservation Architecture

## Core Risk Factors

| Risk | Mitigation Strategy |
|---|---|
| **Stigma / Fear of Exposure** | Zero login required; anonymous local session storage. |
| **Data Leakage of Student Identity** | No collection of IP tracking, names, roll numbers, or contact details. |
| **Crisis Escalation** | Prominent emergency banner with direct national crisis helplines on every view. |
| **Cross-Site Scripting (XSS)** | Sanitized React UI components and modern Content Security Policy headers. |

## Data Flow Privacy Standard

All assessment evaluations happen in memory. No user responses are linked to persistent database records with identifiable metadata.
