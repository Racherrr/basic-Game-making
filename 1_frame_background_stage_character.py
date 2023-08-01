import pygame
import os
######################################
# 기본 초기화(필수)
pygame.init() # 초기화(필수)

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("New Pang") # 게임 이름

# FPS
clock = pygame.time.Clock()
######################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트)
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# 배경만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x = (screen_width / 2) - (character_width / 2)
character_y = screen_height - character_height - stage_height



# 이벤트 루프
running = True # 게임이 진행중인지 확인하는 변수
while running:
    dt = clock.tick(144) # 게임화면의 초당 프레임 수

    # 2. 이벤트 처리 (키보드, 마우스 처리)
    for event in pygame.event.get(): # 어떠한 이벤트가 발생했는가?
        if event.type == pygame.QUIT: # 창닫기 이벤트가 발생했는가?
            running = False # 진행중 게임 변수 변경

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌처리

    # 5. 화면에 그리기

    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x, character_y))

    pygame.display.update() # 게임화면을 다시 그리기(계속해서 그려줘야하기때문)

# pygame 종료
pygame.quit()
