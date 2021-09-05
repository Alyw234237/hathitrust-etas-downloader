import os
import sys
import requests
import imghdr
from http.cookies import SimpleCookie
import time

# Get command line arguments
try:
  argumentList = sys.argv[1:]
  book_id = argumentList[0]
  book_title = argumentList[1]
  first_page = int(argumentList[2])
  last_page = int(argumentList[3])
except:
  print('hathi_downloader.py <book_id> <book_title> <first_page> <last_page>')
  sys.exit(2)

# Cookie for HTTP request (put cookie string in here)
cookie = """
_saml_idp=...; HT_AUTHTYPE=shibboleth; HTexpiration=...
"""

# Clean up cookie string (remove leading/trailing newlines and remove 'Cookie: ' and 'Set-Cookie: ' from start if there)
cookie = cookie.strip('\n')
prefix = 'Cookie: '
cookie = cookie[cookie.startswith(prefix) and len(prefix):]
prefix = 'Set-Cookie: '
cookie = cookie[cookie.startswith(prefix) and len(prefix):]

# Set up book download path
home = os.path.expanduser("~")
book_path = os.path.join(home, book_title)

# Make the book download directory if it doesn't already exist
if not os.path.exists(book_path):
  os.mkdir(book_path)

# Download each page one at a time
for page in range(first_page, last_page + 1):
  # URL for request
  url = "https://babel.hathitrust.org/cgi/imgsrv/image?id=" + str(book_id) + ";seq=" + str(page) + ";size=300;rotation=0"

  # HTTP headers for request
  headers = {
    'Accept': 'image/apng',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'referer': 'https://babel.hathitrust.org/cgi/pt?id=' + str(book_id) + '&view=1up&seq=' + str(page),
  }

  # Process cookies string (convert string into simple cookie then Python dictionary)
  newcookie = SimpleCookie()
  newcookie.load(cookie)
  cookies = {}
  for key, morsel in newcookie.items():
    cookies[key] = morsel.value

  # Get the page
  successful = False
  attempts = 0
  while successful == False:
    if attempts >= 5:
      print("5 unsuccessful attempts in a row to download and/or save a page. Exiting script.")
      print("Please check things and try again (resume download at sequence page " + str(page) + ").")
      sys.exit(1)

    # Request the page
    try:
      response = requests.get(url=url, headers=headers, cookies=cookies, timeout=30)
    except requests.exceptions.RequestException as error: 
      print('Page request unsuccessful: ' + error)
      print('Retrying page in 5 seconds...')
      attempts += 1
      time.sleep(5)
      continue

    # If the content type is an image
    if 'image' in response.headers['Content-Type']:
      # Get the image file type
      image_type = imghdr.what('', response.content)
      # If a standard image binary file type (e.g., PNG, JPEG)
      if image_type:
        # If JPEG, rename to JPG
        if image_type == 'jpeg':
          image_type = 'jpg'

        # Save the file with the correct image file type extension
        file_path = os.path.join(book_path, book_title)
        file_path = file_path + '_' + str(page) + "." + image_type
        file = open(file_path, "wb")
        file.write(response.content)
        file.close()

        # Double check that the file downloaded successfully
        if os.path.exists(file_path) == False:
          print("Error: Failed to write downloaded page to file for sequence page " + str(page) + ". " + 
                "Retrying page in 5 seconds...")
          attempts += 1
          time.sleep(5)
          continue
      # Error if it's not a binary image file (something went wrong)
      # Note: Restricted file SVG will end up here (Content-Type: image/svg+xml, imghdr.what(): None)
      else:
        print("Error: Downloaded page is not the expected image file (per response.content).")
        print("Is the cookie fresh/still good? Is the book checked out? Did we exceed a download limit?") 
        print("Retrying page in 5 seconds...")
        attempts += 1
        time.sleep(5)
        continue
    # Error if it's not a binary image file (something went wrong)
    # Note: "temporarily exceeded viewing" page should end up here (to-do: handle that?)
    else:
      print("Error: Downloaded page is not the expected image file (per response.headers['Content-Type']).")
      print("Is the cookie fresh/still good? Is the book checked out? Did we exceed a download limit?") 
      print("Retrying page in 5 seconds...")
      attempts += 1
      time.sleep(5)
      continue

    successful = True

  # Update user then sleep for a duration to avoid download limits
  print('Downloaded page ' + str(page) + '.')
  time.sleep(1)

# Tell user that we finished and how many pages we downloaded
print('Finished downloading ' + str(last_page - first_page + 1) + ' pages.')

