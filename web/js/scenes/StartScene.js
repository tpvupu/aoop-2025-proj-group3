/**
 * 開始場景
 * Start Scene
 */

class StartScene extends Phaser.Scene {
    constructor() {
        super({ key: 'StartScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x667eea, 0x667eea, 0x764ba2, 0x764ba2, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 標題
        const title = this.add.text(width / 2, 100, '選擇你的冒險', 
            GameUtils.createTextStyle(48, '#FFFFFF', 'Arial')
        );
        title.setOrigin(0.5);
        
        // 按鈕組
        this.createMenuButton(width / 2, height / 2 - 80, '開始新遊戲', () => {
            this.scene.start('CharacterSelectScene');
        });
        
        this.createMenuButton(width / 2, height / 2, '遊戲說明', () => {
            this.scene.start('IntroScene');
        });
        
        this.createMenuButton(width / 2, height / 2 + 80, '音效設定', () => {
            this.showSettingsModal();
        });
        
        this.createMenuButton(width / 2, height / 2 + 160, '返回', () => {
            this.scene.start('FirstScene');
        });
    }
    
    createMenuButton(x, y, text, callback) {
        const button = this.add.container(x, y);
        
        const bg = this.add.rectangle(0, 0, 350, 70, 0x4A90E2);
        bg.setStrokeStyle(4, 0xFFFFFF);
        
        const buttonText = this.add.text(0, 0, text, 
            GameUtils.createTextStyle(32, '#FFFFFF', 'Arial')
        );
        buttonText.setOrigin(0.5);
        
        button.add([bg, buttonText]);
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                bg.setFillStyle(0x5FA3F5);
                this.tweens.add({
                    targets: button,
                    scale: 1.05,
                    duration: 150
                });
            })
            .on('pointerout', () => {
                bg.setFillStyle(0x4A90E2);
                this.tweens.add({
                    targets: button,
                    scale: 1.0,
                    duration: 150
                });
            })
            .on('pointerdown', callback);
        
        return button;
    }
    
    showSettingsModal() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 半透明遮罩
        const overlay = this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.7);
        overlay.setInteractive();
        
        // 設定面板
        const panel = this.add.rectangle(width / 2, height / 2, 500, 400, 0xFFFFFF);
        panel.setStrokeStyle(4, 0x4A90E2);
        
        const titleText = this.add.text(width / 2, height / 2 - 150, '音效設定', 
            GameUtils.createTextStyle(36, '#000000', 'Arial')
        );
        titleText.setOrigin(0.5);
        
        // BGM 開關
        const bgmText = this.add.text(width / 2 - 150, height / 2 - 50, '背景音樂', 
            GameUtils.createTextStyle(28, '#000000', 'Arial')
        );
        
        const bgmToggle = this.createToggle(width / 2 + 100, height / 2 - 50, window.GameState.bgmEnabled);
        bgmToggle.on('click', (enabled) => {
            window.GameState.bgmEnabled = enabled;
        });
        
        // SFX 開關
        const sfxText = this.add.text(width / 2 - 150, height / 2 + 30, '音效', 
            GameUtils.createTextStyle(28, '#000000', 'Arial')
        );
        
        const sfxToggle = this.createToggle(width / 2 + 100, height / 2 + 30, window.GameState.sfxEnabled);
        sfxToggle.on('click', (enabled) => {
            window.GameState.sfxEnabled = enabled;
        });
        
        // 關閉按鈕
        const closeButton = this.add.text(width / 2, height / 2 + 130, '關閉', 
            GameUtils.createTextStyle(32, '#FFFFFF', 'Arial')
        );
        closeButton.setOrigin(0.5);
        closeButton.setBackgroundColor('#4A90E2');
        closeButton.setPadding(20, 10);
        closeButton.setInteractive({ useHandCursor: true })
            .on('pointerdown', () => {
                overlay.destroy();
                panel.destroy();
                titleText.destroy();
                bgmText.destroy();
                sfxText.destroy();
                closeButton.destroy();
            });
    }
    
    createToggle(x, y, initialState) {
        const toggle = this.add.container(x, y);
        let enabled = initialState;
        
        const bg = this.add.rectangle(0, 0, 80, 40, enabled ? 0x4CAF50 : 0xCCCCCC);
        bg.setStrokeStyle(2, 0x333333);
        
        const knob = this.add.circle(enabled ? 20 : -20, 0, 15, 0xFFFFFF);
        
        toggle.add([bg, knob]);
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerdown', () => {
                enabled = !enabled;
                bg.setFillStyle(enabled ? 0x4CAF50 : 0xCCCCCC);
                this.tweens.add({
                    targets: knob,
                    x: enabled ? 20 : -20,
                    duration: 200
                });
                toggle.emit('click', enabled);
            });
        
        return toggle;
    }
}
