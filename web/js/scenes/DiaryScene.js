/**
 * 日記場景
 * Diary Scene - 查看歷史記錄
 */

class DiaryScene extends Phaser.Scene {
    constructor() {
        super({ key: 'DiaryScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const player = window.GameState.getPlayer();
        
        // 半透明背景遮罩
        const overlay = this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.7);
        overlay.setInteractive();
        
        // 日記本背景
        const diaryBg = this.add.rectangle(width / 2, height / 2, 900, 650, 0xFFF9C4);
        diaryBg.setStrokeStyle(5, 0x8D6E63);
        
        // 標題
        const title = this.add.text(width / 2, height / 2 - 280, '📖 我的日記', {
            fontSize: '42px',
            fill: '#5D4037',
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        title.setOrigin(0.5);
        
        // 獲取事件歷史
        const history = player.getEventHistory();
        const entries = Object.entries(history).sort((a, b) => b[0] - a[0]); // 按週數降序
        
        if (entries.length === 0) {
            const emptyText = this.add.text(width / 2, height / 2, 
                '還沒有任何記錄\n開始你的冒險吧！', 
                {
                    fontSize: '28px',
                    fill: '#8D6E63',
                    fontFamily: 'Arial',
                    align: 'center',
                    lineSpacing: 10
                }
            );
            emptyText.setOrigin(0.5);
        } else {
            // 創建滾動內容
            this.createDiaryEntries(entries, width, height);
        }
        
        // 關閉按鈕
        const closeButton = this.add.text(width / 2, height / 2 + 270, '關閉', {
            fontSize: '32px',
            fill: '#FFFFFF',
            fontFamily: 'Arial',
            backgroundColor: '#8D6E63',
            padding: { x: 40, y: 12 }
        });
        closeButton.setOrigin(0.5);
        closeButton.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                closeButton.setScale(1.05);
            })
            .on('pointerout', () => {
                closeButton.setScale(1.0);
            })
            .on('pointerdown', () => {
                this.scene.resume('MainScene');
                this.scene.stop();
            });
    }
    
    createDiaryEntries(entries, width, height) {
        const startY = height / 2 - 220;
        const maxEntries = 6;
        const displayEntries = entries.slice(0, maxEntries);
        
        displayEntries.forEach((entry, index) => {
            const [weekNum, data] = entry;
            const yPos = startY + index * 90;
            
            // 週數標籤
            const weekLabel = this.add.text(width / 2 - 400, yPos, 
                `第 ${weekNum} 週`, 
                {
                    fontSize: '22px',
                    fill: '#5D4037',
                    fontFamily: 'Arial',
                    fontStyle: 'bold'
                }
            );
            
            // 事件描述
            const eventDesc = this.add.text(width / 2 - 300, yPos - 10, 
                data.event.substring(0, 30) + (data.event.length > 30 ? '...' : ''), 
                {
                    fontSize: '18px',
                    fill: '#6D4C41',
                    fontFamily: 'Arial'
                }
            );
            
            // 選擇內容
            const optionDesc = this.add.text(width / 2 - 300, yPos + 15, 
                '→ ' + data.option.substring(0, 40) + (data.option.length > 40 ? '...' : ''), 
                {
                    fontSize: '16px',
                    fill: '#795548',
                    fontFamily: 'Arial'
                }
            );
            
            // 分隔線
            if (index < displayEntries.length - 1) {
                const line = this.add.line(
                    width / 2, yPos + 40,
                    -400, 0, 400, 0,
                    0xBCAAA4, 0.5
                );
                line.setLineWidth(1);
            }
        });
        
        // 如果有更多記錄
        if (entries.length > maxEntries) {
            const moreText = this.add.text(width / 2, height / 2 + 220, 
                `...還有 ${entries.length - maxEntries} 條記錄`, 
                {
                    fontSize: '18px',
                    fill: '#8D6E63',
                    fontFamily: 'Arial',
                    fontStyle: 'italic'
                }
            );
            moreText.setOrigin(0.5);
        }
    }
}
