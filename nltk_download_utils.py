import subprocess
cmd = ['python3','-m','textblob.download_corpora']
subprocess.run(cmd)
print("Working")

import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('all-corpora')