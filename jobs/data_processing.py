import nltk, json
import pandas as pd
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Changes by Frank: Added lemmatizer to generate better list

def load_data_from_file(file_name):
    with open('../data/{0}'.format(file_name)) as data_file:
        if file_name.split('.')[1] == 'json':
            data = json.load(data_file)
        if file_name.split('.')[1] == 'csv':
            data = pd.read_csv(data_file, delimiter=',')
            data = data.to_json()
            data = json.loads(data)
            well_formated = {}
            for key, postId in data['postId'].iteritems():
                well_formated[postId] = {}
                well_formated[postId]['wordLevel'] = data['wordLevel'][key]
                well_formated[postId]['videoSpeed'] = data['videoSpeed'][key]
                well_formated[postId]['subtitleLengthRatio'] = data['subtitleLengthRatio'][key]
                well_formated[postId]['sectionLength'] = data['sectionLength'][key]
                well_formated[postId]['wordList'] = data['wordList'][key]
            data = well_formated
    return data

def safe_data(data, file_title):
    output = json.dumps(data, ensure_ascii=False, encoding='utf8')
    with open("../data/{0}.json".format(file_title), "w+") as save:
        save.write(output.encode('utf8'))

def build_lemmatizer_with_historic(word, stemmer, stop_words):
    lemmatization_result = {}
    word = word.strip().lower()
    double_words = word.split('__')
    if len(double_words) >= 2:
        word = double_words[1]
    words = word.split(' ')
    if len(words) >= 2:
        words_original = []
        words_stemmed = []
        for word in words:
            if word not in stop_words and not word.isdigit():
                try:
                    stemmed = stemmer.stem(word)
                except AttributeError as e:
                    stemmed = stemmer.lemmatize(word)
                words_original.append(word)
                words_stemmed.append(stemmed)
        lemmatization_result['original'] = words_original
        lemmatization_result['stemmed'] = words_stemmed
    else:
        try:
            stemmed = stemmer.stem(word)
        except AttributeError as e:
            stemmed = stemmer.lemmatize(word)
        lemmatization_result['original'] = word
        lemmatization_result['stemmed'] = stemmed
    return lemmatization_result

videos_words = load_data_from_file("videoData_vs_WordList.json")
students1 = load_data_from_file("studentBehaviorInfo_1.json")
students2 = load_data_from_file("studentBehaviorInfo_2.json")
videos_data = load_data_from_file("videoDataInfo.csv")
videos_data_lemmatize = load_data_from_file("videoDataInfo.csv")
students = students1 + students2
stop_words = set(nltk.corpus.stopwords.words("english"))

porter_stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words("english"))
for video in videos_words:
    words = []
    words_lemmatize = []
    id_video = int(video['postId'])
    for word in video['wordList']:
        if word not in stop_words and not word.isdigit():
            word = word.strip().lower()
            words.append(build_lemmatizer_with_historic(word, porter_stemmer, stop_words))
            words_lemmatize.append(build_lemmatizer_with_historic(word, lemmatizer, stop_words))
    videos_data[id_video]['wordList'] = words
    videos_data_lemmatize[id_video]['wordList'] = words_lemmatize


cleaned_students = {}
cleaned_students_lemmatize = {}
for student in students:
    student_id = student['memberId']
    cleaned_students[student_id] = {}
    cleaned_students_lemmatize[student_id] = {}
    cleaned_students[student_id]['chosenVideo'] = student['chosenVideo']
    cleaned_students[student_id]['listenScore'] = student['listenScore']
    cleaned_students[student_id]['vocabularyList'] = []
    cleaned_students_lemmatize[student_id]['chosenVideo'] = student['chosenVideo']
    cleaned_students_lemmatize[student_id]['listenScore'] = student['listenScore']
    cleaned_students_lemmatize[student_id]['vocabularyList'] = []
    for word in student['vocabularyList']:
        stemmed = build_lemmatizer_with_historic(word['word'], porter_stemmer, stop_words)
        stemmed_lemmatize = build_lemmatizer_with_historic(word['word'], lemmatizer, stop_words)
        cleaned_students[student_id]['vocabularyList'].append({'postId':word['postId'], 'word':stemmed})
        cleaned_students_lemmatize[student_id]['vocabularyList'].append({'postId':word['postId'], 'word':stemmed_lemmatize})

safe_data(videos_data, "video_data")
safe_data(cleaned_students, "student_data")
safe_data(videos_data_lemmatize, "video_data_lemmatize")
safe_data(cleaned_students_lemmatize, "student_data_lemmatize")