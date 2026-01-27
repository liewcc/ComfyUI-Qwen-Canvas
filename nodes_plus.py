import torch
import numpy as np
from PIL import Image
import os
import folder_paths
import random
import node_helpers

class QwenCanvasPlus:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "aspect_ratio": ([
                    "1:1 (1328 x 1328)", "16:9 (1664 x 928)", "9:16 (928 x 1664)",
                    "4:3 (1472 x 1104)", "3:4 (1104 x 1472)", "3:2 (1584 x 1056)", "2:3 (1056 x 1584)",
                    "Original (Follow Input)"
                ], {"default": "1:1 (1328 x 1328)"}),
                "vae_encode": (["Enabled", "Disabled"], {"default": "Disabled"}),
                "scaling_strategy": (["Crop", "Pad", "Stretch"], {"default": "Crop"}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}),
            },
            "optional": {
                "pixels": ("IMAGE",),
                "vae": ("VAE",),
            }
        }

    RETURN_TYPES = ("LATENT", "INT", "INT", "IMAGE")
    RETURN_NAMES = ("LATENT", "width", "height", "PREVIEW_IMAGE")
    OUTPUT_NODE = True # 必须声明为输出节点，UI 信号才会生效
    FUNCTION = "execute"
    CATEGORY = "Qwen Toolset"

# 确保类中有此方法，用于计算 1K 像素限制下的宽高
    def calculate_1k_res(self, w, h):
        max_pixels = 1048576 
        current_pixels = w * h
        scale = (max_pixels / current_pixels) ** 0.5 if current_pixels > max_pixels else 1.0
        # 必须是 8 的倍数以适配 VAE
        return (int(w * scale) // 8 * 8, int(h * scale) // 8 * 8)

    def execute(self, aspect_ratio, vae_encode, scaling_strategy, batch_size, pixels=None, vae=None):
        # 1. 初始化原始尺寸反馈
        orig_w, orig_h = 1328, 1328
        if pixels is not None:
            _, p_h, p_w, _ = pixels.shape
            # 即使不编码，也预计算 1K 限制后的比例给前端
            orig_w, orig_h = self.calculate_1k_res(p_w, p_h)

        # 2. 确定当前目标尺寸
        if aspect_ratio == "Original (Follow Input)" and pixels is not None:
            target_w, target_h = orig_w, orig_h
        else:
            try:
                res_str = aspect_ratio.split("(")[1].split(")")[0]
                target_w, target_h = map(int, res_str.split(" x "))
            except:
                target_w, target_h = 1328, 1328

        # 3. 逻辑分支：VAE 编码开启
        if vae_encode == "Enabled" and pixels is not None and vae is not None:
            processed_images = self.process_images(pixels, target_w, target_h, scaling_strategy)
            
            # 生成缩影预览图
            preview_pil = Image.fromarray(np.clip(255. * processed_images[0].cpu().numpy(), 0, 255).astype(np.uint8))
            preview_pil.thumbnail((256, 256))
            
            import folder_paths, random
            tmp_name = f"qwen_p_{random.randint(0, 1000000)}.png"
            tmp_path = os.path.join(folder_paths.get_temp_directory(), tmp_name)
            preview_pil.save(tmp_path, compress_level=4)
            
            latent = vae.encode(processed_images[:, :, :, :3])
            
            # 返回：同时发送图片和最终确定的尺寸 [w, h]
            return {
                "ui": {
                    "images": [{"filename": tmp_name, "type": "temp"}],
                    "original_size": [target_w, target_h] 
                },
                "result": ({"samples": latent}, target_w, target_h, processed_images)
            }
        
        # 4. 逻辑分支：空白/待机模式
        else:
            latent = torch.zeros([batch_size, 4, target_h // 8, target_w // 8])
            blank_image = torch.zeros([1, target_h, target_w, 3])
            
            # 重要：即便没有图片，也要把 original_size 传回去，这样虚线框才会变形
            return {
                "ui": {"original_size": [target_w, target_h]},
                "result": ({"samples": latent}, target_w, target_h, blank_image)
            }

    def process_images(self, pixels, tw, th, strategy):
        results = []
        for img in pixels:
            pil_img = Image.fromarray(np.clip(255. * img.cpu().numpy(), 0, 255).astype(np.uint8))
            iw, ih = pil_img.size
            if strategy == "Stretch":
                new_img = pil_img.resize((tw, th), Image.LANCZOS)
            elif strategy == "Crop":
                scale = max(tw/iw, th/ih)
                nw, nh = int(iw*scale), int(ih*scale)
                pil_img = pil_img.resize((nw, nh), Image.LANCZOS)
                left, top = (nw - tw) / 2, (nh - th) / 2
                new_img = pil_img.crop((left, top, left + tw, top + th))
            else: # Pad
                scale = min(tw/iw, th/ih)
                nw, nh = int(iw*scale), int(ih*scale)
                pil_img = pil_img.resize((nw, nh), Image.LANCZOS)
                new_img = Image.new("RGB", (tw, th), (0, 0, 0))
                new_img.paste(pil_img, ((tw - nw) // 2, (th - nh) // 2))
            results.append(np.array(new_img).astype(np.float32) / 255.0)
        return torch.from_numpy(np.array(results))