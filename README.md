# Monorepo for PanthEON SDK

This repository contains multiple standalone Python services, each organized as an individual package with its own source code, configuration, and tests.

## Project Structure

Example structure of a single service (`s3-service`):

```
s3-service/
├── src/
│   └── s3_service/
│       ├── __init__.py
│       ├── config.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_s3_service.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

* `src/` — contains the main application code.
* `tests/` — includes unit and integration tests.
* `pyproject.toml` — defines the package configuration (managed with Poetry).
* `README.md` — service-level documentation.

## Requirements

* Python 3.10+
* [Poetry](https://python-poetry.org/) for dependency management

## Installation

```bash
poetry install
```

## Running Tests

```bash
poetry run pytest
```

## Adding New Packages

To add a new service, replicate the structure of `s3-service` and update the root documentation as needed.

## Support

### Getting Help

If you need help or have questions about the PanthEON SDK:

- **GitHub Issues**: For bug reports and feature requests, please use our [issue templates](https://github.com/eon-fun/pantheon-sdk-core/issues/new/choose)
- **GitHub Discussions**: For general questions and community discussions, visit our [discussions page](https://github.com/eon-fun/pantheon-sdk-core/discussions)
- **Documentation**: Check our [contributing guide](docs/CONTRIBUTING.md) for development workflows

### Response Time

We aim to respond to issues and discussions within **48 hours** during business days. Please be patient as our maintainers are volunteers.

### Breaking Changes Policy

We follow semantic versioning and maintain backward compatibility:

- **MAJOR version bumps**: We will maintain backward compatibility for at least **6 months** before removing deprecated features
- **MINOR version bumps**: Only add new features, no breaking changes
- **PATCH version bumps**: Bug fixes and security updates only

All breaking changes will be clearly documented in our [CHANGELOG.md](CHANGELOG.md) and announced in advance.

## Maintainers

This project is maintained by:

- **Technical Lead**: [@golemxiv](https://github.com/golemxiv)
- **Primary Maintainer**: [@k1llzz](https://github.com/k1llzz)
- **Core Maintainer**: [@polkadot21](https://github.com/polkadot21)
- **Infrastructure Maintainer**: [@drobotukhin](https://github.com/drobotukhin)

### Maintainer Responsibilities

- Review and merge pull requests
- Triage and respond to issues
- Release new versions
- Maintain project roadmap and direction

### Becoming a Maintainer

We welcome new maintainers! If you're interested in helping maintain this project:

1. **Contribute regularly**: Submit quality PRs and help with issue triage
2. **Show commitment**: Demonstrate sustained involvement over 3+ months
3. **Express interest**: Reach out to existing maintainers via GitHub Discussions
4. **Onboarding**: Current maintainers will provide access and guidance

### Maintainer Rotation

- Maintainers may step down at any time by notifying the team
- Inactive maintainers (6+ months) will be asked about their continued involvement
- New maintainers require approval from at least 2 existing maintainers
