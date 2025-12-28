/**
 * 啟動場景 - 初始化遊戲
 * Boot Scene - Initialize Game Systems
 */

class BootScene extends Phaser.Scene {
    constructor() {
        super({ key: 'BootScene' });
    }
    
    preload() {
        // 創建載入進度條
        this.createLoadingBar();
    }
    
    create() {
        // 設置全局設定
        this.sound.setVolume(GameConfig.audio.bgmVolume);
        
        // 前往資源載入場景
        this.scene.start('PreloadScene');
    }
    
    createLoadingBar() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 載入文字
        const loadingText = this.add.text(width / 2, height / 2 - 50, '啟動遊戲中...', {
            fontSize: '32px',
            fill: '#ffffff',
            fontFamily: 'Arial'
        });
        loadingText.setOrigin(0.5);
        
        // 進度條背景
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(width / 2 - 160, height / 2 - 10, 320, 30);
        
        // 載入事件
        this.load.on('progress', (value) => {
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(width / 2 - 150, height / 2, 300 * value, 10);
        });
        
        this.load.on('complete', () => {
            progressBar.destroy();
            progressBox.destroy();
            loadingText.destroy();
        });
    }
}
