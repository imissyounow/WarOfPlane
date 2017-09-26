import pygame
import sys
import traceback
import myplane 
import bullet
import enemy
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()


bg_size = width, height = 480,650
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

background = pygame.image.load('ui/shoot_background/background.png').convert()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

#载入游戏音乐
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

bomb_sound=pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)

supply_sound = pygame.mixer.Sound('sound/out_porp.wav')
supply_sound.set_volume(0.2)

get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)

get_bullet_sound = pygame.mixer.Sound('sound/get_double_laser.wav')
get_bullet_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound('sound/achievement.wav')
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound('sound/big_spaceship_flying.wav')
enemy3_fly_sound.set_volume(0.2)

enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)

enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)

me_down_sound = pygame.mixer.Sound('sound/game_over.wav')
me_down_sound.set_volume(0.2)

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)
        
def inc_speed(target,inc):
    for each in target:
        each.speed += inc


def main():
    #设置是否在游戏中
    is_playing = False
    is_starting = True
    need_refresh = True

    #游戏开始画面
    if is_starting == True:
        is_starting = False
        start_background_image = pygame.image.load('ui/shoot_background/background.png').convert()
        start_logo_image = pygame.image.load('ui/shoot_background/shoot_copyright.png').convert_alpha()
        start_logo_rect = start_logo_image.get_rect()
        start_logo_rect.left,start_logo_rect.top = (width-start_logo_rect.width)//2,100
        start_begin_image = pygame.image.load('ui/game_start.png').convert_alpha()
        start_begin_rect = start_begin_image.get_rect()
        start_begin_rect.left,start_begin_rect.top = (width-start_begin_rect.width)//2,400
        start_over_image = pygame.image.load('ui/shoot/game_over.png').convert_alpha()
        start_over_rect = start_over_image.get_rect()
        start_over_rect.left,start_over_rect.top = (width-start_over_rect.width)//2,500
        screen.blit(start_background_image,(0,0))
        screen.blit(start_logo_image,start_logo_rect)
        screen.blit(start_begin_image,start_begin_rect)
        screen.blit(start_over_image,start_over_rect)
        pygame.display.flip()

    #游戏结束画面
        gameover_font = pygame.font.Font('font/a.ttf',48)
        again_image = pygame.image.load('ui/game_Reagain.png').convert_alpha()
        again_rect = again_image.get_rect()
        again_rect.left,again_rect.top = ((width-again_rect.width)//2,430)
        gameover_image = pygame.image.load('ui/shoot/game_over.png').convert_alpha()
        gameover_rect = gameover_image.get_rect()
        gameover_rect.left,gameover_rect.top = ((width-gameover_rect.width)//2,490)
        gameover_background_image = pygame.image.load('ui/shoot_background/gameover.png').convert_alpha()
        gameover_background_rect = gameover_background_image.get_rect()

   
    running = True

    while running:
        if not is_playing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and start_begin_rect.collidepoint(event.pos):
                        is_playing = True

                    if event.button == 1 and start_over_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


        
        if is_playing:
            if need_refresh:
                need_refresh = False
                #播放背景音乐
                pygame.mixer.music.play(-1)
                
                #生成我方飞机
                me=myplane.MyPlane(bg_size)


                #生成敌方飞机
                enemies = pygame.sprite.Group()

                #生成敌方小飞机
                small_enemies = pygame.sprite.Group()
                add_small_enemies(small_enemies,enemies,15)

                #生成敌方中飞机
                mid_enemies = pygame.sprite.Group()
                add_mid_enemies(mid_enemies,enemies,8)

                #生成敌方大飞机
                big_enemies = pygame.sprite.Group()
                add_big_enemies(big_enemies,enemies,3)

                clock = pygame.time.Clock()


                #生成普通子弹
                bullet1 = []
                bullet1_index = 0
                BULLET1_NUM = 4
                for i in range(BULLET1_NUM):
                    bullet1.append(bullet.Bullet1(me.rect.midtop))


                #生成超级子弹
                bullet2 = []
                bullet2_index = 0
                BULLET2_NUM = 4
                for i in range(BULLET2_NUM):
                    bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
                    bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))
                    
              

                #坠机图片索引初始化
                e1_destroy_index = 0
                e2_destroy_index = 0
                e3_destroy_index = 0
                me_destroy_index = 0

                #玩家得分初始化
                score = 0
                score_font = pygame.font.Font('font/a.ttf',36)

                #标志是否暂停游戏
                paused= False
                pause_nor_image = pygame.image.load('ui/shoot/game_pause_nor.png').convert_alpha()
                pause_pressed_image = pygame.image.load('ui/shoot/game_pause_pressed.png').convert_alpha()
                resume_nor_image = pygame.image.load('ui/shoot/game_resume_nor.png').convert_alpha()
                resume_pressed_image = pygame.image.load('ui/shoot/game_resume_pressed.png').convert_alpha()
                paused_rect = pause_nor_image.get_rect()
                paused_rect.left,paused_rect.top = width - paused_rect.width - 10,10
                paused_image = pause_nor_image
                #暂停选项
                paused2_again_image = pygame.image.load('ui/shoot/game_again.png').convert_alpha()
                paused2_continue_image = pygame.image.load('ui/shoot/game_continue.png').convert_alpha()
                paused2_over_image = pygame.image.load('ui/shoot/game_over.png').convert_alpha()
                paused2_again_rect = paused2_again_image.get_rect()
                paused2_again_rect.left,paused2_again_rect.top = (width-paused2_again_rect.width)//2,200
                paused2_continue_rect = paused2_continue_image.get_rect()
                paused2_continue_rect.left,paused2_continue_rect.top = (width-paused2_continue_rect.width)//2,300
                paused2_over_rect = paused2_over_image.get_rect()
                paused2_over_rect.left,paused2_over_rect.top = (width-paused2_over_rect.width)//2,400

                #设置难度级别
                level = 1

                #全屏炸弹初始化
                bomb_image = pygame.image.load('ui/shoot/bomb.png').convert_alpha()
                bomb_rect = bomb_image.get_rect()
                bomb_font = pygame.font.Font('font/a.ttf',48)
                bomb_num = 3

                #每30秒发放一个补给包
                bullet_supply = supply.Bullet_Supply(bg_size)
                bomb_supply = supply.Bomb_Supply(bg_size)
                SUPPLY_TIME = USEREVENT
                pygame.time.set_timer(SUPPLY_TIME,30 * 1000)
                
                #超级子弹定时器
                DOUBLE_BULLET_TIME = USEREVENT + 1

                #我方无敌状态定时器
                INVINCIBLE_TIME = USEREVENT + 2

                #标志是否使用超级子弹
                is_double_bullet = False

                #生命数量
                life_image = pygame.image.load('ui/shoot_background/hero1.png').convert_alpha()
                life_rect = life_image.get_rect()
                life_num = 3

                #用于阻止重复打开记录文件
                recorded = False

                #用于切换图片
                switch_image = True

                #用于延迟
                delay=100

            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and paused_rect.collidepoint(event.pos):
                        paused = not paused
                        if paused:
                            pygame.time.set_timer(SUPPLY_TIME,0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:
                            pygame.time.set_timer(SUPPLY_TIME,30*1000)
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()

                    if event.button == 1 and paused2_again_rect.collidepoint(event.pos):
                        if paused:
                            need_refresh = True

                    if event.button == 1 and paused2_continue_rect.collidepoint(event.pos):
                        if paused:
                            paused = not paused
                            pygame.time.set_timer(SUPPLY_TIME,30*1000)
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()

                    if event.button == 1 and paused2_over_rect.collidepoint(event.pos):
                        if paused:
                            exit()

                    if event.button ==1 and gameover_rect.collidepoint(event.pos):
                        if not life_num:
                            exit()
                            
                    if event.button ==1 and again_rect.collidepoint(event.pos):
                        if not life_num:
                            need_refresh = True

                elif event.type == MOUSEMOTION:
                    if paused_rect.collidepoint(event.pos):
                        if paused:
                            paused_image = resume_pressed_image
                        else:
                            paused_image = pause_pressed_image
                    else:
                        if paused:
                            paused_image = resume_nor_image
                        else:
                            paused_image = pause_nor_image

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if not paused:
                            if bomb_num:
                                bomb_num = 1
                                bomb_sound.play()
                                for each in enemies:
                                    if each.rect.bottom > 0:
                                        each.active = False

                elif event.type == SUPPLY_TIME:
                    supply_sound.play()
                    if choice([True,False]):
                        bomb_supply.reset()
                    else:
                        bullet_supply.reset()

                elif event.type == DOUBLE_BULLET_TIME:
                    is_double_bullet = False
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,0)


                elif event.type == INVINCIBLE_TIME:
                    me.invincible = False
                    pygame.time.set_timer(INVINCIBLE_TIME,0)


                
            #根据用户得分增加难度
            if level == 1 and score > 50000:
                level = 2
                upgrade_sound.play()
                #增加三小型敌机，两架中型敌机，一架大型敌机
                add_small_enemies(small_enemies,enemies,3)
                add_mid_enemies(mid_enemies,enemies,2)
                add_big_enemies(big_enemies,enemies,1)
                #提升小型敌机速度
                inc_speed(small_enemies,1)
                
            elif level == 2 and score > 300000:
                level = 3
                upgrade_sound.play()
                #增加5小型敌机，3架中型敌机，2架大型敌机
                add_small_enemies(small_enemies,enemies,5)
                add_mid_enemies(mid_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                #提升小型敌机速度
                inc_speed(small_enemies,1)
                inc_speed(mid_enemies,1)

            elif level == 3 and score > 600000:
                level = 4
                upgrade_sound.play()
                #增加5小型敌机，3架中型敌机，2架大型敌机
                add_small_enemies(small_enemies,enemies,5)
                add_mid_enemies(mid_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                #提升小型敌机速度
                inc_speed(small_enemies,1)
                inc_speed(mid_enemies,1)

            elif level == 4 and score > 1000000:
                level = 5
                upgrade_sound.play()
                #增加5小型敌机，3架中型敌机，2架大型敌机
                add_small_enemies(small_enemies,enemies,5)
                add_mid_enemies(mid_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                #提升小型敌机速度
                inc_speed(small_enemies,1)
                inc_speed(mid_enemies,1)
                

            screen.blit(background,(0,0))

            
            if life_num and not paused:
                #检测用户的键盘操作
                key_pressed = pygame.key.get_pressed()

                if key_pressed[K_w] or key_pressed[K_UP]:
                    me.moveUp()
                if key_pressed[K_s] or key_pressed[K_DOWN]:
                    me.moveDown()
                if key_pressed[K_a] or key_pressed[K_LEFT]:
                    me.moveLeft()
                if key_pressed[K_d] or key_pressed[K_RIGHT]:
                    me.moveRight()


                #绘制全屏炸弹补给并检测是否获得
                if bomb_supply.active:
                    bomb_supply.move()
                    screen.blit(bomb_supply.image,bomb_supply.rect)
                    if pygame.sprite.collide_mask(bomb_supply,me):
                        get_bomb_sound.play()
                        if bomb_num < 3:
                            bomb_num += 1
                        bomb_supply.active = False
                        

                #绘制超级子弹补给并检测是否获得
                if bullet_supply.active:
                    bullet_supply.move()
                    screen.blit(bullet_supply.image,bullet_supply.rect)
                    if pygame.sprite.collide_mask(bullet_supply,me):
                        get_bullet_sound.play()
                        #发射超级子弹
                        is_double_bullet = True
                        pygame.time.set_timer(DOUBLE_BULLET_TIME,18*1000)
                        bullet_supply.active = False


                
                #发射子弹
                if not (delay%10):
                    bullet_sound.play()
                    if is_double_bullet:
                        bullets = bullet2
                        bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                        bullets[bullet2_index+1].reset((me.rect.centerx+30,me.rect.centery))
                        bullet2_index = (bullet2_index+2) % (BULLET2_NUM*2)

                    else:
                        bullets=bullet1
                        bullets[bullet1_index].reset(me.rect.midtop)
                        bullet1_index = (bullet1_index + 1) % BULLET1_NUM


                #检测子弹是否击中敌机
                for b in bullets:
                    if b.active:
                        b.move()
                        screen.blit(b.image,b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                if e in mid_enemies or e in big_enemies:
                                    e.energy -= 1
                                    e.hit = True
                                    if e.energy == 0:
                                        e.active = False
                                else:
                                    e.active = False
                
                #绘制大型敌机：
                for each in big_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            #绘制被打到的特效
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else:
                            if switch_image:
                                screen.blit(each.image1,each.rect)
                            else:
                                screen.blit(each.image2,each.rect)

                        #绘制血槽
                        pygame.draw.line(screen,BLACK,\
                                (each.rect.left,each.rect.top-5),\
                                (each.rect.right,each.rect.top-5),\
                                2)
                        #当生命大于20%时，显示绿色，否则显示红色
                        energy_remain = each.energy / enemy.BigEnemy.energy
                        if energy_remain > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen,energy_color,\
                                         (each.rect.left,each.rect.top-5),\
                                         (each.rect.left+each.rect.width * energy_remain,each.rect.top-5),\
                                         2)
                        #即将出现在画面中，播放音效
                        if each.rect.bottom == -50:
                            enemy3_fly_sound.play(-1)
                    else:
                        #毁灭
                        if not (delay%3):
                            if e3_destroy_index == 0:
                                enemy3_down_sound.play()
                            screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                            e3_destroy_index = (e3_destroy_index+1) % 6
                            if e3_destroy_index == 0:
                                enemy3_fly_sound.stop()
                                score += 10000
                                each.reset()
                            

                #绘制中型敌机
                for each in mid_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit=False
                        else:
                            screen.blit(each.image,each.rect)

                        #绘制血槽
                        pygame.draw.line(screen,BLACK,\
                                (each.rect.left,each.rect.top-5),\
                                (each.rect.right,each.rect.top-5),\
                                2)
                        #当生命大于20%时，显示绿色，否则显示红色
                        energy_remain = each.energy / enemy.MidEnemy.energy
                        if energy_remain > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen,energy_color,\
                                         (each.rect.left,each.rect.top-5),\
                                         (each.rect.left+each.rect.width * energy_remain,each.rect.top-5),\
                                         2)
                    else:
                        #毁灭
                        if not (delay%3):
                            if e2_destroy_index == 0:
                                enemy2_down_sound.play()
                            screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                            e2_destroy_index = (e2_destroy_index+1) % 4
                            if e2_destroy_index == 0:
                                score += 6000
                                each.reset()
                        

                #绘制小型敌机
                for each in small_enemies:
                    if each.active:
                        each.move()
                        screen.blit(each.image,each.rect)
                    else:
                        #毁灭
                        if not (delay%3):
                            if e1_destroy_index == 0:
                                enemy1_down_sound.play()
                            screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                            e1_destroy_index = (e1_destroy_index+1) % 4
                            if e1_destroy_index == 0:
                                score += 1000
                                each.reset()


                #检测我方飞机是否被撞
                enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
                if enemies_down and not me.invincible:
                    me.active = False
                    for e in enemies_down:
                        e.active = False
                          
                #绘制我方飞机
                if me.active:
                    if switch_image:
                        screen.blit(me.image1,me.rect)
                    else:
                        screen.blit(me.image2,me.rect)

                else:
                    #毁灭
                    if not (delay%3):
                        if me_destroy_index == 0:
                            me_down_sound.play()
                        screen.blit(me.destroy_images[me_destroy_index],me.rect)
                        me_destroy_index = (me_destroy_index+1) % 4
                        if me_destroy_index == 0:
                            life_num -= 1
                            me.reset()
                            pygame.time.set_timer(INVINCIBLE_TIME,3*1000)
                            

                #绘制全屏炸弹数量
                bomb_text = bomb_font.render('X %d' % bomb_num,True,WHITE)
                text_rect = bomb_text.get_rect()
                screen.blit(bomb_image,(10,height - 10 - bomb_rect.height))
                screen.blit(bomb_text,(20 + bomb_rect.width,height - 5 - text_rect.height))

                #绘制生命数量
                if life_num:
                    for i in range(life_num):
                        screen.blit(life_image,\
                                    (width-10-(i+1)*life_rect.width,\
                                    height-10-life_rect.height))


            #绘制游戏结束画面
            elif not life_num:
                #背景音乐停止
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                pygame.time.set_timer(SUPPLY_TIME,0)

                if not recorded:
                    recorded = True   
                    #读取历史最高得分
                    with open('record.txt','r') as f:
                        record_score = int (f.read())

                    #如果高于历史最高分，存档
                    if score>record_score:
                        with open('record.txt','w') as f:
                            f.write(str(score))

                #绘制结束界面
                pygame.time.set_timer(SUPPLY_TIME,0)
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                screen.blit(gameover_background_image,(0,0))
                recorded_score_text = gameover_font.render(str(record_score),True,WHITE)
                screen.blit(recorded_score_text,(140,30))
                current_score_text = gameover_font.render(str(score),True,WHITE)
                current_score_rect = current_score_text.get_rect()
                screen.blit(current_score_text,((width-current_score_rect.width)//2,360))
                screen.blit(again_image,again_rect)
                screen.blit(gameover_image,gameover_rect)
                
                            
            

            if life_num:

                #绘制分数
                score_text = score_font.render('Score : %s' % str(score),True,WHITE)
                screen.blit(score_text,(10,5))

                #绘制暂停按钮
                screen.blit(paused_image,paused_rect)
                if paused:
                    screen.blit(paused2_again_image,paused2_again_rect)
                    screen.blit(paused2_continue_image,paused2_continue_rect)
                    screen.blit(paused2_over_image,paused2_over_rect)


            #切换图片

            if not (delay%5):
                    switch_image= not switch_image
                
            delay -= 1
            if not delay:
                delay = 100

            pygame.display.flip()

            clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
