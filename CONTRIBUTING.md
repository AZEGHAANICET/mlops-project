# Contributing to Iris Classifier

Thank you for your interest in contributing to the Iris Classifier project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/mlops-anicet.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes: `pytest`
6. Commit your changes: `git commit -m 'Add some feature'`
7. Push to your branch: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Download data and models:
   ```bash
   dvc pull
   ```

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions small and focused
- Write meaningful commit messages

## Testing

- Write tests for all new features
- Ensure all tests pass: `pytest`
- Aim for high test coverage
- Include both unit tests and integration tests

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md if applicable
3. Ensure all tests pass
4. Request a review from maintainers

## Questions?

If you have any questions, please open an issue on GitHub.

Thank you for contributing! 🎉

