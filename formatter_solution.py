def format_solution():
    temp=open('keysentence_temp.txt','r')
    file=open('keysentence.txt','w')
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
                        file.write(" ")
                        isSpaceFound=True
                
                case 46:
                    file.write(chr(10))

                case _:
                    file.write(char)
                    isSpaceFound=False
        else:
            break