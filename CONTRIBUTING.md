# Contributing to AmiCare

Thank you for contributing to AmiCare! We welcome contributions aimed at making stress self-assessment and mental health resources more accessible to students.

## Code of Conduct

Maintain an empathetic, supportive, and inclusive tone in all code, UI copy, and discussions. Avoid stigmatizing or clinical diagnostic language.

## Development Workflow

1. Setup Python Virtual Environment:
   ```bash
   python -m venv backend/.venv
   # Windows PowerShell
   .\backend\.venv\Scripts\Activate.ps1
   pip install -r backend/requirements.txt
   ```

2. Setup Frontend:
   ```bash
   cd frontend
   npm install
   ```

3. Code Formatting & Linting:
   - Backend: PEP 8 compliant code structure.
   - Frontend: ESLint clean code without unused imports or variables.

4. Git Commit Messages:
   Use standard conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`.

> [!WARNING]
> Do not commit sensitive tokens, database credentials, or real user identifiers into the repository.
