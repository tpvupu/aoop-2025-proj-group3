/**
 * 角色選擇場景
 * Character Select Scene - 模仿 Pygame 版本的四角布局
 */

class CharacterSelectScene extends Phaser.Scene {
    constructor() {
        super({ key: 'CharacterSelectScene' });
        this.animationSpeed = 150; // 每幀持續時間（毫秒）
        this.cards = [];
        this.frameCount = {
            bubu: 8,
            yier: 14,
            mitao: 12,
            huihui: 12
        };
    }
    
    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 背景圖片
        if (this.textures.exists('background_intro')) {
            const bg = this.add.image(width / 2, height / 2, 'background_intro');
            const scale = Math.max(width / bg.width, height / bg.height);
            bg.setScale(scale);
        } else {
            // 備選背景
            const graphics = this.add.graphics();
            graphics.fillGradientStyle(0xC8D4E8, 0xC8D4E8, 0xE8D4B8, 0xE8D4B8, 1);
            graphics.fillRect(0, 0, width, height);
        }
        
        // 標題
        const title = this.add.text(width / 2, 20, '選擇你的角色', 
            {
                fontSize: '40px',
                fill: '#000000',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            }
        );
        title.setOrigin(0.5, 0);
        
        // 卡片配置 - 根據 Pygame 版本的比例設置
        // Pygame: 屏幕 1200x800, 卡片 500x300, margin 30
        const cardWidth = width * (500 / 1200);      // 41.67% of width
        const cardHeight = height * (300 / 800);     // 37.5% of height
        const marginX = width * (30 / 1200);         // 2.5% of width
        const marginY = height * (30 / 800);         // 3.75% of height
        
        const cardConfigs = [
            {
                charKey: 'bubu',
                x: marginX + cardWidth / 2,
                y: marginY + cardHeight / 2,
                description: "大家好～我是布布！\n我喜歡在網路上盡情地打遊戲！\n希望這學期所有的課都可以過"
            },
            {
                charKey: 'yier',
                x: width - marginX - cardWidth / 2,
                y: marginY + cardHeight / 2,
                description: "大家好～我是一二！\n我熱衷於系上活動以及社團～\n認識好多學長姐嘿嘿～"
            },
            {
                charKey: 'mitao',
                x: marginX + cardWidth / 2,
                y: height - marginY - cardHeight / 2,
                description: "大家好～我是蜜桃！\n嗚嗚嗚這學期不小心選太多課...\n現在實在是捲不動了～"
            },
            {
                charKey: 'huihui',
                x: width - marginX - cardWidth / 2,
                y: height - marginY - cardHeight / 2,
                description: "大家好～我是灰灰！\n我正在追求自己真正想做的事！\n重要的是追尋我的快樂貓生！"
            }
        ];
        
        // 創建所有卡片
        cardConfigs.forEach(config => {
            const card = this.createCharacterCard(
                config.x,
                config.y,
                GameConfig.characters[config.charKey],
                cardWidth,
                cardHeight,
                config.description,
                config.charKey
            );
            this.cards.push(card);
        });
        
        // 啟動動畫更新循環
        this.time.addEvent({
            delay: this.animationSpeed,
            loop: true,
            callback: this.updateAnimation,
            callbackScope: this
        });
    }
    
    updateAnimation() {
        // 更新所有卡片的動畫幀
        this.cards.forEach(cardData => {
            if (cardData.animImage) {
                const maxFrames = this.frameCount[cardData.charKey];
                // 每張卡片有自己的幀索引
                cardData.frameIndex = (cardData.frameIndex + 1) % maxFrames;
                const nextFrameKey = `${cardData.charKey}_intro_${cardData.frameIndex}`;
                
                if (this.textures.exists(nextFrameKey)) {
                    cardData.animImage.setTexture(nextFrameKey);
                }
            }
        });
    }
    
    createCharacterCard(x, y, characterData, cardWidth, cardHeight, description, charKey) {
        const card = this.add.container(x, y);
        const cardData = { charKey, animImage: null, container: card, frameIndex: 0 };
        
        // 卡片背景 - 白色半透明，邊框有顏色
        const bg = this.add.rectangle(0, 0, cardWidth, cardHeight, 0xFFFFFF, 0.92);
        const borderColor = parseInt(characterData.color.replace('#', '0x'));
        bg.setStrokeStyle(6, borderColor);
        
        // 左上角：描述文字
        const descText = this.add.text(
            -cardWidth / 2 + 20,
            -cardHeight / 2 + 20,
            description,
            {
                fontSize: '28px',
                fill: '#646464',
                fontFamily: 'JasonHandwriting3, Arial, sans-serif',
                wordWrap: { width: cardWidth - 180 },
                lineSpacing: 8
            }
        );
        descText.setOrigin(0, 0);
        
        // 左下角：角色名稱
        const nameText = this.add.text(
            -cardWidth / 2 + 20,
            cardHeight / 2 - 40,
            characterData.name,
            {
                fontSize: '36px',
                fill: '#323232',
                fontFamily: 'JasonHandwriting3, Arial, sans-serif',
                fontStyle: 'bold'
            }
        );
        nameText.setOrigin(0, 0.5);
        
        // 右下角：角色動畫
        const animImage = this.add.image(
            cardWidth / 2 - 70,
            cardHeight / 2 - 50,
            `${charKey}_intro_0`
        );
        // 調整動畫圖片大小和位置 - 約 140x140 像素
        animImage.setScale(0.19);
        animImage.setOrigin(0.5, 0.5);
        
        cardData.animImage = animImage;
        
        card.add([bg, descText, nameText, animImage]);
        
        // 互動效果
        const originalStroke = borderColor;
        const hoverStroke = this.hexToRgb(characterData.color);
        const hoverColor = Phaser.Display.Color.GetColor(
            Math.max(0, hoverStroke.r - 80),
            Math.max(0, hoverStroke.g - 80),
            Math.max(0, hoverStroke.b - 80)
        );
        
        bg.setInteractive({ useHandCursor: true })
            .on('pointerover', () => {
                // 邊框顏色變深
                bg.setStrokeStyle(6, hoverColor);
                // 輕微縮放
                this.tweens.add({
                    targets: card,
                    scale: 1.02,
                    duration: 150
                });
                // 播放音效
                if (this.sound.context.state !== 'suspended') {
                    try {
                        if (this.sound.isPlaying('sfx_menu_hover')) {
                            this.sound.stopByKey('sfx_menu_hover');
                        }
                        this.sound.play('sfx_menu_hover', { volume: 0.3 });
                    } catch (e) {
                        console.log('音效播放失敗');
                    }
                }
            })
            .on('pointerout', () => {
                // 邊框顏色恢復
                bg.setStrokeStyle(6, originalStroke);
                // 縮放恢復
                this.tweens.add({
                    targets: card,
                    scale: 1.0,
                    duration: 150
                });
            })
            .on('pointerdown', () => {
                this.selectCharacter(characterData);
            });
        
        return cardData;
    }
    
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : { r: 255, g: 255, b: 255 };
    }
    
    
    selectCharacter(characterData) {
        // 設置選擇的角色
        window.GameState.setPlayer(characterData);
        
        // 顯示確認動畫
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const confirmText = this.add.text(width / 2, height / 2, 
            `你選擇了 ${characterData.name}！`, 
            {
                fontSize: '48px',
                fill: '#FFEB3B',
                fontFamily: 'JasonHandwriting3, Arial, sans-serif',
                fontStyle: 'bold'
            }
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
}
