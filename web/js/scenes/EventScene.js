/**
 * 事件選擇場景
 * Event Scene - 玩家做出選擇
 */

class EventScene extends Phaser.Scene {
    constructor() {
        super({ key: 'EventScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const player = window.GameState.getPlayer();
        const eventsData = window.GameState.getEventsData();
        
        // 背景圖片
        if (this.textures.exists('background_intro')) {
            const bg = this.add.image(width / 2, height / 2, 'background_intro');
            const scale = Math.max(width / bg.width, height / bg.height);
            bg.setScale(scale);
        } else {
            this.add.rectangle(width / 2, height / 2, width, height, 0xE8F5E9);
        }
        
        // 獲取當前週的事件
        const weekKey = `week_${player.weekNumber}`;
        const weekEvent = eventsData[weekKey];
        
        if (!weekEvent || !weekEvent.events || !weekEvent.events.options) {
            console.error(`No event data for week ${player.weekNumber}`);
            this.scene.start('MainScene');
            return;
        }
        
        // 標題（週數和事件標題）
        const titleText = this.add.text(width / 2, 60, 
            weekEvent.title || `第 ${player.weekNumber} 週`, 
            {
                fontSize: '42px',
                fill: '#2E7D32',
                fontFamily: 'JasonHandwriting3, Arial',
                fontStyle: 'bold'
            }
        );
        titleText.setOrigin(0.5);
        
        // 事件描述背景
        const descBg = this.add.rectangle(width / 2, 150, 900, 100, 0xFFFFFF);
        descBg.setStrokeStyle(3, 0x4CAF50);
        
        // 事件描述文字
        const eventText = this.add.text(width / 2, 150, weekEvent.events.description || '', {
            fontSize: '24px',
            fill: '#333333',
            fontFamily: 'JasonHandwriting3, Arial',
            align: 'center',
            wordWrap: { width: 850 }
        });
        eventText.setOrigin(0.5);
        
        // 創建選項按鈕
        const options = weekEvent.events.options;
        const optionKeys = Object.keys(options); // ['A', 'B', 'C', 'D']
        const optionColors = [0x2196F3, 0x4CAF50, 0xFF9800, 0x9C27B0];
        
        const baseY = 280;
        const buttonHeight = 70;
        const spacing = 20;
        
        optionKeys.forEach((key, index) => {
            const option = options[key];
            const buttonY = baseY + index * (buttonHeight + spacing);
            
            this.createOptionButton(
                width / 2,
                buttonY,
                option,
                key,
                optionColors[index % optionColors.length],
                weekKey
            );
        });
    }
    
    createOptionButton(x, y, option, optionKey, color, weekKey) {
        const player = window.GameState.getPlayer();
        const button = this.add.container(x, y);
        
        // 按鈕背景
        const bg = this.add.rectangle(0, 0, 800, 70, color);
        bg.setStrokeStyle(3, 0xFFFFFF);
        
        // 活動圖標
        const activityEmoji = GameConfig.activities[option.attribute]?.emoji || '📋';
        const emojiText = this.add.text(-380, 0, activityEmoji, {
            fontSize: '32px'
        });
        emojiText.setOrigin(0, 0.5);
        
        // 選項文字
        const buttonText = this.add.text(-20, 0, option.text, {
            fontSize: '22px',
            fill: '#FFFFFF',
            fontFamily: 'JasonHandwriting3, Arial',
            fontStyle: 'bold'
        });
        buttonText.setOrigin(0.5);
        
        button.add([bg, emojiText, buttonText]);
        
        // 互動效果
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                bg.setFillStyle(this.lightenColor(color));
                this.tweens.add({
                    targets: button,
                    scale: 1.03,
                    duration: 150
                });
            })
            .on('pointerout', () => {
                bg.setFillStyle(color);
                this.tweens.add({
                    targets: button,
                    scale: 1.0,
                    duration: 150
                });
            })
            .on('pointerdown', () => {
                this.selectOption(option, optionKey, weekKey);
            });
        
        return button;
    }
    
    lightenColor(color) {
        const r = (color >> 16) & 0xFF;
        const g = (color >> 8) & 0xFF;
        const b = color & 0xFF;
        
        return ((Math.min(255, r + 30) << 16) | 
                (Math.min(255, g + 30) << 8) | 
                Math.min(255, b + 30));
    }
    
    selectOption(option, optionKey, weekKey) {
        const player = window.GameState.getPlayer();
        
        // 記錄選擇
        player.chosen[player.weekNumber] = optionKey;
        
        // 執行相應的活動以應用屬性變化
        const degree = 1.0;
        switch (option.attribute) {
            case 'study':
                player.study(degree);
                break;
            case 'social':
                player.socialize(degree);
                break;
            case 'play_game':
                player.playGame(degree);
                break;
            case 'rest':
                player.rest(degree);
                break;
        }
        
        // 顯示選擇結果動畫
        this.showChoiceResult(option);
    }
    
    showChoiceResult(option) {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 半透明遮罩
        const overlay = this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0);
        this.tweens.add({
            targets: overlay,
            alpha: 0.8,
            duration: 300
        });
        
        // 結果文字背景
        const resultBg = this.add.rectangle(width / 2, height / 2, 600, 200, 0xFFFFFF);
        resultBg.setStrokeStyle(4, 0x4CAF50);
        resultBg.setAlpha(0);
        
        // 結果文字
        const resultText = this.add.text(width / 2, height / 2 - 40, 
            '你選擇了：\n' + option.text, 
            {
                fontSize: '28px',
                fill: '#333333',
                fontFamily: 'JasonHandwriting3, Arial',
                align: 'center',
                lineSpacing: 15
            }
        );
        resultText.setOrigin(0.5);
        resultText.setAlpha(0);
        
        // 屬性變化提示
        const player = window.GameState.getPlayer();
        const changesText = this.add.text(width / 2, height / 2 + 60, 
            this.formatChanges(player.lastWeekChange), 
            {
                fontSize: '22px',
                fill: '#FF6B6B',
                fontFamily: 'Arial'
            }
        );
        changesText.setOrigin(0.5);
        changesText.setAlpha(0);
        
        // 動畫顯示結果
        this.tweens.add({
            targets: [resultBg, resultText, changesText],
            alpha: 1,
            duration: 600,
            onComplete: () => {
                // 2秒後返回主場景
                this.time.delayedCall(2000, () => {
                    this.scene.start('MainScene');
                });
            }
        });
    }
    
    formatChanges(changeList) {
        // changeList = [mood, energy, social, knowledge]
        const labels = ['😊心情', '💪體力', '🤝社交', '📚知識'];
        const parts = [];
        
        changeList.forEach((change, index) => {
            if (change !== 0) {
                const sign = change > 0 ? '+' : '';
                parts.push(`${labels[index]} ${sign}${Math.round(change)}`);
            }
        });
        
        return parts.length > 0 ? parts.join('  ') : '無變化';
    }
}
