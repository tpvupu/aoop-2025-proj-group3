/**
 * 第一個場景 - 遊戲歡迎畫面
 * First Scene - Welcome Screen
 */

class FirstScene extends Phaser.Scene {
    constructor() {
        super({ key: 'FirstScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景漸層
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x667eea, 0x667eea, 0x764ba2, 0x764ba2, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 播放背景音樂（如果已載入）
        if (window.GameState.bgmEnabled && this.sound.context.state !== 'suspended') {
            try {
                if (!this.sound.isPlaying('bgm_drumdrum')) {
                    this.sound.play('bgm_drumdrum', { loop: true, volume: 0.5 });
                }
            } catch (e) {
                console.log('音樂播放失敗');
            }
        }
        
        // 遊戲標題
        const title = this.add.text(width / 2, height / 2 - 150, '今天的我也想耍廢', 
            GameUtils.createTextStyle(64, '#FFFFFF', 'Arial')
        );
        title.setOrigin(0.5);
        
        // 添加標題動畫
        this.tweens.add({
            targets: title,
            scale: { from: 0.8, to: 1.1 },
            duration: 1500,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.easeInOut'
        });
        
        // 副標題
        const subtitle = this.add.text(width / 2, height / 2 - 80, 'Lazy Me Today Too', 
            GameUtils.createTextStyle(32, '#FFEB3B', 'Arial')
        );
        subtitle.setOrigin(0.5);
        
        // 開始按鈕
        const startButton = this.createButton(width / 2, height / 2 + 50, '開始遊戲', () => {
            this.scene.start('StartScene');
        });
        
        // 說明按鈕
        const introButton = this.createButton(width / 2, height / 2 + 130, '遊戲說明', () => {
            this.scene.start('IntroScene');
        });
        
        // 退出按鈕
        const exitButton = this.createButton(width / 2, height / 2 + 210, '離開遊戲', () => {
            if (confirm('確定要離開遊戲嗎？')) {
                window.close();
            }
        });
        
        // 版權資訊
        const copyright = this.add.text(width / 2, height - 40, 
            'NYCU AOOP 2025 Final Project - Group 3\n陳欣怡 & 楊庭瑞', 
            {
                fontSize: '16px',
                fill: '#FFFFFF',
                fontFamily: 'Arial',
                align: 'center'
            }
        );
        copyright.setOrigin(0.5);
        copyright.setAlpha(0.7);
    }
    
    createButton(x, y, text, callback) {
        const button = this.add.container(x, y);
        
        // 按鈕背景
        const bg = this.add.rectangle(0, 0, 300, 60, 0xFFFFFF, 0.2);
        bg.setStrokeStyle(3, 0xFFFFFF);
        
        // 按鈕文字
        const buttonText = this.add.text(0, 0, text, 
            GameUtils.createTextStyle(28, '#FFFFFF', 'Arial')
        );
        buttonText.setOrigin(0.5);
        
        button.add([bg, buttonText]);
        
        // 互動效果
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                bg.setFillStyle(0xFFFFFF, 0.4);
                this.tweens.add({
                    targets: button,
                    scale: 1.1,
                    duration: 200
                });
            })
            .on('pointerout', () => {
                bg.setFillStyle(0xFFFFFF, 0.2);
                this.tweens.add({
                    targets: button,
                    scale: 1.0,
                    duration: 200
                });
            })
            .on('pointerdown', callback);
        
        return button;
    }
}
