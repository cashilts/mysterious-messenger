
#####################################
# View CGs
#####################################
    
default close_visible = True
default textmsg_CG = False
default album_CG = False
default CG_who = text_messages[0]

label viewCG(textmsg=False, album=False, album_info=[]):
    $ close_visible = True
    $ textmsg_CG = textmsg
    $ album_CG = album
    call screen viewCG_fullsize
    if album:
        call screen character_gallery(album_info[0], 
                                        album_info[1], 
                                        album_info[2])
    return
    
## This is the screen where you can view a full-sized CG when you
## click it. It has a working "Close" button that appears/disappears 
## when you click the CG

screen viewCG_fullsize:
    zorder 5
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
            # From the chatroom, before an answer button
            if pre_choosing and not textmsg_CG and not album_CG:
                action [Call("answer", from_cg=True)]
            # From a text message, not instant texting
            elif textmsg_CG and not persistent.instant_texting:
                action [Hide("viewCG_fullsize"), Show("text_message_screen", 
                                                            the_msg=CG_who)]
            # From an instant text message, before an answer button
            elif textmsg_CG and pre_choosing:
                action [Hide("viewCG_fullsize"), 
                        Show("inst_text_message_screen", 
                            the_sender=CG_who), 
                        Call("answer", from_cg=True)]
                
            # From an instant text message, not before an answer button
            elif textmsg_CG and inst_text:
                action [Hide("viewCG_fullsize"), 
                        Show("inst_text_message_screen", 
                            the_sender=CG_who), Call('play')]
            # Convo is over, just viewing CGs in a text message
            elif textmsg_CG:
                action [Hide("viewCG_fullsize"), 
                        Show("inst_text_message_screen", the_sender=CG_who)]
            # From the album
            elif album_CG:
                action [Hide('viewCG_fullsize'), Return()]
            # From the chatroom, not before an answer button
            else:
                action [Call("play")]
        
        text "Close" style "CG_close"