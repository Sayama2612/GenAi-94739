def analyze(sentence) :
    num_char = len(sentence)

    words = sentence.split()
    num_words = len(words)

    vowels = 'aeiouAEIOU'
    num_vowels = sum(1 for char in sentence if char in vowels)

    return num_char, num_words, num_vowels
