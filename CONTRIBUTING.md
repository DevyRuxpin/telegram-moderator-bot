# Contributing to Telegram Moderator Bot

First off, thank you for considering contributing to Telegram Moderator Bot! It's people like you that make this bot better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what you expected**
* **Include screenshots if possible**
* **Include your Python version and OS**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Provide specific examples to demonstrate the enhancement**
* **Describe the current behavior and explain the behavior you expected**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide (PEP 8)
* Include thoughtful comments in your code
* End all files with a newline
* Write clear commit messages

## Development Setup

1. Fork the repo
2. Clone your fork:
```bash
git clone https://github.com/your-username/telegram-moderator-bot.git
cd telegram-moderator-bot
```

3. Create a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a branch for your changes:
```bash
git checkout -b feature/your-feature-name
```

## Style Guide

### Python Style

* Follow PEP 8
* Use 4 spaces for indentation
* Use descriptive variable names
* Add docstrings to all functions and classes
* Keep lines under 100 characters when possible

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests after the first line

Example:
```
Add user statistics dashboard

- Implement statistics collection
- Create dashboard view
- Add export functionality

Closes #123
```

## Testing

Before submitting a pull request, please:

1. Test your changes thoroughly
2. Ensure the bot runs without errors
3. Test in a real Telegram group if possible
4. Document any new features in README.md

## Questions?

Feel free to create an issue with your question or reach out in our Telegram group!

Thank you for contributing! 🎉

