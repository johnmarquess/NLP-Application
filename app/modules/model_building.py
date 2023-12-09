from gensim import corpora
from gensim.models import TfidfModel, LdaModel


class TopicModelling:
    def __init__(self, docs, num_topics, random_state, chunksize, passes, tfidf_transform=False, per_word_topics=True,
                 no_below=5, no_above=0.5, keep_n=100000):
        self.lda_model = None
        self.dictionary = None
        self.corpus = None
        self.docs = docs
        self.num_topics = num_topics
        self.random_state = random_state
        self.chunksize = chunksize
        self.passes = passes
        self.tfidf_transform = tfidf_transform
        self.per_word_topics = per_word_topics
        self.no_below = no_below
        self.no_above = no_above
        self.keep_n = keep_n

    def create_dictionary_corpus(self):
        """
        Create the dictionary and corpus for the given documents.

        :param self: The instance of the class.
        :return: None
        """
        # Create Dictionary
        self.dictionary = corpora.Dictionary(self.docs)
        self.dictionary.filter_extremes(no_below=self.no_below, no_above=self.no_above, keep_n=self.keep_n)
        # Create Corpus
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.docs]

    def build_model(self):
        """
        Builds an LDA model using the given parameters.

        :param self: The instance of the class.
        :return: The trained LDA model.

        The `build_model` method builds an LDA model using the parameters specified during initialization. If the
        `tfidf_transform` parameter is set to True, the method applies the TF-IDF transformation
        * to the corpus before building the model. Otherwise, it uses the corpus as is.

        The LDA model is built using the `LdaModel` class from the Gensim library. The `corpus_used` parameter is passed
        as the training corpus, `id2word` specifies the dictionary mapping of
        * words to their numeric ids, `num_topics` determines the number of topics to be identified, `random_state` sets
        the random seed for reproducibility, `chunksize` specifies the number
        * of documents processed together, `passes` determines the number of times the model is trained on the entire
        corpus, and `per_word_topics` controls whether probabilities of words in
        * topics are returned.

        After building the model, it is assigned to the `lda_model` attribute of the class and returned.

        Example usage:
        ```
        model = MyClass()
        model.build_model()
        ```
        """
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
