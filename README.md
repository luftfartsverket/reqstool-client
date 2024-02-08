# Reqstool Client

## Overview

Reqstool is a tool for managing requirements with related software verification cases (aka tests) and verification results (test results).

- Requirements are defined in YAML files and can reference each other (depending on the variant different data will be parsed).
- Annotations are then used in code to specify where a requirement is implemented as well as tested.

With this information and the actual test results (e.g., JUnit), use Reqstool to:

- Generate a report (AsciiDoc, which can be transformed into e.g. PDF) listing all requirements, where that requirement is implemented and tested, and whether the tests passed/failed. This report can be used e.g. with auditors ("Yes, we track this requirement, it's implemented (here) and it has been tested with a pass (here).")
- Status the software, i.e. get a list of all requirements, their status on implementation and tests. Reqstool will exit with a status code equal to the number of requirements that have not been implemented and tested with a pass. Hence, it can be used in a pipeline as a gate for deployment to production.

## Installation

You need to have the following installed in order to use the tool:

- Python, 3.10 or later
- pip

To use the tool, you need to install the PyPI package *reqstool*.

```bash
pip install -U reqstool
reqstool -h # to confirm installation
```

## Usage

```bash
reqstool [-h] {command: report-asciidoc,generate-json,status} {location: local,git,maven} ...
```

Use `-h/--help` for more information about each command and location.

## Documentation

For full documentation see [xxx](https://somelink).

## Contributing

- We adhere to the latest version of [Contributor Covenant](https://www.contributor-covenant.org/).
- Fork repo
- Before submitting a PR
  - Perform formatting (black):  `hatch run lint:black src tests`
  - Run linter (flake8): `hatch run lint:flake8`
  - Run tests:
    - all: `hatch run test:pytest --cov=reqstool`
    - unit only: `hatch run test:pytest --cov=reqstool  tests/unit`
    - integration only: `hatch run test:pytest --cov=reqstool  tests/integration`
