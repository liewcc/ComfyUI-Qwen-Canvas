import torch

class QwenCanvasBasic:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "aspect_ratio": ([
                    "1:1 (1328 x 1328)", "16:9 (1664 x 928)", "9:16 (928 x 1664)", 
                    "4:3 (1472 x 1104)", "3:4 (1104 x 1472)", "3:2 (1584 x 1056)", "2:3 (1056 x 1584)"
                ], {"default": "1:1 (1328 x 1328)"}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}),
            }
        }

    RETURN_TYPES = ("LATENT", "INT", "INT")
    RETURN_NAMES = ("LATENT", "width", "height")
    FUNCTION = "generate_empty_latent"
    CATEGORY = "Qwen Toolset"

    def generate_empty_latent(self, aspect_ratio, batch_size):
        try:
            res_str = aspect_ratio.split("(")[1].split(")")[0]
            width, height = map(int, res_str.split(" x "))
        except:
            width, height = 1328, 1328
        
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        return ({"samples": latent}, width, height)