/**
 * 遊戲介紹場景 - 完全按照 Pygame intro_scene.py 配置
 * Introduction Scene
 */

class IntroScene extends Phaser.Scene {
    constructor() {
        super({ key: 'IntroScene' });
        this.textLines = [
            "歡迎來到模擬人生大學版",
            "在這裡，你的每一週都充滿未知挑戰與選擇",
            "你會選擇耍廢？還是成為人生勝利組？",
            "遊戲中的每一步選擇都將影響你的角色發展",
            "在這個遊戲中，你將有四個角色可以選!",
            "從課業到社交，從挑戰到成就，每一週都是新的冒險",
            "按下Enter並點選開始遊戲選擇跟你最像的角色吧!"
        ];
        this.lineIndex = 0;
        this.charIndex = 0;
        this.revealLines = [];
        this.frameCount = 0;
        this.typeSpeed = 3; // Pygame: type_speed = 3
        this.overlayAlpha = 0;
        
        for (let i = 0; i < this.textLines.length; i++) {
            this.revealLines.push("");
        }
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景圖片（與 Pygame 一致）
        if (this.textures.exists('background_intro')) {
            const bg = this.add.image(width / 2, height / 2, 'background_intro');
            bg.setAlpha(0.39); // Pygame: alpha=100/255 ≈ 0.39
            const scale = Math.max(width / bg.width, height / bg.height);
            bg.setScale(scale);
        } else {
            const graphics = this.add.graphics();
            graphics.fillGradientStyle(0xC8D4E8, 0xC8D4E8, 0xE8D4B8, 0xE8D4B8, 1);
            graphics.fillRect(0, 0, width, height);
        }
        
        // 黑色漸進遮罩（確保是黑色 0x000000）
        // Pygame: overlay_alpha 從 0 增加到 200（範圍 0-255）
        this.overlayAlpha = 0;
        this.overlayGraphics = this.add.graphics();
        
        // 動畫角色位置和大小
        // Pygame: CharacterAnimator(..., (900, 50), (240, 220))
        const animX = width * (900 / 1200);
        const animY = height * (50 / 800);
        // 注意：Pygame 的 (240, 220) 是固定像素大小，需要根據螢幕比例縮放
        const targetWidth = width * (240 / 600);
        const targetHeight = height * (220 / 400);
        // 假設原始圖片約 600x600，計算縮放比例
        const animScaleX = targetWidth / 600;
        const animScaleY = targetHeight / 600;
        
        this.animator = this.add.image(animX, animY, 'yier_play_game_0');
        this.animator.setScale(Math.max(animScaleX, animScaleY));
        this.animator.setOrigin(0, 0); // 左上角對齊
        
        this.animFrameIndex = 0;
        this.animFrameCount = 8;
        
        // 動畫更新 - Pygame: frame_delay = 3
        // 這意味著每隔 3 個遊戲幀（在 60 FPS 下）更新一次動畫
        let animFrameCounter = 0;
        this.time.addEvent({
            delay: 1000 / 60, // 每個遊戲幀
            loop: true,
            callback: () => {
                animFrameCounter++;
                if (animFrameCounter >= 3) {
                    animFrameCounter = 0;
                    this.animFrameIndex = (this.animFrameIndex + 1) % this.animFrameCount;
                    const frameKey = `yier_play_game_${this.animFrameIndex}`;
                    if (this.textures.exists(frameKey)) {
                        this.animator.setTexture(frameKey);
                    }
                }
            },
            callbackScope: this
        });
        
        // 文字顯示區域
        this.textObjects = [];
        
        // 打字動畫效果 - 每幀更新
        this.time.addEvent({
            delay: 1000 / 60, // 60 FPS
            loop: true,
            callback: () => this.updateTypewriter(),
            callbackScope: this
        });
        
        // 輸入監聽 - Enter 鍵
        this.input.keyboard.on('keydown-ENTER', () => {
            if (this.lineIndex >= this.textLines.length) {
                // 全部顯示完成，返回 StartScene
                this.scene.start('StartScene');
            } else {
                // 強制顯示全部文字（與 Pygame 一致）
                this.revealLines = this.textLines.map(line => line);
                this.lineIndex = this.textLines.length;
                this.charIndex = 0;
                this.updateTextDisplay();
            }
        });
        
        // 鼠標點擊監聽 - 點擊任何位置也能強制顯示或返回
        this.input.on('pointerdown', () => {
            if (this.lineIndex >= this.textLines.length) {
                // 全部顯示完成，返回 StartScene
                this.scene.start('StartScene');
            } else {
                // 強制顯示全部文字
                this.revealLines = this.textLines.map(line => line);
                this.lineIndex = this.textLines.length;
                this.charIndex = 0;
                this.updateTextDisplay();
            }
        });
    }
    
    updateTypewriter() {
        this.frameCount++;
        
        // 更新黑色遮罩透明度
        // Pygame: if self.overlay_alpha < 200: self.overlay_alpha += 4
        if (this.overlayAlpha < 200) {
            this.overlayAlpha += 4;
        }
        
        // 繪製黑色遮罩
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        this.overlayGraphics.clear();
        this.overlayGraphics.fillStyle(0x000000, this.overlayAlpha / 255);
        this.overlayGraphics.fillRect(0, 0, width, height);
        
        // 打字效果
        // Pygame: if self.line_index < len(self.text_lines) and self.frame_count % self.type_speed == 0
        if (this.lineIndex < this.textLines.length && this.frameCount % this.typeSpeed === 0) {
            // 播放打字音效
            if (this.lineIndex === 0 && this.charIndex === 0) {
                try {
                    this.sound.play('sfx_typing', { loop: false, volume: 0.3 });
                } catch (e) {
                    console.log('打字音效失敗');
                }
            }
            
            const currentLine = this.textLines[this.lineIndex];
            if (this.charIndex < currentLine.length) {
                this.revealLines[this.lineIndex] += currentLine[this.charIndex];
                this.charIndex++;
                
                // 定期重新播放打字音效
                if (this.charIndex % 3 === 0) {
                    try {
                        if (!this.sound.isPlaying('sfx_typing')) {
                            this.sound.play('sfx_typing', { volume: 0.3 });
                        }
                    } catch (e) {}
                }
            } else {
                // 該行完成，進到下一行
                this.lineIndex++;
                this.charIndex = 0;
            }
            
            // 更新文字顯示
            this.updateTextDisplay();
        }
        
        // 如果全部打完，停止打字音效
        if (this.lineIndex >= this.textLines.length) {
            try {
                this.sound.stopByKey('sfx_typing');
            } catch (e) {}
        }
    }
    
    updateTextDisplay() {
        // 清除舊的文字物件
        this.textObjects.forEach(obj => obj.destroy());
        this.textObjects = [];
        
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // Pygame 設置：y = 150, rendered = font.render(...), screen.blit(rendered, (100, y)), y += 75
        let yPos = height * (150 / 800);
        const yGap = height * (75 / 800);
        const xStart = width * (100 / 1200);
        
        // 顯示所有已揭示的文本行
        for (let i = 0; i < this.revealLines.length; i++) {
            if (this.revealLines[i]) {
                const text = this.add.text(
                    xStart,
                    yPos,
                    this.revealLines[i],
                    {
                        fontSize: '36px', // Pygame: font size 36
                        fill: '#FFFFFF', // Pygame: (255, 255, 255)
                        fontFamily: 'JasonHandwriting3, Arial, sans-serif',
                        fontStyle: 'bold', // Pygame 使用 JFONT_PATH_BOLD
                        wordWrap: { width: width * 0.8 }
                    }
                );
                text.setOrigin(0, 0);
                this.textObjects.push(text);
                yPos += yGap;
            }
        }
        
        // 顯示提示文字（全部顯示完時）
        if (this.lineIndex >= this.textLines.length) {
            // Pygame: hint = font.render("按 Enter 返回", True, (200, 200, 200))
            // screen.blit(hint, (self.SCREEN_WIDTH - 300, self.SCREEN_HEIGHT - 60))
            const hintX = width - width * (300 / 1200);
            const hintY = height - height * (60 / 800);
            
            const hint = this.add.text(
                hintX,
                hintY,
                "按 Enter 返回",
                {
                    fontSize: '36px', // 與主文字相同的字體大小
                    fill: '#C8C8C8', // RGB(200, 200, 200)
                    fontFamily: 'JasonHandwriting3, Arial, sans-serif'
                }
            );
            hint.setOrigin(0, 0);
            this.textObjects.push(hint);
        }
    }
}
