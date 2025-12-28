/**
 * 結束場景
 * End Scene - 顯示最終成績和結果
 */

class EndScene extends Phaser.Scene {
    constructor() {
        super({ key: 'EndScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const player = window.GameState.getPlayer();
        
        // 計算最終 GPA
        const result = player.calculateGPA();
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x1A237E, 0x1A237E, 0x311B92, 0x311B92, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 標題
        const title = this.add.text(width / 2, 80, '🎓 學期結束', 
            GameUtils.createTextStyle(56, '#FFD700', 'Arial')
        );
        title.setOrigin(0.5);
        
        // 角色名稱
        const nameText = this.add.text(width / 2, 160, 
            `${player.name} 的成績單`, 
            GameUtils.createTextStyle(36, '#FFFFFF', 'Arial')
        );
        nameText.setOrigin(0.5);
        
        // 成績卡片
        this.createGradeCard(width, height, player, result);
        
        // 評語
        this.createComment(width, height, result);
        
        // 按鈕區
        this.createButtons(width, height);
        
        // 煙火效果（如果成績好）
        if (result.gpa >= 3.5) {
            this.createFireworks();
        }
    }
    
    createGradeCard(width, height, player, result) {
        const cardX = width / 2;
        const cardY = height / 2 - 20;
        
        // 卡片背景
        const card = this.add.rectangle(cardX, cardY, 700, 350, 0xFFFFFF, 0.95);
        card.setStrokeStyle(5, 0xFFD700);
        
        // 期中考成績
        const midtermText = this.add.text(cardX, cardY - 120, 
            `期中考：${player.midterm} 分`, 
            {
                fontSize: '28px',
                fill: '#333333',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            }
        );
        midtermText.setOrigin(0.5);
        
        // 期末考成績
        const finalText = this.add.text(cardX, cardY - 70, 
            `期末考：${player.final} 分`, 
            {
                fontSize: '28px',
                fill: '#333333',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            }
        );
        finalText.setOrigin(0.5);
        
        // 總成績
        const totalText = this.add.text(cardX, cardY - 10, 
            `總成績：${result.score} 分`, 
            {
                fontSize: '32px',
                fill: '#1976D2',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            }
        );
        totalText.setOrigin(0.5);
        
        // 等級
        const gradeColor = this.getGradeColor(result.grade);
        const gradeText = this.add.text(cardX, cardY + 50, 
            `等級：${result.grade}`, 
            {
                fontSize: '48px',
                fill: gradeColor,
                fontFamily: 'Arial',
                fontStyle: 'bold'
            }
        );
        gradeText.setOrigin(0.5);
        
        // 添加放大動畫
        this.tweens.add({
            targets: gradeText,
            scale: { from: 1, to: 1.1 },
            duration: 1000,
            yoyo: true,
            repeat: -1
        });
        
        // GPA
        const gpaText = this.add.text(cardX, cardY + 110, 
            `GPA：${result.gpa.toFixed(2)}`, 
            {
                fontSize: '36px',
                fill: '#4CAF50',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            }
        );
        gpaText.setOrigin(0.5);
    }
    
    getGradeColor(grade) {
        if (grade.startsWith('A')) return '#4CAF50';
        if (grade.startsWith('B')) return '#2196F3';
        if (grade.startsWith('C')) return '#FF9800';
        return '#F44336';
    }
    
    createComment(width, height, result) {
        let comment = '';
        if (result.gpa >= 4.0) {
            comment = '🌟 太棒了！你是學霸！';
        } else if (result.gpa >= 3.5) {
            comment = '👍 表現優秀！繼續加油！';
        } else if (result.gpa >= 3.0) {
            comment = '😊 不錯的成績！還有進步空間！';
        } else if (result.gpa >= 2.5) {
            comment = '💪 及格了！下次可以更好！';
        } else {
            comment = '📚 需要更加努力學習！';
        }
        
        const commentText = this.add.text(width / 2, height / 2 + 200, comment, 
            GameUtils.createTextStyle(32, '#FFEB3B', 'Arial')
        );
        commentText.setOrigin(0.5);
    }
    
    createButtons(width, height) {
        const buttonY = height - 100;
        
        // 查看排行榜按鈕
        this.createButton(width / 2 - 220, buttonY, '🏆 排行榜', 0x2196F3, () => {
            this.scene.start('RankScene');
        });
        
        // 重新開始按鈕
        this.createButton(width / 2, buttonY, '🔄 再玩一次', 0x4CAF50, () => {
            window.GameState.reset();
            this.scene.start('CharacterSelectScene');
        });
        
        // 返回主選單按鈕
        this.createButton(width / 2 + 220, buttonY, '🏠 主選單', 0xFF9800, () => {
            window.GameState.reset();
            this.scene.start('FirstScene');
        });
    }
    
    createButton(x, y, text, color, callback) {
        const button = this.add.container(x, y);
        
        const bg = this.add.rectangle(0, 0, 180, 60, color);
        bg.setStrokeStyle(3, 0xFFFFFF);
        
        const buttonText = this.add.text(0, 0, text, {
            fontSize: '20px',
            fill: '#FFFFFF',
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        buttonText.setOrigin(0.5);
        
        button.add([bg, buttonText]);
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                this.tweens.add({ targets: button, scale: 1.1, duration: 150 });
            })
            .on('pointerout', () => {
                this.tweens.add({ targets: button, scale: 1.0, duration: 150 });
            })
            .on('pointerdown', callback);
        
        return button;
    }
    
    createFireworks() {
        // 簡單的煙火粒子效果
        const colors = [0xFFD700, 0xFF6B6B, 0x4ECDC4, 0xFFE66D, 0x95E1D3];
        
        for (let i = 0; i < 5; i++) {
            this.time.delayedCall(i * 500, () => {
                const x = Phaser.Math.Between(200, 1000);
                const y = Phaser.Math.Between(100, 400);
                
                for (let j = 0; j < 20; j++) {
                    const particle = this.add.circle(x, y, 5, colors[i % colors.length]);
                    
                    const angle = (Math.PI * 2 * j) / 20;
                    const speed = Phaser.Math.Between(100, 200);
                    
                    this.tweens.add({
                        targets: particle,
                        x: x + Math.cos(angle) * speed,
                        y: y + Math.sin(angle) * speed,
                        alpha: { from: 1, to: 0 },
                        duration: 1000,
                        ease: 'Cubic.easeOut',
                        onComplete: () => particle.destroy()
                    });
                }
            });
        }
    }
}
