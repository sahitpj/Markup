import Tkinter as tk
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import numpy as np
import nltk.data
from nltk.corpus import  stopwords
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter 
from scipy.sparse import csr_matrix
import re, math
from multiprocessing import Pool, Process, Queue
import urllib2
import re
from bs4 import BeautifulSoup
from googlesearch import search
import itertools

class webExtracter(object):
    def __init__(self, parent = None):
        self.parent = parent

        
    def Sentence_Checker(self, sentence):
        print 'Process webExtracter.sentence_checker running...'
        scrapped_data = {}
        query = sentence
        z = webExtracter()
        links = search(query, tld="co.in", num=5, stop=1, pause=2)
        p = Pool(processes = 10)
        q = Queue
        data = p.map(z.scrapper, args=itertools.izip(links, itertools.repeat(q)))
        for i in xrange(len(links)):
            scrapped_data[links[i]] = data[i]
        z.Data_Processing(scrapped_data, query)
        
    def sentence_checker(self, sentence, context_sentences, q):
        print 'Process webExtracter.sentence_checker running...'
        jobs = []
        scrapped_data = {}
        query = sentence
        for j in search(query, tld="co.in", num=5, stop=1, pause=2):
            q = Queue()
            z = webExtracter()
            p = Process(target=z.scrapper, args=(j, q))
            jobs.append(p)
            trusted_sources = [r'quora']
            for source in trusted_sources:
                if re.search(source, j):
                    start = time.clock()
                    p.start()
                    p.join()
                    print 'time taken for this process is ', time.clock()-start
                    scrapped_data[j] = q.get()
                    break
            else:
                p.start()
                p.join(2)
                scrapped_data[j] = q.get()
                #print 7
                if p.is_alive():
                    print "this shit is still running... let's kill it..."
                    p.terminate()
                    p.join()
                    scrapped_data[j] = 'KILLED'
        p = webExtracter()
        match_q = p.Data_Processing(scrapped_data, query, context_sentences)
        q.put(match_q)
        q.close()
        q.join_thread()
        
    def scrapper(self, website, q):
        
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            elif re.match('^\[', str(element.encode('utf-8'))):
                return False
            return True  
        flag = 0
        flag_1 = 0
        print 'Process webExtracter.scrapper running...'
        website_data = []
        if re.search(r'youtube', website):
            '''
            wiki = website
            page = urllib2.urlopen(wiki)
            soup = BeautifulSoup(page, 'lxml')
            table = soup.find(id='description')
            data = []
            for entry in table:
                r = entry.text.strip()
                data.append(r)
            result = filter(visible, data)
            ac = []
            for i in list(result): 
                if len(i) > 70:
                    ac.append(i.strip())      
            data = ' '.join(ac)
            q.put(data)
            '''
            q.put(None)
        else:
            patterns = [ r'facebook', r'twitter']
            for pattern in patterns:
                if re.search(pattern, website):
                    flag = 1
                    break
            if flag == 0:
                wiki = website
                
                try:
                    page = urllib2.urlopen(wiki)
                except:
                    flag_1 = 1
                if flag_1 == 0:
                    soup = BeautifulSoup(page, 'lxml')
                    data = soup.findAll(text=True)
                    
                    result = filter(visible, data)
                    for i in list(result): 
                        if len(i) > 100:
                            website_data.append(i.strip())
                    data = ' '.join(website_data)
                    q.put(data)
                    #print 1
                else:
                    q.put(None)
            else:
                q.put(None)
            #print 2
    
    
    
    def sentence_similarity(self, vector1, vector2, id_1, id_2, text_words_count, stopwords=None):
        r = vector1.shape[1]
        
        vector1 = np.array(np.reshape(vector1, (r,1)))
        vector2 = np.array(np.reshape(vector2, (r,1)))
         
        v1 = [ vector1[i][0] for i in xrange(r)]
        v2 = [ vector2[i][0] for i in xrange(r)]
        
        wc = text_words_count[-1]
        #print sum(v1), sum(v2)
        if sum(v1) == 0. or sum(v2) == 0.:
            return  abs(text_words_count[id_2] - text_words_count[id_1])*0.25/wc
        else:
            return (1- cosine_distance(v1, v2))*0.75 + abs(text_words_count[id_2] - text_words_count[id_1])*0.25/wc
           
    
    def build_similarity_matrix(self, vector_sentences, text_words_count , stopwords=None):
        S = np.zeros((len(vector_sentences), len(vector_sentences)))
        
        hh = len(vector_sentences)
        for idx1 in xrange(hh):
            for idx2 in xrange(hh):
                if idx1 == idx2:
                    continue
                l = webExtracter()
                S[idx1][idx2] = l.sentence_similarity(vector_sentences[idx1], vector_sentences[idx2], idx1, idx2, text_words_count, stopwords)
     
        for idx in xrange(len(S)):
            if S[idx].sum() != 0:
                S[idx] /= S[idx].sum()
     
        return S
    
    
    
    def pagerank(self, A, eps=0.0001, d=0.85, attention_factor = 0.45, damped_factor = 0.15):
        p = [0]*len(A)
        for i in xrange(len(A)):
            p[i] = (attention_factor**i)*math.exp(-damped_factor)
        P = np.array(p)
        P = P/np.sum(P)
        while True:
            new_P = np.ones(len(A))/len(A)*(1-d) + d*A.T.dot(P)
            delta = abs((new_P - P).sum())
            if delta <= eps:
                return new_P
                break
            P = new_P
            
    def Single_data_processing(self, data, website, query, context_sentences, q):
        def simple_tokenizer(str_input):
            words = re.sub(r"[^A-Za-z0-9\-]", " ", str_input).lower().split()
            return words
        print '                     \n#####################'
        print '                     '
        print 'Process webExtracter.Single_data_processing running...'
        print '                     '
        print '#####################\n                     '
        if data != 'KILLED' and data != None:
            t = webExtracter()
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            sentences  = tokenizer.tokenize(data)
            u = len(context_sentences)
            context_flag = 0
            if len(context_sentences) > 1:
                context_flag = 1
                for i in xrange(len(context_sentences)-1):
                    sentences.append(context_sentences[i])
            sentences.append(query)
            text_words = []
            text_words_count = []
            wc = 0
            for line in sentences:
                l = line[:-2]
                text_words.extend(l.split())
                try:
                    text_words_count.append(text_words_count[-1]+len(l.split()))
                except:
                    text_words_count.append(len(l.split()))
                
                wc += len(l.split())
                
            vectorizer = TfidfVectorizer(
                use_idf=True, tokenizer=simple_tokenizer, max_features = 50, stop_words='english')
            
            vectorized_sentences = csr_matrix(vectorizer.fit_transform(sentences))
            
            vectorized_dense =  vectorized_sentences.todense()
            vectorized_dense = vectorized_dense[:-u, :]
            
            def cos_distance(vector_1, vector_2):
                if sum(vector_1) == 0. or sum(vector_2) == 0.:
                    l = 0
                    if sum(vector_1) == 0 and sum(vector_2) == 0:
                        l = 0.25
                else:
                    l = cosine_distance(vector_1, vector_2)
                return l
            
            neighbour_vectors = []
            query_vector = vectorized_dense[-1, :]
            if context_flag == 1:
                c = vectorized_dense.shape[1]
                v0 = np.array(np.reshape(query_vector, (c,1)))
                vector_0 =  [ v0[j][0] for j in xrange(c) ]
                neighbour_sentences = vectorized_dense[-u:-1, :]                
                for i in xrange(u-1):
                    v1 = np.array(np.reshape(neighbour_sentences[i, :], (c,1)))
                    vector_0_1 =  [ v1[j][0] for j in xrange(c) ]
                    g = cos_distance(vector_0, vector_0_1)
                    if g > 0.4:
                        neighbour_vectors.append([vector_0_1, g])
                #print neighbour_vectors      
            
            S = t.build_similarity_matrix(vectorized_dense, text_words_count, stopwords)    
            sentence_ranks = t.pagerank(S)
            
            ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranks), key=lambda item: -item[1])]
            
            summary_size = 4
            sum_sentences = sorted(ranked_sentence_indexes[:summary_size])
            
             
            summary = itemgetter(*sum_sentences)(sentences)
            
            #print summary
            
            r = []
            sp = 0.
            for i in xrange(len(summary)):
                print summary[i]
                r.append(summary[i])
                c = vectorized_dense.shape[1]
                p1 = np.array(np.reshape(vectorized_dense[sum_sentences[i], :], (c,1)))
                p2 = np.array(np.reshape(query_vector, (c,1)))
                vector_1 =  [ p1[j][0] for j in xrange(c) ]
                vector_2 =  [ p2[j][0] for j in xrange(c) ]       
                sp += cos_distance(vector_1, vector_2)
                if context_flag == 1:
                    for neighbour_vector in neighbour_vectors:
                        vector_2_1 = neighbour_vector[0]
                        weight = neighbour_vector[1]
                        bd_factor = 0.2*weight
                        sp += (weight-bd_factor)*cos_distance(vector_1, vector_2_1)
                        summary_size += weight
                    print (weight-bd_factor)*cos_distance(vector_1, vector_2_1), weight
            print 'percentage query match = ', sp/summary_size
            q.put(sp/summary_size)
        else:
            q.put(0.5)
            
            
    def Alternate_Data_Processing(self, data, website, query, context_sentences, q):
        
        print 'done'

    def Data_Processing(self, scrapped_data, query, context_sentences):
        print 'Process webExtracter.Data_Processing running...'
        jobs = []
        processed_data = {}
        display_data = {}
        for i in xrange(len(scrapped_data.values())):
            website = scrapped_data.keys()[i]
            data = scrapped_data[website]
            #print data
            q = Queue()
            y = webExtracter()
            p = Process(target=y.Single_data_processing, args=(data, website, query, context_sentences, q))
            jobs.append(p)
            p.start()
            p.join()
            v = q.get()
            processed_data[website] = v
            if v != 0.5 and (data != 'KILLED' or data != None) :
                display_data[website] = v
            k = display_data.values()
            if v != 0.5 and (data != 'KILLED' or data != None):
                print 'approx percentage correctness = ', sum(k)/len(k)*100 ,'%    from website - ', website
            else:
                print website, 'has not been used to decide its correctness factor for now.\nWe are still working on an algorithm for it :)'
                    
        return sum(k)/len(k)*100