Title: nksaidwhat
Date: 2014-03-05 13:49
Modified: 2014-03-05 13:49
Slug: nksaidwhat 
disqus_identifier: nksaidwhat
Author: James Fallisgaard
Summary: nksaidwhat project page

*Part of a broader analytics project concerning North Korean media coverage*

## Project overview
North Korea is a sometimes confoundingly behaving and famously insular nation.  We get a very specific narrative about this country through the media.  You read about their sometimes hilarious behaving dynasty of dear leaders, you hear about complete international isolation, you hear horror stories about work camps, stories from defectors, stories from people who visit and find varying degrees of backward Orwellian state, you see a satellite photo of the nation in darkness surrounded by east asian nations that adopted more capitalist ideals and have drastically modernized over the past 60 years since the Korean War.

+ But how accurate or representative are these stories and sources?
+ How isolated or seemingly bad behaving is this country in the context of the normalized behavior of the rest of the actors in the international community?
+ How much narrative bias have we attached to North Korea, can these things be quantitatively analyzed?

There is a wealth of data available across the internet media regarding the behavior of North Korea over time both internally and amongst the international community.

This project seeks to, through modern data analytics and visualization techniques, peel back the top layers of common narrative regarding North Korea and see what we can infer from textual analysis of international news media.

## Blog post links covering project progress

They will be linked here.

## Project backlog (reprioritized as we develop)

1. Analysis framework for N. Korea's state newspaper archives [kcna.co.jp] [kcna]
	1. kcna.co.jp data miner / scraper functional end-to-end in O.O. Python
	2. Text-indexing database (MongoDB?) to receive payloads from data miner
		1. Auto mirror of KCNA
		2. See differences (ie, a name gets scraped from historical record)
	3. Data processing daemon to field REST API on database server
	4. queryable JSON REST API
2. Project's first analysis deliverable
	1. simple project website (Pelican)
	2. data exploration and analysis
	3. final report with analytics in D3
3. Next data sources / analyses (scrape google news?) --> low visibility at this level of backlog

***

<!--- LINKS -->
[gh_nksaidwhat]:    https://github.com/jfallisg/nksaidwhat
                    "GitHub - nksaidwhat"
[kcna]:             http://www.kcna.co.jp/index-e.htm
                    "KCNA - english"