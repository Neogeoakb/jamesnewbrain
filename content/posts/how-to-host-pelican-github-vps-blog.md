Title: How to combine Pelican, GitHub, and a DigitalOcean VPS to host a cool blog
Date: 2014-02-17 10:36
Modified: 2014-02-17 14:00
Category: tech
Tags: webdev, Pelican, GitHub, VPS, Python, Linux
Slug: how-to-host-pelican-github-vps-blog
Author: James Fallisgaard
Summary: How to host your Pelican generated static-site blog, versioned on Github, on your own DigitalOcean VPS

[TOC]

***

# Why host a blog like this?

The procedure outlined here, and this style of blog as static-site generated from code, is probably for nerds only.  It's sooooo much easier to go sign up for a tumblr and be posting in literally 2 minutes.  This whole process took me like a week of learning, setting up and documenting.  Why put yourself through all this setup, instead of just running with tumblr?  Beacuse...it's fun? It's possibly professionally valuable?  Maybe.  I get the impression that the only people that will notice and appreciate that your blog is built on Pelican are other programmers, in which case its just more signaling that you're "part of the club".  Whatever your reason, you end up with a pretty sweet, svelte blog, and get a tingle of satisfaction knowing that you push builds of your blog to your personal virtualized linux server and commit blog posts to GitHub... we all do what makes us happy I guess!

**The fundamental ideas behind hosting a blog like this compared to other common styles of blog hosting:**

- *Host site on a Virtual Private Server (VPS)*: Instead of hosting your site on a managed hosting service like Dreamhost.com, we'll be managing the server's operating system and software ourselves using a VPS provided by [DigitalOcean] [digitalocean]. Using VPS means you control the server-side of your site, so if you're planning on doing any fancy web-design stuff hosted at the same domain, which is pretty common for a developer hoping to host some portfolio-ish stuff on their `yourDNSdomain.com` website, this is kind of a pre-requisite.
- *Static HTML site generated from source code*: The actual site served to readers will be minimal and efficient HTML, in contrast to the relatively high overhead of using a dynamic blog engine like wordpress or a blog service like tumblr. The server is only serving up static HTML instead of requiring your server compete for resources with a dynamically accessed MySQL database, or any other processing overhead required.
- *[Pelican] [pelican], a popular static site generator written in Python*: Based on the Ruby-written pioneer of this type of static site generation, [Jekyll] [jekyll], Pelican appears to be emerging as the consensus Python-based static site generator, with tons of plugin support and help available online to get you going, including this blog how-to!
- *Use [GitHub] [github]*: Version control your blog posts, written in [Markdown] [markdown] (essentially as human-readable source), which will be BUILT by Pelican before deployment.
- *Learn by doing*: You get to learn how to use all the above.
  
***

# Technology stack covered

This post documents the full process to bring this website/blog up and host it on the internet.  The stack of technologies looks like:

## *LOCAL machine* - running Mac OS 10.9:

| Task                                                          | Tools used                                    |
| --------------------------------------------------------------| --------------------------------------------- |
| Control REMOTE machine (your VPS) via SSH                     | BASH terminal                                 |
| Python environment, synced between LOCAL and REMOTE           | [virtualenv] [venv], [pip] [pip]              |
| Design website layout/theme                                   | HTML/CSS editor ([TextWrangler] [tw])         |
| Write blog posts in Markdown                                  | Markdown editor ([nvALT] [nv], [Byword] [bw]) |
| Create images or take photos                                  | Lightroom, [ImageOptim][io], [ImageAlpha][ia] |
| Test locally - Build HTML from Markdown source                | [Pelican] [pelican]                           |
| Test locally - Serve website, viewable on LOCAL machine       | [Pelican] [pelican] and [Python] [python]     |
| Version control source (website layout, blog posts) to GitHub | [GitHub] [github], BASH terminal              |

## *REMOTE machine* - VPS w/ Ubuntu 12.04:

| Task                                                          | Tools used                                    |
| --------------------------------------------------------------| --------------------------------------------- |
| Security, firewall, other basic security on our VPS           | [UFW] [ufw], [Fail2ban] [f2b], etc            |
| Python environment, synced between LOCAL and REMOTE           | [virtualenv] [venv], [pip] [pip]              |
| Get GitHub-versioned website source code                      | [GitHub] [github]                             |
| Build HTML from Markdown source                               | [Pelican] [pelican]                           |
| Serve website to `yourDNSdomain.com`                          | [nginx] [nginx]                               |
| Automated deployment to build/host site when GitHub updates   | [Fabric] [fabric]                             |

***

# Layout of this document

I've read a huge number of blog posts, tutorials, and code documentation to end up with the process documented in this post (see reference links scattered throughout).

I document here the exact process I ended up using to set this website up from start to finish:

- **FIRST**, we'll build up our website locally, and test the site locally in a web browser.
- **SECOND**, we'll introduce our VPS remote server, and configure it to host our website.
- **LAST**, we'll walk through the workflow of writing a blog post locally, committing it to GitHub, and building and deploying the updated site to the internet on the VPS.

The biggest source of confusion for me, while reading through blog posts and documentation to configure all this stuff for the first time, was the lacking clarity of whether code blocks or documentation were referring to the LOCAL or the REMOTE (VPS) machine.  I try to be crystal clear about this to eliminate confusion, and I think the way this document flows will make more sense to a newbie.

&#x266b; Of course this is only a suggested procedure, and just like anything involving computers or programming, there are multiple ways to accomplish any given task, so feel free to adapt and leave suggestions in the comments when you find better means on your own!

## Notes on reading this document

References are spread through as we go as direct links.

Code block sections will look like:

    :::bash
	# first line will denote "on REMOTE" or "on LOCAL" for clarity.
	$ BASH commands will start with the dollar sign
	# Code will be syntax highlighted according to language

&#x27a9; This symbol represents that this is a specific action that should be followed.

&#x266b; This symbol represents the following is a note / commentary for more detail.

&#x266b; I'll be refferring to your VPS as REMOTE, and your local machine as LOCAL.

***

# PART 1: Build website/blog locally

## I. Establish a local directory for your website project

Create a root directory for your website project. This will be what we turn in to a Git repo that gets backed up on [GitHub] [github], and also contain the source that Pelican will build from.

My personal system is to have a folder in my users' home directory called `dev` wherein I put one-word directories that become GitHub repos. So since my website has a DNS domain of `jamesnewbrain.com`, I created a folder at `~dev/jamesnewbrain`.

    :::bash
	# on LOCAL:
    $ mkdir -p ~/dev/jamesnewbrain/

&#x266b; From now on, when you see `~dev/jamesnewbrain` in code blocks, please substitute with your own root directory created in this step.

## II. Setup Python environment on LOCAL (Python, pip, virtualenv, Pelican, Markdown)

Note that I referenced the following tutorials: [dabapps.com] [dabapps], [duncanlock.net] [duncanlock1], [feross.org] [feross], and [clemesha.org] [clemsha].

1. Install Python (Mac OS 10.9 already has 2.7.5 installed)

2. Install [`pip`] [pip], the package manager for Python modules.

    &#x266b; You're using a `sudo` to install `pip` globally on your machine, since you'll typically want to be able to install/update/uninstall Python modules outside of any specific virtual environment we set up.

    &#x266b; We also install `python-dev` headers in case we will be compiling any python libraries that need them.

        :::bash
    	# on LOCAL:
    	$ sudo aptitude install python-pip python-dev
	
3. Install [`virtualenv`] [venv], the Python virtual environment management system.

    &#x266b; `virtualenv` allows you to compartmentalize sets of Python modules for specific projects from the globally installed modules on your entire system. This way you can have project-specific versions of modules and manage any conflicts between modules on a project-by-project basis.  It also allows you to sync your "blessed" set of Python modules from your LOCAL machine with your REMOTE machine, which we will do later in this procedure.

        :::bash
    	# on LOCAL:
    	$ sudo pip install virtualenv
	
4. From now on, don't use global `pip` commands, instead use `virtualenv`

    &#x27a9; Create a new virtualenv Python environment in your site's project folder:

        :::bash
    	# on LOCAL:
        $ cd ~/dev/jamesnewbrain/
        $ virtualenv env    # can be any <environment_name>

        # switch to the new environment
        $ cd env
        $ source bin/activate
        
    &#x266b; Thus the name of the environment is added to your cmd prompt. This lasts as long as terminal window is open (see it prefixed on the left of any command line).
    
    &#x266b; You can switch back to default python install with `$ deactivate`.
    
    &#x266b; Now can use `pip` (without `sudo`) inside of your virtual environment to install Python modules ONLY IN YOUR CURRENT PROJECT:
    
        :::bash
    	# on LOCAL:
    	$ pip search <package_name>
        $ pip install <package_name>

5. Install the Python packages to our virtual environment we will use to generate our site.

    a. Install [`Pelican`] [pelican]

        :::bash
    	# on LOCAL:
    	$ pip install pelican

    b. Install [`Markdown`] [markdown] manually (the Python version).

        :::bash
    	# on LOCAL:
    	$ pip install markdown

    c. Install [`BeautifulSoup`] [beautsoup], a HTML parser, which we will use later.

        :::bash
    	# on LOCAL:
        $ pip install beautifulsoup4

    d. You can check what's installed in your virtualenv now with:

        :::bash
    	# on LOCAL:
    	$ pip freeze
        
        Jinja2==2.7.2
        Markdown==2.3.1
        MarkupSafe==0.18
        Pygments==1.6
        Unidecode==0.04.14
        beautifulsoup4==4.3.2
        blinker==1.3
        docutils==0.11
        feedgenerator==1.7
        pelican==3.3
        pytz==2013.9
        six==1.5.2
        wsgiref==0.1.2
        
6.  Save a file called `requirements.txt`, which contains the above list of Python packages installed in your virtual environment.

        :::bash
    	# on LOCAL:
    	$ pip freeze > requirements.txt
    	
    &#x266b; Now you can move to any new machine and install the same Python environment quickly with:
    
        :::bash
    	# on LOCAL:
    	$ pip install -r requirements.txt

    &#x266b; You can also update all the modules quickly with:
    
        :::bash
    	# on LOCAL:
    	$ pip install --upgrade -r requirements.txt


## III. Create a default [`Pelican`] [pelican] blog

I read a lot of blog posts to kind of formulate the following configuration. Check out the following: [cbracco.me] [cbracco], [duncanlock.net] [duncanlock1], [jamesmurty.com] [jamesmurty], [gtmanfred.com] [gtmanfred], [claudiodangelis.com] [claudiodangelis], [martinbrochhaus.com] [martinbrochhaus], and [xlarrakoetxea.org] [xlarrakoetxea].

1. Use the Pelican wizard, `pelican-quickstart` from your project's root directory to spin up a default Pelican blog.

        :::bash
    	# on LOCAL:
    	$ cd ~/dev/jamesnewbrain
    	$ pelican-quickstart

    &#x27a9; Walk through the wizard, answering the questions with your own answers.

        :::text
    	Where do you want to create your new web site? [.] 
        What will be the title of this web site? jamesnewbrain
        Who will be the author of this web site? james fallisgaard
        What will be the default language of this web site? [en] en
        Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) y
        What is your URL prefix? (see above example; no trailing slash) http://jamesnewbrain.com
        Do you want to enable article pagination? (Y/n) n
        Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) y
        Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) y
        Do you want to upload your website using FTP? (y/N) n
        Do you want to upload your website using SSH? (y/N) n
        Do you want to upload your website using Dropbox? (y/N) n
        Do you want to upload your website using S3? (y/N) n
        Do you want to upload your website using Rackspace Cloud Files? (y/N) n
        Done. Your new project is available at /Users/yames/dev/jamesnewbrain

2. How to test your website locally using the Pelican devserver.

    `pelican-quickstart` creates a shell script, `develop_server.sh` that you can run locally to start a loop where it will detect changes in your Pelican project (change to config file, change to blog post files), rebuild the HTML automatically, and serve the site locally using the `Python` HTTP web server.

    This is very useful to use while writing blog posts or working on your site's theme, as as soon as you save changes locally as you can see them reflected on a local version of your site just by refreshing your web browser window.
    
        :::bash
    	# on LOCAL:
        $ cd ~/dev/jamesnewbrain
        $ make devserver

    &#x27a9; The default localhost port that Python's webserver will use is 8000.  Navigate to [http://localhost:8000/](http://localhost:8000/) in web browser to see preview.

    &#x266b; If you don't want to actually run the local webserver and just want to force a rebuild of the site's HTML, use `make html`.

    &#x27a9; To regain access to your terminal, use `ctl-c`.
    
    &#x27a9; This keeps the python webserver running in a background process.  To kill this process also, run:

        :::bash
    	# on LOCAL:
        $ sh develop_server.sh stop

3. Customize the file/folder hierarchy to meet your own design goals.

    By default `pelican-quickstart` will make some files you may not end up needing, for example they provide two methods to automate building of your site, a `Makefile` using `MAKE`, and `Fabfile.py` using `Fabric`.  In practice, you'll probably only use one of these methods and delete the unused file. They also do not impose much in terms of folder hierarchy, leaving you with a simple `content` folder to be a generic container for your blogposts and images.  You are free to customize as you want, renaming files and folders and moving things around, as long as you update your `pelicanconf.py` to account for changes in pathing.

    I ended up choosing the following hierarchy for my site.  I will cover the significance of the different directories in this hierarchy throughout the document, for example, you have already seen the creation of the `env` directory to contain your Python virtual environment.  I also comment below the directories we will tell Git not version control, as they are either built dynamically, or contain externals that shouldn't be committed as source in our repository.

        :::text
        jamesnewbrain/
        |-- .gitignore
        |-- Makefile
        |-- README.md
        `-- content
            `-- extras
            `-- images
            `-- pages
            `-- posts
        `-- env                 # ignored by Git
        `-- output              # ignored by Git
        `-- plugins             # ignored by Git
        `-- themes              # ignored by Git
        |-- develop_server.sh
        |-- pelicanconf.py
        |-- requirements.txt

    &#x27a9; If you rename or move either `content` or `pelicanconf.py`, modify `develop_server.sh`, `Makefile` and `pelicanconf.py` accordingly so that `Pelican` will continue to build correctly.

## IV. GitHub versioning your website/blog project

1. Create a Git repo for your project. (This is just a Git repo locally.  You will tie it to GitHub as a backup service in a later step).

        :::bash
    	# on LOCAL:
        $ cd ~/dev/jamesnewbrain
        $ git init

2. Create a .gitignore file for your project to ensure that only source and config files get synced with GitHub.

    &#x27a9; Start by downloading a copy of GitHub's [.gitignore file template] [gitignore] for Python and saving it in the root of your blog project like `~/dev/jamesnewbrain`.
    
    &#x27a9; Edit this `.gitignore` file and add the following lines:

        :::text
        #Custom
        output/
        plugins/
        themes/
        *.pid
    
    &#x266b; You don't want to sync the `output/` directory because this will contain the HTML that we will generate on the VPS from the GitHub-versioned source files.

    &#x266b; GitHub's `.gitignore` template for Python already includes ignoring `env/` directories, so our virtualenv won't sync.  Instead, the `requirements.txt` file used by `pip` will be synced in the root of our project. This is how we will deploy the same Python virtualenv to our REMOTE server.
    
    &#x266b; `plugins/` and `themes` are externals from other repos, so we shouldn't commit those with our own source.

3. Create a file `README.md` in your projects' root.

    This will be GitHub's default readme file.

        :::bash
    	# on LOCAL:
        $ cd ~/dev/jamesnewbrain
        $ touch README.md

    &#x27a9; I started with the following:

        :::markdown
    	# jamesnewbrain.com

        This is a static site generated by [Pelican](http://docs.getpelican.com/en/3.3.0/).

    &#x27a9; Save/exit with `ctl-x` when you're done.

4. Sync your local Git repo with GitHub.com.

    &#x27a9; Start by committing the site to a local Git repo.

        :::bash
    	# on LOCAL:
        $ git add .
        $ git status
        
        # On branch master
        #
        # Initial commit
        #
        # Changes to be committed:
        #   (use "git rm --cached <file>..." to unstage)
        #
        #	new file:   .gitignore
        #	new file:   Makefile
        #	new file:   README.md
        #	new file:   develop_server.sh
        #	new file:   pelicanconf.py
        #	new file:   requirements.txt
        #
        
        $ git commit -m "Initial commit of jamesnewbrain.com"
        $ git status

    &#x27a9; Now let's synchronize our local repo with a remote repo at [GitHub.com] [github].

    &#x27a9; First create an empty repo at [GitHub.com] [github] so that you can get an HTTPS URL to push to from your local machine.  GitHub will provide you with a HTTPS URL like: `https://github.com/jfallisg/jamesnewbrain.git`.

    &#x27a9; Next, add this as the `remote` repository for your local Git repo.

        :::bash
        # on LOCAL:
        $ git remote add origin https://github.com/jfallisg/jamesnewbrain.git
        $ git push -u origin master

    &#x266b; There's a chance you set this up wrong, or make the mistake that I did of copying in the SSH link instead of HTTPS, when you've previously only established credentials to sync with GitHub over HTTPS.  Audit and remediate those issues with the following:
    
        :::bash
        # on LOCAL:
        $ git remote -v         # to tell you what you have set up as remote
        $ cat .git/config       # alternative to audit your settings
        $ git remote rm origin  # to remove previous remote origin from you repo

    &#x27a9; Now that you have established sync with GitHub, from now on, commit changes or new blog posts to your GitHub repo with:

        :::bash
        # on LOCAL:
        $ cd ~/dev/jamesnewbrain
        $ git status                        # optional, check for changes
        $ git add .
        $ git commit -m "describe changes"
        $ git push origin master

Congrats, your website is all set up locally! Now let's set up our VPS and actually host this thing on the internet!

***

# PART 2: DigitalOcean VPS setup to host our Pelican blog

Once you've decided on going the VPS route (and not a cloud-based hosting like Amazon EC2), you'll quickly narrow your VPS providers down to either [DigitalOcean] [digitalocean] or [Linode] [linode].  Both have great reps.  For my use case, DigitalOcean provided a dirt cheap $6/month hosting deal which includes automated backups of my server, which won me over.

## I. Create a DigitalOcean droplet

See [official DigitalOcean tutorial] [do_droplet] for more help.

1. From the [DigitalOcean dashboard] [dod], create Droplet, and select a meaningful/memorable **hostname**.
2. Select size / price plan (I chose their cheapest droplet which gives you 512MB / 1CPU / 20GB SSD / 1TB x-fer for $5 per month).
3. Select region / datacenter near you.
4. Select distribution (I chose Ubuntu 12.04.3 x64).
5. We will add our SSH key later in this procedure.
6. Settings (I chose to enable the following: Enable VirtIO, Private Networking, Backups (for an extra $1 per month)).

DigitalOcean will then spin up your VPS and email you your VPS's IP address, and default root user password.

## II. Configure VPS for remote access

1. Connect to VPS

        :::bash
        # on REMOTE:
        $ ssh root@your_vps_ip

2. Set hostname and set Fully Qualified Domain Name (FQDN)

    I referenced these DigitalOcean tutorials, [Set Hostname] [do_sethostname] and [Set FQDN] [do_setfqdn].

    &#x266b; By default your DigitalOcean droplet's name is your hostname.  I'll refer to these interchangably as `your_hostname`.

    a. First check default hostname:

        :::bash
        # on REMOTE:
        $ hostname      # your_hostname == droplet name by default
        $ hostname -f   # your currently set FQDN, should be localhost by default

    b. Change FQDN to properly reflect our hostname/domain:

        :::bash
        # on REMOTE:
        $ nano /etc/hosts

    &#x27a9; Then insert a line *at the top of the list* like:
    
        :::text
        your_vps_ip     your_hostname.yourDNSdomain.com     your_hostname

    If it's not at the top of the list, localhost will continue to be returned in FQDN lookup. Verify hostname and FQDN work correctly now with another `$ hostname -f` command. You should get `your_hostname.yourDNSdomain.com` back.

3. Configure DNS with DigitalOcean

    a. On your domain registrar's site, login and point Domain Name Server to DigitalOcean domain servers.
    
    b. On DigitalOcean's dashboard, "Add Domain"
    
    c. Input `yourDNSdomain.com`, `your_vps_ip`, and `your_hostname`.
        
    This will create the A record for your domain.  
        
    You should end up with a line like: `A       @       your_vps_ip`
    
    d. Add CNAME records for "www" and wildcard "*" to resolve to default domain level
        `CNAME   www     @`
        `CNAME   *       @`

4. Update Ubuntu on your droplet

        :::bash
    	# on REMOTE:
    	$ aptitude update
        $ aptitude upgrade

## III. Basic security for your VPS

Ubuntu web server security is something I know next to nothing about, so I leaned *heavily* on the following references: [feross.org] [feross], [digitalocean.com/community] [do_serversetup], and from [cbracco.me] [cbracco].

1. Change root password from DigitalOcean's default.

        :::bash
    	# on REMOTE:
    	$ passwd your_new_password

2. Create a new username account to log in to instead of root.

        :::bash
    	# on REMOTE:
    	$ adduser your_username

    I used the same username as my local machine so I have the option to login with `$ ssh your_droplet_name.yourDNSdomain.com`.

    &#x27a9; Specify password, and you can leave other fields blank.

3. Give sudo root privileges to this new user

        :::bash
    	# on REMOTE:
    	$ visudo

    &#x27a9; In nano text editor, navigate to `# User privilege specification`, add a line like the one for "root" user with your new user name like `your_username ALL=(ALL:ALL) ALL`, save with `ctl-x` and `Y` to save.

4. Configure SSH to your server to disallow root logins, and operate on a different default port.

        :::bash
    	# on REMOTE:
    	$ nano /etc/ssh/sshd_config

    &#x27a9; change your_SSH_port `Port 22` to `Port ###` [where ### is less than 1024] [wiki_TCP], and not 22.

    &#x27a9; change the rule for `PermitRootLogin` to `no`

    &#x27a9; add the line `UseDNS no` to the bottom of the file

    &#x27a9; add the line `AllowUsers your_username` to the bottom of the file.

    &#x27a9; `ctl-x` to save and exit.

        :::bash
    	# on REMOTE:
    	$ reload ssh

    &#x27a9; **before logging out of root user**, make sure everything is set up okay by opening a new Terminal window:

        :::bash
    	# on REMOTE:
    	$ ssh -p your_SSH_port your_username@yourDNSdomain.com # if DNS has registered by now
        $ ssh -p your_SSH_port your_SSH_port@your_vps_ip       # alternatively

    &#x27a9; If you successfully have logged in to the new user, close the terminal window that's logged in as `root`.  From now on log in as this new user whenever you connect to your VPS.

5. Configure SSH keys

    See [DigitalOcean’s SSH Key tutorial] [do_sshkeys].

    The point of the next section is to provide an easier and more secure way to log in to your REMOTE VPS using SSH keys.

    a. `ssh-keygen` will create a public/private key pair, saving the:
    
    + public key to `/Users/your_username/.ssh/your_name_specified.pub` (which will be copied to the remote server that we want to authenticate with)
    + private key to `/Users/your_username/.ssh/your_name_specified` (which we will keep on our local machine to do authentication).

            :::bash
        	# on LOCAL:
        	$ ssh-keygen -t rsa -C "your_email_address"

    &#x27a9; You can specify a custom `your_name_specified.pub` for this.

    &#x27a9; Enter a passphrase (if you want).

    b. Copy public key to the server

        :::bash
    	# on LOCAL:
    	$ scp -P your_SSH_port ~/.ssh/your_name_specified.pub your_username@yourDNSdomain.com:

    	# on REMOTE:
    	$ mkdir .ssh
        $ mv your_name_specified.pub .ssh/authorized_keys
        $ chown -R your_username:your_username .ssh
        $ chmod 700 .ssh
        $ chmod 600 .ssh/authorized_keys
        $ exit

    &#x27a9; Now you can connect to your REMOTE VPS without providing a password, as long as you're connecting from the machine where you generated the SSH key with one of the following:

        :::bash
    	# on LOCAL:
        $ ssh -p your_SSH_port your_username@yourDNSdomain.com
        $ ssh -p your_SSH_port your_SSH_port@your_vps_ip`
    
    c. To avoid typing all the above out, you can modify your local SSH config file.
    
    &#x266b; Note, this will also allow you to have multiple saved SSH keys, for example if you had multiple REMOTE servers that you liked to log in to from the same LOCAL machine with different keys associated with each.

        :::bash
    	# on LOCAL:
    	$ nano ~/.ssh/config
    
    &#x27a9; Now you can set up remote servers you want to connect to, each getting their own block in this file.  Use following format:

        :::text
    	Host do                                    # nickname of this server
            HostName yourDNSdomain.com             # this can also be an IP address
            User your_username
            Port your_SSH_port
            IdentityFile "~/.ssh/your_private_key"
        Host awshost1                              # another server you connect to
            HostName some_other_ip_address
            User some_other_username
            IdentityFile "~/.ssh/some_other_combined_key.pem"

    &#x27a9; Once you're finished with this file, ctl-x to save and exit.
    
    From now on, on local machine, you can log in to your remote servers without passwords or remembering the IP addresses, ports, usernames for each one.  You just have to remember the alias you set up as `Host server_nickname` in the `.ssh/config` file.  I use `ssh do` so that my DigitalOcean VPS is just a couple keystrokes away from my local terminal window.

## IV. More advanced (optional) network security for your VPS

I ended up following a lot of the configurations suggested by [feross.org] [feross] and [cbracco.me] [cbracco].

1. Install/config [Fail2Ban] [f2b]

    Check out this DigitalOcean tutorial on [installing fail2ban] [do_fail2ban].

    a. Install it
    
        :::bash
    	# on REMOTE:
    	$ sudo aptitude install fail2ban

    b. Copy default to local jail file

        :::bash
    	# on REMOTE:
    	$ sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
        $ sudo nano /etc/fail2ban/jail.local

    c. Modify configuration file

    &#x27a9; If you have static IP on local machine, add it to `ignoreip` line

    &#x27a9; Change `bantime` from 10 minutes to 1 hour

    &#x27a9; Change `destemail = your_email_address`

    &#x27a9; Change action default to `action = %(action_mwl)s`

    &#x27a9; In `[ssh]` section, make sure enabled = true, and change port number to ours.

    &#x27a9; In `[ssh-ddos]` section, make sure enabled = true, and change port number to ours.

    &#x27a9; Use `ctl-x` to save and exit, and then `$ sudo service fail2ban restart`.

2. Set up [`Uncomplicated Firewall` or UFW] [ufw], which is a front-end to `iptables`.

    See this DigitalOcean tutorial on [installing ufw firewall] [do_ufw].

        :::bash
    	# on REMOTE:
    	$ sudo aptitude install ufw         # if not already installed:
        $ sudo status                       # verify UFW is off
        $ sudo ufw default deny incoming
        $ sudo ufw default allow outgoing
        $ sudo ufw logging on
        $ sudo ufw allow http/tcp
        $ sudo ufw allow 443                # this is https
        $ sudo ufw allow your_SSH_port/tcp  # enter your SSH port
        $ sudo ufw allow 21/tcp             # this is ftp

    Turn on and verify:

        :::bash
    	# on REMOTE:
    	$ sudo ufw enable
        $ sudo ufw status verbose

    &#x27a9; To get a numbered list of what rules are established: `$ sudo ufw status numbered`

    &#x27a9; Can then delete current rules with `$ sudo ufw delete [number]`

3. Enable auto security updates

    a. Install unattended-upgrades

        :::bash
        # on REMOTE:
        $ sudo aptitude install unattended-upgrades
        $ sudo nano /etc/apt/apt.conf.d/10periodic

    b. Overwrite lines to read:

        :::text
        APT::Periodic::Update-Package-Lists "1";
        APT::Periodic::Download-Upgradeable-Packages "1";
        APT::Periodic::AutocleanInterval "7";
        APT::Periodic::Unattended-Upgrade "1";

    c. Open

        :::bash
        # on REMOTE:
        $ sudo nano /etc/apt/apt.conf.d/50unattended-upgrades

    d. Overwrite lines to read:

        :::text
        # on REMOTE:
        Unattended-Upgrade::Allowed-Origins {
            "Ubuntu lucid-security";
        //      "${distro_id}:${distro_codename}-security";
        //      "${distro_id}:${distro_codename}-updates";
        //      "${distro_id}:${distro_codename}-proposed";
        //      "${distro_id}:${distro_codename}-backports";
        };

4. Have system auto-reboot if it runs out of memory

    See article at [fanclub.co.za] [fanclub] for more detail.

        :::bash
        # on REMOTE:
        $ sudo nano /etc/sysctl.conf

    &#x27a9; Add following lines to the bottom of the file, then `ctl-x` to save/exit:

        :::text
        vm.panic_on_oom=1
        kernel.panic=10

5. Secure shared memory

        :::bash
    	# on REMOTE:
    	$ sudo nano /etc/fstab

    &#x27a9; Add following lines to the bottom of the file: `tmpfs /dev/shm tmpfs defaults,noexec,nosuid 0 0`, then `ctl-x` to save/exit.

        :::bash
    	# on REMOTE:
    	$ sudo mount -a

6. Harden network with sysctl settings

        :::bash
    	# on REMOTE:
    	$ sudo nano /etc/sysctl.conf

    &#x27a9; Uncomment any of the following lines:

        :::text
    	net.ipv4.conf.default.rp_filter=1
        net.ipv4.conf.all.rp_filter=1
        net.ipv4.tcp_syncookies=1
        net.ipv4.conf.all.accept_redirects = 0
        net.ipv6.conf.all.accept_redirects = 0
        net.ipv4.conf.all.send_redirects = 0
        net.ipv4.conf.all.accept_source_route = 0
        net.ipv6.conf.all.accept_source_route = 0
        net.ipv4.conf.all.log_martians = 1

    Apply the new settings with:

        :::bash
        # on REMOTE:
        $ sudo sysctl -p

7. Prevent IP spoofing

        :::bash
    	# on REMOTE:
    	$ sudo nano /etc/host.conf

    &#x27a9; Add following line: `nospoof on`.

8. Check for rootkits with RKHunter and CHKRootKit

        :::bash
    	# on REMOTE:
    	$ sudo aptitude install rkhunter chkrootkit
        $ sudo chkrootkit
        $ sudo rkhunter --update
        $ sudo rkhunter --propupd
        $ sudo rkhunter --check

9. Analyze system log files with LogWatch

        :::bash
    	# on REMOTE:
    	$ sudo aptitude install sendmail
        $ sudo aptitude install logwatch libdate-manip-perl
        $ sudo logwatch | less
        $ sudo logwatch --mailto {your email address} --output mail --format html --range 'between -7 days and today'

10. Audit system security with Tiger

        :::bash
    	# on REMOTE:
    	$ sudo aptitude install tiger
        $ sudo tiger
        $ sudo less /var/log/tiger/security.report.*

## V. Set up nginx on VPS (web server to publish your website to the internet)

Check out this [DigitalOcean tutorial] [do_nginx] for reference.

1. Install and start nginx

        :::bash
    	# on REMOTE:
    	$ sudo aptitude install nginx
        $ sudo service nginx start      # to start nginx
        
    &#x266b; My default nginx version as installed by aptitude in Ubuntu was `nginx/1.1.19`.

    &#x27a9; Check nginx is on

        :::bash
    	# on REMOTE:
    	$ ifconfig eth0 | grep inet | awk '{ print $2 }'
    
    &#x27a9; Visit the IP returned in browser to see "Welcome to nginx", this is your server!

2. Confirm nginx is set to start automatically with the server.

        :::bash
    	# on REMOTE:
    	$ update-rc.d nginx defaults

    &#x266b; If you get back `System start/stop links for /etc/init.d/nginx already exist.`, it's already going to start automatically.

3. Change server_names_hash_bucket_size default in nginx.conf.

        :::bash
    	# on REMOTE:
    	$ sudo nano /etc/nginx/nginx.conf

    &#x27a9; Uncomment `# server_names_hash_bucket_size 64;`.

4. Customize the default nginx config.

        :::bash
    	# on REMOTE:
    	$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
        $ sudo nano /etc/nginx/sites-available/default

    &#x27a9; modify the file in `nano` like this:

        :::text
        server {
            listen   80; ## listen for ipv4; this line is default and implied
            listen   [::]:80 default ipv6only=on; ## listen for ipv6
        
            root /usr/share/nginx/html;
            index index.html index.htm index.php;
        
            # Make site accessible from http://localhost/
            server_name _;
            location / {
                try_files $uri $uri/ /index.html;
            }
        
            location /doc/ {
                alias /usr/share/doc/;
                autoindex on;
                allow 127.0.0.1;
                deny all;
            }
        
            # Redirect server error pages to the static page /50x.html
            error_page 500 502 503 504 /50x.html;
            location = /50x.html {
                root /usr/share/nginx/html;
            }
        
            # Pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
            location ~ \.php$ {
                fastcgi_split_path_info ^(.+\.php)(/.+)$;
                fastcgi_pass unix:/tmp/php5-fpm.sock;
                fastcgi_index index.php;
                include fastcgi_params;
            }
        
            # Deny access to .htaccess files, if Apache's document root concurs
            # with Nginx’s one
            location ~ /\.ht {
                deny all;
            }
        }

5.  Set up nginx Virtual Hosts (server blocks) to host multiple websites on single server

    There's a decent tutorial I referenced from the [DigitalOcean community] [do_virtualhosts].

    a. Create a directory to hold new website's HTML (use an actual DNS name)

        :::bash
    	# on REMOTE:
    	$ sudo mkdir -p /var/www/<your domain>/public_html

    &#x27a9; Also make a folder for the automated logs in the same area.

        :::bash
    	# on REMOTE:
    	$ sudo mkdir -p /var/www/<your domain>/logs

    b. Grant ownership and modification permissions.

        :::bash
    	# on REMOTE:
    	$ sudo chown -R <username>:www-data /var/www/<your domain>/public_html

    &#x27a9; Give read access to everyone.

        :::bash
    	# on REMOTE:
    	$ sudo chmod -R 755 /var/www

    c. Create a test index.html page

        :::bash
    	# on REMOTE:
    	$ sudo nano /var/www/<your domain>/public_html/index.html

    &#x27a9; in nano, copy/paste:

        :::html
    	<html>
            <head>
                <title>yourdomain.com</title>
            </head>
            <body>
                <h1>Good job man, you have set up a Virtual Host</h1>
            </body>
        </html>

    d. Create a new virtual host file by copying nginx default config document.

    I referenced [cbracco.me] [cbracco] some more here.

        :::bash
    	# on REMOTE:
    	$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/example.com
    	$ sudo nano /etc/nginx/sites-available/example.com

    &#x27a9; Begin editing your custom nginx config file

    &#x27a9; Uncomment `listen    80;` so that traffic coming through port 80 will be directed to site

    &#x27a9; Change the `root` extension to match our site's directory on the server

    &#x27a9; Change the `server_name` to your DNS domain

    &#x266b; For an example configuration, see below:

        :::text
    	...
        server {
                server_name www.jamesnewbrain.com;
                
                # rewrite www to non-www
                rewrite ^(.*) http://jamesnewbrain.com$1 permanent;
        }
        
        server {
                # Listening ports
                listen   80;                            ## listen for ipv4; this line is default and implied
                listen   [::]:80 default ipv6only=on;   ## listen for ipv6
        
                # Make site accessible from domain
                server_name jamesnewbrain.com;
        
                # Root directory
                root /var/www/jamesnewbrain.com/public_html;
                index index.html index.htm;
        
                # Logs
                access_log /var/www/jamesnewbrain.com/logs/access.log;
                error_log /var/www/jamesnewbrain.com/logs/error.log;
        
                # Includes
                include global/restrictions.conf;
        ...

    e. Create global/restrictions.conf

        :::bash
    	# on REMOTE:
    	$ sudo mkdir /etc/nginx/global
        $ sudo nano /etc/nginx/global/restrictions.conf

    &#x27a9; Edit file so that it resembles:

        :::text
        # Global restrictions configuration file.
        # Designed to be included in any server {} block.&lt;/p&gt;
        location = /favicon.ico {
            log_not_found off;
            access_log off;
        }
        
        location = /robots.txt {
            allow all;
            log_not_found off;
            access_log off;
        }
        
        # Deny all attempts to access hidden files such as .htaccess, .htpasswd, .DS_Store (Mac).
        # Keep logging the requests to parse later (or to pass to firewall utilities such as fail2ban)
        location ~ /\. {
            deny all;
        }
        
        # Deny access to any files with a .php extension in the uploads directory
        # Works in sub-directory installs and also in multisite network
        # Keep logging the requests to parse later (or to pass to firewall utilities such as fail2ban)
        location ~* /(?:uploads|files)/.*\.php$ {
            deny all;
        }

    f. Activate the host by symbolically linking the sites-available dir w/ the sites-enabled dir.

        :::bash
    	# on REMOTE:
    	$ sudo ln -s /etc/nginx/sites-available/<yourdomain.com> /etc/nginx/sites-enabled/<yourdomain.com>

    g. To avoid "conflicting server name error", delete the default nginx server block

        :::bash
    	# on REMOTE:
    	$ sudo rm /etc/nginx/sites-enabled/default

    h. Restart nginx

        :::bash
    	# on REMOTE:
    	$ sudo service nginx restart

## VI. Install Git, sync with our website's GitHub repo.

&#x27a9; Install `Git` on your REMOTE VPS.

    :::bash
    # on REMOTE:
    $ sudo aptitude install git-core
    
&#x266b; We will now clone our GitHub repo to our REMOTE server.  Again, I will show cloning this to `~/dev/jamesnewbrain/`, so apply your own pathing as you like.
    
&#x27a9; Get the HTTPS URL for your website's GitHub repo from the GitHub website.  Mine looks like `https://github.com/jfallisg/jamesnewbrain.git`.

    :::bash
    # on REMOTE:
    $ mkdir ~/dev
    $ cd dev
    $ git clone your_github_HTTPS_URL

&#x266b; You now have a copy of your current website repo on your remote server!  We still have a few steps to get this thing working the way we want to.

&#x27a9; To update your REMOTE repo, use:

    :::bash
	# on REMOTE:
    $ cd ~/dev/jamesnewbrain
    $ git pull origin master

## VII. Set up global Python environment on REMOTE

This is going to be a pretty similar procedure to our setup on our LOCAL machine, the difference being that we will use the `requirements.txt` file generated by `pip freeze` so that our Python `virtualenv` on our REMOTE server matches that of our development environment.

1. Install Python (Ubuntu 12.04 already has 2.7.3 installed)

2. Install [`pip`] [pip], the package manager for Python modules.

    &#x266b; You're using a `sudo` to install `pip` globally on your machine, since you'll typically want to be able to install/update/uninstall Python modules outside of any specific virtual environment we set up.

    &#x266b; We also install `python-dev` headers in case we will be compiling any python libraries that need them.

        :::bash
    	# on REMOTE:
    	$ sudo aptitude install python-pip python-dev
	
3. Install [`virtualenv`] [venv], the Python virtual environment management system.

    &#x266b; Remember that `virtualenv` allows you to compartmentalize sets of Python modules for specific projects from the globally installed modules on your entire system. This way you can have project-specific versions of modules and manage any conflicts between modules on a project-by-project basis.  It also allows you to sync your "blessed" set of Python modules from your LOCAL machine with your REMOTE machine, which we will do later in this procedure.

        :::bash
    	# on REMOTE:
    	$ sudo pip install virtualenv

## VIII. First time sync with GitHub project, finish Python environment setup (on REMOTE server)

1. Install Python environment from GitHub-synced `requirements.txt`

        :::bash
    	# on REMOTE:
    	$ cd ~/dev/jamesnewbrain
    	$ virtualenv env                   # create a Python virtualenv
    	$ source env/bin/activate          # active our Python virtualenv
    	$ pip install -r requirements.txt  # install our site's Python dependencies
    	$ pip freeze                       # check how it went

2. Add a symbolic link between output to project directory and sites-avail/public_html

## IX. Make a snapshot backup of your VPS now

The timing is good for a backup snapshot of your VPS, because all the software we need is installed and configured, but we haven't polluted the machine with any specific source code checkouts of our own.  By saving a snapshot now, if we need to get back to a configured image of our system, we can, but without having to redo all the time-consuming sys-admin activities we did earlier.

&#x27a9; To take a snapshot of the droplet, you'll need to stop your droplet form the command line.

    :::bash
	# on REMOTE:
	$ sudo shutdown -h now

&#x27a9; Now from the DigitalOcean dashboard, select to take a snapshot.  DigitalOcean will turn your server back on for you after they are done.

***

# PART 3: New blog posting workflow

## I. Write a post in Markdown, saving to content/ folder of project

## II. Use Pelican's simple dev server to preview/debug posts

    :::bash
    # on LOCAL:
    $ make devserver

&#x27a9; `ctl-c` doesn't completely kill the server, instead:

    :::bash
    # on LOCAL:
    $ sh develop_server.sh stop

## III. Commit completed post source to GitHub

    :::bash
	# on LOCAL:
    $ cd ~/dev/jamesnewbrain
    $ git add .
    $ git commit -m "describe changes"

## IV. Deploy on remote server

    :::bash
    # on REMOTE:
    $ cd somedir
    $ virtualenv <name of environment directory>
    $ source <name of environment directory>/bin/activate
    $ build HTML with Pelican
    # ? copy/update to that publish_html folder
    # ? have a git hook trigger it

***

# PART 4: Customizing website, automating deployment

***

## I. Customizing your Pelican theme

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

[elegant]:          http://oncrashreboot.com/elegant-best-pelican-theme-features
                    "Elegant - Best Pelican theme"

***

<!---
LINKS
-->
[beautsoup]:        http://www.crummy.com/software/BeautifulSoup/
                    "BeautifulSoup"
[bw]:               http://bywordapp.com/
                    "Byword 2"
[cbracco]:          http://cbracco.me/vps/
                    "cbracco.me - vps"
[claudiodangelis]:  http://www.claudiodangelis.com/2013/blogging-with-jekyll-using-git-github-and-amazon-aws/
                    "claudiodangelis.com - blogging with jekyll"
[clemsha]:          http://www.clemesha.org/blog/modern-python-hacker-tools-virtualenv-fabric-pip/
                    "clemsha.org - modern python hacker tools"
[dabapps]:          http://dabapps.com/blog/introduction-to-pip-and-virtualenv-python/
                    "dabapps.com - intro to pip and virtualenv"
[digitalocean]:     http://digitalocean.com
                    "DigitalOcean"
[dod]:              https://cloud.digitalocean.com/
                    "DigitalOcean - Dashboard"
[do_droplet]:       https://www.digitalocean.com/community/articles/how-to-create-your-first-digitalocean-droplet-virtual-server
                    "DigitalOcean - Droplet creation"
[do_fail2ban]:      https://www.digitalocean.com/community/articles/how-to-protect-ssh-with-fail2ban-on-ubuntu-12-04
                    "DigitalOcean - fail2ban"
[do_nginx]:         https://www.digitalocean.com/community/articles/how-to-install-nginx-on-ubuntu-12-04-lts-precise-pangolin
                    "DigitalOcean - nginx"
[do_serversetup]:   https://www.digitalocean.com/community/articles/initial-server-setup-with-ubuntu-12-04             
                    "digitalocean.com/community - initial server setup with ubuntu"
[do_setfqdn]:       https://www.digitalocean.com/community/questions/how-to-set-fqdn-in-ubuntu
                    "DigitalOcean - Set fqdn"
[do_sethostname]:   https://www.digitalocean.com/community/articles/how-to-set-up-a-host-name-with-digitalocean
                    "DigitalOcean set hostname tutorial"
[do_sshkeys]:       https://www.digitalocean.com/community/articles/how-to-use-ssh-keys-with-digitalocean-droplets
                    "DigitalOcean - SSH Keys"
[do_ufw]:           https://www.digitalocean.com/community/articles/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server
                    "DigitalOcean - ufw"
[do_virtualhosts]:  https://www.digitalocean.com/community/articles/how-to-set-up-nginx-virtual-hosts-server-blocks-on-ubuntu-12-04-lts--3
                    "DigitalOcean - virtual hosts"
[duncanlock1]:      http://duncanlock.net/blog/2013/05/17/how-i-built-this-website-using-pelican-part-1-setup/
                    "duncanlock.net - built website using pelican - pt 1"
[duncanlock2]:      https://github.com/dflock/duncanlock.net/blob/master/content/posts/tech/how-i-built-this-website-using-pelican-part-2-themes.rst
                    "duncanlock.net - built website using pelican - pt 2"
[f2b]:              http://www.fail2ban.org/wiki/index.php/Main_Page
                    "Fail2ban"
[fabric]:           http://docs.fabfile.org/en/1.8/
                    "Fabric"
[fanclub]:          http://www.thefanclub.co.za/how-to/how-secure-ubuntu-1204-lts-server-part-1-basics
                    "fanclub.co.za - secure ubuntu"
[feross]:           http://feross.org/how-to-setup-your-linode/
                    "feross.org - how to set up your linode"
[github]:           https://github.com/
                    "GitHub"
[gitignore]:        https://raw2.github.com/github/gitignore/master/Python.gitignore
                    "github.com - Python.gitignore"
[gtmanfred]:        http://blog.gtmanfred.com/setting-up-pelican-and-git.html
                    "gtmanfred.com - setting up pelican and git"
[homebrew]:         http://brew.sh/
                    "Homebrew - The missing package manager for OS X"
[ia]:               http://pngmini.com/
                    "ImageAlpha"
[io]:               http://imageoptim.com/
                    "ImageOptim"
[linode]:           https://www.linode.com/
                    "Linode"
[jamesmurty]:       http://jamesmurty.com/2013/05/23/migrate-wordpress-blog-to-static-site/
                    "jamesmurty.com - wordpress to static"
[jekyll]:           http://jekyllrb.com/
                    "Jekyll Ruby"
[markdown]:         http://daringfireball.net/projects/markdown/
                    "Markdown"
[martinbrochhaus]:  http://martinbrochhaus.com/pelican2.html
                    "martinbrochhaus.com - pelican"
[nginx]:            http://wiki.nginx.org/Main
                    "nginx"
[nv]:               http://brettterpstra.com/projects/nvalt/
                    "nvALT"
[pelican]:          http://docs.getpelican.com/en/3.3.0/
                    "Get Pelican"
[pip]:              http://www.pip-installer.org/en/latest/
                    "pip"
[pelican-themes]:   http://pelicanthemes.com/
                    "Preview Pelican Themes"
[plcn-thm-galary]:  http://pelican-themes-gallery.place.org/
                    "Pelican Theme Galary"
[plcn_thm_repo]:    https://github.com/getpelican/pelican-themes
                    "Pelican themes repo"
[python]:           http://www.python.org/
                    "Python"
[so_ports]:         http://unix.stackexchange.com/questions/16564/why-are-the-first-1024-ports-restricted-to-the-root-user-only
                    "stackoverflow - first 1024 ports"
[tw]:               http://www.barebones.com/products/textwrangler/
                    "TextWrangler"
[ufw]:              https://help.ubuntu.com/community/UFW
                    "Uncomplicated Firewall"
[venv]:             http://www.virtualenv.org/en/latest/
                    "Fabric"
[wiki_TCP]:         http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
                    "wikipedia - List of TCP and UDP port numbers"
[xlarrakoetxea]:    http://blog.xlarrakoetxea.org/posts/2012/10/creating-a-blog-with-pelican/
                    "xlarrakoetxea.org - creating a blog with pelican"