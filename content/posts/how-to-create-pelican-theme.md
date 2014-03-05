Title: How to create and modify your Pelican blog theme
Date: 2014/02/18 11:41
Modified: 2014/02/19 12:47
Category: tech
Tags: webdev, design, Pelican, GitHub, HTML, CSS
Slug: how-to-create-pelican-theme
disqus_identifier: how-to-create-pelican-theme
Author: James Fallisgaard
status: draft
Summary: Discusses the design, forking, and modification/creation of a Pelican theme for your blog.

# Note on intended audience for this document

You can consider this document an unofficial *part 2* of the tutorial [How-to host a Pelican / GitHub / DigitalOcean VPS blog] [jnb_pel_pt1] I posted previously.  If you need help setting up any part of that sort of website, please see [that page here] [jnb_pel_pt1].

I assume for this document that you have successfully hosted a `Pelican` blog on the internet, are version-controlling your source in [GitHub] [github], and are controlling the server-side of your website in a VPS.  If you aren't on a VPS, you can still reference the Pelican theme creation aspects of this document though!

***

# Layout of this document

I'll walk you through the design process I used, and then the implementation of that design as a Pelican theme you can commit to GitHub and apply to your personal Pelican blog.

**TABLE OF CONTENTS**

[TOC]

***

# Design your website's layout, look and feel

I appreciated the advice from [macdrifter.com] [macdrifter] regarding thinking through the design of your site.

## First, go look for inspiration

Since this was the first site I had designed from scratch since a version of this blog 7 years ago, I spent a lot of time wrestling with these questions and looking for inspiration around the internet and the things around me.  

I knew my basic goals for the site were to serve as a portfolio and process blog for my programming and data science projects, but I also wanted the site to reflect my personality. I combed through coding blogs looking for what I'll call "best-practices" for similar portfolio/process-blogs, I looked at designer and artists personal sites too to get some inspiration from people who should have a better visual eye than the programmers, and I looked at a lot of printed objects, comics, art-books or book covers, magazines, as these are typically my most frequent source of resonant inspiration anyway.

I then saved screenshots or took photographs of what I liked so I could have a folder on my desktop to scroll through with quick-look and try and internalize things for when I started actually trying to design on my own.

Okay, so now we're inspired and we're ready to make some real design decisions for our site.

## Two basic guiding questions

Before touching any code, I wanted to have a firm idea of what the theme design I would implement would be. To figure this out, I started thinking through two threads somewhat simultaneously:

1. How do I want content organized on my site?
    + Do I want a static landing page or to have the root level of my site *be* the blog view?
    + How much granularity in terms of categories and tags do I want to expose to the user?
    + How do I want to treat *projects*? As blog posts or static pages?
    + What special *pages* would I be implementing? A landing page, about page, projects page, etc?
    + Do I want special treatment of Table of Contents?
    + Any dynamic javascript I'll want to implement in the actual theme for functionality like fancy scrolling, or searching, or anything else?
2. What do I want the site to look like?
    + Color scheme? 
    + Typography?
    + Sidebars, headers, footers?
    + Width, responsive design?

## Decide basic governing ideas

First I decided on some basic things I wanted to accomplish with my site's theme:

+ Minimalist focus on the article at hand, minimal doodads or links
+ Want to consolidate as many extra *types of pages* as possible, while still maximizing functionality
+ Unique look from other coding blogs out there (open to using more color!)
+ Strong sense of vertical hierarchy

## Decide how you want content organized on the site

I started by making a list of what page types (templates) a typical coding blog would have:

+ LANDING/HOME page
+ BLOG-POSTS view
    + a BLOG-POST
+ PROJECTS view
    + a PROJECT
+ ABOUT
+ archives:
    + ARCHIVE by time
    + ARCHIVE by category
    + ARCHIVE by tag
+ on all pages:
    + HEADER
    + SIDEBAR
    + FOOTER

Then I decided how I personally wanted my theme to consolidate these page types:

+ LANDING/HOME will contain the PROJECTS view, and the ARCHIVE by time; tags appear at bottom
+ No BLOG-POSTS view
    + a BLOG-POST will have links to other BLOG-POST's with same tags at the bottom
+ a PROJECT is a BLOG-POST
+ ABOUT will contain full bio, resume, and extensive links
+ on all pages:
    + HEADER will display on every page, and will contain a brief bio and some links
    + No SIDEBAR
    + No FOOTER

And so by consolidation, I've ended up with these 4 basic page types to implement:

+ LANDING/HOME
+ BLOG-POST
+ ABOUT
+ The all pages (header) template

## Decide what you want the site to look like

### Layout of info in the basic page types you decide to implement

Since I consolidated down to 4 basic page-types above, I will show some rough notes of what information I'll include in each page type.

####LANDING/HOME page####

    :::text
	Header
	

####BLOG-POST####

    :::text
	Header

####ABOUT####

    :::text
	Right sidebar:
    RSS | GitHub | twitter | LinkedIn | Flickr | Instagram | Visaul.ly
    Body:
    Photo
    Simple bio
    CV/RESUME (with link to PDF version at top)
    About the site

####The all pages (header) template####

    :::text
	@jamesnewbrain
    the online braindump of James Fallisgaard
    Right now I’m working on nksaidwhat?
    Posts & Projects | GitHub | Comics&Coffee | jamesnewwho?

### Color

+ [kuler.adobe.com](https://kuler.adobe.com/create/color-wheel/)
+ [dabblet.com](http://dabblet.com/)

### Typography

####Font####

+ I love the typography of `Byword`, can I just lift it?
+ [free fonts](http://www.fontsquirrel.com/fonts)

####Size####

+ I prefer the smaller text size of [monome.org](http://monome.org)

### Overall page layout and width

####Strong sense of vertical hierarchy####

+ Standardize organization hierarchy number system? (using headers? or ordered lists?)

####Default width####

####Responsive design VS specific grid resolutions####

## Finally, draw a prototype

***

# Customizing your Pelican theme

1. Go to [pelicanthemes.com] [pelican-themes] or [pelican-themes-gallery.place.org] [plcn-thm-galary] to view different themes currently checked in to the official [Pelican Themes repo] [plcn_thm_repo] on GitHub.

2. To preview different themes live locally using your own content:

    a. Clone the Pelican themes repo locally. I took some advice from [duncanlock.net] [duncanlock2] regarding recursive cloning of the repo's submodules.

        :::bash
    	# on LOCAL:
        $ git clone --recursive git@github.com:getpelican/pelican-themes.git
        # now, you can pull latest changes in future with 
        $ cd pelican-themes
        $ git pull --recurse-submodules

    b. Start your Pelican devserver with `make devserver` in your Pelican site's root directory.
    
    &#x266b; By keeping this running in the background, as you change your Pelican configuration settings and point to different themes, Pelican will rebuild your site's local HTML automatically upon modifying any files, so you can just refresh your web browser and see the changes.
    
    &#x27a9; Don't forget to end the process you have to not only `ctl-c` to get a command line, but then `sh develop_server.sh stop` to actually stop the background Python webserver process.

    b. Modify your `pelicanconf.py` file by adding a `THEME` variable where you cite the path to the theme's root folder.  You can then change this path, and rebuild the HTML to see a preview of your site built with the newly selected theme.

        :::text
    	THEME = '/users/yames/dev/zmisc/pelican-themes/bootstrap2'

3. Once you find a good starting place, you'll want to customize the theme to your own taste.  If the design diverges enough, you'll want to actually fork the repo and commit the new theme with a new name on GitHub.

4. If using [Elegant] [elegant] Pelican theme, can customize Table of Contents to get it to display on the side rather than in-line with your document.

    Here's how this works: The `toc` plugin for Markdown will generate a table of contents from the Header tags throughout your document.  Then when Pelican is generating HTML, the `extract_toc` plugin for Pelican will extract this table of contents and insert it in to the `<nav>` tag of your HTML.  Then the Elegant plugin for Pelican will display the contents of this `<nav>` tag in a left sidebar instead of the body of your posts' text.

    &#x27a9;; `toc` plugin for Markdown ships with Python's Markdown by default, so all you'll need to do is enable it in your Pelican config file, so edit `pelicanconf.py` and add the line `MD_EXTENSIONS = (['toc'])`.

    &#x266b;; The next several steps will enable the `extract_toc` plugin for Pelican to work.

    &#x27a9; Clone pelican-plugins locally, so they are available for LOCAL Pelican install to build from.

        :::bash
    	# on LOCAL:
        $ cd /users/yames/dev/zmisc
        $ git clone https://github.com/getpelican/pelican-plugins

    &#x27a9; Install BeautifulSoup for Python

        :::bash
    	# on LOCAL:
        # make sure you're in your virtualenv
        $ pip install beautifulsoup4

    &#x27a9; Make sure to update requirements.txt with `$ pip freeze` and commit to GitHub so REMOTE will install BeautifulSoup too.

    &#x27a9; Edit `pelicanconf.py`

        :::text
    	PLUGIN_PATH = '/users/yames/dev/zmisc/pelican-plugins'
        PLUGINS = ['extract_toc']

    &#x27a9; In an actual blogpost `*.md` document, make sure to add a line containing `[TOC]` after the metadata, before your blog post text.

<!---
LINKS
-->
[duncanlock2]:      https://github.com/dflock/duncanlock.net/blob/master/content/posts/tech/how-i-built-this-website-using-pelican-part-2-themes.rst
                    "duncanlock.net - built website using pelican - pt 2"
[elegant]:          http://oncrashreboot.com/elegant-best-pelican-theme-features
                    "Elegant - Best Pelican theme"
[github]:           https://github.com
                    "GitHub"
[jnb_pel_pt1]:      http://jamesnewbrain.com/how-to-host-pelican-github-vps-blog.html
                    "jamesnewbrain.com - How to host a Pelican/GitHub/VPS blog"
[macdrifter]:       http://www.macdrifter.com/2012/08/moving-to-pelican-design-planning.html
                    "macdrifter.com - moving to pelican design planning"
[pelican-themes]:   http://pelicanthemes.com/
                    "Preview Pelican Themes"
[plcn-thm-galary]:  http://pelican-themes-gallery.place.org/
                    "Pelican Theme Galary"
[plcn_thm_repo]:    https://github.com/getpelican/pelican-themes
                    "Pelican themes repo"
[terriyu]:          http://terriyu.info/blog/posts/2013/07/pelican-setup/
                    "terriyu.info - pelican setup"