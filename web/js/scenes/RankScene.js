/**
 * 排行榜場景（簡化版）
 * Rank Scene
 */

class RankScene extends Phaser.Scene {
    constructor() {
        super({ key: 'RankScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x1A237E, 0x1A237E, 0x4A148C, 0x4A148C, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 標題
        const title = this.add.text(width / 2, 80, '🏆 GPA 排行榜', 
            GameUtils.createTextStyle(48, '#FFD700', 'Arial')
        );
        title.setOrigin(0.5);
        
        // 說明文字
        const desc = this.add.text(width / 2, 150, 
            '此功能需要連接後端數據庫\n目前顯示模擬數據', 
            {
                fontSize: '20px',
                fill: '#FFFFFF',
                fontFamily: 'Arial',
                align: 'center',
                lineSpacing: 8
            }
        );
        desc.setOrigin(0.5);
        desc.setAlpha(0.7);
        
        // 模擬排行榜數據
        const mockRankings = [
            { name: '一二', gpa: 4.3, grade: 'A+', character: '一二' },
            { name: '布布', gpa: 3.7, grade: 'A-', character: '布布' },
            { name: '蜜桃', gpa: 3.3, grade: 'B+', character: '蜜桃' },
            { name: '灰灰', gpa: 3.0, grade: 'B', character: '灰灰' },
            { name: '玩家1', gpa: 2.7, grade: 'B-', character: '一二' }
        ];
        
        // 顯示排行榜
        const startY = 230;
        const rowHeight = 80;
        
        mockRankings.forEach((rank, index) => {
            const yPos = startY + index * rowHeight;
            const isTop3 = index < 3;
            const bgColor = isTop3 ? 0xFFD700 : 0xFFFFFF;
            const bgAlpha = isTop3 ? 0.2 : 0.1;
            
            // 排名背景
            const bg = this.add.rectangle(width / 2, yPos, 800, 70, bgColor, bgAlpha);
            bg.setStrokeStyle(2, 0xFFFFFF, 0.3);
            
            // 排名
            const rankText = this.add.text(width / 2 - 350, yPos, 
                `${index + 1}`, 
                {
                    fontSize: isTop3 ? '36px' : '28px',
                    fill: isTop3 ? '#FFD700' : '#FFFFFF',
                    fontFamily: 'Arial',
                    fontStyle: 'bold'
                }
            );
            rankText.setOrigin(0.5);
            
            // 獎牌表情
            if (index === 0) {
                const medal = this.add.text(width / 2 - 300, yPos, '🥇', {
                    fontSize: '32px'
                });
                medal.setOrigin(0.5);
            } else if (index === 1) {
                const medal = this.add.text(width / 2 - 300, yPos, '🥈', {
                    fontSize: '32px'
                });
                medal.setOrigin(0.5);
            } else if (index === 2) {
                const medal = this.add.text(width / 2 - 300, yPos, '🥉', {
                    fontSize: '32px'
                });
                medal.setOrigin(0.5);
            }
            
            // 玩家名稱
            const nameText = this.add.text(width / 2 - 200, yPos, 
                rank.name, 
                {
                    fontSize: '26px',
                    fill: '#FFFFFF',
                    fontFamily: 'Arial'
                }
            );
            nameText.setOrigin(0, 0.5);
            
            // 等級
            const gradeText = this.add.text(width / 2 + 50, yPos, 
                rank.grade, 
                {
                    fontSize: '28px',
                    fill: '#4CAF50',
                    fontFamily: 'Arial',
                    fontStyle: 'bold'
                }
            );
            gradeText.setOrigin(0.5);
            
            // GPA
            const gpaText = this.add.text(width / 2 + 200, yPos, 
                `GPA: ${rank.gpa.toFixed(1)}`, 
                {
                    fontSize: '24px',
                    fill: '#FFD700',
                    fontFamily: 'Arial'
                }
            );
            gpaText.setOrigin(0.5);
        });
        
        // 返回按鈕
        const backButton = this.add.text(width / 2, height - 80, '返回', 
            GameUtils.createTextStyle(32, '#FFFFFF', 'Arial')
        );
        backButton.setOrigin(0.5);
        backButton.setBackgroundColor('#4A90E2');
        backButton.setPadding(40, 15);
        backButton.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                backButton.setScale(1.05);
            })
            .on('pointerout', () => {
                backButton.setScale(1.0);
            })
            .on('pointerdown', () => {
                this.scene.start('EndScene');
            });
    }
}
