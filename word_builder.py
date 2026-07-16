# word_builder.py
from spellchecker import SpellChecker


class WordBuilder:
    def __init__(self):
        self.spell = SpellChecker()
        self.current_word = ""
        self.sentence = ""
        self.last_letter = ""
        self.last_confidence = 0.0

    def add_letter(self, ch, confidence):
        self.last_letter = ch
        self.last_confidence = confidence
        self.current_word += ch

    def add_space(self):
        self._commit_word()
        self.sentence += " "

    def finalize_word(self):
        self._commit_word()

    def _commit_word(self):
        if not self.current_word:
            return
        corrected = self._suggest(self.current_word)
        if self.sentence and not self.sentence.endswith(" "):
            self.sentence += " "
        self.sentence += corrected
        self.current_word = ""

    def _suggest(self, word):
        miss = self.spell.unknown([word.upper()])
        if miss:
            suggestion = self.spell.correction(word.upper())
            return suggestion or word
        return word

    def reset_sentence(self):
        self.current_word = ""
        self.sentence = ""
        self.last_letter = ""
        self.last_confidence = 0.0

    def get_display_text(self):
        text = self.sentence
        if self.current_word:
            if text and not text.endswith(" "):
                text += " "
            text += self.current_word
        return text
