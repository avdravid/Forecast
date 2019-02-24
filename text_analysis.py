#!/usr/bin/env python3
from profanity import profanity 
from depression import Depression
import json


class TextAnalyzer():
    def __init__(self, txt):
        self.txt = txt
        with open('words.json') as json_file:  
            data = json.load(json_file)
            self.general_words = data["general"]
            self.academic_words = data["academic"]
            self.suicidal_words = data["suicidal"]
            self.social_words = data["social"]
            self.family_words = data["family"]
            self.drugs_words = data["drugs"]
            self.financial_words = data["financial"]
            self.guns_words = data["guns"]
            self.date_words = data["dates"]
            self.revenge_words = data["revenge"]
        
    
    def run(self):
        depression = Depression(self.txt, self.general_words, self.academic_words, self.suicidal_words, self.social_words, self.family_words, self.drugs_words, self.financial_words, self.guns_words, self.date_words, self.revenge_words)
        score = depression.totalRatio + profanity.contains_profanity(self.txt) * 0.2 * depression.totalRatio
        if score > 50:
            #depressed
            return (depression.getCategory(), score)
        else:
            #not depressed
            return (0, 0)