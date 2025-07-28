# Contributing to CivicMind AI

First off, thank you for considering contributing to CivicMind AI! 🎉

It's people like you that make CivicMind AI such a great platform for civic engagement and community building.

## 🌟 Code of Conduct

This project and everyone participating in it is governed by our commitment to creating inclusive, respectful, and helpful communities. By participating, you are expected to uphold these values.

### Our Values
- **Dharma**: Do what's right for the community
- **Ahimsa**: Non-harmful, constructive contributions
- **Seva**: Service-oriented mindset
- **Respect**: Honor diverse perspectives and cultures

## 🤝 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and expected**
- **Include screenshots if applicable**
- **Specify your environment** (OS, Python version, etc.)

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Code Contributions 👨‍💻

#### Development Environment Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/civicmind-ai.git
   cd civicmind-ai
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Create a branch for your feature**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

#### Code Style Guidelines

- **Follow PEP 8** for Python code style
- **Use type hints** for all function parameters and return values
- **Write comprehensive docstrings** using Google style
- **Keep functions focused** and under 50 lines when possible
- **Use meaningful variable names**

Example:
```python
def analyze_civic_issue(
    description: str, 
    location: str, 
    priority: Priority = Priority.MEDIUM
) -> CivicAnalysisResult:
    """
    Analyze a civic issue and provide recommendations.
    
    Args:
        description: Detailed description of the civic issue
        location: Geographic location (city, state format)
        priority: Issue priority level
    
    Returns:
        Analysis result with recommendations and next steps
    
    Raises:
        ValidationError: If input parameters are invalid
    """
```

#### Testing Guidelines

- **Write tests** for all new functionality
- **Maintain test coverage** above 80%
- **Use descriptive test names**
- **Test edge cases and error conditions**

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=civicmind

# Run specific test file
pytest tests/test_agents.py
```

#### Agent Development Guidelines

When creating new civic agents:

1. **Inherit from `BaseCivicAgent`**
2. **Implement required abstract methods**
3. **Focus on community-first solutions**
4. **Respect cultural sensitivities**
5. **Provide clear, actionable guidance**

Example agent structure:
```python
class NewCivicAgent(BaseCivicAgent):
    def get_system_prompt(self) -> str:
        return """
        You are a specialist in [domain] civic issues.
        Always prioritize community resolution before legal escalation.
        Be respectful of cultural differences and local customs.
        """
    
    def analyze_issue(self, description: str, location: str, context: Dict) -> AgentResponse:
        # Your implementation here
        pass
```

## 📝 Documentation Contributions

We welcome improvements to documentation:

- **Fix typos and grammatical errors**
- **Improve clarity and examples**
- **Add missing documentation**
- **Translate documentation to other languages**

## 🌍 Localization

Help make CivicMind AI accessible worldwide:

- **Translate interface text**
- **Adapt cultural references**
- **Add region-specific civic knowledge**
- **Implement local government API integrations**

## 🚀 Pull Request Process

1. **Ensure your code follows the style guidelines**
2. **Update documentation** for any new features
3. **Add or update tests** as appropriate
4. **Ensure all tests pass**
5. **Update the CHANGELOG.md** if applicable
6. **Fill out the pull request template completely**

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Description of testing performed

## Checklist:
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## 🔍 Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. **Maintainers will review your PR** within 48 hours
2. **Address any feedback** promptly and respectfully
3. **Make requested changes** in new commits
4. **Once approved**, a maintainer will merge your PR

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- **New civic agents** for different domains (housing, environmental, etc.)
- **Government API integrations** (311 systems, permit portals)
- **Multi-language support**
- **Mobile app development**

### Medium Priority
- **Performance optimizations**
- **Enhanced analytics and reporting**
- **Voice input/output capabilities**
- **Better error handling and logging**

### Documentation & Community
- **Tutorial videos and guides**
- **Community examples and case studies**
- **API documentation improvements**
- **Accessibility improvements**

## 🏆 Recognition

Contributors will be recognized in several ways:

- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Invited to maintainer discussions**
- **Conference speaking opportunities** (for significant contributions)

## 📞 Getting Help

Need help with your contribution?

- **GitHub Discussions**: Ask questions and get help
- **Discord**: Join our real-time chat (link in README)
- **Email**: civicmind-dev@googlegroups.com
- **Office Hours**: Bi-weekly video calls (Fridays 2-3 PM PST)

## 🎉 Your First Contribution

New to open source? Here are some good first issues:

- Look for issues labeled `good first issue`
- Documentation improvements
- Adding test cases
- Fixing typos or small bugs

## 🔄 Release Process

1. **Version bumping** follows semantic versioning
2. **Release notes** are generated from merged PRs
3. **Releases** happen monthly or as needed for critical fixes
4. **Breaking changes** are clearly documented and communicated

## 📜 License

By contributing to CivicMind AI, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for helping make civic engagement more accessible and effective for communities worldwide! 🌍✨
