# LUE tutorial

🚧 🚧 🚧 🚧 🚧 🚧 Work in progress. 🚧 🚧 🚧 🚧 🚧 🚧

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Use cases
We have added relatively simple use-cases here, to illustrate what LUE can be used for. They
are very simple, which is on purpose of course. LUE hides much of the complicated stuff to
perform very large models on large amounts of hardware.

BTW, we accept pull-requests for additional use-cases, so please do contribute yours if you
have any.

Current list:

- [Universal Soil Loss Equation (USLE)](use_case/usle)
- [Conway's Game of Life](use_case/game_of_life)
- [Merge raster](use_case/merge_raster)
    - Run a non-LUE numerical simulation model concurrently for multiple areas, and aggregate
      the results in a single LUE dataset.
