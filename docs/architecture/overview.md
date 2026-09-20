# AmiCare System Architecture & PDD Specification

## Community Impact & SDG 3 Alignment

AmiCare is designed specifically for SDG 3 (Good Health and Well-Being). The platform targets early awareness to prevent academic burnout and mental strain among university students.

```
+-----------------------------------------------------------------------------------+
|                            AmiCare Student Platform                               |
+-----------------------------------------------------------------------------------+
                                          |
     +------------------------------------+-----------------------------------+
     |                                    |                                   |
     v                                    v                                   v
+-----------------------+   +---------------------------+   +-----------------------+
|  Self-Assessment UI   |   |   Helpline Referral DB    |   |   Breathing & Care    |
| (PSS-4 / GAD-7 Scale) |   |  (Tele-MANAS, KIRAN 24/7) |   | (Box & 4-7-8 Breathing)|
+-----------+-----------+   +-------------+-------------+   +-----------+-----------+
            |                             |                             |
            +-----------------------------+-----------------------------+
                                          |
                                          v
                            +---------------------------+
                            |     FastAPI Backend API   |
                            |   (Python .venv + SQLite) |
                            +---------------------------+
```

## Data Flow Pipeline

1. **Student Response Ingestion**: Student completes non-diagnostic questions. No PII stored.
2. **Score Computation**: PSS-4 / GAD-7 algorithm calculates total score tier (Low, Moderate, Elevated).
3. **Guidance Synthesis**: Matches student score tier with self-care techniques (Breathing, Grounding).
4. **Targeted Helpline Referral**: Recommends appropriate crisis lines (e.g. Tele-MANAS 14416 for elevated risk).
