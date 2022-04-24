import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S ConjP S

NP -> N  | AdjP NP | N PP | NP ConjP NP | Det AdjP N | Det N | P  Det N

VP -> V | Adv V | V Adv | V NP | AdvP NP | V NP PP | V PP | VP Conj VP | V NP Adv | V NP PP PP

AdvP -> Adv | Adv V | V Adv

AdjP -> Adj | Adj AdjP | Adv Adj | V Det NP

PP -> P NP

ConjP -> Conj | S Conj VP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

            
def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    final_processed_sentence =""
    processed_sentence = sentence.lower()
    processed_sentence = processed_sentence.split()

    for word in processed_sentence:
        processed_word = filter(str.isalnum, word)
        processed_word = filter(str.isalnum, processed_word)
        words = "".join(processed_word)
        final_processed_sentence += words + " "
    tokenized_words = nltk.word_tokenize(final_processed_sentence)

    return tokenized_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    output = list()
    #print("tree height",tree.height())
    #iterate the tree from bottom up starting at the last NONTERMINALS
    for x in range(tree.height()):
        if x < 2:
            continue
        for s in tree.subtrees(lambda tree: tree.height() == x):
            #convert subtrees to text so I can search for Noun Phrases
            s_text = str(s)
            #find subtree that have 1 Noun Phrases
            if s_text.count("(NP") == 1:
                #make sure the Noun Phrase is at the top of the subtree
                if s_text.find("(NP", 0, 3) > -1:      
                    #print(s_text,"#######")
                    #select the remaining noun phrase and add to list
                    output.append(s)
    
    return(output)
  

if __name__ == "__main__":
    main()
