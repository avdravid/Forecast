#!/usr/bin/env python3

from fuzzywuzzy import fuzz

class Depression:
    def __init__(self, content, general_words, academic_words, suicidal_words, social_words, family_words, drugs_words, financial_words, guns_words, date_words, revenge_words):
        self.content = []
        words = content.lower().split(" ")
        self.totalRatio = 0
        if len(words) >= 3:
            for i in range(len(words)):
                if i + 2 < len(words):
                    self.content.append(words[i] + " " + words[i+1] + " " + words[i+2])
        else:
            self.content = [content]
        self.general_words = self.helper(general_words)
        self.academic_words = self.helper(academic_words)
        self.suicidal_words = self.helper(suicidal_words)
        self.social_words = self.helper(social_words)
        self.family_words = self.helper(family_words)
        self.drugs_words = self.helper(drugs_words)
        self.financial_words = self.helper(financial_words)
        
        if self.totalRatio > 50:
            if self.getCategory() == "Suicidal":
                self.guns_words = self.helper(guns_words)
                self.date_words = self.helper(date_words)
                if self.guns_words > 50:
                    self.totalRatio += 200
                if self.date_words > 50:
                    self.totalRatio += 200
            elif self.getCategory() == "Academic":
                self.guns_words = self.helper(guns_words)
                if self.guns_words > 50:
                    self.totalRatio += 200
            elif self.getCategory() == "Social" or self.getCategory() == "Family":
                self.revenge_words = self.helper(revenge_words)
                if self.revenge_words > 40:
                    self.totalRatio += 50
        
    def helper(self, key_list):
        score = 0
        for phrase in self.content:
            for trigger in key_list:
                ratio = fuzz.ratio(trigger, phrase)
                if ratio > 60:
                    '''print("Current Trigger: " + trigger)
                    print("Current Phrase: " + phrase)
                    print("Ratio: " + str(fuzz.ratio(trigger, phrase)))'''
                    score += ratio 
        self.totalRatio += score           
        return score
    
    def getCategory(self):
        scores = [self.general_words,
        self.academic_words,
        self.suicidal_words,
        self.social_words,
        self.family_words,
        self.drugs_words,
        self.financial_words]
        
        if max(scores) == self.general_words:
            return "General"
        elif max(scores) == self.academic_words:
            return "Academic"
        elif max(scores) == self.suicidal_words:
            return "Suicidal"
        elif max(scores) == self.social_words:
            return "Social"
        elif max(scores) == self.family_words:
            return "Family"
        elif max(scores) == self.drugs_words:
            return "Drugs/Alcohol"
        elif max(scores) == self.financial_words:
            return "Financial"
                           
