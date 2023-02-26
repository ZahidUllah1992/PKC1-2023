import openai
import requests

# Set up OpenAI API key and model ID
openai.api_key = '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'
model_id = 'text-davinci-003'

# Define function to generate text using OpenAI's GPT-3 API
def generate_text(topic):
    prompt = f"Please write a short article about {topic}."
    response = openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text


# Set up WordPress API endpoint and authentication
api_url = 'http://bestcoffeeroaster.net/test-seo/wp-admin'
username = 'Admin'
password = '9CTll@?a#6@U#'

# Define function to create a new post on WordPress
def create_post(title, content):
    headers = {'Content-Type': 'application/json'}
    data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    response = requests.post(api_url, auth=(username, password), headers=headers, json=data)
    return response

# Generate a new post
topic = 'Best Coffee'
title = f"Article about {topic}"
content = generate_text(topic)


# Create a new post on WordPress
response = create_post(title, content)
print(content)
if response.status_code == 201:
    print('Post created successfully!')
else:
    print(f'Error creating post: {response.text}')