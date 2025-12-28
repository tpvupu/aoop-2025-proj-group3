/**
 * 角色類別
 * Character Class - 管理角色屬性和行為
 */

class Character {
    constructor(characterData, characterId = '') {
        // 基本屬性
        this.characterId = characterId; // 角色ID (bubu, yier, mitao, huihui)
        this.name = characterData.name;
        this.chineseName = characterData.name; // 中文名字
        this.intelligence = characterData.intelligence;
        this.mood = characterData.mood;
        this.energy = characterData.energy;
        this.social = characterData.social;
        this.description = characterData.description;
        this.color = characterData.color;
        
        // 學業相關
        this.knowledge = 0;
        this.midterm = 0;
        this.final = 0;
        this.totalScore = 0;
        this.gpa = 0;
        this.grade = 'F';
        
        // 遊戲進度
        this.weekNumber = 0;
        this.luckyProf = 3;
        
        // 記錄
        this.chosen = new Array(17).fill('0');
        this.lastWeekChange = [0, 0, 0, 0]; // [心情, 體力, 社交, 知識]
        this.eventHistory = {};
        this.weeklyAdvice = {};
    }
    
    /**
     * 讀書活動
     */
    study(degree = 1.0) {
        const growth = Math.round(
            this.intelligence * 0.14 +
            this.mood * 0.06 +
            this.social * 0.04 +
            this.energy * 0.06
        );
        
        const modifier = this.weekNumber < 8 
            ? 1 + (8 - this.weekNumber) * 0.1
            : 1 + (16 - this.weekNumber) * 0.1;
        
        const adjustedGrowth = Math.round(growth / modifier);
        
        this.lastWeekChange = [
            -Math.round(adjustedGrowth * 0.8 * degree),
            -Math.round(adjustedGrowth * 0.2 * degree),
            -Math.round(adjustedGrowth * 0.2 * degree),
            Math.round((adjustedGrowth + 1) * degree)
        ];
        
        this.applyChanges();
    }
    
    /**
     * 社交活動
     */
    socialize(degree = 1.0) {
        const growth = Math.round((100 - this.social) * 0.25);
        
        this.lastWeekChange = [
            Math.round(growth * 0.2 * degree),
            -Math.round(growth * 0.2 * degree),
            Math.round(growth * degree),
            Math.round(1 * degree)
        ];
        
        this.applyChanges();
    }
    
    /**
     * 玩遊戲活動
     */
    playGame(degree = 1.0) {
        const growth = Math.round((100 - this.mood) * 0.25);
        
        this.lastWeekChange = [
            Math.round(growth * degree),
            -Math.round(growth * 0.1 * degree),
            -Math.round(growth * 0.1 * degree),
            Math.round(1 * degree)
        ];
        
        this.applyChanges();
    }
    
    /**
     * 休息活動
     */
    rest(degree = 1.0) {
        const growth = Math.round((100 - this.energy) * 0.25);
        
        this.lastWeekChange = [
            Math.round(growth * 0.1 * degree),
            Math.round(growth * degree),
            -Math.round(growth * 0.2 * degree),
            Math.round(1 * degree)
        ];
        
        this.applyChanges();
    }
    
    /**
     * 應用屬性變化
     */
    applyChanges() {
        this.mood = GameUtils.clamp(this.mood + this.lastWeekChange[0], 0, 100);
        this.energy = GameUtils.clamp(this.energy + this.lastWeekChange[1], 0, 100);
        this.social = GameUtils.clamp(this.social + this.lastWeekChange[2], 0, 100);
        this.knowledge = GameUtils.clamp(this.knowledge + this.lastWeekChange[3], 0, 100);
    }
    
    /**
     * 計算成績
     */
    calculateGrade() {
        const score = Math.round(
            this.knowledge * 0.55 +
            this.mood * 0.2 +
            this.energy * 0.1 +
            this.intelligence * 0.2
        );
        
        return GameUtils.randomInt(score + 6, score + 10);
    }
    
    /**
     * 獲取期中考成績
     */
    getMidterm() {
        this.midterm = Math.round(this.calculateGrade() + this.knowledge * 0.25);
    }
    
    /**
     * 獲取期末考成績
     */
    getFinal() {
        this.final = Math.round(this.calculateGrade()) - 5;
    }
    
    /**
     * 計算最終 GPA
     */
    calculateGPA() {
        let totalScore = this.midterm * 0.40 + this.final * 0.40 + this.knowledge * 0.2;
        totalScore = Math.max(0, Math.round(Math.sqrt(totalScore) * 15.5 - 55));
        this.totalScore = totalScore;
        
        this.grade = GameUtils.calculateGrade(totalScore);
        this.gpa = GameUtils.calculateGPA(this.grade);
        
        return {
            score: this.totalScore,
            grade: this.grade,
            gpa: this.gpa
        };
    }
    
    /**
     * 增加一週
     */
    nextWeek() {
        this.weekNumber++;
    }
    
    /**
     * 獲取當前狀態
     */
    getStatus() {
        return {
            name: this.name,
            week: this.weekNumber,
            intelligence: this.intelligence,
            mood: this.mood,
            energy: this.energy,
            social: this.social,
            knowledge: this.knowledge,
            midterm: this.midterm,
            final: this.final,
            totalScore: this.totalScore,
            grade: this.grade,
            gpa: this.gpa
        };
    }
    
    /**
     * 記錄事件選擇
     */
    recordEvent(weekNumber, eventText, optionText, changes) {
        this.eventHistory[weekNumber] = {
            event: eventText,
            option: optionText,
            changes: changes,
            timestamp: new Date().toISOString()
        };
    }
    
    /**
     * 獲取事件歷史
     */
    getEventHistory() {
        return this.eventHistory;
    }
    
    /**
     * 重置角色（重新開始）
     */
    reset() {
        this.knowledge = 0;
        this.midterm = 0;
        this.final = 0;
        this.totalScore = 0;
        this.gpa = 0;
        this.grade = 'F';
        this.weekNumber = 0;
        this.luckyProf = 3;
        this.chosen = new Array(17).fill('0');
        this.lastWeekChange = [0, 0, 0, 0];
        this.eventHistory = {};
        this.weeklyAdvice = {};
    }
}
