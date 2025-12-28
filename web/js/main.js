/**
 * 主遊戲初始化
 * Main Game Entry Point
 */

// Phaser 遊戲配置
const phaserConfig = {
    type: Phaser.AUTO,
    width: GameConfig.width,
    height: GameConfig.height,
    parent: 'game-container',
    backgroundColor: '#667eea',
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    scene: [
        BootScene,
        PreloadScene,
        StartScene,
        IntroScene,
        CharacterSelectScene,
        StoryScene,
        MainScene,
        EventScene,
        DiaryScene,
        RankScene,
        EndScene
    ],
    physics: {
        default: 'arcade',
        arcade: {
            debug: false
        }
    }
};

// 全局遊戲實例
let game;

// 全局遊戲狀態管理
const GameState = {
    player: null,
    currentWeek: 0,
    bgmEnabled: true,
    sfxEnabled: true,
    eventsData: null,
    
    /**
     * 設置玩家
     */
    setPlayer(characterData) {
        this.player = new Character(characterData);
    },
    
    /**
     * 獲取玩家
     */
    getPlayer() {
        return this.player;
    },
    
    /**
     * 重置遊戲狀態
     */
    reset() {
        if (this.player) {
            this.player.reset();
        }
        this.currentWeek = 0;
    },
    
    /**
     * 載入事件數據
     */
    setEventsData(data) {
        this.eventsData = data;
    },
    
    /**
     * 獲取事件數據
     */
    getEventsData() {
        return this.eventsData;
    }
};

// 當 DOM 載入完成後初始化遊戲
window.addEventListener('load', () => {
    // 初始化 Phaser 遊戲
    game = new Phaser.Game(phaserConfig);
    
    // 將全局狀態掛載到 window 供場景使用
    window.GameState = GameState;
});

// 更新載入進度
function updateLoadingProgress(progress, text = '載入中...') {
    const loadingBarFill = document.getElementById('loading-bar-fill');
    const loadingText = document.getElementById('loading-text');
    
    if (loadingBarFill) {
        loadingBarFill.style.width = `${progress * 100}%`;
    }
    
    if (loadingText) {
        loadingText.textContent = text;
    }
}

// 隱藏載入畫面
function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }, 500);
    }
}

// 錯誤處理
window.addEventListener('error', (event) => {
    console.error('Game Error:', event.error);
    // 可以在這裡加入錯誤提示 UI
});

// 防止右鍵選單（可選）
document.addEventListener('contextmenu', (e) => {
    if (e.target.tagName === 'CANVAS') {
        e.preventDefault();
    }
});
