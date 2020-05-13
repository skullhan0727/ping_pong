"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-5) and scene_info["platform_1P"][0]+20 < (pred+5): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-5) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-5) and scene_info["platform_2P"][0]+20 < (pred+5): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-5) : return 1 # goes right
            else : return 2 # goes left

    def ml_loop_for_1P(before_block_x,block_x): 

        """        
        if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
            x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) // scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
            bound = pred // 200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '1P',pred = pred)
        else : # 球正在向上 # ball goes up
            return move_to(player = '1P',pred = 100)
        """
 
        ball_x=scene_info["ball"][0]
        ball_y=scene_info["ball"][1]

        platform_x=scene_info["platform_1P"][0]
        platform_y=scene_info["platform_1P"][1]


        block_x=scene_info["blocker"][0]
        block_y=scene_info["blocker"][1]

        ball_x_speed=scene_info["ball_speed"][0]
        ball_y_speed=scene_info["ball_speed"][1]

        frame=scene_info["frame"]


        speed=block_x-before_block_x


        while ball_y<415:

            if (frame%200)==0 and frame >=200:
                if ball_x_speed>0:
                    ball_x_speed=abs(ball_x_speed)+1
                else:
                    ball_x_speed=-abs(ball_x_speed)-1
                if ball_y_speed>0:
                    ball_y_speed=abs(ball_y_speed)+1
                else:
                    ball_y_speed=-abs(ball_y_speed)-1



            predict_ball_x_speed=ball_x_speed
            predict_ball_y_speed=ball_y_speed
            predict_ball_x=ball_x
            predict_ball_y=ball_y

  


            hit_y_left=(ball_y_speed/ball_x_speed)*(block_x-ball_x)+ball_y
            hit_y_right=(ball_y_speed/ball_x_speed)*(block_x+30-ball_x)+ball_y
            hit_x_top=(ball_x_speed/ball_y_speed)*(240-ball_y)+ball_x
            hit_x_down=(ball_x_speed/ball_y_speed)*(260-ball_y)+ball_x 
            #print("hit_y_left: ",hit_y_left,"hit_y_right: ",hit_y_right)
            if ball_x+ball_x_speed<block_x+30<ball_x and 240<hit_y_right<260:
                        predict_ball_x=block_x+30
                        predict_ball_x_speed=-ball_x_speed

            elif ball_x<block_x<ball_x+ball_x_speed and 240<hit_y_left<260:   
                        predict_ball_x=block_x
                        predict_ball_x_speed=-ball_x_speed




            #print("hit_x_top: ",hit_x_top,"hit_x_down: ",hit_x_down)
            if ball_y+ball_y_speed<260<ball_y and block_x<hit_x_down<block_x+30:
                        predict_ball_y=260
                        predict_ball_y_speed=-ball_y_speed
  
            elif ball_y<240<ball_y+ball_y_speed and block_x<hit_x_top<block_x+30:
                        predict_ball_y=240
                        predict_ball_y_speed=-ball_y_speed

            else:
                predict_ball_y=ball_y+ball_y_speed
 


            if block_x+speed>170:
                speed=-speed
                predict_block_x=170

            elif block_x+speed<0:
                speed=-speed

                predict_block_x=0

            else: 
                
                predict_block_x=block_x+speed


                
                
            if ball_x!=predict_ball_x:
                ball_x=predict_ball_x
            else:
                ball_x=ball_x+predict_ball_x_speed
                
            if ball_y!=predict_ball_y:
                ball_y=predict_ball_y
            else:
                ball_y=ball_y+predict_ball_y_speed
            
                
            





            if ball_y>=415:

                predict_ball_y_speed=-predict_ball_y_speed
                """
                if ball_x_speed>0:
                    if command_1P=="MOVE_LEFT":
                        predict_ball_x_speed=-predict_ball_x_speed
                if ball_x_speed<0:
                    if command_1P=="MOVE_RIGHT":
                        predict_ball_x_speed=-predict_ball_x_speed
                """
                ball_y=415
            elif ball_y<80:
                predict_ball_y_speed=-predict_ball_y_speed
                ball_x=80


            if ball_x>195:
                predict_ball_x_speed=-predict_ball_x_speed
                ball_x=195
            elif ball_x<0:
                predict_ball_x_speed=-predict_ball_x_speed
                ball_x=0




            ball_x_speed=predict_ball_x_speed
            ball_y_speed=predict_ball_y_speed
            block_x=predict_block_x
            


            frame+=1
        
        should_x2=ball_x
        #print(should_x2)
        print(should_x2,"PLATFORM_x:",scene_info["platform_1P"][0],"frame",scene_info["frame"],"x:",scene_info["ball"][0],"y:",scene_info["ball"][1],"block_x:",scene_info["blocker"][0],"block_y:",scene_info["blocker"][1],"ball_speed_x:",scene_info["ball_speed"][0],"ball_speed_y:",scene_info["ball_speed"][1],)
        return move_to(player = '1P',pred = should_x2)
        


        """
        # if 240<scene_info["ball"][1]<260 and scene_info["ball"][0]!=0 and scene_info["ball"][0]!=195 and ball_x_speed!=before_ball_x_speed:
        #   scene_info["blocker"][0],"block_y:",scene_info["blocker"][1] 


        now_ball_x=ball_x
        now_ball_y=ball_y
        
        now_ball_x=blocker_x

        vector_x_right= True if ball_speed_x>0 else False
        vector_y_down= True if ball_speed_y >0 else False



        hit_y=0

        while hit_y<415:
            if vector_x_right:
                hit_x=195
            else:
                hit_x=0

            if vector_y_down:
                hit_y=415
            else:
                hit_y=80     

            if abs(now_ball_x-hit_x) <abs(now_ball_y-hit_y):
                if vector_y_down:
                    hit_y=((abs(now_ball_x-hit_x)-1)//abs(ball_speed_x)+1)*abs(ball_speed_y)+now_ball_y
                    if hit_y>415:
                        hit_y=((abs(now_ball_x-hit_x))/abs(ball_speed_x))*abs(ball_speed_y)+now_ball_y
                else:
                    hit_y=-((abs(now_ball_x-hit_x)-1)//abs(ball_speed_x)+1)*abs(ball_speed_y)+now_ball_y
                    if hit_y<0:
                        hit_y=-((abs(now_ball_x-hit_x))/abs(ball_speed_x))*abs(ball_speed_y)+now_ball_y
                        
                vector_x_right=not vector_x_right 
            else:
                #這邊可能會切球
                if vector_x_right:
                    hit_x=((abs(now_ball_y-hit_y))/abs(ball_speed_x))*abs(ball_speed_x)+now_ball_x
                else:
                    hit_x=-((abs(now_ball_y-hit_y))/abs(ball_speed_y))*abs(ball_speed_x)+now_ball_x
                vector_y_down=not vector_y_down  




            now_ball_x=hit_x
            now_ball_y=hit_y
        """

    

    def ml_loop_for_2P():  # as same as 1P
        ball_x=scene_info["ball"][0]
        ball_y=scene_info["ball"][1]

        platform_x=scene_info["platform_1P"][0]
        platform_y=scene_info["platform_1P"][1]

        ball_speed_x=scene_info["ball_speed"][0]
        ball_speed_y=vector_y_down=scene_info["ball_speed"][1]

        now_ball_x=ball_x
        now_ball_y=ball_y

        vector_x_right= True if ball_speed_x>0 else False
        vector_y_down= True if ball_speed_y >0 else False

        hit_y=500


        while hit_y>80:
            if vector_x_right:
                hit_x=195
            else:
                hit_x=0

            if vector_y_down:
                hit_y=415
            else:
                hit_y=80     

            if abs(now_ball_x-hit_x) <abs(now_ball_y-hit_y):
                if vector_y_down:
                    hit_y=((abs(now_ball_x-hit_x)-1)//abs(ball_speed_x)+1)*abs(ball_speed_y)+now_ball_y
                    if hit_y>415:
                        hit_y=((abs(now_ball_x-hit_x))/abs(ball_speed_x))*abs(ball_speed_y)+now_ball_y
                else:
                    hit_y=-((abs(now_ball_x-hit_x)-1)//abs(ball_speed_x)+1)*abs(ball_speed_y)+now_ball_y
                    if hit_y<0:
                        hit_y=-((abs(now_ball_x-hit_x))/abs(ball_speed_x))*abs(ball_speed_y)+now_ball_y
                        
                vector_x_right=not vector_x_right 
            else:
                #這邊可能會切球
                if vector_x_right:
                    hit_x=((abs(now_ball_y-hit_y))/abs(ball_speed_x))*abs(ball_speed_x)+now_ball_x
                else:
                    hit_x=-((abs(now_ball_y-hit_y))/abs(ball_speed_y))*abs(ball_speed_x)+now_ball_x
                vector_y_down=not vector_y_down  
                



            now_ball_x=hit_x
            now_ball_y=hit_y

        should_x=hit_x
        return move_to(player = '2P',pred = should_x)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()
    i=5
    block_x=85

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        before_block_x=block_x
        block_x=scene_info["blocker"][0]
        

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information
        # 3.4 Send the instruction for this frame to the game process
        if not ball_served and i<5:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            i=i+1
        elif not ball_served and i==5:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True   
         
        else:

            if side == "1P":
                command = ml_loop_for_1P(before_block_x,block_x)
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                #print("right")
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                #print("left")
            """
            if scene_info["ball"][0]==195 or scene_info["ball"][0]==0:
                print("########x:",scene_info["ball"][0],"y:",scene_info["ball"][1])
            """

            #if scene_info["ball"][1]==80 or scene_info["ball"][1]==415:
            #if scene_info["ball"][1]==415:
            #   print("******x:",scene_info["ball"][0],"y:",scene_info["ball"][1],"PLATFORM_x:",scene_info["platform_1P"][0],"PLATFORM_y:",scene_info["platform_1P"][1])
            #print("x:",scene_info["ball"][0],"y:",scene_info["ball"][1],"ball_speed_x:",scene_info["ball_speed"][0],"ball_speed_y:",scene_info["ball_speed"][1],"PLATFORM_x:",scene_info["platform_1P"][0],"PLATFORM_y:",scene_info["platform_1P"][1])
            #print("block_x:",scene_info["blocker"][0],"block_y:",scene_info["blocker"][1])
            #print("x:",scene_info["ball"][0],"y:",scene_info["ball"][1],"ball_speed_x:","block_x:",scene_info["blocker"][0],"block_y:",scene_info["blocker"][1],scene_info["ball_speed"][0],"ball_speed_y:",scene_info["ball_speed"][1],"PLATFORM_x:",scene_info["platform_1P"][0],"PLATFORM_y:",scene_info["platform_1P"][1])

            #print("frame",scene_info["frame"],"x:",scene_info["ball"][0],"y:",scene_info["ball"][1],"block_x:",scene_info["blocker"][0],"block_y:",scene_info["blocker"][1],"ball_speed_x:",scene_info["ball_speed"][0],"ball_speed_y:",scene_info["ball_speed"][1],"PLATFORM_x:",scene_info["platform_1P"][0],"PLATFORM_y:",scene_info["platform_1P"][1])



                

           


