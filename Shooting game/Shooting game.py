import pygame
import random as r
import sys
import os

pygame.init()
pygame.mixer.init()



# 화면 크기 설정
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))


#화면 타이틀 설정
pygame.display.set_caption("shooting game")


#FPS 설정
clock = pygame.time.Clock()


#이미지 경로 설정
current_path = os.path.dirname(__file__)  #현재 파일의 위치 반환
image_path = os.path.join(current_path, "game_images") #images 폴더 위치 반환
sound_path = os.path.join(current_path, "game_sounds") #sounds 폴더 위치 반환




#게임 사운드 설정
missile_sound = pygame.mixer.Sound(os.path.join(sound_path, "shot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(sound_path, "explosion.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(sound_path, "crash.wav"))
earth_explosion_sound = pygame.mixer.Sound(os.path.join(sound_path, "earth explosion.wav"))


pygame.mixer.music.load(os.path.join(sound_path, "bgm.mp3"))
pygame.mixer.music.play(-1)





#게임 하는데 필요한 이미지 넣기
background = pygame.image.load(os.path.join(image_path, "background.png"))

spaceship = pygame.image.load(os.path.join(image_path, "spaceship.png"))

missile = pygame.image.load(os.path.join(image_path, "missile.png"))


explosion = pygame.image.load(os.path.join(image_path, "explosion.png"))


#우주선 불러오기
spaceship_size = spaceship.get_rect().size
spaceship_width = spaceship_size[0]
spaceship_height = spaceship_size[1]
spaceship_x_pos = screen_width/2 - spaceship_width/2
spaceship_y_pos = screen_height - spaceship_height



#미사일 불러오기
missile_size = missile.get_rect().size
missile_width = missile_size[0]

#미사일은 한번에 여러번 발사가 가능하다
missiles = []

missile_speed = 15

#우주선 이동 속도 및 방향
to_x = 0
to_y = 0
spaceship_speed = 7


#여러개의 운석 만들기
rock_images = ["rock01.png","rock02.png","rock03.png","rock04.png","rock05.png",\
                   "rock06.png","rock07.png","rock08.png","rock09.png","rock10.png",\
                   "rock11.png","rock12.png","rock13.png","rock14.png","rock15.png",\
                   "rock16.png","rock17.png","rock18.png","rock19.png","rock20.png",\
                   "rock21.png","rock22.png","rock23.png","rock24.png","rock25.png",\
                   "rock26.png","rock27.png","rock28.png","rock29.png","rock30.png"]

rock = pygame.image.load(os.path.join(image_path,r.choice(rock_images)))
rock_size = rock.get_rect().size 
rock_width = rock_size[0]
rock_height = rock_size[1] 
rock_x_pos = r.randint(0, screen_width - rock_width)
rock_y_pos = 0
rock_speed = 3

#놓친 운석 
rock_passed = 0

#파괴한 운석 
rock_destroyed = 0

#제거되는 운석
rock_removed = -1

#제거되는 미사일
missile_removed = -1

# 폰트 정의
game_font = pygame.font.Font(None, 20)
game_font1 = pygame.font.Font(None, 40)

# 게임 오버 메시지
game_result = "Game over"

# 총 시간
total_time = 100

# 시작 시간 정보
start_ticks = pygame.time.get_ticks() # 현재 tick을 받아옴

# 게임 작동을 위한 코드(기본 공식이라 생각하면 된다.)
running = True
while running:
    dt = clock.tick(30) #게임 화면의 초당 프레임을 설정
 
    # 10 fps : 1초 동안에 10번 동작 : 1번에 10만큼 이동
    # 20 fps : 1초 동안에 20번 동작 : 1번에 5만큼 이동


    # 게임 창이 닫히는 이벤트가 발생했을 경우
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #우주선의 움직임을 처리한다.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                to_x +=spaceship_speed
            elif event.key == pygame.K_LEFT:
                to_x -=spaceship_speed
            elif event.key == pygame.K_SPACE:
                missile_sound.play()
                missile_x_pos = spaceship_x_pos + (spaceship_width/2) - (missile_width/2)
                missile_y_pos = spaceship_y_pos
                missiles.append([missile_x_pos,missile_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                to_x = 0


    spaceship_x_pos += to_x



    # 우주선 이동 경계값 처리
    if spaceship_x_pos < 0:
        spaceship_x_pos = 0
    elif spaceship_x_pos > screen_width - spaceship_width:
        spaceship_x_pos = screen_width - spaceship_width

    # 슈팅 게임에 필요한 텍스트들 만들기
    destroy_text = game_font.render("rock_destroyed:" + str(rock_destroyed), True, (255,0,0))
    pass_text = game_font.render("rock_passed:" + str(rock_passed), True, (0,191,255))



    # 운석 떨어지는 코드 만들기

    rock_y_pos += rock_speed

    if rock_y_pos > screen_height:
        rock = pygame.image.load(os.path.join(image_path,r.choice(rock_images)))
        rock_size = rock.get_rect().size 
        rock_width = rock_size[0]
        rock_height = rock_size[1] 
        rock_x_pos = r.randint(0, screen_width - rock_width)
        rock_y_pos = 0
        rock_speed +=1
        rock_passed +=1

    if rock_passed >=10:
        earth_explosion_sound.play()
        game_result = "Game over"
        running = False
    
    # 한계 값을 정하지 않으면 속도가 너무 빨라져 게임이 안됨
    if rock_speed >10:
        rock_speed = 10

    # 미사일 위치 조정
    missiles = [[m[0], m[1] - missile_speed] for m in missiles]

     #천장에 닿은 미사일 없애기
    missiles = [[m[0], m[1]] for m in missiles if m[1]>0]

    # 우주선과 운석의 충돌 처리
    spaceship_rect = spaceship.get_rect()
    spaceship_rect.left = spaceship_x_pos
    spaceship_rect.top = spaceship_y_pos

    rock_rect = rock.get_rect()
    rock_rect.left = rock_x_pos
    rock_rect.top = rock_y_pos

    #충돌 체크
    if spaceship_rect.colliderect(rock_rect):
        crash_sound.play()
        game_result = "Game over"
        running = False
        break

    for missile_idx, missile_val in enumerate(missiles):
            missile_pos_x = missile_val[0]
            missile_pos_y = missile_val[1]

        #무기 정보 업그레이드
            missile_rect = missile.get_rect()
            missile_rect.left = missile_pos_x
            missile_rect.top = missile_pos_y




            if missile_rect.colliderect(rock_rect):
                explosion_sound.play()
                del(rock)
                del(missiles)
                missiles = []
                
                # 미사일 위치 조정
                missiles = [[m[0], m[1] - missile_speed] for m in missiles]

                #천장에 닿은 미사일 없애기
                missiles = [[m[0], m[1]] for m in missiles if m[1]>0]

                rock = pygame.image.load(os.path.join(image_path,r.choice(rock_images)))
                rock_size = rock.get_rect().size 
                rock_width = rock_size[0]
                rock_height = rock_size[1] 
                rock_x_pos = r.randint(0, screen_width - rock_width)
                rock_y_pos = 0
                rock_speed +=1
                rock_destroyed +=1

                if rock_destroyed >=30:
                    game_result = 'Mission Compelete'
                    running = False

        

    #해당 무기에 관한 위치 값이 없으므로 먼저 만들어준다.

  

    # 게임에 필요한 그림들 그리기
    screen.blit(background, (0,0)) 
   
    screen.blit(spaceship, (spaceship_x_pos, spaceship_y_pos))

    for missile_x_pos, missile_y_pos in missiles:
        screen.blit(missile,(missile_x_pos, missile_y_pos))

    screen.blit(spaceship, (spaceship_x_pos, spaceship_y_pos))
    screen.blit(rock,(rock_x_pos,rock_y_pos))


    #타이머 집어 넣기
    #경과 시간(기존 이미지 전부 넣고 후에 추가로 넣어야 충돌 안생긴다.)

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과시간을 1000으로 나눠서 초 단위로 표시
    timer = game_font1.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))

    #출력할 글자, True, 글자 생성
    screen.blit(timer, (220,10))

    #파괴된 운석과 통과된 운석들을 생성해준다.
    screen.blit(destroy_text, (360, 0))
    screen.blit(pass_text, (10, 0))

  

    #시간이 0이하일 경우 게임을 종료한다
    if total_time - elapsed_time <=0:
        game_result = "Time over"
        running = False




    # 게임 업데이트
    pygame.display.update()



#게임 오버 메시지
msg = game_font1.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg,msg_rect)
pygame.display.update()



pygame.time.delay(2000)
# 게임 종료
pygame.quit()

