# Universal Soil Loss Equation
The [usle.py](usle.py) script in this directory calculates the average anual soil loss, using the USLE
equation and some dummy data. The goal is to show off how the LUE framework can be used to perform
the necessary calculations. Given enough hardware, LUE will perform the calculations in parallel.
For very large problem sizes, LUE can use multiple distributed cooperating processes. There is
no need to change the [usle.py](usle.py) script for that. See [usle-desktop.sh](usle-desktop.sh)
for an example of running the script on a single computer.

Note how the statement for calculating the anual soil loss in [usle.py](usle.py) matches the
one from the literature. Nevertheless, the calculations are performed in parallel, with tasks from
multiple LUE operations being scheduled for execution at the same time.

Because of the garbage input, the results are garbage as well.

Equation: A = R * K * L * S * C * P

With:

- A: Long-term average annual soil loss
- R: Rainfall erosivity factor
- K: Soil erodibility factor
- L: Topographic factor: slope length
- S: Topographic factor: slope gradient
- C: Cropping management factor
- P: Conservation practices factor

See also:
- https://en.wikipedia.org/wiki/Universal_Soil_Loss_Equation

![Indication of soil loss: Tirol (Austria)](erosivity_tirol.png "Indication of soil loss: Tirol (Austria)")

![Indication of soil loss: detail](erosivity_detail.png "Indication of soil loss: detail")
