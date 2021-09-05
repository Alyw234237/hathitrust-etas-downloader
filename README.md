
# HathiTrust ETAS Downloader Readme

## Description

This is a Python 3 script for downloading books on the [HathiTrust](https://www.hathitrust.org/) [Emergency Temporary Access Service](https://www.hathitrust.org/ETAS-Description) (ETAS). It downloads the pages individually one by one as image files. While it used to be possible to download PDF pages from HathiTrust ETAS, this is unfortunately no longer possible. Note that in order to download ETAS books with this script, **you must have institutional access to the HathiTrust ETAS.**

For a similar but unrelated project, see the [ETAS Download Helper](https://sourceforge.net/projects/etasdownloadhelper/).

## Usage

Script usage (in a terminal or command prompt):

```
python hathi_downloader.py <book_id> <book_title> <first_page> <last_page>
```

<book\_title> will be the name of the folder the book is downloaded into. The path for the folder will be "$home/$book\_title" (where $home is the home directory on your machine).

Python 3 must be installed and added to the PATH in order for this script to work. Required Python modules (e.g., [imghdr](https://docs.python.org/3/library/imghdr.html), [http.cookies](https://docs.python.org/3/library/http.cookies.html), any others) are also needed if not already installed via pip.

**Prior to using this script to download a book, you must do the following things:**

1. Log in to HathiTrust ETAS with Google Chrome via your institutional credentials.
2. Check out the ETAS book you want to download.
3. Retrieve a SAML authentication cookie and put it into the script (see [below](#authentication-cookie)).

After the book has been downloaded, it can be converted into a PDF (see [below](#conversion-into-pdf)).

### Authentication Cookie

To get the SAML authentication cookie, do the following:

1. After checking out the book, make sure you're on the page where you can view/scroll through it.
2. Open Chrome developer tools on the page.
3. Press Ctrl+Shift+I OR right-click the page and click "Inspect" OR click the Chrome hamburger menu, click "More tools", and click "Developer tools".
4. Go to the "Network" tab in Chrome developer tools.
5. Close out of the console if it's open (it may be covering things).
6. Under the "Name" column, click an image.
7. You may need to scroll through a few pages on the book view for items to show up here.
8. In the "Headers" tab, find "Cookie:"
9. Copy the contents.
    1. Will be long and look something like this (but can vary):
        1. `\_saml\_idp =...; HT\_AUTHTYPE=shibboleth; HTexpiration=...`
    2. Don’t get “Set-Cookie:”—check a different item if you see that.
10. Put the copied cookie string into the "cookie" variable in the script on line 21.

Once you've done that, the script should now be able to download the book.

Note that the cookie expires every now and then (maybe once every 24 hours or so) and will need to be replaced by doing the above steps again each time it expires.

## Conversion into PDF

After the book has been downloaded, you can convert it into a PDF with a program like [Adobe Acrobat Pro DC](https://www.adobe.com/acrobat/acrobat-pro.html), add bookmarks, OCR it, and do whatever else you'd like (e.g., upload to [LibGen](https://en.wikipedia.org/wiki/LibGen)!).

### Differing Page Sizes

If you have a problem with pages being different sizes after combining the pages into a PDF, this is because PNG and JPEG pages seem to use different pixels per inch (PPI). To fix this, you can use [ImageMagick](https://imagemagick.org/script/index.php)'s [mogrify](https://imagemagick.org/script/mogrify.php) in the book folder to normalize the PPIs via the following commands:

```
mogrify -units "PixelsPerInch" -density 300 *.jpg
mogrify -units "PixelsPerInch" -density 300 *.png
```

Note that for these commands to work, ImageMagick must be installed, added to PATH, and legacy utilities (which includes mogrify) must be checked during ImageMagick setup/installation.

