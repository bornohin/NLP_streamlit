"""

"""
Title_html = """
    <style>
        .title h1{
          user-select: none;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>Natural Language Processing on Streamlit.</h1>
    </div>
    """


# Core Pkgs
import streamlit as st 
import os

# Copied this below inside main function
# st.markdown(Title_html, unsafe_allow_html=True) #Title rendering

# Import NLTK
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('all-corpora')

# NLTK utils
import nltk_download_utils

# NLP Pkgs
from textblob import TextBlob 
import spacy
from gensim.summarization import summarize

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# Function for Sumy Summarization
def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

# Function to Analyse Tokens and Lemma
@st.cache
def text_analyzer(my_text):
	nlp = spacy.load('en_core_web_lg')
	docx = nlp(my_text)
	# tokens = [ token.text for token in docx]
	allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
	return allData

# Function For Extracting Entities
@st.cache
def entity_analyzer(my_text):
	nlp = spacy.load('en_core_web_lg')
	docx = nlp(my_text)
	tokens = [ token.text for token in docx]
	entities = [(entity.text,entity.label_)for entity in docx.ents]
	allData = ['"Token":{},\n"Entities":{}'.format(tokens,entities)]
	return allData

        
# selection = st.radio("Which operation do you want to make?", ["Show Tokens and Lemma", "Show Named Entities", 
# "Show Sentiment Analysis", "Show Text Summarization"])

def main():
	# """ NLP Based App with Streamlit """

	# Title
	st.markdown(Title_html, unsafe_allow_html=True) #Title rendering
	# st.title("NLP Based App with Streamlit.")
	st.subheader("Natural Language Processing On the Go..")
	st.markdown("""
    	#### Description
    	+ This is a Natural Language Processing (NLP) based App showing basic NLP task like
    	Tokenization, NER, Sentiment Analysis and Text Summarization.
    	""")

	selection = st.radio("Which operation do you want to make?", ["Show Tokens and Lemma", "Show Named Entities", 
	"Show Sentiment Analysis", "Show Text Summarization"])

	# Tokenization
	# if st.radio("Show Tokens and Lemma"):
	if selection == "Show Tokens and Lemma":
		st.subheader("Tokenize Your Text")

		message = st.text_area("Enter Text")
		if st.button("Analyze"):
			nlp_result = text_analyzer(message)
			st.json(nlp_result)

	# Entity Extraction
	# if st.radio("Show Named Entities"):
	if selection == "Show Named Entities":
		st.subheader("Analyze Your Text")

		message = st.text_area("Enter Text")
		if st.button("Extract"):
			entity_result = entity_analyzer(message)
			st.json(entity_result)

	# Sentiment Analysis
	# if st.radio("Show Sentiment Analysis"):
	if selection == "Show Sentiment Analysis":
		st.subheader("Analyse Your Text")

		message = st.text_area("Enter Text")
		if st.button("Analyze"):
			blob = TextBlob(message)
			result_sentiment = blob.sentiment
			st.success(result_sentiment)

	# Summarization
	# if st.radio("Show Text Summarization"):
	if selection == "Show Text Summarization":
		st.subheader("Summarize Your Text")

		message = st.text_area("Enter Text")
		summary_options = st.selectbox("Choose Summarizer",['sumy','gensim'])
		if st.button("Summarize"):
			if summary_options == 'sumy':
				st.text("Using Sumy Summarizer ..")
				summary_result = sumy_summarizer(message)
			elif summary_options == 'gensim':
				st.text("Using Gensim Summarizer ..")
				summary_result = summarize(message)
			else:
				st.warning("Using Default Summarizer")
				st.text("Using Gensim Summarizer ..")
				summary_result = summarize(message)

		
			st.success(summary_result)



	st.sidebar.subheader("About App")
	st.sidebar.text("NLP App with Streamlit")
	# st.sidebar.info("Cudos to the Streamlit Team")
	

	st.sidebar.subheader("By")
	st.sidebar.text("Tom Islam")
	my_url = """<a style='display: block;' href="https://tomislam.com/" target="_blank">Visit My Site.</a>
	"""
	my_linkedin = """<a style='display: block;' href="https://www.linkedin.com/in/bornohin/" target="_blank">Find me on linkedin</a>
	"""
	st.sidebar.text("Inspiration from Jesse E.Agbe")
	st.sidebar.markdown(my_url, unsafe_allow_html=True)
	st.sidebar.markdown(my_linkedin, unsafe_allow_html=True)
	

if __name__ == '__main__':
	main()