from flask import Flask, request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/health')
def health():
  return 'OK'

@app.route('/parse-html', methods=['POST'])
def parse_html():

  html = request.data
  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(html, 'html.parser')
  # Find all the img tags
  img_tags = soup.find_all('img')
  # Find all span tags with style exactly 'font-weight:600;font-style:;text-decoration:'
  bold_spans = soup.find_all('span', style="font-weight:600;font-style:;text-decoration:")
  print(bold_spans)
  # Find all the spans with style exactly "color:rgb(51, 126, 169);font-weight:600;font-style:italic;text-decoration:" that also contain a <a href> tag with "twitter" in the href
  other_bold_spans = soup.find_all('span', style="color:rgb(51, 126, 169);font-weight:600;font-style:italic;text-decoration:")
  for span in other_bold_spans:
    # Find the <a> tag with the href
    a_tag = span.find('a', href=lambda x: 'twitter' in x)
    if a_tag:
      print(a_tag)
  
  # Loop through the img tags
  for img in img_tags:
    # Get the alt attribute of the image
    alt_text = img['alt']
    # Remove the image from the HTML
    img.extract()
    if (alt_text):
      # Create a new paragraph tag
      p_tag = soup.new_tag('p')
      # Set the text of the paragraph tag to the alt text
      p_tag.string = alt_text
      # Add the alt text to the HTML
      soup.body.insert(-1, p_tag)
      # Add a line break to the HTML that is 5em
      line_break = soup.new_tag('br')
      line_break['style'] = 'line-height: 5em;'
      soup.body.insert(-1, line_break)

  # Loop through the bold spans and remove them from the HTML
  for span in bold_spans:
    span.extract()

  # loop through all the iframes and turn them into img tags that are 600px by 400px
  iframes = soup.find_all('iframe')
  for iframe in iframes:
    src = iframe['src']
    img_tag = soup.new_tag('img', src=src)
    img_tag['width'] = 600
    img_tag['height'] = 400
    iframe.replace_with(img_tag)

  # find all the spans
  spans = soup.find_all('span')
  # for each span, if it has text in the span, then add two <br/> tags after the text, inside the span
  for span in spans:
    if span.text:
      br_tag = soup.new_tag('br')
      br_tag2 = soup.new_tag('br')
      span.append(br_tag)
      span.append(br_tag2)

  # Return the modified HTML
  return soup.prettify()

if __name__ == '__main__':
  app.run(host='localhost', port=8080)