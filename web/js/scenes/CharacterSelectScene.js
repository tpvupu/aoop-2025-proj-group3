/**
 * 角色選擇場景
 * Character Select Scene
 */

class CharacterSelectScene extends Phaser.Scene {
    constructor() {
        super({ key: 'CharacterSelectScene' });
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景
        const graphics = this.add.graphics();
        graphics.fillGradientStyle(0x667eea, 0x667eea, 0x764ba2, 0x764ba2, 1);
        graphics.fillRect(0, 0, width, height);
        
        // 標題
        const title = this.add.text(width / 2, 80, '選擇你的角色', 
            GameUtils.createTextStyle(48, '#FFFFFF', 'Arial')
        );
        title.setOrigin(0.5);
        
        // 角色卡片位置
        const cardPositions = [
            { x: width / 4, y: height / 2 + 20 },
            { x: width / 2, y: height / 2 + 20 },
            { x: width * 3 / 4, y: height / 2 + 20 }
        ];
        
        // 創建角色卡片（只顯示三個，第四個可以滾動或放在下方）
        const characters = ['bubu', 'yier', 'mitao'];
        characters.forEach((charKey, index) => {
            this.createCharacterCard(
                cardPositions[index].x,
                cardPositions[index].y,
                GameConfig.characters[charKey]
            );
        });
        
        // 第四個角色放在下方
        this.createCharacterCard(
            width / 2,
            height / 2 + 280,
            GameConfig.characters['huihui']
        );
        
        // 返回按鈕
        this.createBackButton();
    }
    
    createCharacterCard(x, y, characterData) {
        const card = this.add.container(x, y);
        
        // 卡片背景
        const bg = this.add.rectangle(0, 0, 240, 280, 0xFFFFFF, 0.95);
        bg.setStrokeStyle(4, parseInt(characterData.color.replace('#', '0x')));
        
        // 角色名稱
        const nameText = this.add.text(0, -110, characterData.name, {
            fontSize: '32px',
            fill: characterData.color,
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        nameText.setOrigin(0.5);
        
        // 角色頭像圖片
        const avatarMap = {
            '布布': 'bubu_head',
            '一二': 'yier_head',
            '蜜桃': 'mitao_head',
            '灰灰': 'huihui_head'
        };
        
        const avatarKey = avatarMap[characterData.name] || 'bubu_head';
        let avatar;
        
        try {
            avatar = this.add.image(0, -30, avatarKey);
            avatar.setScale(1.5);
        } catch (e) {
            // 如果圖片載入失敗，使用純色圓形替代
            avatar = this.add.circle(0, -30, 50, parseInt(characterData.color.replace('#', '0x')));
        }
        
        // 屬性顯示
        const statsY = 40;
        const statsText = this.add.text(0, statsY, 
            `智力: ${characterData.intelligence}\n` +
            `心情: ${characterData.mood}\n` +
            `體力: ${characterData.energy}\n` +
            `社交: ${characterData.social}`,
            {
                fontSize: '18px',
                fill: '#333333',
                fontFamily: 'Arial',
                align: 'center',
                lineSpacing: 5
            }
        );
        statsText.setOrigin(0.5);
        
        card.add([bg, nameText, avatar, statsText]);
        
        // 點擊選擇
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                this.tweens.add({
                    targets: card,
                    scale: 1.05,
                    duration: 200
                });
                bg.setStrokeStyle(6, parseInt(characterData.color.replace('#', '0x')));
            })
            .on('pointerout', () => {
                this.tweens.add({
                    targets: card,
                    scale: 1.0,
                    duration: 200
                });
                bg.setStrokeStyle(4, parseInt(characterData.color.replace('#', '0x')));
            })
            .on('pointerdown', () => {
                this.selectCharacter(characterData);
            });
        
        return card;
    }
    
    selectCharacter(characterData) {
        // 設置選擇的角色
        window.GameState.setPlayer(characterData);
        
        // 顯示確認動畫
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const confirmText = this.add.text(width / 2, height / 2, 
            `你選擇了 ${characterData.name}！`, 
            GameUtils.createTextStyle(48, '#FFEB3B', 'Arial')
        );
        confirmText.setOrigin(0.5);
        confirmText.setAlpha(0);
        
        this.tweens.add({
            targets: confirmText,
            alpha: 1,
            duration: 500,
            onComplete: () => {
                this.time.delayedCall(1000, () => {
                    this.scene.start('StoryScene');
                });
            }
        });
    }
    
    createBackButton() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const backButton = this.add.text(100, height - 60, '← 返回', 
            GameUtils.createTextStyle(24, '#FFFFFF', 'Arial')
        );
        backButton.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                backButton.setScale(1.1);
            })
            .on('pointerout', () => {
                backButton.setScale(1.0);
            })
            .on('pointerdown', () => {
                this.scene.start('StartScene');
            });
    }
}
