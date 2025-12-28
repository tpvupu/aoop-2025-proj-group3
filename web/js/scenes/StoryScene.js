/**
 * 劇情場景
 * Story Scene - 用於顯示週開始前的劇情
 */

class StoryScene extends Phaser.Scene {
    constructor() {
        super({ key: 'StoryScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const player = window.GameState.getPlayer();
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x667eea, 0x667eea, 0x764ba2, 0x764ba2, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 根據週數顯示不同劇情
        let storyText = '';
        if (player.weekNumber === 0) {
            storyText = `歡迎，${player.name}！\n\n新的學期開始了！\n作為一名大學生，你需要在學習、社交、娛樂和休息之間找到平衡。\n\n每週你都會面臨選擇，這些選擇將影響你的狀態和最終成績。\n\n準備好開始你的大學生活了嗎？`;
        } else if (player.weekNumber === 8) {
            storyText = `第 ${player.weekNumber} 週\n\n期中考試週到了！\n\n是時候檢驗你這半學期的學習成果了。\n你目前的知識積累將決定你的期中考成績。\n\n加油！`;
        } else if (player.weekNumber === 16) {
            storyText = `第 ${player.weekNumber} 週\n\n期末考試週來臨！\n\n這是最後的衝刺階段。\n你這一學期的努力即將得到回報。\n\n全力以赴吧！`;
        } else {
            storyText = `第 ${player.weekNumber + 1} 週\n\n新的一週開始了。\n你感覺如何？\n\n繼續保持平衡，朝著目標前進！`;
        }
        
        // 顯示劇情文字
        const story = this.add.text(width / 2, height / 2 - 50, storyText, {
            fontSize: '28px',
            fill: '#FFFFFF',
            fontFamily: 'Arial',
            align: 'center',
            lineSpacing: 15,
            wordWrap: { width: 900 }
        });
        story.setOrigin(0.5);
        
        // 打字機效果（簡化版）
        story.setAlpha(0);
        this.tweens.add({
            targets: story,
            alpha: 1,
            duration: 1000
        });
        
        // 繼續按鈕
        const continueButton = this.add.text(width / 2, height - 100, '點擊繼續 ▶', 
            GameUtils.createTextStyle(32, '#FFEB3B', 'Arial')
        );
        continueButton.setOrigin(0.5);
        continueButton.setAlpha(0);
        
        // 延遲顯示按鈕
        this.time.delayedCall(1500, () => {
            this.tweens.add({
                targets: continueButton,
                alpha: 1,
                duration: 500
            });
            
            // 閃爍效果
            this.tweens.add({
                targets: continueButton,
                alpha: { from: 1, to: 0.5 },
                duration: 800,
                yoyo: true,
                repeat: -1
            });
            
            continueButton.setInteractive({ useHandCursor: true })
                .on('pointerdown', () => {
                    this.proceedToNext();
                });
        });
        
        // 點擊任意位置繼續
        this.input.on('pointerdown', () => {
            if (continueButton.alpha > 0.8) {
                this.proceedToNext();
            }
        });
    }
    
    proceedToNext() {
        const player = window.GameState.getPlayer();
        
        // 增加週數
        player.nextWeek();
        
        // 根據週數決定下一個場景
        if (player.weekNumber === 8 || player.weekNumber === 16) {
            // 考試週
            this.showExamScene();
        } else if (player.weekNumber > 16) {
            // 遊戲結束
            this.scene.start('EndScene');
        } else {
            // 普通週，進入事件選擇
            this.scene.start('EventScene');
        }
    }
    
    showExamScene() {
        const player = window.GameState.getPlayer();
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 清除當前內容
        this.children.removeAll();
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x667eea, 0x667eea, 0x764ba2, 0x764ba2, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 考試標題
        const examTitle = this.add.text(width / 2, height / 2 - 150, 
            player.weekNumber === 8 ? '期中考試' : '期末考試', 
            GameUtils.createTextStyle(56, '#FFEB3B', 'Arial')
        );
        examTitle.setOrigin(0.5);
        
        // 計算成績
        if (player.weekNumber === 8) {
            player.getMidterm();
            var score = player.midterm;
            var scoreText = `期中考成績：${score} 分`;
        } else {
            player.getFinal();
            var score = player.final;
            var scoreText = `期末考成績：${score} 分`;
        }
        
        const resultText = this.add.text(width / 2, height / 2, scoreText, 
            GameUtils.createTextStyle(40, '#FFFFFF', 'Arial')
        );
        resultText.setOrigin(0.5);
        resultText.setAlpha(0);
        
        // 動畫顯示成績
        this.time.delayedCall(1000, () => {
            this.tweens.add({
                targets: resultText,
                alpha: 1,
                scale: { from: 0.5, to: 1 },
                duration: 800,
                ease: 'Back.easeOut'
            });
        });
        
        // 繼續按鈕
        const continueButton = this.add.text(width / 2, height - 100, '繼續', 
            GameUtils.createTextStyle(32, '#FFFFFF', 'Arial')
        );
        continueButton.setOrigin(0.5);
        continueButton.setBackgroundColor('#4A90E2');
        continueButton.setPadding(30, 15);
        continueButton.setAlpha(0);
        
        this.time.delayedCall(2500, () => {
            continueButton.setAlpha(1);
            continueButton.setInteractive({ useHandCursor: true })
                .on('pointerdown', () => {
                    if (player.weekNumber === 16) {
                        // 期末考後進入結束場景
                        this.scene.start('EndScene');
                    } else {
                        // 期中考後繼續遊戲
                        this.scene.start('MainScene');
                    }
                });
        });
    }
}
