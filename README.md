# CurveFitting
日本語の[README](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/README_JP.md)はこちら
## Introduction
When modeling in Blender, vertex arrangements can sometimes become uneven. 
CurveFitting smooths the uneven arrangements of vertices while preserving the original shape.

## System Requirements
Blender 4.2 and newer.      
If you want to use CurveFitting in Blender 3.6 and earlier, please use CurveFitting V0.1.x.

## Installation
### From Github
1. Download the latest `curve_fitting.zip` from the [release page](https://github.com/zuda77/CurveFitting_blender_addon/releases).
2. Launch Blender and navigate to the header menu: Edit -> Preferences...
3. In the Preferences window, click the "Add-ons" button and then the "Install..." button in the top-right corner to open a file dialog.
4. Select the downloaded `curve_fitting.zip` file. CurveFitting will then appear in the Add-ons list.
5. Mark a check-box for CurveFitting in the Add-ons list to enable the feature and complete the installation.

### From Blender Extension
1. Click the "Get add-on" button on the [Blender Extension](https://extensions.blender.org/add-ons/curvefitting/) website.

## Usage
1. Select the vertices you want to smooth. Ensure the vertices are connected by edges or faces.
2. Open the context menu by right-clicking and select "Curve Fitting". Alternatively, you can call the function via the header menu: Vertex -> Curve Fitting.
3. Adjust the "Curve Degree" value in the properties panel at the bottom-left of the screen to fine-tune the shape of curves or surfaces to your preference.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/property_panel.PNG"> <br>
Properties Panel
</p>

## Features
CurveFitting moves vertices onto a curve or surface approximated by a polynomial calculated from the selected vertices.

#### - Curve Degree
"Curve Degree" in the properties panel sets the degree of the polynomial. 
Higher degrees allow for fitting more complex shapes, but the simplicity of the shape is lost. Adjust this value according to the shape of the original vertex arrangement.  
The following table shows examples when changing the degree from 1 to 4:

|Curve Degree|Vertex Model<br>Curve|Vertex Model<br>Surface|Curve Image|
|:-:|:-:|:-:|:-:|
|Before Processing<br>Original Shape|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/before.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_before2.PNG" width="45%">|-|
|1|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_1deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_1deg2.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_1deg.PNG)|
|2|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_2deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_2deg2.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_2deg.PNG)|
|3|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_3deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_3deg2.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_3deg.PNG)|
|4|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_4deg.PNG" width="45%">|<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surf_4deg2.PNG" width="45%">|![grafik](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_4deg.PNG)|

#### - Ends Weight
- For Curves: Adjusts the immovability of the start and end points of the selected vertex sequence. The default value is 10.
- Larger values make the start and end points harder to move. The minimum value of 1 allows points to move according to the calculated approximation.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/ends_points.PNG" width="60%"> <br>
Ends weight points on the curve AND RIGHT
</P>

#### - Border Weight
- For Surfaces: Adjusts the immovability of points on the boundary of the faces set that includes the selected vertices. The default value is 1.
- Larger values make the start and end points harder to move. The minimum value of 1 allows points to move according to the calculated approximation.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/boder_points.PNG" width="60%"> <br>
Border weight points on the surfase
</P>

## Algorithm
### Curve Fitting - Curve
1. Define the selected vertex sequence as `P` (blue markers in the figure below).
2. Perform principal component analysis (PCA) on `P`. Use the obtained principal components 1, 2, and 3 as the `i`, `j`, and `k` axes, respectively.
3. Transform the `xyz` coordinates of `P` into `ijk` coordinates: `P(x, y, z)` -> `P(i, j, k)`.
4. Project `P` onto the `i`, `j`, and `k` axes, selecting the axis without overlaps as the scan axis. In the figure below, the scan axis is the `i`-axis.
5. Project `P` onto the `ij` plane and calculate the approximation curve using the least squares method.
6. For each `i`-coordinate of `P`, calculate the corresponding `j'` from the approximation curve (orange markers in the figure).
7. Similarly, calculate the `k'` coordinate (green markers in the figure). The updated vertex sequence is `P'(i, j', k')`.
8. Transform the updated `P'` back into xyz coordinates: `P'(i, j', k') -> P'(x', y', z')`.
9. Apply `P'(x', y', z')` to Blender.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/algorithm.PNG" width="80%"> <br>
Algorithm for curve
</p>

### Curve Fitting - Surface
1. Define the selected vertices as points `P` (blue markers in the figure below).
2. Compute the average position of `P` as point `C`.
3. Define the set of faces including `P` as `S`.
4. Calculate the average normal vector `k` from the normal vectors `S`.
5. Define plane `T` passing through `C` with normal vector　`k`. Construct vectors `i` and `j` orthogonal to `k` and to each other. In this implementation, project `P` onto `T` and define `i` as the vector from `C` to the farthest projected point. Calculate `j` as the cross product of `i` and `k`.
6. Convert `P`'s `xyz` coordinates to `ijk` coordinates: `P(x, y, z) -> P(i, j, k)`.
7. Approximate the surface as `k' = F(i, j)` using the least squares method.
8. Update vertex positions to `P'(i, j, k')` and convert back to `xyz` coordinates: `P'(i, j, k') -> P'(x', y', z')`.
9. Apply `P'(x', y', z')` to Blender.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/surface_fitting_algorithm2.PNG" width="40%"> <br>
Algorithm for surfase
</p>

## Note
Since the Curve Fitting algorithm is implemented only for Cartesian coordinates, shapes that overlap when projected onto a plane, such as circles or spirals, may fail to process correctly.

## License
The "Curve Fitting" add-on is licensed under the [GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.html).

## Author
- Zuda77

For feedback, suggestions, or bug reports, please contact us via [issues](https://github.com/zuda77/CurveFitting_blender_addon/issues).
