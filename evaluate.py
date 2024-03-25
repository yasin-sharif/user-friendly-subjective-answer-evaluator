import numpy as np
import pandas as pd
import loading_functions as lf
import helping_functions as hf

def automate(filename):
    marks=[]
    index=0
    df=pd.read_excel(filename)
    while True:
        try:
            stu_ans=df.iloc[index,1]
            solution=df.iloc[index,2]
            keywords=df.iloc[index,3]
            limit=df.iloc[index,4]
            index=index+1

            # print('writing response to files')
            f = open("answer_temp.txt", "w")
            f.write(stu_ans)
            f.close()
            f = open("temp_keywords.txt", "w")
            f.write(keywords)
            f.close()
            f = open("keysentence_temp.txt", "w")
            f.write(solution)
            f.close()
            
            ans_words, ans_vect, ans_sent, ans_sent_vect, key_text, key_vect, keysent_text, keysent_vect =lf.load()
            
            # print(ans_words,ans_sent,key_text,keysent_text)
            #loading all the data which will be preprocessed before loading
            #print(ans_words)
            #print(ans_sent)
            #print(key_text)
            #print(keysent_text)
            '''
            percentage of keyword present
            average distance between keywords and answer words
            average similarity between keysentence words and answer sentence words
            '''
            grade_vector=[0.0, 0.0, 0.0]          # vector to store answer parameters


            def percent_key_present():                       # function to find percentage of keywords present
                count=0
                for keyword in key_text:
                    for word in ans_words:
                        if word==keyword:
                            count+=1
                            break
                accuracy=(count/(len(key_text)))
                grade_vector[0]=accuracy


            def average_vector_distance():      # function to find avg of min distance of keywords and answer words
                summ=0
                for keyword_vec in key_vect:
                    absmin=hf.vector_distance(ans_vect[0],keyword_vec)  # initial reference
                    i=0
                    min_index=0
                    for ans in ans_vect:
                        temp_distance=hf.vector_distance(ans,keyword_vec)
                        if temp_distance<absmin:
                            absmin=temp_distance
                            min_index=i
                        i=i+1
                    summ=summ+absmin
                grade_vector[1]=(summ/len(key_vect))

                            
            def average_similarity():           # function to calculate average similarities between key sentence words and answer sentence words
                summ=0.0
                for line_key in keysent_text:
                    words_key=line_key.split()
                    max_match=0.0
                    for line_ans in ans_sent:
                        words_ans=line_ans.split()
                        common_words=[]
                        for w in words_key:
                            if w in words_ans:
                                common_words.append(w)
                        current_match=len(common_words)/len(words_key)
                        if current_match>max_match:
                            max_match=current_match
                    summ=summ+max_match
                grade_vector[2]=(summ/len(keysent_text))

                
            percent_key_present()
            average_vector_distance()
            average_similarity()

            temp_vector=np.zeros((3,1))     # creates 3x1 dimension with 0
            
            for i in range(3):              # copying the grade vector to temp_vector
                temp_vector[i][0]=grade_vector[i]
            if temp_vector[1]>3.0 and temp_vector[1]<4.0 :
                temp_vector[1]=temp_vector[1]-1.20
            elif temp_vector[1]>4.0 and temp_vector[1]<5.0 :
                temp_vector[1]=temp_vector[1]-1.70
            elif temp_vector[1]>5.0 and temp_vector[1]<6.0 :
                temp_vector[1]=temp_vector[1]-2.20
            elif temp_vector[1]>6.0 and temp_vector[1]<7.0 :
                temp_vector[1]=temp_vector[1]-2.70
            elif temp_vector[1]>7.0 and temp_vector[1]<8.0 :
                temp_vector[1]=temp_vector[1]-3.20
            elif temp_vector[1]>8.0 and temp_vector[1]<9.0 :
                temp_vector[1]=temp_vector[1]-3.70
            elif temp_vector[1]>9.0 and temp_vector[1]<10.0 :
                temp_vector[1]=temp_vector[1]-4.20
        

            def determine_raw_match(match):
                p1,p2,p3=(grade_vector[0],grade_vector[1],grade_vector[2])


                if match>=0.85:
                    match=1.0
                elif match<0.85 and match>=0.825:
                    match=0.95
                elif match<0.825 and match>=0.80:
                    match=0.90
                elif match<0.775 and match>=0.750:
                    match=0.85
                elif match<0.750 and match>=0.725:
                    match=0.80
                elif match<0.725 and match>=0.700:
                    match=0.75
                elif match<0.700 and match>=0.650:
                    match=0.70
                elif match<0.650 and match>=0.600:
                    match=0.65
                elif match<0.600 and match>=0.550:
                    match=0.60
                elif match<0.550 and match>=0.500:
                    match=0.55
                elif match<0.500 and match>=0.450:
                    match=0.50
                elif match<0.450 and match>=0.400:
                    match=0.45
                elif match<0.400 and match>=0.350:
                    match=0.40
                elif match<0.350 and match>=0.300:
                    match=0.35
                elif match<0.300 and match>=0.250:
                    match=0.30
                elif match<0.250 and match>=0.200:
                    match=0.25
                elif match<0.200 and match>=0.150:
                    match=0.20
                elif match<0.150 and match>=0.100:
                    match=0.10
                else:
                    match=0.0

                return match
                    

            def mark_suggest(percent):
                mark=limit*(percent/100)      # eg: 1.8 left=1, right=0.8
                left=int(mark)
                right=mark-left
                if right<0.3:
                    return left
                elif right>0.3 and right<0.8:
                    return left+0.5
                else:
                    return left+1.0
            
            raw_match=hf.predict_matching(temp_vector)
            p_mat=determine_raw_match(raw_match)
            print('Graded vector:--------',grade_vector)
            print('Tuned vector:---------',temp_vector)

            p_key_match=float((temp_vector[0]+temp_vector[2])*50)
            p_semant_match=p_mat*100
            mark=mark_suggest(p_semant_match)
            marks.append(mark)
                
            print('Key matching:---------',p_key_match,'%')
            print('Semantic matching:----', p_semant_match,'%')
            print('Mark suggested:-------',mark)
            #return p_semant_match
        
        except IndexError:
            break

    df['marks']=marks
    df.to_excel('response.xlsx',index=False)
    return index


def evaluate(stu_ans,solution,keywords):

    #limit=int(input("Enter question's mark limit: "))
    limit=2

    # print('writing response to files')
    f = open("answer_temp.txt", "w")
    f.write(stu_ans)
    f.close()
    f = open("temp_keywords.txt", "w")
    f.write(keywords)
    f.close()
    f = open("keysentence_temp.txt", "w")
    f.write(solution)
    f.close()
    
    ans_words, ans_vect, ans_sent, ans_sent_vect, key_text, key_vect, keysent_text, keysent_vect =lf.load()
    
    print(ans_words,'\n','\n',ans_sent,'\n','\n',key_text,'\n','\n',keysent_text)
    #loading all the data which will be preprocessed before loading
    #print(ans_words)
    #print(ans_sent)
    #print(key_text)
    #print(keysent_text)
    '''
    percentage of keyword present
    average distance between keywords and answer words
    average similarity between keysentence words and answer sentence words
    '''
    grade_vector=[0.0, 0.0, 0.0]          # vector to store answer parameters


    def percent_key_present():                       # function to find percentage of keywords present
        count=0
        for keyword in key_text:
            for word in ans_words:
                if word==keyword:
                    count+=1
                    break
        accuracy=(count/(len(key_text)))
        grade_vector[0]=accuracy


    def average_vector_distance():      # function to find avg of min distance of keywords and answer words
        summ=0
        for keyword_vec in key_vect:
            absmin=hf.vector_distance(ans_vect[0],keyword_vec)  # initial reference
            i=0
            min_index=0
            for ans in ans_vect:
                temp_distance=hf.vector_distance(ans,keyword_vec)
                if temp_distance<absmin:
                    absmin=temp_distance
                    min_index=i
                i=i+1
            summ=summ+absmin
        grade_vector[1]=(summ/len(key_vect))

                    
    def average_similarity():           # function to calculate average similarities between key sentence words and answer sentence words
        summ=0.0
        for line_key in keysent_text:
            words_key=line_key.split()
            max_match=0.0
            for line_ans in ans_sent:
                words_ans=line_ans.split()
                common_words=[]
                for w in words_key:
                    if w in words_ans:
                        common_words.append(w)
                current_match=len(common_words)/len(words_key)
                if current_match>max_match:
                    max_match=current_match
            summ=summ+max_match
        grade_vector[2]=(summ/len(keysent_text))

        
    percent_key_present()
    average_vector_distance()
    average_similarity()

    temp_vector=np.zeros((3,1))     # creates 3x1 dimension with 0
    
    for i in range(3):              # copying the grade vector to temp_vector
        temp_vector[i][0]=grade_vector[i]
    if temp_vector[1]>3.0 and temp_vector[1]<4.0 :
        temp_vector[1]=temp_vector[1]-1.20
    elif temp_vector[1]>4.0 and temp_vector[1]<5.0 :
        temp_vector[1]=temp_vector[1]-1.70
    elif temp_vector[1]>5.0 and temp_vector[1]<6.0 :
        temp_vector[1]=temp_vector[1]-2.20
    elif temp_vector[1]>6.0 and temp_vector[1]<7.0 :
        temp_vector[1]=temp_vector[1]-2.70
    elif temp_vector[1]>7.0 and temp_vector[1]<8.0 :
        temp_vector[1]=temp_vector[1]-3.20
    elif temp_vector[1]>8.0 and temp_vector[1]<9.0 :
        temp_vector[1]=temp_vector[1]-3.70
    elif temp_vector[1]>9.0 and temp_vector[1]<10.0 :
        temp_vector[1]=temp_vector[1]-4.20
   

    def determine_raw_match(match):
        p1,p2,p3=(grade_vector[0],grade_vector[1],grade_vector[2])


        if match>=0.85:
            match=1.0
        elif match<0.85 and match>=0.825:
            match=0.95
        elif match<0.825 and match>=0.80:
            match=0.90
        elif match<0.775 and match>=0.750:
            match=0.85
        elif match<0.750 and match>=0.725:
            match=0.80
        elif match<0.725 and match>=0.700:
            match=0.75
        elif match<0.700 and match>=0.650:
            match=0.70
        elif match<0.650 and match>=0.600:
            match=0.65
        elif match<0.600 and match>=0.550:
            match=0.60
        elif match<0.550 and match>=0.500:
            match=0.55
        elif match<0.500 and match>=0.450:
            match=0.50
        elif match<0.450 and match>=0.400:
            match=0.45
        elif match<0.400 and match>=0.350:
            match=0.40
        elif match<0.350 and match>=0.300:
            match=0.35
        elif match<0.300 and match>=0.250:
            match=0.30
        elif match<0.250 and match>=0.200:
            match=0.25
        elif match<0.200 and match>=0.150:
            match=0.20
        elif match<0.150 and match>=0.100:
            match=0.10
        else:
            match=0.0

        return match
              

    def mark_suggest(percent):
        mark=limit*(percent/100)      # eg: 1.8 left=1, right=0.8
        left=int(mark)
        right=mark-left
        if right<0.3:
            return left
        elif right>0.3 and right<0.8:
            return left+0.5
        else:
            return left+1.0
    
    raw_match=hf.predict_matching(temp_vector)
    p_mat=determine_raw_match(raw_match)
    print('Graded vector:--------',grade_vector)
    print('Tuned vector:---------',temp_vector)

    p_key_match=float((temp_vector[0]+temp_vector[2])*50)
    p_semant_match=p_mat*100
    mark=mark_suggest(p_semant_match)
        
    print('Key matching:---------',p_key_match,'%')
    print('Semantic matching:----', p_semant_match,'%')
    print('Mark suggested:-------',mark)
    return [mark,p_key_match,p_semant_match]