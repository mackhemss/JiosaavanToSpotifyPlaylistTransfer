from bs4 import BeautifulSoup

html = '<a event_item="[object Object]" title="Taake Jhanke" class="o-flag__img" href="/song/taake-jhanke/AQc9CEZlWHc"><img src="https://c.saavncdn.com/125/Queen-2014-150x150.jpg" alt="Taake Jhanke"></a>'

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the <a> tag
a_tag = soup.find('a')

# Extract the title attribute
title = a_tag['title']

print("Title:", title)