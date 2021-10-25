#IMPORTANT make sure to change the coordinates to fit your screen, any line that needs changing is marked with a #coords
import random,mouse,pyautogui,datetime,os,pytesseract,re,keyboard,time,win32api,win32con
from PIL import Image
#GUILD NAME!!! CHANGE THIS TO YOUR GUILD!
phrase_start = 'your guild name here'
phrases = [
    #These are the ones I use for my ads, feel free to use them too
    #index 0 is the actual phrase, index 1 is the weight (YES THE RNG IS WEIGHTED), and the third is to make groups that should not have dupes (i.e there can only be one with a 4 as the 3rd index)
    #the sorting and breaks is purely cosmetic
    #valid None
    ['Small Guild', 0.2, None],
    ['Dedicated Playerbase', 0.5, None],
    ['Looking to Grow', 0.3, None],
    ['1% Tax', 0.7, None],
    ['Faction War Bonuses', 0.65, None],
    ['Crafting Stations', 0.5, None],
    ['Laborers', 0.55, None],
    ['1v1 Tourneys', 0.4, None],
    ['0 Fame Requirement', 0.5, None],
    ['Discord Optional', 0.5, None],
    ['Friends', 0.3, None],
    ['+18', 0.5, None],
    ['English', 0.5, None],
    ['Thetford Based', 1, None],
    ['Guild Island', 0.4, None],
    #0 gameplay
    ['PVP', 0.5, 0],
    ['PVE', 0.5, 0],
    #1 gameplay pt2
    ['Gathering', 0.5, 1],
    ['Crafting', 0.5, 1],
    ['Dungeons', 0.5, 1],
    ['Hellgates', 0.5, 1],
    ['Faction Warfare', 0.4, 1],
    #4 new players
    ['New Players Welcome', 0.6, 4],
    ['Noobs Welcome', 0.6, 4],
    ['Players of All Skill Levels', 0.6, 4],
    ['All Players Welcome', 0.5, 4],
    #meme None
    ['NOT a Furry Guild', 0.2, None],
    ['Huge Balls', 0.02, None],
    ['Ballsack', 0.1, None],
    ['You Will Live To See Manmade Horrors Beyond Your Comprehension', 0.01, None],
    ['Die', 0.2, None],
    ['pls goth girls join', 0.08, None],
    ['Glorious China', 0.01, None],
    ['Piss', 0.02, None],
    ['Darren Korb', 0.02, None],
    #2 money
    ['We Just Like Money', 0.15, 2],
    ['Money', 0.2, 2],
    ['Money Moves', 0.2, 2],
    ['All About The Money', 0.2, 2],
    #3 status
    ['ELITE VETERAN Core', 0.10, 3],
    ['Literally Top Guild', 0.11, 3],
    #6 cats
    ['Floppa', 0.01, 6],
    ['Sogga', 0.01, 6],
    ['Bingus', 0.01, 6],
    ['Grozza', 0.01, 6],
    ]
#tells people to pm you, which is how the bot knows to invite
phrase_end = 'PM FOR INVITE'
#does something(?) important for the weight
weight = 0
for phrase in phrases:
    weight += phrase[1]
#oytesseract sucks and wont work without this
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#a randomizer to dodge action logs
def randomizer(int):
    return int + random.randrange(-25,25) * 0.01
#uh does something else important for the randomizer
def get_phrases(num):
    base = 0
    for phrase in phrases:
        base += phrase[1]
        if base / weight >= num:
            return phrases.index(phrase)

#generates a string of unique numbers coresponding to their index in the phrase list
#first iteration, doesn't account for weight or the second unique identifier
def msg_code():
    index = 0
    msg_list = []
    while index < len(phrases):
        ident = random.randint(0,(len(phrases)-1))
        if msg_list:
            match = False
            for item in msg_list:
                if int(ident) == int(item):
                    match = True
            if match == False:
                msg_list.append(ident)
                index += 1
        else:
            msg_list.append(random.randint(0,(len(phrases)-1)))
            index += 1
    return msg_list

#second iteration, works beautifully
#love this bastahd
def msg_code2():
    total_length = 0
    msg_list = []
    dupe_list = []
    first = True
    while total_length < 108:
        if first:
            rand1 = random.random()
            ident = get_phrases(rand1)
            msg_list.append(ident)
            total_length += len(phrases[ident][0])
            total_length += 3
            if phrases[ident][2]:
                dupe_list.append(phrases[ident][2])
            first = False
        else:
            rand1 = random.random()
            ident = get_phrases(rand1)

            add = True
            for number1 in msg_list:
                if ident == number1:
                    add = False
            for number2 in dupe_list:
                if phrases[ident][2] == number2:
                    add = False
            if (len(phrases[ident][0]) + total_length) > 113:
                add = False
                break
            if add:
                total_length += 3
                total_length += len(phrases[ident][0])
                dupe_list.append(phrases[ident][2])
                msg_list.append(ident)
    return msg_list

#turns the numbers into phrases and assembles the full message
#doesn't work because it was built for the first version of the last function
def assemble_msg(sequence):
    final_message = ''
    fm_list = []
    for num in sequence:
        fm_list.append(phrases[num])
    final_message += phrase_start
    final_message += ' | '
    for phrase in fm_list:
        if (len(phrase) + len(final_message)) < 145:
            final_message += phrase
            final_message += ' | '
    final_message += phrase_end
    return final_message

#does basically the same thing as the last function, with some parts moved to the previous function
def assemble_msg2(sequence):
    final_message = ''
    fm_list = []
    for num in sequence:
        fm_list.append(phrases[num][0])
    final_message += phrase_start
    final_message += ' | '
    for phrase in fm_list:
        final_message += phrase
        final_message += ' | '
    final_message += phrase_end
    return final_message

#click function, didn't work for some parts of the b0t
def click(x,y):
    mouse.move(x,y)
    time.sleep(randomizer(0.3))
    leftClick()
#a secondary click function using win32api cause how could that go wrong
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#opens chat and sends the generated message from before
def type_msg(msg):
    time.sleep(randomizer(0.4))
    keyboard.send('enter')
    time.sleep(randomizer(0.4))
    click(297,2134) #coords
    time.sleep(randomizer(0.3))
    click(295,2130) #coords
    time.sleep(randomizer(0.4))
    pyautogui.write(msg)
    time.sleep(randomizer(0.4))
    keyboard.send('enter')
    time.sleep(randomizer(0.4))

#takes a screenshot of the chat box and then reduces each message to just the username, returns as a list
def get_chat(user_list):
    if not user_list:
        user_list = []
    pyautogui.screenshot('chat.png',region=(0,1700,700,400)) #coords ; first two are the coordinates of the top left point, second two are the length from that point it will go. make this of the chat box only
    chat_im = Image.open('chat.png')
    result = pytesseract.image_to_string(chat_im)
    msg_split = result.split(':')
    for item in msg_split:
        from_ = re.search('from',item)
        if from_:
            span = (from_.span())[1]
            item = item[span:]
            item = item.strip()
            not_added = True
            for user in user_list:
                if user == item:
                    not_added = False
            count = 0
            for character in item:
                if character == 'l' or character == '1' or character == 'i' or character == 'L' or character == 'I':
                    count += 1
                if not character.isalnum():
                    not_added = False
                if character == 'é':
                    not_added = False
            if count > 5:
                not_added = False
            if len(item) > 16:
                not_added = False
            if not_added:
                user_list.append(item)
    return user_list

#the mouse clicks to invite someone to a guild
def invite(user):
    time.sleep(randomizer(1))
    keyboard.send('g')
    time.sleep(randomizer(1))
    click(131,1621) #coords
    time.sleep(randomizer(1))
    pyautogui.write(user)
    time.sleep(randomizer(1))
    print('invited',user)
    click(2122,1137) #coords
    time.sleep(randomizer(0.4))
    click(1911,1055) #coords
    time.sleep(randomizer(0.4))
    keyboard.send('g')
    time.sleep(randomizer(0.4))

#main function! on the first loop it sends an ad immediately, it then checks chat for any messages, if there are it grabs the username and invites them to the guild. when there are
#no more users to invite and 30 seconds have passed since the last ad it sends another ad and prints how many players have been invited and who they are
def main():
    time.sleep(5)
    sent_list = []
    user_list = []
    old_list = []
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    bung = True
    first = True
    while bung == True:
        if first:
            msg = assemble_msg2(msg_code2())
            type_msg(msg)
            print('ad sent!',msg)
            time1 = datetime.datetime.now()
            time21 = datetime.datetime.now()
            first = False
        user_list = get_chat(user_list)
        for player in user_list:
            player_found = False
            for old_player in old_list:
                if player == old_player:
                    player_found = True
            if not player_found:
                print('new PM from',player)
                old_list.append(player)
        #a2
        for user in user_list:
            sent = False
            if not sent_list:
                invite(user)
                sent_list.append(user)
                sent = True
            else:
                for player in sent_list:
                    if user == player:
                        sent = True
            if not sent:
                invite(user)
                sent_list.append(user)
        #another version of the few lines of code after it. no idea why it didnt work. I just redid it in a different order and it worked so idk
        # for user in user_list:
        #     print(user,':',user_list)
        #     sent = False
        #     if sent_list:
        #         print(sent_list)
        #         for sent in sent_list:
        #             if user == sent:
        #                 print(user,'already sent!')
        #                 sent = True
        #     if not sent_list:
        #         invite(user)
        #         sent_list.append(user)
        #         sent = True
        #     if not sent:
        #         invite(user)
        #         sent_list.append(user)
        time22 = datetime.datetime.now()
        duration2 = time22 - time21
        duration2 = duration2.total_seconds()
        time2 = datetime.datetime.now()
        duration = time2 - time1
        duration = duration.total_seconds()
        if int(duration2) >= randomizer(10):
            print(duration)
            time21 = datetime.datetime.now()
        if int(duration) >= randomizer(31):
            msg = assemble_msg2(msg_code2())
            type_msg(msg)
            print('ad sent!',msg)
            usr_list_msg = 'Invited '+str(len(user_list))+' : '
            for user in user_list:
                user_ap = user + ', '
                usr_list_msg += user_ap
            print(usr_list_msg)
            time1 = datetime.datetime.now()
if __name__ == "__main__":
    main()

#enjoy and message me with nay questions
