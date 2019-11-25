##############################################
## This screen allows you to view replays
## of chatrooms and phone calls you've already
## seen in-game
###############################################

image history_button = Frame('Menu Screens/History/main02_button_01.png',
                                49, 52, 270, 53)
image history_button_hover = Fixed('history_button', 
                            Transform('history_button', alpha=0.5))
image history_icon_album = 'Menu Screens/History/history_icon_album.png'
image history_icon_chat = 'Menu Screens/History/history_icon_chat.png'
image history_icon_call = 'Menu Screens/History/history_icon_call.png'
image history_icon_guest = 'Menu Screens/History/history_icon_guest.png'

## This screen lets you view the album or the chat history
screen select_history():

    tag menu

    use menu_header("History", Show('main_menu', Dissolve(0.5))):

        style_prefix "select_history" 
        window: 
            hbox:      
                spacing 30    
                button:
                    action Show('photo_album', Dissolve(0.5))
                    hbox:
                        add 'history_icon_album' yalign 0.5
                        text 'ALBUM'
                button:
                    action Show('select_history_route', Dissolve(0.5))
                    hbox:
                        add 'history_icon_chat' yalign 0.5
                        text "CHAT HISTORY" 


style select_history_hbox:
    is default
    spacing 15
    align (0.5, 0.5)

style select_history_button:
    is default
    align (0.5, 0.2)
    background 'history_button'
    hover_background 'history_button_hover'
    padding (40,20,40,30)
    xysize (318,114)

style select_history_text:
    is default
    color "#fff" 
    size 28 
    xsize 50 
    font sans_serif_1b
    align (0.5, 0.5)

style select_history_window:
    is default
    xysize (740, 1100)
    align (0.5, 0.5)


default which_history_route = None

screen select_history_route():

    tag menu

    use menu_header("History", Show('main_menu', Dissolve(0.5))):

        style_prefix 'history_route'
        for route in all_routes:
            textbutton _(route.route_history_title + " Route"):
                action [SetVariable('which_history_route', route.route),
                        Show('chat_select', days=route.route)]

style history_route_button:
    is other_settings_end_button
    padding (30,30)

style history_route_button_text:
    is mode_select

image history_chat_active = Frame("Menu Screens/History/msgsl_bg_active.png", 10,10)
image history_chat_inactive = Frame("Menu Screens/History/msgsl_bg_inactive.png", 10,10)
image history_chat_participated = Transform("Menu Screens/History/chat_history_participated.png", zoom=0.8)
image history_chat_alone = Transform("Menu Screens/History/chat_history_alone.png", zoom=0.8)

init python:

    # This function lets the program know whether or not it
    # should display this particular item in the history screen
    def display_history(item, index, archive_list):
        global persistent
        # First check if it's a chatroom
        if (isinstance(item, Chat_History)
                or isinstance(item, store.Chat_History)):
            # This chatroom is only visible if one or both
            # of its expired or regular chats have been seen
            return (persistent.completed_chatrooms.get(item.expired_chat)
                    or persistent.completed_chatrooms.get(item.chatroom_label))
        # Check if it's a VN
        if (isinstance(item, VN_Mode) or isinstance(item, store.VN_Mode)):
            # Again, only visible if this VN's label has been seen
            return persistent.completed_chatrooms.get(item.vn_label)

        # Otherwise, it's a text label
        # We need to check if the item immediately after it is visible
        if index < len(archive_list)-1:
            return display_history(archive_list[index+1], index+1, archive_list)

        # Otherwise all has failed so we assume we don't display it
        return False

    ## Returns true if there is at least one label in these two lists
    ## that has been seen
    def calls_available_history(calls):
        for c in calls:
            if persistent.completed_chatrooms.get(c):
                return True
        return False

default expired_replay = False
# This is a dictionary that holds a giant list of all the
# labels the player has seen/played through
default persistent.completed_chatrooms = {}

image contact_darken = "Menu Screens/History/contact_darken.png"
image call_incoming_outline = "Menu Screens/History/call_icon_incoming_outline.png"
image call_outgoing_outline = "Menu Screens/History/call_icon_outgoing_outline.png"

screen chatroom_item_history(chatroom):

    python:
        played_reg = False
        played_expired = False
        vn_played = False
        my_vn = False
        is_chatroom = (isinstance(chatroom, Chat_History)
                        or isinstance(chatroom, store.Chat_History))
        is_vn = (isinstance(chatroom, VN_Mode)
                    or isinstance(chatroom, store.VN_Mode))
                    
        # Now we set up some variables to see whether or not the player
        # has seen one version of this chatroom or not
        if is_chatroom:
            my_vn = chatroom.vn_obj
            played_reg = persistent.completed_chatrooms.get(
                                                chatroom.chatroom_label)
            played_expired = persistent.completed_chatrooms.get(
                                                chatroom.expired_chat)
            if my_vn:
                vn_played = persistent.completed_chatrooms.get(my_vn.vn_label)
            else:
                vn_played = True
        elif is_vn:
            my_vn = chatroom
            vn_played = persistent.completed_chatrooms.get(my_vn.vn_label)
        else:
            played_reg = True
            played_expired = True
            vn_played = True

        # This determines if there are enough participants
        # in this chat to make the viewport scroll automatically
        if is_chatroom and chatroom.original_participants:
            if len(chatroom.original_participants) > 4:
                part_anim = participant_scroll
            else:
                part_anim = null_anim
        else:
            part_anim = null_anim

        replay_dictionary = {'observing': True,
                            'current_chatroom': chatroom,
                            'current_day': current_day,
                            'current_day_num': current_day_num,
                            'name': persistent.name}

        expired_replay_dictionary = {'expired_replay': True,
                            'observing': True,
                            'current_chatroom': chatroom,
                            'current_day': current_day,
                            'current_day_num': current_day_num,
                            'name': persistent.name}

    null height 10
    if not is_chatroom and not is_vn:
        text chatroom color "#fff" font sans_serif_1b xalign 0.575
    elif is_chatroom:
    
        
        window:
            xoffset 70
            xysize (620, 160)
            xalign 0.0
            background 'chat_active'
            # These are the two buttons to replay the chat
            hbox:
                align (0.98,0.83)
                spacing 10
                button:
                    xysize (80,80)
                    if played_expired:
                        background 'history_chat_active'  
                        hover_foreground '#fff5'                      
                        action Replay(chatroom.expired_chat, 
                                        scope=expired_replay_dictionary)
                    else:
                        background Fixed('history_chat_inactive', "#000c")
                        foreground "#0003"
                        action Show("confirm", message=("You have not yet"
                            + " viewed this chat in-game."),
                        yes_action=Hide('confirm'))
                    add 'history_chat_alone' align (0.5, 0.5)
                    if not played_expired:
                        add 'plot_lock' align (0.5, 0.5)
                button:
                    xysize(80,80)
                    if played_reg:
                        hover_foreground '#fff5'
                        background 'history_chat_active'                        
                        action Replay(chatroom.chatroom_label,
                                        scope=replay_dictionary)
                    else:
                        background Fixed('history_chat_inactive', "#000c")
                        foreground "#0003"
                        action Show("confirm", message=("You have not yet"
                            + " viewed this chat in-game."),
                        yes_action=Hide('confirm'))
                    add 'history_chat_participated' align (0.5, 0.5)
                    if not played_reg:
                        add 'plot_lock' align (0.5, 0.5)
                    
                
            vbox:
                yoffset 3
                spacing 18
                # This box displays the trigger time and
                # title of the chatroom; optionally at
                # a scrolling transform so you can read
                # the entire title
                hbox:
                    spacing 30
                    window:
                        xysize (75,27)
                        xoffset 77
                        yoffset 13
                        text chatroom.trigger_time:
                            color '#fff' 
                            size 27 
                            xalign 0.5 yalign 0.5 
                            text_align 0.5
                    viewport:
                        yoffset 13
                        xoffset 77                
                        xysize(400,27)
                        if len(chatroom.title) > 30: 
                            window:
                                xysize(400,27)
                                text chatroom.title at chat_title_scroll:
                                    color '#fff' 
                                    size 25 
                                    xalign 0.0 yalign 0.5 
                                    text_align 0.0 
                                    layout 'nobreak' 
                        else:
                            text chatroom.title:
                                color '#fff' 
                                size 25 
                                xalign 0.0 yalign 0.5 
                                text_align 0.0 
                                layout 'nobreak'
                # Shows a list of all the people who were in/
                # are in this chatroom
                viewport:
                    xysize(530, 85)
                    yoffset 13
                    xoffset 77            
                    yalign 0.5
                    window:
                        xysize(355, 85)
                        hbox at part_anim:
                            yalign 0.5
                            spacing 5
                            if chatroom.original_participants:
                                for person in chatroom.original_participants:
                                    if person.participant_pic:
                                        add person.participant_pic

            

    # If there's a VN object, we display it now
    if my_vn and not my_vn.party:
        window:
            xysize(700, 160)
            xalign 0.0
            xoffset 10
            
            has hbox
            add 'vn_marker'
            
            button:
                xysize(555, 126)
                foreground 'vn_active'
                hover_foreground 'vn_active_hover'
                activate_sound 'audio/sfx/UI/select_vn_mode.mp3'
                action [Preference("auto-forward", "disable"),
                        Replay(my_vn.vn_label,
                                scope=replay_dictionary)] 
                
                if my_vn.who:
                    add 'vn_' + my_vn.who.file_id xoffset -5
                else:
                    add 'vn_other' xoffset -5
    
    # It's the VN that leads to the party
    if my_vn and my_vn.party:
        window:
            xysize(600, 300)
            xalign 1.0
        
            button:
                xysize(463, 185)
                xalign 0.5
                yalign 0.5
                background 'vn_party'              
                activate_sound 'audio/sfx/UI/select_vn_mode.mp3'
                if my_vn.available and can_play:
                    hover_foreground 'vn_party'
                    # Note: afm is ~30 at its slowest, 0 when it's off, 
                    # and 1 at its fastest
                    action [Preference("auto-forward", "disable"), 
                            Replay(my_vn.vn_label,
                                scope=replay_dictionary)]  

    # Now we add an hbox of the phone calls available around this chatroom
    if (is_chatroom and (chatroom.incoming_calls_list 
                or chatroom.outgoing_calls_list)
            and calls_available_history(chatroom.incoming_calls_list + 
                                            chatroom.outgoing_calls_list)):
        hbox:
            xalign 1.0
            xoffset -40
            add Transform('call_mainicon', size=(60,60)) align (0.5, 0.75)
            for c in chatroom.incoming_calls_list:
                # If the player has seen this phone call
                if persistent.completed_chatrooms.get(c):
                    button:
                        background Transform(c.split('_')[-1] + '_contact', 
                                                        size=(85,85))
                        hover_background Fixed(Transform(c.split('_')[-1]
                                        + '_contact', size=(85,85)),
                                        Transform(c.split('_')[-1]
                                        + '_contact', size=(85,85)))
                        add Transform('contact_darken', 
                                    size=(85,85), alpha=0.3) align (0.5,0.5)
                        add 'call_incoming_outline' align (1.0, 1.0)
                        xysize (85,85)
                        action Replay(c, scope=replay_dictionary)
            for c in chatroom.outgoing_calls_list:
                # If the player has seen this phone call
                if persistent.completed_chatrooms.get(c):
                    button:
                        background Transform(c.split('_')[-1] + '_contact', 
                                                        size=(85,85))
                        hover_background Fixed(Transform(c.split('_')[-1]
                                        + '_contact', size=(85,85)),
                                        Transform(c.split('_')[-1]
                                        + '_contact', size=(85,85)))
                        add Transform('contact_darken', 
                                    size=(85,85), alpha=0.3) align (0.5,0.5)
                        add 'call_outgoing_outline' align (1.0, 1.0)
                        xysize (85,85)
                        action Replay(c, scope=replay_dictionary)
                       
                
            
        


style timeline_button:
    xysize (181,62)    
    text_align 0.5
    xalign 0.05
    yalign 0.5
    background 'vn_time_bg' padding (20,20)

style timeline_button_text:
    color '#fff'
    size 40
    xalign 0.5

style timeline_hbox:
    xysize (620, 160)
    xoffset 70
    xalign 0.0


