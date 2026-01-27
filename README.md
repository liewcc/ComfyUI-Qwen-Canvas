# ComfyUI-Qwen-Canvas

A specialized canvas toolset for ComfyUI, optimized for **Qwen-VL** and other large vision-language model workflows. It provides intelligent resolution scaling and real-time visual feedback.

## Features
- **Smart 1K Scaling**: Automatically calculates and limits resolution within 1,048,576 pixels (1K) to ensure compatibility with model constraints.
- **Multiple Aspect Ratios**: Presets for 1:1, 16:9, 9:16, 4:3, 3:2, and more.
- **Scaling Strategies**: Support for **Crop**, **Pad**, and **Stretch** when processing input images.
- **Live Preview**: Built-in JavaScript integration to show dynamic canvas outlines and VAE encoded previews directly on the node.
- **Dual Node System**: 
  - 🔥 **Qwen Canvas (Plus)**: Full-featured with VAE encoding and image processing.
  - 🖼️ **Qwen Canvas (Basic)**: Lightweight empty latent generator.

## Installation
1. Search for `ComfyUI-Qwen-Canvas` in **ComfyUI Manager** and click Install.
2. Alternatively, clone this repo into your `custom_nodes` directory:
   ```bash
   git clone [https://github.com/liewcc/ComfyUI-Qwen-Canvas.git](https://github.com/liewcc/ComfyUI-Qwen-Canvas.git)