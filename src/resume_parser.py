import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
import spacy
import spacy_transformers

def clean_text(s):
    tokens = word_tokenize(s.lower())
    tokens = [WordNetLemmatizer().lemmatize(t) for t in tokens if t not in set(stopwords.words('english') + list(string.punctuation))]
    return ' '.join(tokens)

nlp = spacy.load("en_core_web_sm")
class data_extraxt:
    def __init__(self, raw_text: str):
        self.text = raw_text
        self.clean_text = clean_text(self.text)
        self.doc = nlp(self.clean_text)

    def extract_names(self):  #need some filter
        names = [e.text for e in self.doc.ents if e.label_ == 'PERSON']
        return names[0] if names else "Name not found"

    def extract_education(self):
        return [e.text for e in self.doc.ents if e.label_ == 'DEGREE']

    def extract_emails(self):
        email_pattern = r'\w+@\S+\.\S+'
        return re.findall(email_pattern, self.text)

    def extract_phones(self):
        phone_pattern = r'[+]?[0-9]{0,3}\s?[(]?[1-9][0-9]{2}[)\-\s]*[0-9]{3}[\-\s]?[0-9]{4}'
        phones = re.findall(phone_pattern, self.text)
        phone = []
        for p in phones:
            phone.append("".join([i for i in p if i.isnumeric()]))
        return phone

    def extract_links(self):
        link_pattern = r'(?:https?://|www\.)\S+'
        return re.findall(link_pattern, self.text)

    def extract_entities(self): #education/previous company
        entity_labels = ['GPE', 'ORG']
        entities = [e.text for e in self.doc.ents if e.label_ in entity_labels]
        return entities

    def extract_experience(self):
        experience_section = []
        in_experience_section = False

        for token in self.doc:
            if token.text == 'experience':
                in_experience_section = True
                #print(token.text)
            if in_experience_section:
                #print(token.text)
                experience_section.append(token.text)
        return " ".join(experience_section)

    def extract_keywords(self):
        return [t.text for t in self.doc if t.pos_ in ['NOUN', 'PROPN']]

def to_JSON(text):
    extractor = data_extraxt(text)
    resume_dict = {
        'resume': text,
        'clean_text': extractor.clean_text,
        'name': extractor.extract_names(),
        'email': extractor.extract_emails(),
        'phone': extractor.extract_phones(),
        'link': extractor.extract_links(),
        'keywords': extractor.extract_keywords(),
        'education': extractor.extract_education(),
        'experience': extractor.extract_experience()
    }
    return resume_dict