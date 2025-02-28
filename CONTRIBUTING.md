# Contributing to the UnityChipForXiangShan Project

First off, thank you for considering contributing to our project! We appreciate your time and effort, and we value every contribution.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please create an issue on GitHub. Before creating a new issue, please check if the issue already exists.

1. Go to the [Issues](https://github.com/XS-MLVP/UnityChipForXiangShan/issues) page.
2. Search for existing issues to avoid duplicates.
3. If no similar issue exists, click on "New Issue" and fill out the template with as much detail as possible.
4. Add appropriate tags to your issue for better categorization, such as bug, DUT name, etc.

### Submitting Code Changes

We follow the GitHub Flow for our development process. Here are the steps to submit your code changes:

1. **Fork the repository**: Click the "Fork" button at the top right of the repository page.
2. **Clone your fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/XS-MLVP/UnityChipForXiangShan.git
   cd UnityChipForXiangShan
   ```
3. **Create a new branch**: Create a new branch for your changes.
   ```bash
   git checkout -b my-feature-branch
   ```
4. **Make your changes**: Make your changes to the codebase. For adding comprehensive unit tests, please refer to the [corresponding documentation](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/).
5. **Commit your changes**: Commit your changes with a descriptive commit message.
   ```bash
   git add .
   git commit -m "Description of my changes"
   ```
6. **Push to your fork**: Push your changes to your forked repository.
   ```bash
   git push origin my-feature-branch
   ```
7. **Create a Pull Request**: Go to the original repository and create a pull request from your fork. Fill out the pull request template with as much detail as possible.

### Code Style

Please ensure your code adheres to the following style guidelines:

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use meaningful variable and function names.
- Write comments and docstrings to explain your code.
- Ensure your code is well-formatted and linted.

### Writing Tests

If you add new functionality, please write tests to ensure it works correctly. We use [pytest](https://docs.pytest.org/en/stable/) for testing. If it is DUT-related, please refer to [this documentation](https://open-verify.cc/UnityChipForXiangShan/docs/03_add_test/); if it is non-DUT-related, please refer to [here](tests/README.md).


### Documentation

If your changes affect the documentation, please update the relevant sections. We use [docsy](https://www.docsy.dev/) for documentation. To build the documentation locally, use the following commands:

```bash
cd UnityChipForXiangShan
make doc
```

### Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

### Getting Help

If you need help or have any questions, feel free to reach out by creating an issue or joining our community QQ group: 600480230.

### Acknowledgments

Thank you for your contributions! Your support and involvement help make this project better.
