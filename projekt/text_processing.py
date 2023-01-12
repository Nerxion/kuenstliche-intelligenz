import nltk, re
import spacy
from nltk.corpus import wordnet as wn

class text_processing():
    ''' class for processing text '''
    def __init__(self):
        self.stem = nltk.stem.PorterStemmer()
        self.nlp = spacy.load("en_core_web_sm")

    def get_synonyms_and_hypernyms(self, text:str):
        ''' returns synonyms and hypernyms of a string '''
        # TODO
        synsets = wn.synsets(text)

        s = synsets[0]
        hypernyms = []
        hyper = s.hypernyms()[0]
        hypernyms.append(hyper.lemma_names()[0])
        while hyper.lemma_names()[0] != "entity":
            hyper = hyper.hypernyms()[0]
            hypernyms.append(hyper.lemma_names()[0])

        synonyms = []

        for syn in synsets:
            for i in syn.lemmas():
                synonyms.append(i.name())
            
        return set(synonyms), hypernyms

    def get_key_words(self, text:str):
        ''' returns keywords of a string '''
        # TODO: Synonyme and maybe (hypernyms) maybe in dict
        key_words = []
        linearr = nltk.word_tokenize(text)
        linearr = [ele.lower() for ele in linearr if not re.compile(r'[^a-zA-Z]+').match(ele)] # für jedes Wort checken, dass es kein Sonderzeichen/Zahl, dann in lowerform in die Liste hinzufügen
        linearrtag = nltk.pos_tag(linearr)
        linearr = [a for (a, b) in linearrtag if b[0] == 'N' or b[0] == 'V' or b[0] == 'W']
        for ele in linearr:
            key_words.append(self.stem.stem(ele))
        return key_words

    def get_named_entities(self, text:str):
        ''' returns named entities of a string '''
        doc = self.nlp(text)
        entity_dicc = dict()

        for entity in doc.ents:
            if entity.label_ not in entity_dicc.keys():
                entity_dicc[entity.label_] = [entity.text]
            else:
                entity_dicc[entity.label_].append(entity.text)

        return entity_dicc


test = text_processing()

print(test.get_key_words("This sentence is just for testing"))
print(test.get_named_entities("Abraham was born in Frankfurt"))
print(test.get_synonyms_and_hypernyms("sentence"))