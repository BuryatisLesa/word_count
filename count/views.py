import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# Глобальная переменная для хранения слов
loaded_words = []

def load_words_from_file(file):
    global loaded_words
    text = file.read().decode('utf-8').lower()
    words = re.findall(r'[a-zA-Z]+', text)
    loaded_words.extend(words)

def count_word_occurrences(word):
    word = word.lower()
    return loaded_words.count(word)

def clear_memory():
    global loaded_words
    loaded_words = []

def home(request):
    if request.method == 'POST':
        if 'upload_file' in request.FILES:
            uploaded_file = request.FILES['upload_file']
            load_words_from_file(uploaded_file)
            return render(request, 'count/home.html', {'message': f'Файл {uploaded_file.name} загружен!'})
        
        elif 'wordcount' in request.POST:
            word = request.POST['wordcount']
            count = count_word_occurrences(word)
            return render(request, 'count/home.html', {'count': count, 'word': word})
        
        elif 'clear_memory' in request.POST:
            clear_memory()
            return render(request, 'count/home.html', {'message': 'Память очищена!'})

    return render(request, 'count/home.html')
