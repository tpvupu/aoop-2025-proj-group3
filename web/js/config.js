/**
 * 遊戲配置文件
 * Game Configuration
 */

const GameConfig = {
    // 屏幕尺寸
    width: 1200,
    height: 800,
    
    // 顏色配置
    colors: {
        intelligence: 0x87CEFA, // 淺藍
        mood: 0xFFB6C1,         // 粉紅
        energy: 0x90EE90,       // 淺綠
        social: 0xFFA500,       // 橘色
        knowledge: 0xDDA0DD     // 紫色
    },
    
    // 資源路徑
    paths: {
        images: '../resource/image/',
        sounds: '../resource/music/',
        fonts: '../resource/font/',
        gifs: '../resource/gif/',
        events: '../event/events.json'
    },
    
    // 遊戲週數
    totalWeeks: 16,
    midtermWeek: 8,
    finalWeek: 16,
    
    // 角色數據
    characters: {
        bubu: {
            name: '布布',
            intelligence: 65,
            mood: 80,
            energy: 60,
            social: 70,
            description: '活潑開朗的布布，總是充滿活力！',
            color: '#FFB6C1'
        },
        yier: {
            name: '一二',
            intelligence: 85,
            mood: 60,
            energy: 70,
            social: 55,
            description: '聰明認真的一二，學霸的代表。',
            color: '#87CEFA'
        },
        mitao: {
            name: '蜜桃',
            intelligence: 70,
            mood: 75,
            energy: 65,
            social: 80,
            description: '甜美可愛的蜜桃，人見人愛。',
            color: '#FFDAB9'
        },
        huihui: {
            name: '灰灰',
            intelligence: 75,
            mood: 70,
            energy: 75,
            social: 65,
            description: '穩重可靠的灰灰，全面發展。',
            color: '#D3D3D3'
        }
    },
    
    // 活動類型
    activities: {
        study: {
            name: '讀書',
            emoji: '📚',
            description: '專心學習，提升知識！'
        },
        socialize: {
            name: '社交',
            emoji: '🤝',
            description: '和朋友聚會，增進社交能力！'
        },
        play_game: {
            name: '玩遊戲',
            emoji: '🎮',
            description: '放鬆心情，享受遊戲時光！'
        },
        rest: {
            name: '休息',
            emoji: '💤',
            description: '好好休息，恢復體力！'
        }
    },
    
    // 音效音量
    audio: {
        bgmVolume: 0.5,
        sfxVolume: 0.7
    }
};

// 全局工具函數
const GameUtils = {
    /**
     * 限制數值範圍
     */
    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    },
    
    /**
     * 隨機整數
     */
    randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    
    /**
     * 格式化文字換行
     */
    wrapText(text, maxWidth) {
        const words = text.split('');
        const lines = [];
        let currentLine = '';
        
        for (let word of words) {
            if (currentLine.length < maxWidth) {
                currentLine += word;
            } else {
                lines.push(currentLine);
                currentLine = word;
            }
        }
        if (currentLine) {
            lines.push(currentLine);
        }
        
        return lines.join('\n');
    },
    
    /**
     * 計算 GPA 等級
     */
    calculateGrade(score) {
        if (score >= 90) return 'A+';
        if (score >= 85) return 'A';
        if (score >= 80) return 'A-';
        if (score >= 77) return 'B+';
        if (score >= 73) return 'B';
        if (score >= 70) return 'B-';
        if (score >= 67) return 'C+';
        if (score >= 63) return 'C';
        if (score >= 60) return 'C-';
        return 'F';
    },
    
    /**
     * 計算 GPA 數值
     */
    calculateGPA(grade) {
        const gpaMap = {
            'A+': 4.3, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'F': 0.0
        };
        return gpaMap[grade] || 0.0;
    },
    
    /**
     * 創建文字樣式
     */
    createTextStyle(size, color = '#FFFFFF', fontFamily = 'Arial') {
        return {
            fontSize: `${size}px`,
            fill: color,
            fontFamily: fontFamily,
            align: 'center',
            stroke: '#000000',
            strokeThickness: 3
        };
    }
};
