import pygame
import sys
from math import cos, sin, radians, atan2 
import random 

# Pygame'i başlat
pygame.init()

# ----------------- BOYUTLANDIRMA VE KONUM FAKTÖRLERİ -----------------
BOYUT_FAKTORU = 1.6 

# Ekran boyutları
EKRAN_GENISLIK = 800
EKRAN_YUKSEKLIK = 480 
ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
pygame.display.set_caption("Undertale Projesi") # Pencere başlığı da güncellendi

# Renkler
KIRMIZI_GUC = (255, 0, 0)     
MAVI_CAN = (0, 255, 255)      
YESIL_IYI = (0, 200, 0)       
TURUNCU = (255, 165, 0)       
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
SARI_UYARI = (255, 255, 0) 
KIRMIZI_PATLAMA = (200, 0, 0) 
GRI = (100, 100, 100)
MORA_YAKIN = (100, 0, 200)

# FONT Ayarı
pygame.font.init()
font_kucuk = pygame.font.SysFont(None, int(24 * BOYUT_FAKTORU)) 
font_buyuk = pygame.font.SysFont(None, int(30 * BOYUT_FAKTORU)) 
font_dpad = pygame.font.SysFont(None, int(40 * BOYUT_FAKTORU)) 
font_uyari = pygame.font.SysFont(None, int(80 * BOYUT_FAKTORU), bold=True) 

# ----------------- OYUN DURUMLARI -----------------
START_SCREEN = -2   # Oyna tuşunun olduğu başlangıç ekranı
COMMAND_PHASE = 0
ATTACK_PHASE = 1
GAME_OVER = 2       
GAME_WON = 3        

game_state = START_SCREEN 

# ----------------- OYUN DEĞİŞKENLERİ -----------------
ruh_boyut = int(15 * BOYUT_FAKTORU) 
ruh_hiz = 6
dusman_hp = 200 
oyuncu_hp = 100
oyuncu_adi = "OYUNCU" # Yeni: Adımız artık sabit 'OYUNCU'
show_player_attack_button = False 

# Saldırı değişkenlerinin başlangıçta tanımlanması (Hata giderme için önemli)
current_attack_type = None
active_attack_objects = [] 
attack_sequence = [1, 2, 3] 
current_attack_index = 0
attack_start_time = 0
attack_duration_ms = 2000 
warning_duration_ms = 1000 
area_attack_side = None 
laser_blast_object = None
warning_timer = 0


# Savaş Kutusu Ayarları
KUTU_GENISLIK = int(300 * BOYUT_FAKTORU)
KUTU_YUKSEKLIK = int(120 * BOYUT_FAKTORU)
KUTU_X = int(50 / BOYUT_FAKTORU)
KUTU_Y = EKRAN_YUKSEKLIK // 2 - KUTU_YUKSEKLIK // 2 
KUTU_KALINLIK = 3 
ruh_x = KUTU_X + (KUTU_GENISLIK - ruh_boyut) // 2
ruh_y = KUTU_Y + (KUTU_YUKSEKLIK - ruh_boyut) // 2

# Büyük Düşman Kare
BUYUK_DUSMAN_BOYUT = int(80 * BOYUT_FAKTORU)
BUYUK_DUSMAN_X = KUTU_X + (KUTU_GENISLIK // 2) - (BUYUK_DUSMAN_BOYUT // 2)
BUYUK_DUSMAN_Y = KUTU_Y - BUYUK_DUSMAN_BOYUT - 20 

# Komut Düğmeleri Ayarları
BUTON_YUKSEKLIK = int(40 * BOYUT_FAKTORU)
KOMUT_ARALIK = 10 
BUTON_GENISLIK = 80 
KOMUT_Y = EKRAN_YUKSEKLIK - BUTON_YUKSEKLIK - KOMUT_ARALIK 

# Komut Tuşlarının X konumu: Sağ alta hizalandı
DPAD_MERKEZ_X = EKRAN_GENISLIK - int(60 * BOYUT_FAKTORU) - int(20 * BOYUT_FAKTORU)
KOMUT_BASLANGIC_X = DPAD_MERKEZ_X - (BUTON_GENISLIK * 3) - (KOMUT_ARALIK * 3) + 30 

ATTACK_RECT = pygame.Rect(KOMUT_BASLANGIC_X, KOMUT_Y, BUTON_GENISLIK, BUTON_YUKSEKLIK)
MEDIC_RECT = pygame.Rect(KOMUT_BASLANGIC_X + BUTON_GENISLIK + KOMUT_ARALIK, KOMUT_Y, BUTON_GENISLIK, BUTON_YUKSEKLIK)
RUN_RECT = pygame.Rect(KOMUT_BASLANGIC_X + 2 * (BUTON_GENISLIK + KOMUT_ARALIK), KOMUT_Y, BUTON_GENISLIK, BUTON_YUKSEKLIK)

# Oyuncu Saldırı Tuşu 
PLAYER_ATTACK_RECT = pygame.Rect(KUTU_X + KUTU_GENISLIK // 4, KUTU_Y + KUTU_YUKSEKLIK // 4, KUTU_GENISLIK // 2, KUTU_YUKSEKLIK // 2)

# D-Pad (Joystick) Ayarları
OK_BOYUT = int(60 * BOYUT_FAKTORU)    
OK_ARALIK = int(20 * BOYUT_FAKTORU)   
DPAD_MERKEZ_X = EKRAN_GENISLIK - OK_BOYUT - OK_ARALIK 
DPAD_MERKEZ_Y = EKRAN_YUKSEKLIK - OK_BOYUT - OK_ARALIK 
UP_RECT = pygame.Rect(DPAD_MERKEZ_X - OK_BOYUT // 2, DPAD_MERKEZ_Y - OK_BOYUT - OK_ARALIK, OK_BOYUT, OK_BOYUT)
DOWN_RECT = pygame.Rect(DPAD_MERKEZ_X - OK_BOYUT // 2, DPAD_MERKEZ_Y + OK_ARALIK, OK_BOYUT, OK_BOYUT)
LEFT_RECT = pygame.Rect(DPAD_MERKEZ_X - OK_BOYUT - OK_ARALIK, DPAD_MERKEZ_Y - OK_BOYUT // 2, OK_BOYUT, OK_BOYUT)
RIGHT_RECT = pygame.Rect(DPAD_MERKEZ_X + OK_ARALIK, DPAD_MERKEZ_Y - OK_BOYUT // 2, OK_BOYUT, OK_BOYUT)

# Oyun Sonu ve Başlangıç Tuşları
RESTART_RECT = pygame.Rect(EKRAN_GENISLIK // 2 - 100, EKRAN_YUKSEKLIK // 2 + 150, 200, 50) # Konum güncellendi
PLAY_RECT = pygame.Rect(EKRAN_GENISLIK // 2 - 100, EKRAN_YUKSEKLIK // 2, 200, 50) 

# ----------------- SALDIRI SINIFLARI (Aynı Kaldı) -----------------
class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x; self.y = start_y; self.size = int(8 * BOYUT_FAKTORU); self.color = KIRMIZI_GUC
        self.speed = 5; self.active = True
        angle = atan2(target_y - start_y, target_x - start_x); self.dx = cos(angle) * self.speed; self.dy = sin(angle) * self.speed
    def update(self):
        if not self.active: return
        self.x += self.dx; self.y += self.dy
        if self.x < KUTU_X - 50 or self.x > KUTU_X + KUTU_GENISLIK + 50 or self.y < KUTU_Y - 50 or self.y > KUTU_Y + KUTU_YUKSEKLIK + 50:
            self.active = False
    def draw(self):
        if self.active: pygame.draw.rect(ekran, self.color, (self.x, self.y, self.size, self.size))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size) if self.active else None

class LaserBlast:
    def __init__(self, target_pos):
        self.blaster_size = int(50 * BOYUT_FAKTORU); self.blaster_color = BEYAZ
        self.x = KUTU_X + KUTU_GENISLIK // 2 - self.blaster_size // 2; self.y = KUTU_Y - self.blaster_size - 10
        self.active = True; self.target_time = pygame.time.get_ticks() + 1000 
        self.fired = False; self.laser_hit_time = 0; self.target_line = target_pos 
        self.laser_thickness = int(15 * BOYUT_FAKTORU) 
        blaster_center = (self.x + self.blaster_size // 2, self.y + self.blaster_size // 2)
        self.angle = atan2(self.target_line[1] - blaster_center[1], self.target_line[0] - blaster_center[0])
    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.fired and current_time > self.target_time:
            self.fired = True; self.laser_hit_time = current_time + 500 
        if self.fired and current_time > self.laser_hit_time: self.active = False
    def draw(self):
        if not self.active: return
        pygame.draw.rect(ekran, self.blaster_color, (self.x + 5, self.y + 5, self.blaster_size-10, self.blaster_size-10))
        pygame.draw.rect(ekran, self.blaster_color, (self.x, self.y, self.blaster_size, self.blaster_size), 3)
        if self.fired and pygame.time.get_ticks() < self.laser_hit_time:
            blaster_center = (self.x + self.blaster_size // 2, self.y + self.blaster_size // 2)
            extension_length = 1000 
            end_x = blaster_center[0] + cos(self.angle) * extension_length
            end_y = blaster_center[1] + sin(self.angle) * extension_length
            pygame.draw.line(ekran, KIRMIZI_GUC, blaster_center, (end_x, end_y), self.laser_thickness)

# ----------------- YARDIMCI VE SIFIRLAMA FONKSİYONLARI -----------------

def draw_dpad_button(rect, text):
    pygame.draw.rect(ekran, MAVI_CAN, rect, 2) 
    text_surface = font_dpad.render(text, True, MAVI_CAN)
    text_rect = text_surface.get_rect(center=rect.center)
    ekran.blit(text_surface, text_rect)

def get_area_attack_rect(side):
    if side == 'LEFT':
        return pygame.Rect(KUTU_X, KUTU_Y, KUTU_GENISLIK / 2, KUTU_YUKSEKLIK)
    elif side == 'RIGHT':
        return pygame.Rect(KUTU_X + KUTU_GENISLIK / 2, KUTU_Y, KUTU_GENISLIK / 2, KUTU_YUKSEKLIK)
    return pygame.Rect(0, 0, 0, 0)

# Oyun sıfırlama fonksiyonu (Oyunu COMMAND_PHASE'e başlatır)
def reset_game_state(new_state):
    global game_state, dusman_hp, oyuncu_hp, show_player_attack_button, current_attack_index, active_attack_objects, current_attack_type, laser_blast_object
    
    game_state = new_state
    dusman_hp = 200
    oyuncu_hp = 100
    show_player_attack_button = False
    current_attack_index = 0
    active_attack_objects = []
    current_attack_type = None 
    laser_blast_object = None

# ----------------- SALDIRI YÖNETİMİ -----------------

def start_attack_sequence(damage=0):
    global game_state, current_attack_index, active_attack_objects, dusman_hp, show_player_attack_button
    
    if dusman_hp > 0 and damage > 0:
        dusman_hp = max(0, dusman_hp - damage) 

    if dusman_hp <= 0:
        game_state = GAME_WON
        return
        
    game_state = ATTACK_PHASE
    current_attack_index = 0
    active_attack_objects = []
    show_player_attack_button = False 
    start_next_attack()

def start_next_attack():
    global current_attack_type, attack_start_time, current_attack_index, warning_timer, area_attack_side, laser_blast_object
    
    if current_attack_index >= len(attack_sequence):
        end_attack_phase()
        return

    current_attack_type = attack_sequence[current_attack_index]
    attack_start_time = pygame.time.get_ticks()
    
    global active_attack_objects, laser_blast_object
    active_attack_objects = []
    laser_blast_object = None

    if current_attack_type == 2:
        import random
        warning_timer = pygame.time.get_ticks()
        area_attack_side = random.choice(['LEFT', 'RIGHT'])
    
    if current_attack_type == 3:
        player_target_pos = (ruh_x + ruh_boyut // 2, ruh_y + ruh_boyut // 2)
        laser_blast_object = LaserBlast(player_target_pos)

def end_attack_phase():
    global game_state, current_attack_type, active_attack_objects, show_player_attack_button
    game_state = ATTACK_PHASE 
    current_attack_type = None
    active_attack_objects = []
    show_player_attack_button = True 

# ----------------- ANA OYUN DÖNGÜSÜ -----------------

calisiyor = True
saat = pygame.time.Clock()

while calisiyor:
    
    current_time = pygame.time.get_ticks()
    ruh_rect = pygame.Rect(ruh_x, ruh_y, ruh_boyut, ruh_boyut)

    move_up, move_down, move_left, move_right = False, False, False, False
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    
    # 1. Olayları İşleme (Kullanıcı Girişleri)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calisiyor = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos 
            
            if game_state == START_SCREEN:
                if PLAY_RECT.collidepoint(pos):
                    reset_game_state(COMMAND_PHASE)
            
            elif game_state == COMMAND_PHASE:
                # Ana komut düğmeleri
                if ATTACK_RECT.collidepoint(pos):
                    start_attack_sequence(damage=0) 
                if MEDIC_RECT.collidepoint(pos):
                    oyuncu_hp = min(100, oyuncu_hp + 10) 
                    start_attack_sequence(damage=0) 
                if RUN_RECT.collidepoint(pos):
                    start_attack_sequence(damage=0)
            
            elif game_state == ATTACK_PHASE and show_player_attack_button:
                 # Oyuncu Saldırı Tuşu
                 if PLAYER_ATTACK_RECT.collidepoint(pos):
                     if dusman_hp > 0:
                        start_attack_sequence(damage=10) # 10 hasar ver
            
            elif game_state == GAME_OVER or game_state == GAME_WON:
                if RESTART_RECT.collidepoint(pos):
                    reset_game_state(COMMAND_PHASE) # Oyunu sıfırla ve COMMAND_PHASE'e başlat

    # 2. Oyun Mantığını Güncelleme 
    if game_state == ATTACK_PHASE:
        # Ruh Hareketi Mantığı
        if mouse_buttons[0]: 
            if UP_RECT.collidepoint(mouse_pos): move_up = True
            if DOWN_RECT.collidepoint(mouse_pos): move_down = True
            if LEFT_RECT.collidepoint(mouse_pos): move_left = True
            if RIGHT_RECT.collidepoint(mouse_pos): move_right = True
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: move_left = True
        if keys[pygame.K_RIGHT]: move_right = True
        if keys[pygame.K_UP]: move_up = True
        if keys[pygame.K_DOWN]: move_down = True
        
        yeni_ruh_x, yeni_ruh_y = ruh_x, ruh_y
        
        if not show_player_attack_button: 
            if move_left: yeni_ruh_x -= ruh_hiz
            if move_right: yeni_ruh_x += ruh_hiz
            if move_up: yeni_ruh_y -= ruh_hiz
            if move_down: yeni_ruh_y += ruh_hiz

        min_x = KUTU_X
        max_x = KUTU_X + KUTU_GENISLIK - ruh_boyut
        min_y = KUTU_Y
        max_y = KUTU_Y + KUTU_YUKSEKLIK - ruh_boyut

        ruh_x = max(min_x, min(yeni_ruh_x, max_x))
        ruh_y = max(min_y, min(yeni_ruh_y, max_y))

        # Saldırı Güncellemesi ve Çarpışma Kontrolü
        if not show_player_attack_button:
            # Attack 1: Hedefli Mermiler
            if current_attack_type == 1 and current_time - attack_start_time < attack_duration_ms:
                if current_time % 300 < 50: 
                    start_x = KUTU_X + KUTU_GENISLIK // 2
                    start_y = KUTU_Y
                    target_x = ruh_x + ruh_boyut // 2 
                    target_y = ruh_y + ruh_boyut // 2
                    active_attack_objects.append(Projectile(start_x, start_y, target_x, target_y))

            # Attack 2: Uyarı/Alan Saldırısı
            if current_attack_type == 2:
                warning_attack_elapsed = current_time - warning_timer
                
                if warning_attack_elapsed > warning_duration_ms:
                    area_rect = get_area_attack_rect(area_attack_side)
                    
                    if ruh_rect.colliderect(area_rect):
                        oyuncu_hp -= 1 
                        if oyuncu_hp <= 0:
                            game_state = GAME_OVER
                            
                    if current_time - attack_start_time < attack_duration_ms and warning_attack_elapsed > warning_duration_ms + 500:
                         warning_timer = current_time
                         area_attack_side = 'RIGHT' if area_attack_side == 'LEFT' else 'LEFT'

            # Attack 3: Lazer
            if laser_blast_object and laser_blast_object.active:
                laser_blast_object.update()
                
            # Mermi ve Lazer çarpışma
            for obj in list(active_attack_objects):
                obj.update()
                if not obj.active:
                    active_attack_objects.remove(obj)
                    continue
                if current_attack_type == 1:
                    if ruh_rect.colliderect(obj.get_rect()):
                        oyuncu_hp -= 5 
                        obj.active = False
                        if oyuncu_hp <= 0:
                            game_state = GAME_OVER
            
            # Saldırı süresi bitti mi?
            if current_time - attack_start_time > attack_duration_ms:
                current_attack_index += 1
                start_next_attack()
            
    # 3. Grafik Çizimi
    ekran.fill(SIYAH)

    if game_state == START_SCREEN:
        # Version Alpha yazısı
        text_version = font_kucuk.render("Version: ALPHA", True, GRI)
        ekran.blit(text_version, (10, 10))

        # Ana Başlık
        text_title = font_uyari.render("UNDERTALE PROJESİ", True, MAVI_CAN)
        ekran.blit(text_title, text_title.get_rect(center=(EKRAN_GENISLIK // 2, EKRAN_YUKSEKLIK // 2 - 80)))
        
        # OYNA Tuşu
        pygame.draw.rect(ekran, YESIL_IYI, PLAY_RECT)
        text_play = font_buyuk.render("OYNA", True, BEYAZ)
        ekran.blit(text_play, text_play.get_rect(center=PLAY_RECT.center))
        
        # Yapımcı Bilgileri (Yeni)
        y_pos = PLAY_RECT.bottom + 20
        yapimci_text = font_kucuk.render("YAPIMCI: YILDIRIM123", True, BEYAZ)
        proje_text = font_kucuk.render("PROJE: UKZCM", True, BEYAZ)
        yardimci_text = font_kucuk.render("YARDIMCI: GEMINI YAPAY ZEKA", True, BEYAZ)
        
        ekran.blit(yapimci_text, yapimci_text.get_rect(center=(EKRAN_GENISLIK // 2, y_pos)))
        ekran.blit(proje_text, proje_text.get_rect(center=(EKRAN_GENISLIK // 2, y_pos + int(24 * BOYUT_FAKTORU))))
        ekran.blit(yardimci_text, yardimci_text.get_rect(center=(EKRAN_GENISLIK // 2, y_pos + int(48 * BOYUT_FAKTORU))))


    elif game_state == GAME_OVER:
        text_gameover = font_uyari.render("GAME OVER", True, KIRMIZI_GUC)
        ekran.blit(text_gameover, text_gameover.get_rect(center=(EKRAN_GENISLIK // 2, EKRAN_YUKSEKLIK // 2 - 50)))
        
        pygame.draw.rect(ekran, YESIL_IYI, RESTART_RECT)
        text_restart = font_buyuk.render("RESTART", True, BEYAZ)
        ekran.blit(text_restart, text_restart.get_rect(center=RESTART_RECT.center))

    elif game_state == GAME_WON:
        text_gamewon = font_uyari.render("TEBRİKLER KAZANDINIZ", True, SARI_UYARI)
        ekran.blit(text_gamewon, text_gamewon.get_rect(center=(EKRAN_GENISLIK // 2, EKRAN_YUKSEKLIK // 2 - 50)))
        
        pygame.draw.rect(ekran, YESIL_IYI, RESTART_RECT)
        text_restart = font_buyuk.render("RESTART", True, BEYAZ)
        ekran.blit(text_restart, text_restart.get_rect(center=RESTART_RECT.center))
        
    else: # COMMAND_PHASE veya ATTACK_PHASE
        
        # Version Alpha yazısı
        text_version = font_kucuk.render("Version: ALPHA", True, GRI)
        ekran.blit(text_version, (10, 10))
        
        # HP GÖSTERGELERİ 
        
        # Düşman HP (Sol Üst - Oynanış sırasında görünür)
        text_enemy = font_kucuk.render(f"ENEMY", True, KIRMIZI_GUC)
        ekran.blit(text_enemy, (KUTU_X, 20))
        text_enemy_hp = font_kucuk.render(f"HP:{max(0, dusman_hp)}", True, KIRMIZI_GUC)
        ekran.blit(text_enemy_hp, (KUTU_X, 20 + int(24 * BOYUT_FAKTORU)))

        # Oyuncu Adı ve HP (Savaş kutusunun altında, Sol Taraf)
        text_name = font_kucuk.render(oyuncu_adi, True, BEYAZ)
        ekran.blit(text_name, (KUTU_X, KUTU_Y + KUTU_YUKSEKLIK + 10))
        
        hp_bar_width = int(100 * BOYUT_FAKTORU)
        hp_bar_height = int(10 * BOYUT_FAKTORU)
        hp_bar_x = KUTU_X + text_name.get_width() + 10 
        hp_bar_y = KUTU_Y + KUTU_YUKSEKLIK + 10 + (text_name.get_height() // 2) - (hp_bar_height // 2)
        
        # Gri Arka Plan (Maksimum HP)
        pygame.draw.rect(ekran, GRI, (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        # Yeşil Can Çubuğu (Mevcut HP)
        current_hp_width = (oyuncu_hp / 100) * hp_bar_width
        pygame.draw.rect(ekran, YESIL_IYI, (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))
        
        text_you_hp = font_kucuk.render(f"{max(0, oyuncu_hp)}/100", True, BEYAZ)
        ekran.blit(text_you_hp, (hp_bar_x + hp_bar_width + 10, hp_bar_y - 5))

        # BÜYÜK DÜŞMAN KARE 
        pygame.draw.rect(ekran, KIRMIZI_GUC, (BUYUK_DUSMAN_X, BUYUK_DUSMAN_Y, BUYUK_DUSMAN_BOYUT, BUYUK_DUSMAN_BOYUT))

        # ----------------- SAVAŞ ALANI ÇİZİMİ -----------------
        
        # Alan saldırısı uyarısı/patlaması
        if current_attack_type == 2:
            area_rect = get_area_attack_rect(area_attack_side)
            
            if current_time - warning_timer < warning_duration_ms:
                pygame.draw.rect(ekran, SARI_UYARI, area_rect, 5) 
                text_uyari = font_uyari.render("!", True, SARI_UYARI)
                ekran.blit(text_uyari, text_uyari.get_rect(center=area_rect.center))
            else:
                pygame.draw.rect(ekran, KIRMIZI_PATLAMA, area_rect) 

        # Lazer Blaster çizimi
        if laser_blast_object and laser_blast_object.active:
            laser_blast_object.draw()

        # SAVAŞ KUTUSU (Beyaz Çubuklar)
        pygame.draw.rect(ekran, BEYAZ, (KUTU_X, KUTU_Y, KUTU_GENISLIK, KUTU_YUKSEKLIK), KUTU_KALINLIK)
        
        # RUH (Küçük Kırmızı Kare)
        if game_state == ATTACK_PHASE: 
            pygame.draw.rect(ekran, KIRMIZI_GUC, (ruh_x, ruh_y, ruh_boyut, ruh_boyut))
        
        # Mermileri çiz
        for obj in active_attack_objects:
            obj.draw()

        # ----------------- ARAYÜZ ÇİZİMİ -----------------
        
        # Komut düğmeleri sadece COMMAND_PHASE'de görünür
        if game_state == COMMAND_PHASE:
            # ATTACK Düğmesi
            pygame.draw.rect(ekran, KIRMIZI_GUC, ATTACK_RECT)
            text_attack = font_buyuk.render("ATTACK", True, BEYAZ)
            ekran.blit(text_attack, text_attack.get_rect(center=ATTACK_RECT.center))
            
            # MEDIC Düğmesi
            pygame.draw.rect(ekran, YESIL_IYI, MEDIC_RECT)
            text_medic = font_buyuk.render("MEDIC", True, BEYAZ)
            ekran.blit(text_medic, text_medic.get_rect(center=MEDIC_RECT.center))
            
            # RUN Düğmesi
            pygame.draw.rect(ekran, TURUNCU, RUN_RECT)
            text_run = font_buyuk.render("RUN", True, BEYAZ)
            ekran.blit(text_run, text_run.get_rect(center=RUN_RECT.center))

        # D-PAD ve Oyuncu Saldırı Tuşu sadece ATTACK_PHASE'de görünür
        if game_state == ATTACK_PHASE:
            
            # D-PAD ÇİZİMİ 
            if not show_player_attack_button:
                draw_dpad_button(UP_RECT, "^")
                draw_dpad_button(DOWN_RECT, "v")
                draw_dpad_button(LEFT_RECT, "<")
                draw_dpad_button(RIGHT_RECT, ">")
            
            # OYUNCU SALDIRI TUŞU 
            if show_player_attack_button:
                 pygame.draw.rect(ekran, KIRMIZI_GUC, PLAYER_ATTACK_RECT)
                 text_player_attack = font_buyuk.render("SALDIR", True, BEYAZ)
                 ekran.blit(text_player_attack, text_player_attack.get_rect(center=PLAYER_ATTACK_RECT.center))


    # Ekranı güncelle
    pygame.display.flip()
    
    # FPS Ayarı
    saat.tick(60) 

# Pygame'i kapat
pygame.quit()
sys.exit()
