# API Endpoints Specification

## Base URL
`http://127.0.0.1:8000/api`

## Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Server healthcheck status |
| `GET` | `/assessment/questions` | Retrieve self-assessment question set |
| `POST` | `/assessment/evaluate` | Submit answers, calculate score & get recommendations |
| `GET` | `/helplines` | List referral helplines (optional filter by `category`) |
| `GET` | `/helplines/{id}` | Get detailed helpline information |
| `GET` | `/resources` | Retrieve self-care guides and exercises |

## Example Request/Response

### `POST /api/assessment/evaluate`
**Request Payload:**
```json
{
  "answers": [
    {"question_id": 1, "score": 2},
    {"question_id": 2, "score": 3},
    {"question_id": 3, "score": 1},
    {"question_id": 4, "score": 2}
  ]
}
```

**Response Payload:**
```json
{
  "total_score": 8,
  "max_score": 16,
  "level": "Moderate Stress",
  "summary": "You are experiencing moderate stress. It is common during academic peaks.",
  "recommendations": [
    "Try the 4-7-8 box breathing exercise.",
    "Consider speaking with a student counselor or peer mentor."
  ],
  "recommended_helplines": [
    {
      "id": 1,
      "name": "Tele-MANAS",
      "number": "14416",
      "category": "24/7 National Crisis Line"
    }
  ]
}
```
