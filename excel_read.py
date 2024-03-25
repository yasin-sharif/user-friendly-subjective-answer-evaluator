import pandas as pd
df=pd.read_excel('response.xlsx')

index=0
while True:
    try:
        print(df.iloc[index,1])
        print(df.iloc[index,2])
        print(df.iloc[index,3])
        index=index+1
    except IndexError:
        break
