// qwen_visual.js
import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Qwen.Canvas.Suite",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "QwenCanvas" || nodeData.name === "QwenCanvasPlus") {

            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                this.size = [220, 240]; 
                this._qwen_img = null; 

                const widgetsToWatch = ["aspect_ratio", "vae_encode", "scaling_strategy", "batch_size"];
                
                widgetsToWatch.forEach(name => {
                    const widget = this.widgets.find(w => w.name === name);
                    if (widget) {
                        const originalCallback = widget.callback;
                        widget.callback = (...args) => {
                            this._qwen_img = null;
                            this.setDirtyCanvas(true, true);
                            if (originalCallback) originalCallback.apply(this, args);
                        };
                    }
                });
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                if (message?.images && message.images.length > 0) {
                    const imgData = message.images[0];
                    const img = new Image();
                    img.src = `/view?filename=${imgData.filename}&type=${imgData.type}&subfolder=${imgData.subfolder || ""}`;
                    img.onload = () => {
                        this._qwen_img = img;
                        this.setDirtyCanvas(true, true);
                    };
                } else {
                    this._qwen_img = null;
                }
                this.imgs = null; 
            };

            nodeType.prototype.onDrawBackground = function(ctx) {
                this.imgs = null; 
            };

            nodeType.prototype.onDrawForeground = function (ctx) {
                if (this.flags.collapsed) return;

                const isPlus = this.type === "QwenCanvasPlus";
                const vaeMode = this.widgets.find(w => w.name === "vae_encode")?.value || "Disabled";
                const widget = this.widgets.find(w => w.name === "aspect_ratio");

                if (vaeMode === "Disabled") {
                    this._qwen_img = null;
                }

                let lastWidgetY = 0;
                if (this.widgets && this.widgets.length > 0) {
                    const lastWidget = this.widgets[this.widgets.length - 1];
                    lastWidgetY = lastWidget.last_y + (lastWidget.computedHeight || 24) + 10;
                }

                let rw = 1, rh = 1;
                if (widget.value === "Original (Follow Input)" && this._qwen_ratio) {
                    [rw, rh] = this._qwen_ratio.map(v => Number(v) || 1);
                } else {
                    const ratioMatch = widget.value.match(/(\d+):(\d+)/);
                    if (ratioMatch) {
                        rw = parseInt(ratioMatch[1]);
                        rh = parseInt(ratioMatch[2]);
                    }
                }

                rw = Math.max(rw, 0.1);
                rh = Math.max(rh, 0.1);

                const boxH = 100;
                const maxImgSize = 100;   // 加大一點，更顯眼但仍安全
                let dw, dh;
                if (rw >= rh) {
                    dw = maxImgSize;
                    dh = maxImgSize * (rh / rw);
                } else {
                    dh = maxImgSize;
                    dw = maxImgSize * (rw / rh);
                }

                this.size[1] = lastWidgetY + boxH + 15;

                ctx.save();

                // 背景面板（左右留 10px 邊距）
                ctx.fillStyle = "rgba(0,0,0,0.6)";
                ctx.beginPath();
                ctx.roundRect(10, lastWidgetY, this.size[0]-20, boxH, 10);
                ctx.fill();

                // 動態計算中心點（真正居中）
                const contentAreaWidth = this.size[0] - 20;
                const centerX = 10 + contentAreaWidth / 2;
                const centerY = lastWidgetY + (boxH / 2);
                const x = centerX - dw / 2;
                const y = centerY - dh / 2;

                const boxX = x;
                const boxY = y;
                const boxW = dw;
                const boxH_actual = dh;

                // 內容區深色底
                ctx.fillStyle = "#0f0f0f";
                ctx.fillRect(boxX, boxY, boxW, boxH_actual);

                // 有圖且 VAE 啟用 → 畫圖片（保持比例、置中）
                let hasContent = false;
                if (isPlus && vaeMode === "Enabled" && this._qwen_img) {
                    const img = this._qwen_img;
                    const imgRatio = img.naturalWidth / img.naturalHeight;
                    const boxRatio = boxW / boxH_actual;

                    let drawW = boxW;
                    let drawH = boxH_actual;
                    let drawX = boxX;
                    let drawY = boxY;

                    if (imgRatio > boxRatio) {
                        drawH = boxW / imgRatio;
                        drawY = boxY + (boxH_actual - drawH) / 2;
                    } else {
                        drawW = boxH_actual * imgRatio;
                        drawX = boxX + (boxW - drawW) / 2;
                    }

                    ctx.drawImage(img, drawX, drawY, drawW, drawH);
                    hasContent = true;
                }

                // 始終畫框線
                ctx.strokeStyle = hasContent ? "rgba(0, 255, 200, 0.7)" : "#00FFC8";
                ctx.lineWidth = 1.8;
                
                if (hasContent) {
                    ctx.setLineDash([]);
                } else {
                    ctx.setLineDash([5, 4]);
                }

                const inset = 1;
                ctx.strokeRect(
                    boxX + inset,
                    boxY + inset,
                    boxW - inset * 2,
                    boxH_actual - inset * 2
                );

                ctx.setLineDash([]);

                ctx.restore();
            };

            const origOnExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                if (message?.original_size) {
                    this._qwen_ratio = message.original_size;
                }
                origOnExecuted?.apply(this, arguments);
            };
        }
    }
});