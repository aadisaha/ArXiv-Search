import openai
import re
import streamlit as st
import feedparser
api_key = st.text_input("API KEY:")
openai.api_key = api_key



# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

def generate_summary(text):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant that takes abstracts and extracts key takeaways and insights briefly and concisely but accurately."},
      {"role": "user", "content": 'What is the core technology improvement in one sentence? "' + text}
    ]
  )

  return (response.choices[0].message['content'])



def overall_summary(text):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant that synthesizes descriptions of new technology breakthroughs and groups similar breakthroughs together and extracts key takeaways and insights briefly and concisely but accurately."},
      {"role": "user", "content": 'What are some key breakthroughs that have occured and what new technologies are "' + text}
    ]
  )

  return (response.choices[0].message['content'])

st.title("ArXiv Summarizer")

query = st.text_input("What do you want to learn about?")
st.write('Give us a moment to learn about: ', query)

url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=1000&sortBy=relevance&sortOrder=descending'
feed = feedparser.parse(url)
st.write(len(feed.entries), "Entries in Last 7 Days")

# Initialize variables
abstracts = ""
summaries = []


i=1

# Loop through the entries in the RSS feed
for entry in feed.entries:
  st.write(str(i) +". " + entry.title)
  st.write(entry.link)
  x = generate_summary((entry.summary))
  summaries.append(x)
  st.write(x)
  st.write("------------------------")
  i += 1
summary = "".join(summaries)




MAX_LENGTH = 20000

# Loop through the entries in the RSS feed
for sum in summaries:
    # If adding the current summary to the abstract would exceed the maximum length,
    # summarize the current abstract and append it to the list of summaries
    if len(abstracts) + len(sum) > MAX_LENGTH:
        x = overall_summary(abstracts)
        summary_list.append(x)
        abstracts = ""
    # Add the current summary to the abstract
    abstracts += sum
    

# Summarize the final abstract and append it to the list of summaries
summary = generate_summary(abstracts)
summaries.append(summary)

# Print the list of summaries
for i, summary in enumerate(summary_list):
    st.write(f"Overall Summary: {i+1}: {summary}")



if __name__ == "__main__":
    main()
