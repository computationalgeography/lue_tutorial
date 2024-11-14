# LUE tutorial

🚧 🚧 🚧 🚧 🚧 🚧 Work in progress. 🚧 🚧 🚧 🚧 🚧 🚧

| Branch                                                                         | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                            | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [main](https://github.com/computationalgeography/lue_tutorial/tree/main)       | [![Linux](https://github.com/computationalgeography/lue_tutorial/actions/workflows/linux.yml/badge.svg?branch=main)](https://github.com/computationalgeography/lue_tutorial/actions/workflows/linux.yml) [![macOS](https://github.com/computationalgeography/lue_tutorial/actions/workflows/macos.yml/badge.svg?branch=main)](https://github.com/computationalgeography/lue_tutorial/actions/workflows/macos.yml) [![Windows](https://github.com/computationalgeography/lue_tutorial/actions/workflows/windows.yml/badge.svg?branch=main)](https://github.com/computationalgeography/lue_tutorial/actions/workflows/windows.yml)          |
| [develop](https://github.com/computationalgeography/lue_tutorial/tree/develop) | [![Linux](https://github.com/computationalgeography/lue_tutorial/actions/workflows/linux.yml/badge.svg?branch=develop)](https://github.com/computationalgeography/lue_tutorial/actions/workflows/linux.yml) [![macOS](https://github.com/computationalgeography/lue_tutorial/actions/workflows/macos.yml/badge.svg?branch=develop)](https://github.com/computationalgeography/lue_tutorial/actions/workflows/macos.yml) [![Windows](https://github.com/computationalgeography/lue_tutorial/actions/workflows/windows.yml/badge.svg?branch=develop)](https://github.com/computationalgeography/lue_tutorial/actions/workflows/windows.yml) |

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


## Quick start

To be able to run one or more use-cases, the following steps must be performed first:

- Install a Conda client, like [Miniforge](https://conda-forge.org/miniforge/).
- Clone the tutorial repository:

    ```bash
    git clone https://github.com/computationalgeography/lue_tutorial.git
    cd lue_tutorial
    ```

- Create and activate a Conda environment with the required Python packages:

    ```bash
    conda env create --file=environment/configuration/conda_environment.yml
    conda activate lue_tutorial
    ```
