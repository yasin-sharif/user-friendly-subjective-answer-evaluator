def format_answer():
    temp=open('answer_temp.txt','r')
    file=open('answer.txt','w')
    isSpaceFound=False
    while True:
        char=temp.read(1)
        if char:
            num=ord(char)
            match num:
                case 32: 
                    if not isSpaceFound:
                        file.write(char)
                        isSpaceFound=True
                        
                case 9 | 10:
                    if not isSpaceFound:
                        file.write(" ");
                        isSpaceFound=True
                                    
                case _:
                    if num!=44:
                        file.write(char)
                        isSpaceFound=False

        else:
            break