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
        
        // 背景
        this.add.rectangle(width / 2, height / 2, width, height, 0xE8F5E9);
        
        // 獲取當前週的事件
        const weekEvent = eventsData[player.weekNumber];
        
        if (!weekEvent) {
            console.error(`No event data for week ${player.weekNumber}`);
            this.scene.start('MainScene');
            return;
        }
        
        // 週數顯示
        const weekText = this.add.text(width / 2, 80, 
            `第 ${player.weekNumber} 週`, 
            GameUtils.createTextStyle(42, '#2E7D32', 'Arial')
        );
        weekText.setOrigin(0.5);
        
        // 事件描述
        const eventBg = this.add.rectangle(width / 2, 180, 900, 120, 0xFFFFFF);
        eventBg.setStrokeStyle(3, 0x4CAF50);
        
        const eventText = this.add.text(width / 2, 180, weekEvent.event, {
            fontSize: '26px',
            fill: '#333333',
            fontFamily: 'Arial',
            align: 'center',
            wordWrap: { width: 850 }
        });
        eventText.setOrigin(0.5);
        
        // 選項顯示
        const optionsTitle = this.add.text(width / 2, 280, '請選擇你的行動：', {
            fontSize: '28px',
            fill: '#1B5E20',
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        optionsTitle.setOrigin(0.5);
        
        // 創建選項按鈕
        const options = weekEvent.options;
        const optionColors = [0x2196F3, 0x4CAF50, 0xFF9800, 0x9C27B0];
        
        if (options && options.length > 0) {
            options.forEach((option, index) => {
                this.createOptionButton(
                    width / 2,
                    360 + index * 90,
                    option,
                    optionColors[index % optionColors.length]
                );
            });
        }
        
        // 添加活動圖標提示
        this.createActivityIcons();
    }
    
    createOptionButton(x, y, option, color) {
        const player = window.GameState.getPlayer();
        const button = this.add.container(x, y);
        
        // 按鈕背景
        const bg = this.add.rectangle(0, 0, 800, 70, color);
        bg.setStrokeStyle(3, 0xFFFFFF);
        
        // 活動圖標
        const activityEmoji = GameConfig.activities[option.activity]?.emoji || '📋';
        const emojiText = this.add.text(-380, 0, activityEmoji, {
            fontSize: '32px'
        });
        emojiText.setOrigin(0, 0.5);
        
        // 選項文字
        const buttonText = this.add.text(-20, 0, option.text, {
            fontSize: '24px',
            fill: '#FFFFFF',
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        buttonText.setOrigin(0.5);
        
        // 變化提示
        const changesText = this.formatChanges(option.changes);
        const changesDisplay = this.add.text(350, 0, changesText, {
            fontSize: '16px',
            fill: '#FFEB3B',
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        changesDisplay.setOrigin(1, 0.5);
        
        button.add([bg, emojiText, buttonText, changesDisplay]);
        
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
                this.selectOption(option);
            });
        
        return button;
    }
    
    formatChanges(changes) {
        const parts = [];
        if (changes.mood !== 0) parts.push(`😊${changes.mood > 0 ? '+' : ''}${changes.mood}`);
        if (changes.energy !== 0) parts.push(`💪${changes.energy > 0 ? '+' : ''}${changes.energy}`);
        if (changes.social !== 0) parts.push(`🤝${changes.social > 0 ? '+' : ''}${changes.social}`);
        if (changes.knowledge !== 0) parts.push(`📚${changes.knowledge > 0 ? '+' : ''}${changes.knowledge}`);
        return parts.join(' ');
    }
    
    lightenColor(color) {
        const r = (color >> 16) & 0xFF;
        const g = (color >> 8) & 0xFF;
        const b = color & 0xFF;
        
        return ((Math.min(255, r + 30) << 16) | 
                (Math.min(255, g + 30) << 8) | 
                Math.min(255, b + 30));
    }
    
    selectOption(option) {
        const player = window.GameState.getPlayer();
        
        // 記錄選擇
        const eventData = window.GameState.getEventsData()[player.weekNumber];
        player.recordEvent(player.weekNumber, eventData.event, option.text, option.changes);
        
        // 執行對應的活動
        const degree = 1.0;
        switch (option.activity) {
            case 'study':
                player.study(degree);
                break;
            case 'socialize':
                player.socialize(degree);
                break;
            case 'play_game':
                player.playGame(degree);
                break;
            case 'rest':
                player.rest(degree);
                break;
            default:
                // 直接應用變化
                player.mood = GameUtils.clamp(player.mood + (option.changes.mood || 0), 0, 100);
                player.energy = GameUtils.clamp(player.energy + (option.changes.energy || 0), 0, 100);
                player.social = GameUtils.clamp(player.social + (option.changes.social || 0), 0, 100);
                player.knowledge = GameUtils.clamp(player.knowledge + (option.changes.knowledge || 0), 0, 100);
                player.lastWeekChange = [
                    option.changes.mood || 0,
                    option.changes.energy || 0,
                    option.changes.social || 0,
                    option.changes.knowledge || 0
                ];
        }
        
        // 顯示選擇結果動畫
        this.showChoiceResult(option);
    }
    
    showChoiceResult(option) {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 半透明遮罩
        const overlay = this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.8);
        
        // 結果文字
        const resultText = this.add.text(width / 2, height / 2 - 50, 
            '你選擇了：\n' + option.text, 
            {
                fontSize: '36px',
                fill: '#FFFFFF',
                fontFamily: 'Arial',
                align: 'center',
                lineSpacing: 15
            }
        );
        resultText.setOrigin(0.5);
        resultText.setAlpha(0);
        
        // 變化提示
        const changesText = this.add.text(width / 2, height / 2 + 60, 
            this.formatChanges(option.changes), 
            {
                fontSize: '32px',
                fill: '#FFEB3B',
                fontFamily: 'Arial'
            }
        );
        changesText.setOrigin(0.5);
        changesText.setAlpha(0);
        
        // 動畫顯示
        this.tweens.add({
            targets: [resultText, changesText],
            alpha: 1,
            duration: 800,
            onComplete: () => {
                this.time.delayedCall(2000, () => {
                    this.scene.start('MainScene');
                });
            }
        });
    }
    
    createActivityIcons() {
        const width = this.cameras.main.width;
        
        // 圖例
        const legend = this.add.text(width - 50, 100, 
            '圖例：\n😊 心情\n💪 體力\n🤝 社交\n📚 知識', 
            {
                fontSize: '18px',
                fill: '#333333',
                fontFamily: 'Arial',
                align: 'left',
                lineSpacing: 8,
                backgroundColor: '#FFFFFF',
                padding: { x: 15, y: 10 }
            }
        );
        legend.setOrigin(1, 0);
        legend.setAlpha(0.9);
    }
}
