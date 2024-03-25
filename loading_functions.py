import numpy as np
from gensim.models.keyedvectors import KeyedVectors as ww
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from formatter_keywords import format_keyword
import formatter_answer as f_ans
import formatter_solution as f_sol

print('--> model loading')
# loading google's pretrained word vector model
model = ww.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True, limit=500000)
print('--> model loaded')


def pre_process() :
    print('--> preprocessing starts')
    lemmatizer = WordNetLemmatizer()                # to lemmatize the words
    stop_words = set(stopwords.words('english'))    # getting a list of all stop words
    stop_words.remove('same')

    format_keyword()
    f_ans.format_answer()
    f_sol.format_solution()

    print('--> keywords ... ',end='')
    # pre-processing of keywords
    f_key=open("keywords.txt")
    s1=f_key.read().strip().split(",")  # strip for removing whitespaces
    for i in range(len(s1)):
        s1[i]=s1[i].lower()             # converting all words to lowercase
    f_key=open("keywords.txt","w")

    length=len(s1)
    for i in range(len(s1)):          
        word=s1[i]
        if word not in stop_words :
            lemtized=word
            for c in ["n", "a", "v", "r", "s"]:     # nound, adjective, verb, adverb, satellite adjective
                lemtized=lemmatizer.lemmatize(lemtized, pos=c)                
            f_key.write(lemtized)       # writing back the lemmatized keyword
        if i<(length-1):
            f_key.write(",")
        #f_key.write(',')
    print('processed')            


    print('--> key sentences ... ',end='')
    # pre-processing of key sentences
    f_keysen=open("keysentence.txt")    
    sentences=[]
    liist=[]    
    for line in f_keysen:
        sentences.append(line)      # getting each sentences
        
    for sent in sentences:          # lemmatizing each sentences
        s1=sent.strip().split()
        new_sent=""        
        for i in range(len(s1)) :
            s1[i]=s1[i].lower()
            
        for i in range(len(s1)) :
            w=s1[i]
            if w not in stop_words :
                lemtized=w
                for c in ["n", "a", "v", "r", "s"] :
                    lemtized=lemmatizer.lemmatize(lemtized, pos=c)                    
                new_sent=new_sent+" "+lemtized                
        liist.append(new_sent.lstrip())     # removes leading whitespace at the left

    f_keysen=open("keysentence.txt", "w")    
    for s in liist :
        f_keysen.write(s)
        f_keysen.write("\n")
    print('processed')            
        

    print('--> answers ... ',end='')
    # pre-processing of answer
    f_answer=open("answer.txt")
    s=f_answer.read().strip().replace('\n',' ')
    
    li=sent_tokenize(s)     # sentence based tokenizing
    liist=[]
    for sent in li:         # lemmatizing each sentences
        s1=sent.replace('.',' ').strip().split()
        new_sent=""
        for i in range(len(s1)):
            s1[i]=s1[i].lower()
        for i in range(len(s1)):
            w=s1[i]
            if w not in stop_words:
                lemtized=w
                for c in ["n", "a", "v", "r", "s"] :
                    lemtized=lemmatizer.lemmatize(lemtized, pos=c)
                new_sent=new_sent+" "+lemtized
        liist.append(new_sent.lstrip())
        
    se=""
    for s in liist:
        se=se+s
        se=se+'. '
    f_answer=open("answer.txt", "w")
    f_answer.write(se)
    print('prosessed')            

    print('--> preprocessing ends')    


# finding the word vector for each word in the answer
def load_answer():
    f_answer=open("answer.txt")
    s=f_answer.read().strip().replace('.',' ').split()
    ans=list()
    words=list()
    for word in s:
        try:
            ans.append(model[word])         # uses only lower case words
            words.append(word)
        except:
            dump=0
    return (words,np.array(ans))            # return a list of words in answer and matrix of dim(n,300)
# returns=> answer words, word vector for each word


def load_answer_sent():
    ans_sent_vec=[]
    f_answer=open("answer.txt")
    s=f_answer.read().strip().split('.')
    lines=[]
    for line in s:
        lines.append(line.strip())
    for line in lines:
        temp_sentence=line.split()
        temp_vector=np.squeeze(np.zeros((1,300)))    # zeros will create a nested array, so squeeze will return the needed array
        for word in temp_sentence:
            try:
                temp_vector=temp_vector+model[word]       # cumulative vector sum of all words in a sentence
            except:
                None
        ans_sent_vec.append(temp_vector)        
    return (lines,ans_sent_vec)
# returns=> each line of answer, cummulative word vector for each line


def load_keywords():
    f_key=open("keywords.txt")
    s1=f_key.read().strip().split(",")
    for i in range(len(s1)) :
        s1[i]=s1[i]
    vector=list()
    keywords=list()
    for word in s1:
        try:
            vector.append(model[word])
            keywords.append(word)
        except:
            None
    return (keywords,vector)
# returns=> keywords, word vector for each keyword


def load_keysent():
    f_keysen=open("keysentence.txt")
    s1=[]
    for line in f_keysen:
        s1.append(line.strip())
    return s1
# returns=> sentences of key sentences


def load_keysent_vec():
    f_keysen=open("keysentence.txt")
    s1=list()
    for line in f_keysen:
        temp_s=line.strip().split()
        count=0
        temp_v=np.squeeze(np.zeros((1,300)))
        for word in temp_s:
            try :
                temp_v=temp_v+model[word]
            except :
                count=count+1
        s1.append(temp_v/(len(temp_s)-count))
    return s1
# returns=> cummulative word vector for each key sentences


def load():
    pre_process()
    x1=load_answer()
    x2=load_answer_sent()
    x3=load_keywords()

    return (x1[0],x1[1],x2[0],x2[1],x3[0],x3[1],load_keysent(),load_keysent_vec())


    

    
