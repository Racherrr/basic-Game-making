# 1. 모든 공을 없애면 게임 종료(성공)
# 2. 캐릭터는 공에 닿으면 게임 종료(실패)
# 3. 시간제한 99초 초과 시 게임 종료(실패)

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

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 3

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기가 한번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 6

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "ballon1.png")),
    pygame.image.load(os.path.join(image_path, "ballon2.png")),
    pygame.image.load(os.path.join(image_path, "ballon3.png")),
    pygame.image.load(os.path.join(image_path, "ballon4.png"))
]

# 공 속도
ball_speed_y = [-7.7, -6, -5, -4]

# 공 정보
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 100, # 공의 x좌표
    "pos_y" : 100, # 공의 y좌표
    "img_idx" : 0,
    "to_x" : -1.8, # x축 이동방향
    "to_y" : -3.7, # y축 이동방향
    "init_spe_y" : ball_speed_y[0]})

# 사라질 무기와 공 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메시지
game_result = "Game Over"


running = True # 게임이 진행중인지 확인하는 변수
while running:
    dt = clock.tick(144) # 게임화면의 초당 프레임 수

    # 2. 이벤트 처리 (키보드, 마우스 처리)
    for event in pygame.event.get(): # 어떠한 이벤트가 발생했는가?
        if event.type == pygame.QUIT: # 창닫기 이벤트가 발생했는가?
            running = False # 진행중 게임 변수 변경

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x = character_x + (character_width / 2) - (weapon_width / 2)
                weapon_y = character_y
                weapons.append([weapon_x, weapon_y])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x += character_to_x

    if character_x < 0:
        character_x = 0
    elif character_x > screen_width - character_width:
        character_x = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_x = ball_val["pos_x"]
        ball_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_x <= 0 or ball_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치
        if ball_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"]
        else: # 그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.1
    
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x
    character_rect.top = character_y

    # 공 rect정보 업데이트
    for ball_idx, ball_val in enumerate(balls):
        ball_x = ball_val["pos_x"]  
        ball_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_x
        ball_rect.top = ball_y 
        
        if character_rect.colliderect(ball_rect):
            running = False
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x = weapon_val[0]
            weapon_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x
            weapon_rect.top = weapon_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기를 없애기 위한 정보
                ball_to_remove = ball_idx # 해당 공을 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현제 공 정보를 가져오기
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx +1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]


                    # 왼쪽으로 가는 공
                    balls.append({
                        "pos_x" : ball_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x좌표
                        "pos_y" : ball_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y좌표
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : -1.8, # x축 이동방향
                        "to_y" : -5, # y축 이동방향
                        "init_spe_y" : ball_speed_y[ball_img_idx + 1]})

                    # 오른쪽으로 가는 공
                    balls.append({
                        "pos_x" : ball_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x좌표
                        "pos_y" : ball_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y좌표
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : 1.8, # x축 이동방향
                        "to_y" : -5, # y축 이동방향
                        "init_spe_y" : ball_speed_y[ball_img_idx + 1]})
                break

    # 충돌된 공, 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False


    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    for weapon_x, weapon_y in weapons:
        screen.blit(weapon, (weapon_x, weapon_y))

    for idx, val in enumerate(balls):
        ball_x = val["pos_x"]
        ball_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_x, ball_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x, character_y))
    
    # 경과 시간 계산
    elapsed_tiem = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_tiem)), True, (255,255,255) )
    screen.blit(timer, (10,10))

    if total_time - elapsed_tiem <= 0:
        game_result = "Time Over"
        running = False





    pygame.display.update() # 게임화면을 다시 그리기(계속해서 그려줘야하기때문)

# 게임오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
