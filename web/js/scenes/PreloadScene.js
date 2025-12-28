/**
 * 資源載入場景
 * Preload Scene - Load Game Assets
 */

class PreloadScene extends Phaser.Scene {
    constructor() {
        super({ key: 'PreloadScene' });
    }
    
    preload() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        // 創建載入畫面
        this.createLoadingScreen(width, height);
        
        // 載入 JSON 數據
        this.loadJSON();
        
        // 載入圖片資源（需根據實際檔案調整）
        this.loadImages();
        
        // 載入音效（需根據實際檔案調整）
        this.loadAudio();
        
        // 更新載入進度
        this.load.on('progress', (value) => {
            this.progressBar.clear();
            this.progressBar.fillStyle(0x00f2fe, 1);
            this.progressBar.fillRect(width / 2 - 150, height / 2, 300 * value, 10);
            
            this.loadingText.setText(`載入中... ${Math.floor(value * 100)}%`);
            
            // 同步更新 HTML 載入畫面
            updateLoadingProgress(value, `載入中... ${Math.floor(value * 100)}%`);
        });
        
        this.load.on('complete', () => {
            this.loadingText.setText('載入完成！');
            updateLoadingProgress(1, '載入完成！');
        });
    }
    
    create() {
        // 隱藏 HTML 載入畫面
        hideLoadingScreen();
        
        // 前往第一個遊戲場景
        this.time.delayedCall(500, () => {
            this.scene.start('FirstScene');
        });
    }
    
    createLoadingScreen(width, height) {
        // 背景
        this.add.rectangle(width / 2, height / 2, width, height, 0x667eea);
        
        // 遊戲標題
        const title = this.add.text(width / 2, height / 2 - 150, '今天的我也想耍廢', {
            fontSize: '48px',
            fill: '#ffffff',
            fontFamily: 'Arial',
            fontStyle: 'bold'
        });
        title.setOrigin(0.5);
        
        const subtitle = this.add.text(width / 2, height / 2 - 100, 'Lazy Me Today Too', {
            fontSize: '28px',
            fill: '#ffffff',
            fontFamily: 'Arial'
        });
        subtitle.setOrigin(0.5);
        
        // 進度條背景
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(width / 2 - 160, height / 2 - 10, 320, 30);
        
        // 進度條
        this.progressBar = this.add.graphics();
        
        // 載入文字
        this.loadingText = this.add.text(width / 2, height / 2 + 50, '載入中...', {
            fontSize: '24px',
            fill: '#ffffff',
            fontFamily: 'Arial'
        });
        this.loadingText.setOrigin(0.5);
    }
    
    loadJSON() {
        // 載入事件數據
        // 注意：需要將 events.json 放到 web 目錄下可訪問的位置
        // 或者直接在這裡內嵌數據
        
        // 臨時：創建模擬數據
        const mockEventsData = this.createMockEventsData();
        window.GameState.setEventsData(mockEventsData);
    }
    
    loadImages() {
        // 載入 UI 圖片
        this.load.image('bubu_head', 'assets/images/Bubu_head.png');
        this.load.image('yier_head', 'assets/images/Yier_head.png');
        this.load.image('mitao_head', 'assets/images/Mitao_head.png');
        this.load.image('huihui_head', 'assets/images/Huihui_head.png');
        
        // 載入情感表情
        this.load.image('emoji_happy', 'assets/images/happy.png');
        this.load.image('emoji_sad', 'assets/images/sad.png');
        this.load.image('emoji_angry', 'assets/images/angry.png');
        this.load.image('emoji_heart', 'assets/images/heart.png');
        
        // 載入按鈕和 UI
        this.load.image('notebook', 'assets/images/notebook.png');
        this.load.image('set_icon', 'assets/images/set.png');
        this.load.image('event_icon', 'assets/images/event_icon.PNG');
        
        // 載入背景
        this.load.image('background_intro', 'assets/images/background_intro.png');
        
        // 載入角色選擇場景的 intro 動畫幀
        const frameCount = {
            bubu: 8,
            yier: 14,
            mitao: 12,
            huihui: 12
        };
        
        Object.keys(frameCount).forEach(charKey => {
            for (let i = 0; i < frameCount[charKey]; i++) {
                this.load.image(`${charKey}_intro_${i}`, `assets/gifs/${charKey}_intro_frames/frame_${i}.png`);
            }
        });
    }
    
    loadAudio() {
        // 載入背景音樂
        try {
            const bgmPath = 'assets/sounds/bgm/';
            this.load.audio('bgm_drumdrum', bgmPath + 'drumdrum.ogg');
            this.load.audio('bgm_yier_bubu', bgmPath + 'yier_bubu.ogg');
            this.load.audio('bgm_mitao_huihui', bgmPath + 'mitao_huihui.ogg');
        } catch (e) {
            console.log('BGM 載入失敗');
        }
        
        // 載入音效
        try {
            const sfxPath = 'assets/sounds/sound_effect/';
            this.load.audio('sfx_bling', sfxPath + 'bling.ogg');
            this.load.audio('sfx_bo', sfxPath + 'bo.ogg');
            this.load.audio('sfx_dong', sfxPath + 'dong.ogg');
            this.load.audio('sfx_menu_hover', sfxPath + 'menu_hover.ogg');
        } catch (e) {
            console.log('音效載入失敗');
        }
    }
    
    createMockEventsData() {
        // 創建模擬事件數據
        const mockData = {};
        
        for (let week = 1; week <= 16; week++) {
            if (week === 8 || week === 16) {
                // 考試週
                mockData[week] = {
                    event: week === 8 ? '期中考試週到了！' : '期末考試週到了！',
                    options: []
                };
            } else {
                // 普通週
                mockData[week] = {
                    event: `第 ${week} 週：你遇到了一些選擇...`,
                    options: [
                        {
                            text: '專心讀書準備考試',
                            changes: { mood: -10, energy: -5, social: -5, knowledge: 15 },
                            activity: 'study'
                        },
                        {
                            text: '和朋友出去玩',
                            changes: { mood: 15, energy: -5, social: 15, knowledge: 2 },
                            activity: 'socialize'
                        },
                        {
                            text: '在宿舍打遊戲',
                            changes: { mood: 15, energy: -3, social: -3, knowledge: 2 },
                            activity: 'play_game'
                        },
                        {
                            text: '好好休息恢復體力',
                            changes: { mood: 5, energy: 15, social: -5, knowledge: 2 },
                            activity: 'rest'
                        }
                    ]
                };
            }
        }
        
        return mockData;
    }
}
