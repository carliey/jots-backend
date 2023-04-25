import re
from .stability import dream
from .upload import add

from app.image.model import Image

import markdown
from bs4 import BeautifulSoup

def clean(text: str, note_id: int):
    # Define the regular expression pattern to match [image: prompt]
    pattern = r'\[image:\s+([^\]]*)\]'

    # Use re.sub() to replace each [image: prompt] with a base64-encoded image
    def replace(match):
        prompt = match.group(1)
        encoded_string = dream(prompt)
        image_url = add(encoded_string)
        image = Image.create(prompt, image_url, note_id)
        return f'[img:{image.id}]'

    # Use re.sub() to replace all [image: prompt] patterns with images
    text = re.sub(pattern, replace, text)

    # Return the modified string wrapped in <p> tags
    return text

def cleaner(text: str):
    # Define the regular expression pattern to match [image: prompt]
    pattern = r'\[image:\s+([^\]]*)\]'

    # Use re.sub() to replace all [image: prompt] patterns with images
    text = re.sub(pattern, lambda x:"" , text)

    # Return the modified string wrapped in <p> tags
    return text

def md2text(md_text):
    html = markdown.markdown(cleaner(md_text))
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()
