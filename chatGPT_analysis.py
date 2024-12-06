#code emotions text data using GPT-Sami (11, 2023)
import time
import json
import openai
import os
import pandas as pd

API_KEY = "XXXXX"
NUM_SCORES_CALCULATED = 467
engine = 'gpt-3.5-turbo'
openai.api_key = API_KEY
temp = 0


# def generate_emotional_prompt(phrases):
#     return f'How much effort did the writer put into crafting the supportive phrases on a 1-7 scale? Answer only with ' \
#            f'one number, with 1 being "minimal effort" and 7 being "significant effort." Here are the phrases: {phrases}. ' \
#            f'Please rate the independent phrases holistically.'
#
#
# def generate_direct_prompt(phrases):
#     return f'The supportive phrases were written as if the writer was talking to the family directly on a 1-7 scale. ' \
#            f'Answer only with one number, with 1 being "strongly disagree" and 7 being "strongly agree." Here are the ' \
#            f'phrases: {phrases}'
#
#
# def generate_subjective_prompt(phrases):
#     return f'If you were the family seeking help, how supported would you feel when rating these phrases on a 1-7 ' \
#            f'scale? ' \
#            f'Answer only with one number, with 1 being "not supported at all" and 7 being "extremely supported." Here ' \
#            f'are the phrases: {phrases}'
#
#
# def generate_sympathy_prompt(phrases):
#     return f'How much sympathy is present in the phrases on a 1-7 scale? ' \
#            f'Answer only with one number, with 1 being "no sympathy" and 7 being "a great deal of sympathy." Here are ' \
#            f'the phrases: {phrases}'
#
#
# def generate_sentiment_prompt(phrases):
#     return f'How negative or positive are the phrases on a 1-7 scale? Answer only with one number, with 1 being ' \
#            f'"very negative" and 7 being "very positive." Here are the phrases: {phrases}'


EFFORT_PROMPT = 'You are a helpful assistant. You will be given a Python list of phrases. Rate, on a scale of 1 to 7, '\
                'the overall effort the writer put into crafting supportive phrases. Answer only with one number, ' \
                'with 1 being "minimal effort" and 7 being "significant effort". Rate the independent phrases ' \
                'holistically. Do not explain yourself.'

DIRECT_PROMPT = 'You are a helpful assistant. You will be given a Python list of phrases. Rate, on a scale of 1 to 7, '\
                'were the supportive phrases written as if the writer was talking directly to the family? Answer only '\
                'with one number, with 1 being "strongly disagree" and 7 being "strongly agree". ' \
                'Rate the independent phrases holistically. Do not explain yourself.'

SUBJECTIVE_PROMPT = 'You are the family seeking help. You will be given a Python list of phrases. Rate, on a scale of '\
                    '1 to 7, how supported would you feel by the phrases? Answer only with one number, with 1 being ' \
                    '"not supported at all" and 7 being "extremely supported". Rate the independent phrases ' \
                    'holistically. Do not explain yourself.'

SYMPATHETIC_PROMPT = 'You are a helpful assistant. You will be given a Python list of phrases. Rate, on a scale of 1 ' \
                     'to 7, how much sympathy was present in the phrases. Answer only with one number, with 1 being ' \
                     '"no sympathy" and 7 being "a great deal of sympathy". Rate the independent phrases holistically.'\
                     ' Do not explain yourself.'

SENTIMENT_PROMPT = 'You are a helpful assistant. You will be given a Python list of phrases. Rate, on a scale of 1 to '\
                   '7,' \
                   ' how negative or positive were the phrases. Answer only with one number, with 1 being ' \
                   '"very negative" and 7 being "very positive". Rate the independent phrases holistically. ' \
                   'Do not explain yourself.'


def filter_text(ser):
    for index, lst in ser.items():
        ser[index] = [phrase.strip() for phrase in lst if len(phrase.split()) >= 1]
    return ser


def get_score(phrase_list, prompt):
    completion = openai.ChatCompletion.create(
        model=engine,
        temperature=temp,
        messages=[{
            'role': 'user',
            'content': phrase_list
        }, {
            'role': 'system',
            'content': prompt
        }]
    )
    response = completion.choices[0].message.content
    time.sleep(2)
    while len(response) != 1 or not response.isdigit():
        print("Re-prompting...")
        completion = openai.ChatCompletion.create(
            model=engine,
            temperature=temp,
            messages=[{
                'role': 'user',
                'content': phrase_list
            }, {
                'role': 'system',
                'content': prompt
            }]
        )
        response = completion.choices[0].message.content
        time.sleep(2)
    rating = float(response)
    return rating


def construct_scores_list(ser, prompt):
    emotion = saved['data'][0]['emotion']
    directness = saved['data'][1]['directness']
    subjective = saved['data'][2]['subjective']
    sympathy = saved['data'][3]['sympathy']
    sentiment = saved['data'][4]['sentiment']
    lst = []
    if prompt == "emotion":
        print(emotion)
        index = emotion['index']
        lst = emotion['list']
        for i in range(index, NUM_SCORES_CALCULATED):
            print(i, "emotion")
            emotion['index'] = i
            lst.append(get_score(ser[i], EFFORT_PROMPT))
        emotion['index'] = NUM_SCORES_CALCULATED
    elif prompt == "direct":
        print(directness)
        index = directness['index']
        lst = directness['list']
        for i in range(index, NUM_SCORES_CALCULATED):
            print(i, "direct")
            directness['index'] = i
            lst.append(get_score(ser[i], DIRECT_PROMPT))
        directness['index'] = NUM_SCORES_CALCULATED
    elif prompt == "subjective":
        print(subjective)
        index = subjective['index']
        lst = subjective['list']
        for i in range(index, NUM_SCORES_CALCULATED):
            print(i, "subjective")
            subjective['index'] = i
            lst.append(get_score(ser[i], SUBJECTIVE_PROMPT))
        subjective['index'] = NUM_SCORES_CALCULATED
    elif prompt == "sympathy":
        print(sympathy)
        index = sympathy['index']
        lst = sympathy['list']
        for i in range(index, NUM_SCORES_CALCULATED):
            print(i, "sympathy")
            sympathy['index'] = i
            lst.append(get_score(ser[i], SYMPATHETIC_PROMPT))
        sympathy['index'] = NUM_SCORES_CALCULATED
    elif prompt == "sentiment":
        print(sentiment)
        index = sentiment['index']
        lst = sentiment['list']
        for i in range(index, NUM_SCORES_CALCULATED):
            print(i, "sentiment")
            sentiment['index'] = i
            lst.append(get_score(ser[i], SENTIMENT_PROMPT))
        sentiment['index'] = NUM_SCORES_CALCULATED
    return lst


def fill_list(score_list, remaining):
    for i in range(remaining):
        score_list.append(0)


while True:
    try:
        print("running")
        data = pd.read_excel(r"C:\Users\Sami\Downloads\text-467.xlsx")
        with open("saved.json", "r") as f:
            saved = json.load(f)

        cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        df = pd.DataFrame(data, columns=cols)

        df.fillna('', inplace=True)
        df['combined'] = df[cols].apply(lambda row: '_'.join(row.values.astype(str)).split('_'), axis=1)
        combined_ser = df['combined']

        filtered_ser = filter_text(combined_ser)

        emotional_score_list = construct_scores_list(filtered_ser, "emotion")
        direct_score_list = construct_scores_list(filtered_ser, "direct")
        subjective_score_list = construct_scores_list(filtered_ser, "subjective")
        sympathy_score_list = construct_scores_list(filtered_ser, "sympathy")
        sentiment_score_list = construct_scores_list(filtered_ser, "sentiment")

        df['directness_score'] = direct_score_list
        df['emotional_score'] = emotional_score_list
        df['subjective_score'] = subjective_score_list
        df['sympathy_score'] = sympathy_score_list
        df['sentiment_score'] = sentiment_score_list
        df.drop('combined', axis=1, inplace=True)
        file_name = "text-N467-emotional-effort.xlsx"
        df.to_excel(file_name)
        print('File written successfully')
    except Exception as e:
        print(e)
        with open("saved.json", "w") as f:
            json.dump(saved, f)
        print("saved")
        time.sleep(10)
        continue
    break
