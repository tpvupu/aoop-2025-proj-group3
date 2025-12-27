import os


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
# -----------------------------------------------------------------------------
# 資源路徑 (Asset Paths)
# -----------------------------------------------------------------------------
# 基本目錄路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 資源目錄
RESOURCE_DIR = os.path.join(BASE_DIR, 'resource')

# 各類子資源目錄
IMAGE_DIR = os.path.join(RESOURCE_DIR, 'image')
FONT_DIR = os.path.join(RESOURCE_DIR, 'font')
MUSIC_DIR = os.path.join(RESOURCE_DIR, 'music')
GIF_DIR = os.path.join(RESOURCE_DIR, 'gif')

# 字體路徑
JFONT_PATH_BOLD = os.path.join(FONT_DIR, 'JasonHandwriting3-SemiBold.ttf')
JFONT_PATH_REGULAR = os.path.join(FONT_DIR, 'JasonHandwriting3-Regular.ttf')
JFONT_PATH_Light = os.path.join(FONT_DIR, 'JasonHandwriting3-Light.ttf')
HFONT_PATH = os.path.join(FONT_DIR, 'hanyizhuziguozhiruantang.ttf')
CFONT_PATH = os.path.join(FONT_DIR, 'ChenYuluoyan-Thin-Monospaced.ttf')
MFONT_PATH = os.path.join(FONT_DIR, 'MoreSugar-Regular.ttf')

# 背景音樂路徑

class BGM:
    BGM_PATH = os.path.join(MUSIC_DIR, 'bgm')
    DRUMDRUM_PATH = os.path.join(BGM_PATH, 'drumdrum.ogg')
    MITAO_HUIHUI_PATH = os.path.join(BGM_PATH, 'mitao_huihui.ogg')
    YIER_BUBU_PATH = os.path.join(BGM_PATH, 'yier_bubu.ogg')

# 音效路徑
class SoundEffect:
    """音效類別，包含各種音效的路徑"""
    SOUND_PATH = os.path.join(MUSIC_DIR, 'sound_effect')
    BLING_PATH = os.path.join(SOUND_PATH, 'bling.ogg')
    BO_PATH = os.path.join(SOUND_PATH, 'bo.ogg')
    CHEER_CHEER_PATH = os.path.join(SOUND_PATH, 'cheer_cheer.ogg')
    DONG_PATH = os.path.join(SOUND_PATH, 'dong.ogg')
    DONGDONG_PATH = os.path.join(SOUND_PATH, 'dongdong.ogg')
    LUCKYWHEEL_PATH = os.path.join(SOUND_PATH, 'luckywheel.ogg')
    MENU_HOVER_PATH = os.path.join(SOUND_PATH, 'menu_hover.ogg')
    NEXT_PAGE_PATH = os.path.join(SOUND_PATH, 'next_page.ogg')
    SHOU_PATH = os.path.join(SOUND_PATH, 'shou.ogg')
    SHOU2_PATH = os.path.join(SOUND_PATH, 'shou2.ogg')
    SMALL_DRUM_PATH = os.path.join(SOUND_PATH, 'small_drum.ogg')
    TYPING_PATH = os.path.join(SOUND_PATH, 'typing.ogg')


# Image 路徑
class ImagePath:
    BACK_PATH = os.path.join(IMAGE_DIR, 'back.png')
    LEFT_PATH = os.path.join(IMAGE_DIR, 'left.png')
    RIGHT_PATH = os.path.join(IMAGE_DIR, 'right.png')
    BACKGROUND_PATH = os.path.join(IMAGE_DIR, 'background_intro.png')
    BUTTON_PATH = os.path.join(IMAGE_DIR, 'button.png')
    SET_PAGE_PATH = os.path.join(IMAGE_DIR, 'set_page.png')
    SET_PATH =  os.path.join(IMAGE_DIR, 'set.png')

    BUBU_HEAD_PATH = os.path.join(IMAGE_DIR, 'Bubu_head.png')
    YIER_HEAD_PATH = os.path.join(IMAGE_DIR, 'Yier_head.png')
    MITAO_HEAD_PATH = os.path.join(IMAGE_DIR, 'Mitao_head.png')
    HUIHUI_HEAD_PATH = os.path.join(IMAGE_DIR, 'Huihui_head.png')

    EVENT_ICON_PATH = os.path.join(IMAGE_DIR, 'event_icon.PNG')
    EVENT_WINDOW_PATH = os.path.join(IMAGE_DIR, 'event_window.PNG')
    EVENT_BUBU_PATH = os.path.join(IMAGE_DIR, 'event_window_bubu.PNG')
    EVENT_YIER_PATH = os.path.join(IMAGE_DIR, 'event_window_yier.PNG')
    EVENT_MITAO_PATH = os.path.join(IMAGE_DIR, 'event_window_mitao.PNG')
    EVENT_HUIHUI_PATH = os.path.join(IMAGE_DIR, 'event_window_huihui.PNG')

    SAD_W_PATH = os.path.join(IMAGE_DIR, 'sad_white.png')
    SAD_PATH = os.path.join(IMAGE_DIR, 'sad.png')
    
    HAPPY_W_PATH = os.path.join(IMAGE_DIR, 'happy_white.png')
    HAPPY_PATH = os.path.join(IMAGE_DIR, 'happy.png')
    
    LIGHTENING_PATH = os.path.join(IMAGE_DIR, 'lightening.png')
    LIGHTENING_W_PATH = os.path.join(IMAGE_DIR, 'lightening_white.png')
    
    ROCKET_PATH = os.path.join(IMAGE_DIR, 'rocket.png')
    ROCKET_W_PATH = os.path.join(IMAGE_DIR, 'rocket_white.png')
    
    KISS_PATH = os.path.join(IMAGE_DIR, 'kiss.png')
    KISS_W_PATH = os.path.join(IMAGE_DIR, 'kiss_white.png')
    
    HEART_PATH = os.path.join(IMAGE_DIR, 'heart.png')
    HEART_W_PATH = os.path.join(IMAGE_DIR, 'heart_white.png')
    
    HEHE_PATH = os.path.join(IMAGE_DIR, 'hehe.png')
    HEHE_W_PATH = os.path.join(IMAGE_DIR, 'hehe_white.png')

    ANGRY_PATH = os.path.join(IMAGE_DIR, 'angry.png')
    ANGRY_W_PATH = os.path.join(IMAGE_DIR, 'angry_white.png')

    FEEDBACK_PATH = os.path.join(IMAGE_DIR, 'game_UI', 'feedback_qr.png')
    FIRST_SCENE_PATH = os.path.join(IMAGE_DIR, 'game_UI', 'first_scene.png')

    DIARY_IMG_PATH = os.path.join(IMAGE_DIR, 'diary_image.png')
    NOTEBOOK_PATH = os.path.join(IMAGE_DIR, 'notebook.png')
    YES_NO_IMG_PATH = os.path.join(IMAGE_DIR, 'yes_no_button.jpeg')



# 重要檔案路徑
SIMULATION_PLOTS_DIR = os.path.join(BASE_DIR, 'simulation_plots')

# Result 
GPA_HIGHLIGHT_PATH = os.path.join(SIMULATION_PLOTS_DIR, 'gpa_highlight.png')
TOTAL_SCORE_HIGHLIGHT_PATH = os.path.join(SIMULATION_PLOTS_DIR, 'total_highlight.png')
# Midterm & Final
MIDTERM_FINAL_HIGHLIGHT_PATH = os.path.join(SIMULATION_PLOTS_DIR, 'midterm_final_highlight.png')

EVENT_DIR = os.path.join(BASE_DIR, 'event')
EVENTS_JSON_PATH = os.path.join(EVENT_DIR, 'events.json')



# 自動取得所有 GIF 路徑
GIF_PATHS = {}
for fname in os.listdir(GIF_DIR):
    if fname.lower().endswith('_frames') and os.path.isdir(os.path.join(GIF_DIR, fname)):
        key = fname.upper() 
        GIF_PATHS[key] = os.path.join(GIF_DIR, fname)

# 你可以這樣使用：
# from setting import GIF_PATHS
# print(GIF_PATHS['BUBU_CRYING_FRAMES'])