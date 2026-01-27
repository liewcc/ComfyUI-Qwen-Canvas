# ComfyUI-Qwen-Canvas

A precision canvas and latent generator designed specifically for **Qwen Image Edit** workflows. It ensures your inputs perfectly align with the high-performance training buckets used by Alibaba's Qwen team.


## 🌟 Why ComfyUI-Qwen-Canvas?

Most models are sensitive to input resolutions. Using standard 512x512 or 1024x1024 latents often results in "composition drift" or "hallucinations" because the model was never trained on those shapes. 

This node acts as a **Hardware-Software Bridge**:
1.  **Official Training Buckets**: Automatically snaps to the exact resolutions Qwen was trained on (up to ~1.7M pixels).
2.  **Visual Proxy**: Real-time dashed-line feedback on the node itself to show the target aspect ratio before you even press "Queue".
3.  **Smart Fitting**: Intelligently fits your reference images into the "Golden Standard" frames using three professional scaling strategies.

---

## 🚀 Features

### 1. Official Resolution Presets
The node enforces the specific resolutions used in Qwen's final training stage to maximize inference quality:

| Aspect Ratio | Target Resolution | Total Pixels |
| :--- | :--- | :--- |
| **1:1** (Square) | $1328 \times 1328$ | ~1.76 M |
| **4:3** (SD) | $1472 \times 1104$ | ~1.62 M |
| **3:4** (Portrait) | $1104 \times 1472$ | ~1.62 M |
| **3:2** (Full Frame) | $1584 \times 1056$ | ~1.67 M |
| **2:3** (Sketch) | $1056 \times 1584$ | ~1.67 M |
| **16:9** (Widescreen) | $1664 \times 928$ | ~1.54 M |
| **9:16** (Vertical) | $928 \times 1664$ | ~1.54 M |

### 2. Intelligent Scaling Strategies (Plus Version)
When providing an input image, choose how it adapts to the Qwen canvas:
* **Crop**: Fills the canvas and cuts off edges (Best for maintaining subject scale).
* **Pad**: Fits the whole image inside the canvas with black bars (Best for keeping the whole composition).
* **Stretch**: Forces the image to match the ratio (Best for precise pixel alignment).

### 3. Real-time Node Canvas
The node's UI dynamically updates:
* **Dashed Outline**: Shows the aspect ratio visually on the node body.
* **Live Preview**: If `vae_encode` is enabled, a low-res thumbnail of the processed result appears directly on the node for instant verification.

---

## 🛠 Node Types

### QwenCanvas (Basic)
* **Purpose**: A fast, lightweight "Empty Latent" generator.
* **Usage**: Select your ratio and link it to your sampler.

### QwenCanvasPlus (Advanced)
* **Purpose**: The ultimate image-to-image / editing pre-processor.
* **Inputs**: Accepts optional `pixels` and `VAE`.
* **Modes**: 
    * **Original (Follow Input)**: Automatically calculates the best "1K-limited" resolution based on your input's unique shape, while remaining VAE-compatible (multiples of 8).

---

## 📦 Installation

1.  **ComfyUI Manager**: Search for `ComfyUI-Qwen-Canvas` and click **Install**.
2.  **Manual**:
    ```bash
    cd ComfyUI/custom_nodes
    git clone [https://github.com/liewcc/ComfyUI-Qwen-Canvas.git](https://github.com/liewcc/ComfyUI-Qwen-Canvas.git)
    ```

## 💡 Pro Tip
When using **Qwen Image Edit** workflows, always use the **Plus** node with `scaling_strategy` set to **Pad**. This ensures the model sees your entire original image within its optimal "vision window," preventing the loss of important details at the edges.
