# optbyes: Generate a schedule of matchups that minimizes A
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![test](https://github.com/ueduck/optbyes/actions/workflows/ci.yml/badge.svg)](https://github.com/ueduck/optbyes/actions/workflows/ci.yml)

## What is it?
**optbyes** generates a schedule of matchups that minimizes *[byes](https://en.wikipedia.org/wiki/Bye_(sports))*, given the number of teams and the desired order of matchups for each team.

## Creating a development environment
### 1. Install Python
macOS (Homebrew)
```
brew install python@3.10
```
Windows (PowerShell)
```
winget install python -v 3.10
```
or install from [downloads page](https://www.python.org/downloads/).

### 2. Install poetry
macOS, Windows (WSL)
```
curl -sSL https://install.python-poetry.org | python3 -
```
Windows (PowerShell)
```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
For details, see [official installation instructions](https://python-poetry.org/docs/#installing-with-the-official-installer).

### 3. Clone this repository to your local computer
```
git clone https://github.com/ueduck/optbyes
```

### 4. Build environment
```
poetry install
```

## Dependencies
1. [Gurobipy - The Gurobi Optimizer is a mathematical optimization software library for solving mixed-integer linear and quadratic optimization problems.](https://pypi.org/project/gurobipy/)
1. [networkx - NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.](https://networkx.org/documentation/stable/index.html)
1. [matplotlib - Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. Matplotlib makes easy things easy and hard things possible.](https://matplotlib.org)
1. [scipy - Fundamental algorithms for scientific computing in Python](https://scipy.org)
