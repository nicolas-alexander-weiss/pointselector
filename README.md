# pointselector

Basic matplotlib-based tool to point and click to assemble basic 2D datasets for visualization purposes.

## Simplex Selector

This is the preferred tool to be run.

**Dependencies**: numpy, matplotlib

**Execution**: *python3 simplexselector*

**Usage**:

- Adding vertices by left-clicking
- Going into selection mode by pressing "shift"-key once.
  - Left clicking then will then select nearest (already existing) point
- Pressing "enter" to confirm selection and add as a "simplex" / subset.
- Closing the window will output the list of selected points and subsets then.