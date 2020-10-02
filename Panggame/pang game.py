import pygame
import os

pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480

screen = pygame.display.set_mode((screen_width, screen_height))


#화면 타이틀 설정
pygame.display.set_caption("pang game")


#FPS
clock = pygame.time.Clock()


#이미지 경로 설정(1)
current_path = os.path.dirname(__file__)  #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images and sounds") #images 폴더 위치 반환
sound_path = image_path #같은 폴더 안에 있으므로 이미지 경로와 같다


#게임 하는데 필요한 모든 이미지 경로
background = pygame.image.load(os.path.join(image_path, "pangbackground.png"))

stage = pygame.image.load(os.path.join(image_path, "pangstage.png"))

character = pygame.image.load(os.path.join(image_path, "pangcharacter.png"))

weapon = pygame.image.load(os.path.join(image_path, "pangweapon.png"))

#게임에 필요한 사운드 넣기
weapon_sound = pygame.mixer.Sound(os.path.join(sound_path, "shot.wav"))

#스테이지는 이미지 넓이가 스크린과 같아서 y값만 입력해주면 된다.
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#무기는 한번에 여러번 발사 가능하며 캐릭터를 중심으로 해서 나가므로 height 변수를 만들지 않는다.
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapons=[]

#무기의 스피드 정해준다.
weapon_speed = 10


#공 만들기(4개 크기 모두 따로 처리할것)

ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))]




#각 공마다의 스피드를 적용해준다(모두 다름)

ball_speed_y = [-18,-15,-12,-9]

balls=[]

balls.append({"pos_x" : 50,"pos_y" : 50, "img_idx" : 0,"to_x" : 3,"to_y" : -6, "init_spd_y" : ball_speed_y[0]})

#사라질 무기와 공 변수
weapon_to_remove =-1
ball_to_remove =-1



#캐릭터 불러오기
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_pos_x = screen_width/2 - character_width/2
character_pos_y = screen_height - character_height



#캐릭터 이동 속도 및 방향
to_x = 0
character_speed = 5


# 폰트 정의
game_font = pygame.font.Font(None, 40)



# 총 시간
total_time = 50

# 시작 시간 정보
start_ticks = pygame.time.get_ticks() # 현재 tick을 받아옴

#게임 종료 메시지
#Time out(시간 초과)
#Mission Complete(미션 클리어)
#Game over(캐릭터가 공에 맞음)

game_result = "Game over"

# 게임 작동을 위한 코드(기본 공식이라 생각하면 된다.)
running = True
while running:
    dt = clock.tick(30) #게임 화면의 초당 프레임을 설정

    # 캐릭터가 1초 동안에 100만큼 이동해야 한다
    # 10 fps : 1초 동안에 10번 동작 : 1번에 10만큼 이동
    # 20 fps : 1초 동안에 20번 동작 : 1번에 5만큼 이동


    # 게임 창이 닫히는 이벤트가 발생했을 경우
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #캐릭터의 움직임을 처리한다.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                to_x +=character_speed
            elif event.key == pygame.K_LEFT:
                to_x -=character_speed
            elif event.key == pygame.K_SPACE:
                weapon_sound.play()
                weapon_pos_x = character_pos_x + (character_width/2) - (weapon_width/2)
                weapon_pos_y = character_pos_y
                weapons.append([weapon_pos_x, weapon_pos_y])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                to_x = 0


    # 게임 내 캐릭터 위치 설정     
    character_pos_x += to_x


    # 캐릭터 이동 경계값 처리
    if character_pos_x < 0:
        character_pos_x = 0
    elif character_pos_x > screen_width - character_width:
        character_pos_x = screen_width - character_width

    #무기 위치 처리
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    #천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1]>0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        # 가로벽에 닿았을 때 공의 위치 변경(튕김 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1

        # 세로 위치(역시 튕김 효과)
        if ball_pos_y > screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        #튕지기 않을 경우 속도를 증가시킨다.
        else:
            ball_val["to_y"] +=0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    #충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_pos_x
    character_rect.top = character_pos_y

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
               weapon_to_remove = weapon_idx
               ball_to_remove = ball_idx


               #가장 작은 크기의 공이 아니라면 둘로 나뉘어진다.
               if ball_img_idx <3:
                   ball_width = ball_rect.size[0]
                   ball_height = ball_rect.size[1]

                   #나눠진 공 정보
                   small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                   small_ball_width = small_ball_rect.size[0]
                   small_ball_height = small_ball_rect.size[1]
                   balls.append({"pos_x" : ball_pos_x + (ball_width/2) - (small_ball_width/2),"pos_y" : ball_pos_y+ (ball_height/2) - (small_ball_height/2),"img_idx" : ball_img_idx+1,"to_x" : -3,"to_y" : -6, "init_spd_y" : ball_speed_y[ball_img_idx+1]})#왼쪽 공
                   balls.append({"pos_x" : ball_pos_x + (ball_width/2) - (small_ball_width/2),"pos_y" : ball_pos_y+ (ball_height/2) - (small_ball_height/2),"img_idx" : ball_img_idx+1,"to_x" : 3,"to_y" : -6, "init_spd_y" : ball_speed_y[ball_img_idx+1]})#오른쪽 공
               break
        else:
            continue
        break

    #충돌된 무기와 공을 없애버리자

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    # 모든 공이 사라질 경우 게임은 종료된다
    if len(balls) ==0:
        game_result = "Mission Complete"
        running = False



        # 배경, 적, 캐릭터 그리기
    screen.blit(background, (0,0))
   

    for weapon_pos_x, weapon_pos_y in weapons:
        screen.blit(weapon, (weapon_pos_x, weapon_pos_y))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x, ball_pos_y))

  

    screen.blit(stage, (0,screen_height - stage_height)) 

    screen.blit(character, (character_pos_x, character_pos_y))

    #타이머 집어 넣기
    #경과 시간(기존 이미지 전부 넣고 후에 추가로 넣어야 충돌 안생긴다.)

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과시간을 1000으로 나눠서 초 단위로 표시
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))

    #출력할 글자, True, 글자 생성
    screen.blit(timer, (10,10))

    #시간이 0이하일 경우 게임을 종료한다
    if total_time - elapsed_time <=0:
        game_result = "Time over"
        running = False




    # 게임 업데이트
    pygame.display.update()

#게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update()

pygame.time.delay(2000)
# 게임 종료
pygame.quit()
