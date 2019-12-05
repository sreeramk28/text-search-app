from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import TextForm
from .forms import SearchForm
def getparagraphs(text):
    paras = text.split("\r\n\r\n")
    sz = len(paras)
    return paras
def indexing(paras):
    """indexing format:
        { word : {paraID, frequency in paraID}}"""
    """key-value pair for word_dict:
        key = string & value = dictionary"""
    """key value pair for word_dict[<some word>]
        key = integer & value = integer"""
    word_dict = {}
    sz = len(paras)
    for i in range(sz):
         words = paras[i].split()
         for j in range(len(words)):
             words[j] = words[j].lower()
             if words[j][-1] == '.':
                 words[j] = words[j][:-1]
         for word in words:
            if word not in word_dict.keys():
                word_dict[word] = {i+1: 1}
            else:
                if i+1 not in word_dict[word].keys():
                    word_dict[word][i+1] = 1
                else:
                    word_dict[word][i+1] += 1
    leng = len(word_dict)
    """The value dictionary for each word is arranged in descending order
        of frequency"""
    for keyword in word_dict:
        tmp = word_dict[keyword]
        sorted_tmp = sorted(tmp.items(), key=lambda kv: kv[1])
        sorted_tmp.reverse()
        word_dict[keyword] = sorted_tmp
    return word_dict
def search(word, word_dict, paras):
    word = word.lower()
    top10paras = ""
    """the first 10 (or lesser) IDs of the word represent the
        paragraphs to be returned"""
    if word in word_dict.keys():
        cnt = 0
        for tup in word_dict[word]:
            top10paras += paras[tup[0] - 1]
            top10paras += "\r\n\r\n"
            cnt += 1
            if cnt == 10:
                break
    else:
        top10paras += "WORD NOT FOUND"
    return top10paras
def get_page_1(request):
    # if this is a POST request we need to process the form data
    args = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if 'index' in request.POST:
            form1 = TextForm(request.POST)
        # check whether it's valid:
            if form1.is_valid():
            # process the data in form.cleaned_data as required
                text1 = form1.cleaned_data['doctext']
                args['form1'] = form1
                paras = getparagraphs(text1)
                word_dict = indexing(paras)
                """store dictionary data and documents in the current session &
                    redirect to the word search page"""
                request.session['diction'] = word_dict
                request.session['paras'] = paras
                return HttpResponseRedirect('/success/success/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form1 = TextForm()
        args['form1'] = form1
    return render(request, 'search/home.html', args)
def search_page(request):
    args = {}
    result = "OK"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if 'word' in request.POST:
            form = SearchForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                word_input = form.cleaned_data['word']
                word_dict = request.session['diction']
                paras = request.session['paras']
                result = search(word_input, word_dict, paras)
                args['form'] = form
                args['result'] = result
        if 'clear' in request.POST:
            request.session['diction'] = {}
            return HttpResponseRedirect('/search/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
        args['form'] = form
    return render(request, 'search/result.html', args)
