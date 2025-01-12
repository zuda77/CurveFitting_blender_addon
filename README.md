# CurveFitting
日本語の[README](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/README_JP.md)はこちら
## Introduction
While modeling with Blender, the arrangement of vertices can sometimes become messy.  
CurveFitting smooths out messy vertex arrangements while maintaining the original shape.

## Environment
Developed and tested with Blender ver. 3.6.  
It may work with other versions as well.

## Installation
1. Download the latest CurveFitting.zip from the [release](https://github.com/zuda77/CurveFitting_blender_addon/releases) page.
2. Launch Blender and select Edit -> Preferences... from the header menu to open the Preferences window.
3. In the Preferences window, click the Add-ons button, then click the Install... button in the top right corner to open a file dialog.
4. Select the CurveFitting.zip file in the file dialog. CurveFitting will be added to the Add-ons list in the Preferences window.
5. Mark a check-box for CurveFitting in the Add-ons list to enable the feature and complete the installation.

## Usage
1. Select the vertices you want to smooth. Ensure the vertices are connected by edges.
2. Open the context menu by right-clicking and select "Curve Fitting". Alternatively, you can call the function via the header menu: Vertex -> Curve Fitting.
3. Adjust the curve to your liking by changing the Curve Degree value in the property panel at the bottom left of the screen.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/prop_2deg.PNG"> <br>
Property Panel
</p>

## Features
Curve Fitting moves the selected vertices to a polynomial approximation curve calculated from them.

#### - Curve Degree
The Curve Degree in the property panel sets the degree of the polynomial approximation curve.  
Higher degrees allow for fitting more complex shapes, but the simplicity of the shape is lost. Adjust this value according to the shape of the original vertex arrangement.  
The table below shows examples when the degree is changed from 1 to 4.

| Curve Degree | Vertex Model | Curve Image |
|:-:|:-:|:-:|
| Before Processing<br>Original Shape | <img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/before.PNG" width="45%"> | - |
| 1 | <img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_1deg.PNG" width="45%"> | ![Curve 1 Degree](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_1deg.PNG) |
| 2 | <img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_2deg.PNG" width="45%"> | ![Curve 2 Degree](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_2deg.PNG) |
| 3 | <img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_3deg.PNG" width="45%"> | ![Curve 3 Degree](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_3deg.PNG) |
| 4 | <img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/leaf_4deg.PNG" width="45%"> | ![Curve 4 Degree](https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/curve_4deg.PNG) |

#### - Ends Weight
This value makes the start and end points of the selected vertices less likely to move. The default value is 10; Larger values make moving the start and end points harder. At the minimum value of 1, the start and end points move according to the calculated approximation curve.

## Algorithm
The Curve Fitting algorithm follows these steps:

1. Define the selected vertex sequence as P (blue markers in the figure below).
2. Perform principal component analysis (PCA) on P. Use the obtained principal components 1, 2, and 3 as the i, j, and k axes, respectively.
3. Transform the xyz coordinates of P into ijk coordinates: P(x, y, z) -> P(i, j, k).
4. Project P onto the i, j, and k axes, selecting the axis without overlaps as the scan axis. In the figure below, the scan axis is the i-axis.
5. Project P onto the ij plane and calculate the approximation curve using the least squares method.
6. For each i-coordinate of P, calculate the corresponding j' from the approximation curve (orange markers in the figure).
7. Similarly, calculate the k' coordinate (green markers in the figure). The updated vertex sequence is P'(i, j', k').
8. Transform the updated P' back into xyz coordinates: P'(i, j', k') -> P'(x', y', z').
9. Apply P'(x', y', z') to Blender.

<p align="center">
<img src="https://github.com/zuda77/CurveFitting_blender_addon/blob/main/images/algorithm.PNG" width="80%"> <br>
Curve Fitting Algorithm
</p>

## Note
The Curve Fitting algorithm is implemented only for orthogonal coordinate systems. Therefore, it fails in cases where an operating axis cannot be determined, such as when projecting onto a plane for circles or spirals.

## License
"Curve Fitting" is licensed under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).

## Author
* Zuda77

For suggestions, requests, or bug reports, please contact me via [issues](https://github.com/zuda77/CurveFitting_blender_addon/issues).
