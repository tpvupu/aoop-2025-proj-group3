/**
 * 開始場景 - 根據 Pygame start_scene.py 配置
 * Start Scene
 */

class StartScene extends Phaser.Scene {
    constructor() {
        super({ key: 'StartScene' });
        this.animationFrames = 0;
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景圖片（與 CharacterSelectScene 相同）
        if (this.textures.exists('background_intro')) {
            const bg = this.add.image(width / 2, height / 2, 'background_intro');
            const scale = Math.max(width / bg.width, height / bg.height);
            bg.setScale(scale);
        } else {
            const graphics = this.add.graphics();
            graphics.fillGradientStyle(0xC8D4E8, 0xC8D4E8, 0xE8D4B8, 0xE8D4B8, 1);
            graphics.fillRect(0, 0, width, height);
        }
        
        // 白色透明遮罩
        const mask = this.add.rectangle(width / 2, height / 2, width, height, 0xFFFFFF, 0.1);
        mask.setOrigin(0.5, 0.5);
        
        // 標題 - "Lazy Me Today Too" (72px 字體)
        const title = this.add.text(width / 2, 80, 'Lazy Me Today Too',
            {
                fontSize: '72px',
                fill: '#8E5833',
                fontFamily: 'JasonHandwriting3, Arial, sans-serif',
                fontStyle: 'bold'
            }
        );
        title.setOrigin(0.5);
        
        // 裝飾動畫（左右兩側，Pygame 配置為 300x300）
        const leftAnimScale = (300 / 600) * (width / 1200);
        const rightAnimScale = (300 / 600) * (width / 1200);
        
        const leftAnim = this.add.image(width * 0.04, height / 2, 'four_char_0');
        leftAnim.setScale(leftAnimScale);
        leftAnim.setOrigin(0.5, 0.5);
        
        const rightAnim = this.add.image(width * 0.96, height / 2, 'four_char2_0');
        rightAnim.setScale(rightAnimScale);
        rightAnim.setOrigin(0.5, 0.5);
        
        // 動畫更新
        let leftFrameIndex = 0, rightFrameIndex = 0;
        const leftFrameCount = 4, rightFrameCount = 4;
        
        this.time.addEvent({
            delay: 300, // frame_delay = 3 表示每 3 幀換一次
            loop: true,
            callback: () => {
                leftFrameIndex = (leftFrameIndex + 1) % leftFrameCount;
                rightFrameIndex = (rightFrameIndex + 1) % rightFrameCount;
                
                const leftKey = `four_char_${leftFrameIndex}`;
                const rightKey = `four_char2_${rightFrameIndex}`;
                
                if (this.textures.exists(leftKey)) {
                    leftAnim.setTexture(leftKey);
                }
                if (this.textures.exists(rightKey)) {
                    rightAnim.setTexture(rightKey);
                }
            },
            callbackScope: this
        });
        
        // 按鈕配置（根據 Pygame 配置）
        const buttonTexts = [
            { text: '開始遊戲', action: 'CHARACTER_SELECT' },
            { text: '遊戲介紹', action: 'SHOW_INTRO' },
            { text: '調整音量', action: 'SOUND_CONTROL' },
            { text: '退出遊戲', action: 'QUIT' }
        ];
        
        const buttonW = 300;
        const buttonH = 70;
        const spacing = 30;
        const totalH = buttonTexts.length * (buttonH + spacing) - spacing;
        const startY = (height - totalH) / 2 + 50;
        
        buttonTexts.forEach((btnConfig, i) => {
            const btnX = width / 2;
            const btnY = startY + i * (buttonH + spacing);
            this.createButton(btnX, btnY, btnConfig.text, btnConfig.action, buttonW, buttonH);
        });
    }
    
    createButton(x, y, text, action, width, height) {
        const button = this.add.container(x, y);
        let scale = 1.0;
        
        const bg = this.add.rectangle(0, 0, width, height, 0xB4B4B4);
        bg.setStrokeStyle(3, 0x787878);
        
        const buttonText = this.add.text(0, 0, text,
            {
                fontSize: '48px',
                fill: '#323232',
                fontFamily: 'JasonHandwriting3, Arial, sans-serif',
                fontStyle: 'bold'
            }
        );
        buttonText.setOrigin(0.5);
        
        button.add([bg, buttonText]);
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                bg.setFillStyle(0xC8C8FA);
                if (this.sound.context.state !== 'suspended') {
                    try {
                        this.sound.play('sfx_menu_hover', { volume: 0.3 });
                    } catch (e) {
                        console.log('音效播放失敗');
                    }
                }
            })
            .on('pointerout', () => {
                bg.setFillStyle(0xB4B4B4);
            })
            .on('pointerdown', () => {
                this.handleButtonClick(action);
            });
        
        // 動畫效果
        this.time.addEvent({
            delay: 16,
            loop: true,
            callback: () => {
                const rect = bg.getBounds();
                if (rect && this.input.activePointer) {
                    const pointer = this.input.activePointer;
                    const isHovered = pointer.x >= rect.x - width / 2 && 
                                    pointer.x <= rect.x + width / 2 &&
                                    pointer.y >= rect.y - height / 2 &&
                                    pointer.y <= rect.y + height / 2;
                    
                    const target = isHovered ? 1.1 : 1.0;
                    scale += (target - scale) * 0.2;
                    button.setScale(scale);
                }
            },
            callbackScope: this
        });
        
        return button;
    }
    
    handleButtonClick(action) {
        switch (action) {
            case 'CHARACTER_SELECT':
                this.scene.start('CharacterSelectScene');
                break;
            case 'SHOW_INTRO':
                this.scene.start('IntroScene');
                break;
            case 'SOUND_CONTROL':
                this.scene.start('SoundControlScene');
                break;
            case 'QUIT':
                if (confirm('確定要離開遊戲嗎？')) {
                    window.close();
                }
                break;
        }
    }
}
