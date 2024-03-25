def format_keyword():
    temp=open('temp_keywords.txt','r')
    file=open('keywords.txt','w')
    isSpaceFound=False
    isCommaFound=False
    while True:
        char=temp.read(1)
        if char:
            num=ord(char)
            match num:
                case 32:
                    if not isSpaceFound and not isCommaFound:
                        file.write(',')
                        isSpaceFound=True
                        isCommaFound=True
                                    
                case 9 | 10:
                        if not isCommaFound:
                            file.write(",")
                            isSpaceFound=True
                            isCommaFound=True
                
                case 46:
                    file.write(",")
                    file.write(chr(10))

                case 44:
                    if not isCommaFound:
                        file.write(',')
                        isCommaFound=True

                case _:
                    file.write(char)
                    isSpaceFound=False
                    isCommaFound=False
        else:
            break