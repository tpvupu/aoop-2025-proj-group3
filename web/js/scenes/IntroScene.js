/**
 * 遊戲介紹場景
 * Introduction Scene
 */

class IntroScene extends Phaser.Scene {
    constructor() {
        super({ key: 'IntroScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x667eea, 0x667eea, 0x764ba2, 0x764ba2, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 標題
        const title = this.add.text(width / 2, 80, '遊戲說明', 
            GameUtils.createTextStyle(48, '#FFFFFF', 'Arial')
        );
        title.setOrigin(0.5);
        
        // 說明內容
        const introContent = [
            '🎮 遊戲目標',
            '扮演一名大學生，在一個學期（16週）中平衡學習、社交、娛樂和休息，',
            '最終獲得好成績！',
            '',
            '📊 四大屬性',
            '• 心情 😊：影響學習效率和生活品質',
            '• 體力 💪：維持日常活動所需',
            '• 社交 🤝：人際關係和社會能力',
            '• 知識 📚：學習成果，直接影響考試成績',
            '',
            '📅 遊戲流程',
            '每週做出選擇，平衡四大屬性。',
            '第8週：期中考試',
            '第16週：期末考試',
            '最終根據表現計算GPA！',
            '',
            '💡 小提示',
            '• 不同活動會影響不同屬性',
            '• 保持屬性平衡很重要',
            '• 記得查看日記回顧歷史選擇'
        ];
        
        let yPos = 160;
        introContent.forEach(line => {
            const text = this.add.text(width / 2, yPos, line, {
                fontSize: line.includes('🎮') || line.includes('📊') || line.includes('📅') || line.includes('💡') 
                    ? '28px' : '20px',
                fill: '#FFFFFF',
                fontFamily: 'Arial',
                align: 'center',
                fontStyle: line.includes('•') ? '' : 'bold'
            });
            text.setOrigin(0.5);
            yPos += line.includes('🎮') || line.includes('📊') || line.includes('📅') || line.includes('💡') 
                ? 40 : 28;
        });
        
        // 返回按鈕
        const backButton = this.createButton(width / 2, height - 80, '返回', () => {
            this.scene.start('StartScene');
        });
    }
    
    createButton(x, y, text, callback) {
        const button = this.add.container(x, y);
        
        const bg = this.add.rectangle(0, 0, 250, 60, 0x4A90E2);
        bg.setStrokeStyle(3, 0xFFFFFF);
        
        const buttonText = this.add.text(0, 0, text, 
            GameUtils.createTextStyle(32, '#FFFFFF', 'Arial')
        );
        buttonText.setOrigin(0.5);
        
        button.add([bg, buttonText]);
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                bg.setFillStyle(0x5FA3F5);
                this.tweens.add({ targets: button, scale: 1.1, duration: 150 });
            })
            .on('pointerout', () => {
                bg.setFillStyle(0x4A90E2);
                this.tweens.add({ targets: button, scale: 1.0, duration: 150 });
            })
            .on('pointerdown', callback);
        
        return button;
    }
}
