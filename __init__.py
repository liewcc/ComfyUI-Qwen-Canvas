from .nodes_basic import QwenCanvasBasic
from .nodes_plus import QwenCanvasPlus

NODE_CLASS_MAPPINGS = {
    # 保持这个 Key 不变，旧工作流就能直接读取 Basic 版逻辑
    "QwenCanvas": QwenCanvasBasic,
    # 新增 Plus 版节点 ID
    "QwenCanvasPlus": QwenCanvasPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenCanvas": "🖼️ Qwen Canvas (Basic)",
    "QwenCanvasPlus": "🔥 Qwen Canvas (Plus)"
}

WEB_DIRECTORY = "." # 必须保留，确保 JS 加载

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]