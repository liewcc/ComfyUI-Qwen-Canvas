# ComfyUI-Qwen-Canvas

A specialized canvas toolset for ComfyUI, optimized for **Qwen Image Edit** workflows. It provides intelligent resolution scaling and real-time visual feedback.

## 🎯 Qwen Official Training Standards
To achieve the best inference results, this node enforces the specific resolutions used during Qwen's final training stage.

| Aspect Ratio | Target Resolution | Total Pixels |
| :--- | :--- | :--- |
| **1:1** (Square) | $1328 \times 1328$ | ~1.76 M |
| **4:3** (SD) | $1472 \times 1104$ | ~1.62 M |
| **3:4** (Portrait) | $1104 \times 1472$ | ~1.62 M |
| **3:2** (Full Frame) | $1584 \times 1056$ | ~1.67 M |
| **2:3** (Sketch) | $1056 \times 1584$ | ~1.67 M |
| **16:9** (Widescreen) | $1664 \times 928$ | ~1.54 M |
| **9:16** (Vertical) | $928 \times 1664$ | ~1.54 M |

## Features
## 🚀 Why use this node?
Generic "Empty Latent" nodes often use resolutions that Qwen wasn't trained on, leading to poor editing results. 

**ComfyUI-Qwen-Canvas** acts as a "Calibration Tool":
1. It looks up the **Official Training Bucket** based on your selected ratio.
2. It generates a **Latent/Image space** that perfectly mimics the training environment.
3. It fits your input image into this "Golden Standard" frame using Crop, Pad, or Stretch.

## Installation
1. Search for `ComfyUI-Qwen-Canvas` in **ComfyUI Manager** and click Install.
2. Alternatively, clone this repo into your `custom_nodes` directory:
   ```bash
   git clone [https://github.com/liewcc/ComfyUI-Qwen-Canvas.git](https://github.com/liewcc/ComfyUI-Qwen-Canvas.git)
