/**
 * 主遊戲場景
 * Main Game Scene - 顯示角色狀態和週進度
 */

class MainScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MainScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const player = window.GameState.getPlayer();
        
        // 背景 - 嘗試載入原有背景圖
        try {
            if (this.textures.exists('background_intro')) {
                this.add.image(width / 2, height / 2, 'background_intro').setScale(
                    Math.max(width / 1200, height / 800)
                );
            } else {
                this.add.rectangle(width / 2, height / 2, width, height, 0xF0F4F8);
            }
        } catch (e) {
            this.add.rectangle(width / 2, height / 2, width, height, 0xF0F4F8);
        }
        
        // 頂部資訊欄
        this.createTopBar();
        
        // 角色顯示區（中央）
        this.createCharacterDisplay();
        
        // 屬性顯示
        this.createStatsDisplay();
        
        // 按鈕區
        this.createButtons();
        
        // 週變化提示
        if (player.lastWeekChange.some(v => v !== 0)) {
            this.showWeekChanges();
        }
    }
    
    createTopBar() {
        const width = this.cameras.main.width;
        const player = window.GameState.getPlayer();
        
        // 頂部背景
        const topBg = this.add.rectangle(width / 2, 50, width, 100, 0x4A90E2);
        
        // 角色名稱
        const nameText = this.add.text(50, 50, player.name, 
            GameUtils.createTextStyle(36, '#FFFFFF', 'Arial')
        );
        nameText.setOrigin(0, 0.5);
        
        // 週數顯示
        const weekText = this.add.text(width / 2, 50, 
            `第 ${player.weekNumber} 週 / 16`, 
            GameUtils.createTextStyle(32, '#FFEB3B', 'Arial')
        );
        weekText.setOrigin(0.5);
        
        // 設定按鈕
        const settingsBtn = this.add.text(width - 100, 50, '⚙️', {
            fontSize: '40px'
        });
        settingsBtn.setOrigin(0.5);
        settingsBtn.setInteractive({ useHandCursor: true })
            .on('pointerdown', () => {
                this.showSettingsMenu();
            });
    }
    
    createCharacterDisplay() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const player = window.GameState.getPlayer();
        
        // 角色圓形頭像（佔位符）
        const avatarBg = this.add.circle(width / 2, height / 2 - 50, 100, 
            parseInt(player.color.replace('#', '0x'))
        );
        avatarBg.setStrokeStyle(5, 0xFFFFFF);
        
        // 角色名稱
        const charName = this.add.text(width / 2, height / 2 + 80, player.name, 
            GameUtils.createTextStyle(48, player.color, 'Arial')
        );
        charName.setOrigin(0.5);
        
        // 互動提示
        const hintText = this.add.text(width / 2, height / 2 + 140, 
            '查看屬性詳情 👇', 
            {
                fontSize: '20px',
                fill: '#666666',
                fontFamily: 'Arial'
            }
        );
        hintText.setOrigin(0.5);
        
        // 點擊角色查看詳細信息
        avatarBg.setInteractive({ useHandCursor: true })
            .on('pointerdown', () => {
                this.showDetailedStats();
            });
    }
    
    createStatsDisplay() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const player = window.GameState.getPlayer();
        
        const statsConfig = [
            { name: '智力', key: 'intelligence', color: 0x87CEFA, icon: '🧠' },
            { name: '心情', key: 'mood', color: 0xFFB6C1, icon: '😊' },
            { name: '體力', key: 'energy', color: 0x90EE90, icon: '💪' },
            { name: '社交', key: 'social', color: 0xFFA500, icon: '🤝' },
            { name: '知識', key: 'knowledge', color: 0xDDA0DD, icon: '📚' }
        ];
        
        const startX = 150;
        const startY = height - 180;
        const barWidth = 200;
        const barHeight = 25;
        const gap = 35;
        
        statsConfig.forEach((stat, index) => {
            const yPos = startY + index * gap;
            const value = player[stat.key];
            
            // 圖標
            this.add.text(startX - 40, yPos, stat.icon, {
                fontSize: '24px'
            });
            
            // 屬性名稱
            this.add.text(startX, yPos, `${stat.name}:`, {
                fontSize: '20px',
                fill: '#333333',
                fontFamily: 'Arial'
            });
            
            // 進度條背景
            this.add.rectangle(startX + 80, yPos, barWidth, barHeight, 0xCCCCCC);
            
            // 進度條
            const barFill = this.add.rectangle(
                startX + 80 - barWidth / 2 + (barWidth * value / 100) / 2,
                yPos,
                barWidth * value / 100,
                barHeight,
                stat.color
            );
            barFill.setOrigin(0, 0.5);
            
            // 數值顯示
            this.add.text(startX + 80 + barWidth / 2 + 20, yPos, `${value}`, {
                fontSize: '20px',
                fill: '#333333',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            });
        });
    }
    
    createButtons() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 下一週按鈕
        this.createButton(width - 200, height - 80, '下一週 ▶', 0x4CAF50, () => {
            this.scene.start('StoryScene');
        });
        
        // 日記按鈕
        this.createButton(width - 200, height - 160, '📖 日記', 0x2196F3, () => {
            this.scene.launch('DiaryScene');
            this.scene.pause();
        });
    }
    
    createButton(x, y, text, color, callback) {
        const button = this.add.container(x, y);
        
        const bg = this.add.rectangle(0, 0, 180, 60, color);
        bg.setStrokeStyle(3, 0xFFFFFF);
        
        const buttonText = this.add.text(0, 0, text, 
            GameUtils.createTextStyle(24, '#FFFFFF', 'Arial')
        );
        buttonText.setOrigin(0.5);
        
        button.add([bg, buttonText]);
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                this.tweens.add({ targets: button, scale: 1.05, duration: 150 });
            })
            .on('pointerout', () => {
                this.tweens.add({ targets: button, scale: 1.0, duration: 150 });
            })
            .on('pointerdown', callback);
        
        return button;
    }
    
    showWeekChanges() {
        const width = this.cameras.main.width;
        const player = window.GameState.getPlayer();
        
        const changes = player.lastWeekChange;
        const labels = ['心情', '體力', '社交', '知識'];
        
        let changeText = '上週變化：\n';
        changes.forEach((change, index) => {
            if (change !== 0) {
                const sign = change > 0 ? '+' : '';
                changeText += `${labels[index]} ${sign}${change}  `;
            }
        });
        
        const notification = this.add.text(width / 2, 150, changeText, {
            fontSize: '24px',
            fill: '#FFFFFF',
            fontFamily: 'Arial',
            backgroundColor: '#333333',
            padding: { x: 20, y: 10 },
            align: 'center'
        });
        notification.setOrigin(0.5);
        notification.setAlpha(0);
        
        this.tweens.add({
            targets: notification,
            alpha: 1,
            duration: 500,
            onComplete: () => {
                this.time.delayedCall(3000, () => {
                    this.tweens.add({
                        targets: notification,
                        alpha: 0,
                        duration: 500,
                        onComplete: () => notification.destroy()
                    });
                });
            }
        });
    }
    
    showDetailedStats() {
        const player = window.GameState.getPlayer();
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 創建彈窗
        const overlay = this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.7);
        overlay.setInteractive();
        
        const panel = this.add.rectangle(width / 2, height / 2, 600, 500, 0xFFFFFF);
        
        const title = this.add.text(width / 2, height / 2 - 200, '角色詳細資訊', 
            GameUtils.createTextStyle(36, '#000000', 'Arial')
        );
        title.setOrigin(0.5);
        
        const status = player.getStatus();
        const infoText = `
角色：${status.name}
週數：${status.week} / 16

【屬性】
智力：${status.intelligence}
心情：${status.mood}
體力：${status.energy}
社交：${status.social}
知識：${status.knowledge}

【考試成績】
期中考：${status.midterm > 0 ? status.midterm + ' 分' : '尚未考試'}
期末考：${status.final > 0 ? status.final + ' 分' : '尚未考試'}
        `.trim();
        
        const info = this.add.text(width / 2, height / 2 + 20, infoText, {
            fontSize: '20px',
            fill: '#333333',
            fontFamily: 'Arial',
            lineSpacing: 8
        });
        info.setOrigin(0.5);
        
        const closeBtn = this.add.text(width / 2, height / 2 + 200, '關閉', 
            GameUtils.createTextStyle(28, '#FFFFFF', 'Arial')
        );
        closeBtn.setOrigin(0.5);
        closeBtn.setBackgroundColor('#4A90E2');
        closeBtn.setPadding(30, 10);
        closeBtn.setInteractive({ useHandCursor: true })
            .on('pointerdown', () => {
                overlay.destroy();
                panel.destroy();
                title.destroy();
                info.destroy();
                closeBtn.destroy();
            });
    }
    
    showSettingsMenu() {
        // 簡化版設定選單
        alert('設定功能開發中...');
    }
}
