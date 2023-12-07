from gensim import corpora
from gensim.models import TfidfModel, LdaModel


class TopicModeling:
    def __init__(self, docs, num_topics, random_state, chunksize, passes, tfidf_transform=False, per_word_topics=True):
        self.docs = docs
        self.num_topics = num_topics
        self.random_state = random_state
        self.chunksize = chunksize
        self.passes = passes
        self.tfidf_transform = tfidf_transform
        self.per_word_topics = per_word_topics

    def create_dictionary_corpus(self):
        # Create Dictionary
        self.dictionary = corpora.Dictionary(self.docs)
        # Create Corpus
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.docs]

    def build_model(self):
        # Optionally apply TF-IDF transformation
        if self.tfidf_transform:
            tfidf = TfidfModel(self.corpus)
            corpus_tfidf = tfidf[self.corpus]
            corpus_used = corpus_tfidf
        else:
            corpus_used = self.corpus

        # Build LDA model
        self.lda_model = LdaModel(corpus=corpus_used,
                                  id2word=self.dictionary,
                                  num_topics=self.num_topics,
                                  random_state=self.random_state,
                                  chunksize=self.chunksize,
                                  passes=self.passes,
                                  per_word_topics=self.per_word_topics)
        return self.lda_model
