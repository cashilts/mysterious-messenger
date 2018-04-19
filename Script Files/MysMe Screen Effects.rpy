init python:

    # A function to make the Max Speed button work
    def toggle_skipping():
        config.skipping = not config.skipping     

    # So you can increase/decrease the speed of the chat
    def slow_pv():
        global pv
        if pv <= 1.1:
            pv += 0.09  
        return
        
    def fast_pv():
        global pv
        if pv >= 0.53:
            pv -= 0.09
        return

    # Add a name & colour here if you'd like to add
    # another heart icon
    heartcolour = {'s' : "#ff2626", 
                    'z' : "#c9c9c9", 
                    'ja' : "#d0b741", 
                    'ju' : "#a59aef", 
                    'y' : "#31ff26", 
                    'r' : "#fcef5a",
                    'ra' : "#b81d7b",
                    'v' : "#50b2bc",
                    'u' : "#ffffff",
                    'sa' : "#b81d7b",
                    } 
                    
    
    #************************************
    # Heart Points
    #************************************
    heart_points = {'s' : 0, 
                    'z' : 0, 
                    'ja' : 0, 
                    'ju' : 0, 
                    'y' : 0, 
                    'r' : 0,
                    'v' : 0,
                    'u' : 0,
                    'sa' : 0
                    } 

    # This is a helper function for the heart icon
    # it dynamically recolours a generic white heart
    # depending on the character
    # If you'd like to define your own character & heart icon,
    # just add it to the heartcolour list
    # and when you type "call heart_icon("my custom character") it will
    # automatically recolour it
    def heart_icon_fn(st,at):
        if heartChar in heartcolour:
            colour = heartcolour[heartChar]
        else:
            colour = white
        return im.MatrixColor("Heart Point/Unknown Heart Point.png", im.matrix.colorize("#000000", colour)), 0.1
        
    # Similarly, this recolours the heartbreak animation
    # It has multiple frames, so there are a lot of 
    # similar functions defined below
    def heart_break_fn1(st,at):    
        if heartChar in heartcolour:
            colour = heartcolour[heartChar]
        else:
            colour = white
        return im.MatrixColor("Heart Point/HeartBreak/stat_animation_6.png", im.matrix.colorize("#000000", colour)), 0.1
        
    def heart_break_fn2(st,at):   
        if heartChar in heartcolour:
            colour = heartcolour[heartChar]
        else:
            colour = white
        return im.MatrixColor("Heart Point/HeartBreak/stat_animation_7.png", im.matrix.colorize("#000000", colour)), 0.1
        
    def heart_break_fn3(st,at):   
        if heartChar in heartcolour:
            colour = heartcolour[heartChar]
        else:
            colour = white
        return im.MatrixColor("Heart Point/HeartBreak/stat_animation_8.png", im.matrix.colorize("#000000", colour)), 0.1
        
    def heart_break_fn4(st,at):   
        if heartChar in heartcolour:
            colour = heartcolour[heartChar]
        else:
            colour = white
        return im.MatrixColor("Heart Point/HeartBreak/stat_animation_9.png", im.matrix.colorize("#000000", colour)), 0.1

# This is a variable that detects if you're choosing an option from a menu
# If so, it uses this variable to know it should darken the screen behind
# the choices
default choosing = False
# Variable that detects if the answer screen should be
# showing. Largely only useful if you view a CG when you should
# be answering a prompt
default pre_choosing = False
# Keeps track of the total number of hp (heart points) you've received per chatroom
default chatroom_hp = 0

#************************************
# Heart Icons
#************************************ 
image heart_icon = DynamicDisplayable(heart_icon_fn)
image heartbreak1 = DynamicDisplayable(heart_break_fn1)
image heartbreak2 = DynamicDisplayable(heart_break_fn2)
image heartbreak3 = DynamicDisplayable(heart_break_fn3)
image heartbreak4 = DynamicDisplayable(heart_break_fn4)
image heartbreak5 = "Heart Point/HeartBreak/stat_animation_10.png"

label heart_icon(character):
    $ heartChar = character
    show heart_icon onlayer heart at heart
    $ addchat("answer","",0)
    #hide heart_icon onlayer heart
    # This counts heart points
    # Ray and Saeran are counted as one person
    if character == 'ra':
        $ character = 'sa'
    if character in heart_points:
        $ points = heart_points[character]
        $ points += 1
        $ newVal = {character: points}
        $ heart_points.update(newVal)
        $ chatroom_hp += 1
    return
    
label heart_break(character):
    $ heartChar = character
    show heartbreak1 onlayer heart at heartbreak
    $ addchat("answer", "",0.12)
    hide heartbreak1 onlayer heart

    show heartbreak2 onlayer heart at heartbreak
    $ renpy.pause(0.12, hard=True)
    hide heartbreak2 onlayer heart

    show heartbreak3 onlayer heart at heartbreak
    $ renpy.pause(0.12, hard=True)
    hide heartbreak3 onlayer heart

    show heartbreak4 onlayer heart at heartbreak
    $ renpy.pause(0.12, hard=True)
    hide heartbreak4 onlayer heart

    show heartbreak5 onlayer heart at heartbreak
    $ renpy.pause(0.12, hard=True)
    hide heartbreak5 onlayer heart

    if character == 'ra':
        $ character = 'sa'
    if character in heart_points:
        $ points = heart_points[character]
        $ points -= 1
        $ newVal = {character: points}
        $ heart_points.update(newVal)
        $ chatroom_hp -= 1
    return

#************************************
# Answer Button
#************************************ 

# Call this label before you show a menu
# to show the answer button
label answer:
    $ addchat("answer","",0)
    hide screen viewCG
    #hide screen pause
    $ pre_choosing = True
    call screen answer_button
    return

image answerbutton: 
    block:
        "Phone UI/Answer-Dark.png" with Dissolve(0.5, alpha=True)
        0.5
        "Phone UI/Answer-Dark.png"
        0.5
        "Phone UI/Answer.png" with Dissolve(0.5, alpha=True)
        0.5
        "Phone UI/Answer.png"
        0.5
        repeat
        
screen answer_button:
    image "pausebutton" xalign 0.96 yalign 0.16
    image "Phone UI/pause_square.png" yalign 0.59
    image "answerbutton" ypos 1220
    imagebutton:
        xanchor 0.0
        yanchor 0.0
        xpos 0
        ypos 1220
        focus_mask None
        idle "Phone UI/answer_transparent.png"
        activate_sound "sfx/UI/answer_screen.mp3"
        action [ToggleVariable("choosing", False, True), Return()]       

    
#************************************
# Pause/Play footers
#************************************ 

image pausebutton:
    "Phone UI/pause_sign.png" with Dissolve(0.5, alpha=True)
    0.5
    "Phone UI/pause_sign.png"
    0.5
    "transparent.png" with Dissolve(0.5, alpha=True)
    0.5
    "transparent.png"
    0.5
    repeat
    

image fast-slow-button = "Phone UI/fast-slow-transparent.png"
    
# This is the screen that shows the pause button
# (but the chat is still playing)
screen pause:
    imagebutton:
        xanchor 0.0
        yanchor 0.0
        xpos 0
        ypos 1220
        focus_mask True
        idle "Phone UI/Pause.png"
        if not choosing:
            action [Call("play"), Return()]
    if choosing:        
        image "Phone UI/choice_dark.png"
     
    if not choosing:
        # Fast button
        imagebutton:
            xalign 0.985
            yalign 0.997
            focus_mask None
            idle "fast-slow-button"
            action [fast_pv, Call("speed_num_label")]#, renpy.restart_interaction] 
                
        # Slow button
        imagebutton:
            xalign 0.015
            yalign 0.997
            focus_mask None
            idle "fast-slow-button"
            action [slow_pv, Call("speed_num_label")]#, renpy.restart_interaction]
        
          
label play:
    $ addchat("pause","",0)
    call screen play_button
    #show screen play_button
    #pause
    hide screen play_button
    return
    
# This screen is visible when the chat isn't paused
screen play_button:
    if not choosing:
        image "pausebutton" xalign 0.96 yalign 0.16
        image "Phone UI/pause_square.png" yalign 0.59
    else:
        image "Phone UI/choice_dark.png"
    imagebutton:
        xanchor 0.0
        yanchor 0.0
        xpos 0
        ypos 1220
        focus_mask True
        idle "Phone UI/Play.png"
        action Return()
        

#************************************
# Chat Header Overlay
#************************************ 
## This screen shows the current time in the top righthand corner
## It's currently just for cosmetic purposes since I wanted to 
## display the current time as if it were a real phone
# The real MysMe screen doesn't technically have this
# but eventually it will likely be adapted to show the time like
# you see in VN sections
screen clock_screen:
    zorder 3
    add myClock:
        xalign 1.0
        yalign 0.0

image maxSpeed = im.FactorScale("Phone UI/max_speed_active.png",1.1)
image noMaxSpeed = im.FactorScale("Phone UI/max_speed_inactive.png",1.1)
        
## This screen just shows the header/footer above the chat
screen phone_overlay:  
    image "Phone UI/Phone-UI.png"   # You can set this to your own image
    if config.skipping:
        imagebutton:
            xanchor 0.0
            yanchor 0.0
            xpos 100
            ypos 73
            focus_mask True
            idle "Phone UI/max_speed_active.png"
            hover "maxSpeed"
            action [toggle_skipping, renpy.restart_interaction]
            # The restart_interaction makes it so the Max Speed button
            # is visibly toggled after you press it
    else:
        imagebutton:
            xanchor 0.0
            yanchor 0.0
            xpos 100
            ypos 73
            focus_mask True
            idle "Phone UI/max_speed_inactive.png"
            hover "noMaxSpeed"
            action [toggle_skipping, renpy.restart_interaction]

    

#************************************
# Chat Speed Modifiers
#************************************ 

## This speeds up/slows down the speed of the chat
## FIXME: sometimes skips dialogue/slows chat flow when clicking
image speed_txt = ParameterizedText(style = "speednum_style")

label speed_num_label:
    python:
        global pv  
        if pv <= 0.45:
            speednum = "9"
        elif pv <= 0.54:
            speednum = "8"
        elif pv <= 0.63:
            speednum = "7"
        elif pv <= 0.72:
            speednum = "6"
        elif pv <= 0.81:
            speednum = "5"
        elif pv <= 0.90:
            speednum = "4"
        elif pv <= 0.99:
            speednum = "3"
        elif pv <= 1.08:
            speednum = "2"
        elif pv <= 1.17:
            speednum = "1" 
        else:
            speednum = "!!"
    hide speed_txt onlayer hack
    show speed_txt "{size=30}SPEED{/size}\n [speednum]" onlayer hack at speed_msg
    return


#************************************
# View CGs
#************************************            
default close_visible = True

label viewCG:
    $ close_visible = True
    hide screen clock_screen
    call screen viewCG_fullsize
    show screen clock_screen
    return
    
image close_button = "CGs/close-overlay.png"

## This is the screen where you can view a full-sized CG when you
## click it in the chatroom. It has a working "Close" button
## that appears/disappears when you click the CG
## It can be fairly easily adapted to show CGs in a gallery as well
screen viewCG_fullsize:
    imagebutton:
        xalign 0.5
        yalign 0.5
        focus_mask True
        idle fullsizeCG
        action ToggleVariable("close_visible", False, True)
        
    if close_visible:
        imagebutton:
            xalign 0.5
            yalign 0.0
            focus_mask True
            idle "close_button"
            if pre_choosing:
                action [Call("answer")]
            else:
                action [Call("play")]
        
        text "Close" style "CG_close"


#************************************
# Save & Exit
#************************************ 
   
# Call this label to show the save & exit sign
label save_exit:
    $ addchat("answer","",0)
    call screen save_and_exit
    return

    
image save_exit = "Phone UI/Save&Exit.png"  
image signature = "Phone UI/signature01.png"
image heart_hg = "Phone UI/heart-hg-sign.png"
        
# This is the screen that shows Save & Exit at the bottom
screen save_and_exit:
    imagebutton:
        xanchor 0.0
        yanchor 0.0
        xpos 0
        ypos 1220
        focus_mask True
        idle "save_exit"
        action [ToggleVariable("choosing", False, True), Call("press_save_and_exit"), Return()]
        
label press_save_and_exit:
    call screen signature_screen
    return

# This shows the signature screen, which records your total heart points
# It shows hourglass points as well but currently there is no variable
# tallying how many hourglasses you get in a chatroom
# TODO: Hourglass points
screen signature_screen:
    image "save_exit" ypos 1220
    if choosing:
        image "Phone UI/choice_dark.png"
    image "signature" xalign 0.5 yalign 0.5
    image "heart_hg" xalign 0.5 ypos 650
    text "This conversation will be archived in the RFA records." style "save_exit_text" yalign 0.46
    text "I hereby agree to treat this conversation as confidential." style "save_exit_text" yalign 0.56
    
    imagebutton:
        xalign 0.5
        yanchor 0.0
        ypos 780
        focus_mask True
        idle "Phone UI/sign-button.png"
        activate_sound "sfx/UI/end_chatroom.mp3"
        hover "Phone UI/sign-button-clicked.png"
        action [SetVariable("chatroom_hp", 0), Call("start")]
    
    text "sign" style "sign" 
    text "[chatroom_hp]" style "points" xalign 0.385
    text "0" style "points" xalign 0.73
    
#************************************
# Chat Setup
#************************************ 

# This simplifies things when you're setting up a chatroom,
# so call it when you're about to begin
# If you pass it the name of the background you want (enclosed in
# single ' or double " quotes) it'll set that up too
# Note that it automatically clears the chatlog, so if you want
# to change the background but not clear the messages on-screen,
# you'll also have to pass it 'False' as its second argument
label chat_begin(background=None, clearchat=True, resetHP=True):
    $ global pv
    if clearchat:
        $ chatlog = []
        $ pv = 0.8
    if resetHP:
        $ chatroom_hp = 0
    show screen phone_overlay
    show screen clock_screen
    show screen messenger_screen 
    show screen pause
    # Fills the beginning of the screen with 'empty space' so the messages begin
    # showing up at the bottom of the screen (otherwise they start at the top)
    if clearchat:
        $ addchat("filler","\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",0)
    
    # Sets the correct background and nickname colour
    # You'll need to add other backgrounds here if you define
    # new ones
    if background == "morning":
        scene bg morning
        $ nickColour = black
    elif background == "noon":
        scene bg noon
        $ nickColour = black
    elif background == "evening":
        scene bg evening
        $ nickColour = black
    elif background == "night":
        scene bg night
        $ nickColour = white
    elif background == "earlyMorn":
        scene bg earlyMorn
        $ nickColour = white
    elif background == "hack":
        scene bg hack
        $ nickColour = white
    elif background == "redhack":
        scene bg redhack
        $ nickColour = white
    return
        
#************************************
# Hack Scrolls
#************************************
# You can call this when you want to display the green
# scrolled hacking effect
# Don't forget to show your desired background after calling
# the hack screen or pass the background name to chat_begin

image hack scroll: 
    "Hack-Long.png"
    subpixel True
    yalign 0.0
    linear 1.0 yalign 1.0
    yalign 0.0
    linear 1.0 yalign 1.0
    
image redhack scroll:
    "Hack-Red-Long.png"
    subpixel True
    yalign 0.0
    linear 1.0 yalign 1.0
    yalign 0.0
    linear 1.0 yalign 1.0
    
label hack:
    $ addchat("answer","",0)
    scene black onlayer hack
    show hack scroll at flicker onlayer hack
    $ renpy.pause(0.72, hard=True)
    show hack scroll at flicker onlayer hack
    $ renpy.pause(0.72, hard=True)
    hide hack scroll onlayer hack
    hide black onlayer hack
    return
    
label redhack:
    $ addchat("answer","",0)
    scene black onlayer hack
    show redhack scroll at flicker onlayer hack
    $ renpy.pause(0.72, hard=True)
    show redhack scroll at flicker onlayer hack
    $ renpy.pause(0.72, hard=True)
    hide redhack scroll onlayer hack
    hide black onlayer hack
    return
    
# These are the special "banners" that crawl across the screen
# Just call them using "call banner_well" etc

#************************************
# Banners
#************************************
image banner annoy:
    "Banners/Annoy/annoy_0.png"
    0.12
    "Banners/Annoy/annoy_1.png"
    0.12
    "Banners/Annoy/annoy_2.png"
    0.12
    "Banners/Annoy/annoy_3.png"
    0.12
    "Banners/Annoy/annoy_4.png"
    0.12
    "Banners/Annoy/annoy_5.png"
    0.12
    
image banner heart:
    "Banners/Heart/heart_0.png"
    0.12
    "Banners/Heart/heart_1.png"
    0.12
    "Banners/Heart/heart_2.png"
    0.12
    "Banners/Heart/heart_3.png"
    0.12
    "Banners/Heart/heart_4.png"
    0.12
    "Banners/Heart/heart_5.png"
    0.12
        
image banner lightning:
    "Banners/Lightning/lightning_0.png"
    0.12
    "Banners/Lightning/lightning_1.png"
    0.12
    "Banners/Lightning/lightning_2.png"
    0.12
    "Banners/Lightning/lightning_3.png"
    0.12
    "Banners/Lightning/lightning_4.png"
    0.12
    "Banners/Lightning/lightning_5.png"
    0.12
    
image banner well:
    "Banners/Well/well_0.png"
    0.12
    "Banners/Well/well_1.png"
    0.12
    "Banners/Well/well_2.png"
    0.12
    "Banners/Well/well_3.png"
    0.12
    "Banners/Well/well_4.png"
    0.12
    "Banners/Well/well_5.png"
    0.12
    
label banner_lightning:
    show banner lightning at truecenter onlayer heart
    $ addchat("answer","",0.72)
    hide banner lightning onlayer heart
    return
    
label banner_heart:
    show banner heart at truecenter onlayer heart
    $ addchat("answer","",0.72)
    hide banner heart onlayer heart
    return
    
label banner_well:
    show banner well at truecenter onlayer heart
    $ addchat("answer","",0.72)
    hide banner well onlayer heart
    return
    
label banner_annoy:
    show banner annoy at truecenter onlayer heart
    $ addchat("answer","",0.72)
    hide banner annoy onlayer heart
    return
    
    
#************************************
# Input Screen
#************************************
    
# This is just the screen you see when the program
# prompts you to enter a username
screen input(prompt, defAnswer = ""):

    window style "input_window":
        text prompt style "input_prompt"
        input id "input" default defAnswer style "input_answer"
        
#************************************
# Countdown Screen
#************************************

# Not actually in MysMe; this is just a screen to test out timed responses
# Could be a neat game mechanic
screen countdown(timer_jump, time=5): # I set a default reaction time of 5 seconds
    timer time repeat False action [ Hide('countdown'), Jump(timer_jump) ]
    bar value AnimatedValue(0, time, time, time) at alpha_dissolve

screen hidden_countdown(time=5): # I set a default reaction time of 5 seconds
    timer time repeat False action [ Hide('hidden_countdown'), Return ]
    bar value AnimatedValue(0, time, time, time) at alpha_dissolve
        
        
screen answer_countdown(time=5): # I set a default reaction time of 5 seconds
    timer time repeat False action [ Hide('answer_countdown'), Hide('continue_answer_button'), ToggleVariable("timed_choose", False, True) ]
    bar value AnimatedValue(0, time, time, time) at alpha_dissolve
        
#************************************
# Continue Answer
#************************************

# Some experiments with getting the chat to continue while you come up with a response

default timed_choose = False

label continue_answer(themenu, time=5):
    $ timed_choose = True
    show screen answer_countdown(time)
    hide screen viewCG
    $ pre_choosing = True
    show screen continue_answer_button(themenu)
    return

        
screen continue_answer_button(themenu):
    zorder 4
    image "answerbutton" ypos 1220
    imagebutton:
        xanchor 0.0
        yanchor 0.0
        xpos 0
        ypos 1220
        focus_mask None
        idle "Phone UI/answer_transparent.png"
        activate_sound "sfx/UI/answer_screen.mp3"
        action [ToggleVariable("choosing", False, True), Hide('continue_answer_button'), Jump(themenu)] 
    
    
    
    
    
    
    
    