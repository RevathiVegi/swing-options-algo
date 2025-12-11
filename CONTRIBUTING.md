# Welcome
Thanks for your interest in contributing to Swing Options Algo!
Every contribution, big or small, helps strengthen the project.

## How to Contribute
1. Fork & Clone
Fork the repository
Clone your fork locally
Create a feature branch:
git checkout -b feature/<your-feature>

2. Setup
Use a virtual environment:
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

## Code Guidelines
### Style
Follow PEP8
Use type hints
Keep functions small and clean

### Logging
Use the logging module
Avoid print() in production paths

## Testing
Run tests before pushing:
pytest -q

## Commits
Use clear, descriptive commit messages:
Fix ensure_trade_pnl calculation in run_sim

### Pull Requests
Before submitting a PR:
Ensure tests pass
Ensure linting is clean
Update documentation if relevant
Provide a clear PR description

### Reporting Issues
Include:
What happened
What you expected
How to reproduce
Logs or screenshots if useful

### Code of Conduct
Be respectful, constructive, and collaborative.
