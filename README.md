# WEFUNK API -- a RESTful endpoint for accessing wefunkradio.com

## Purpose
WEFUNKradio, based out of Montreal, has an archive full of funky, rappy, jazzy tracks, dating back 10 years. Their website is great, but that's on their website. I'd like to be able to access it in other ways. In particular, I'd like to have the flexibility to write a slick mobile (namely Android) app without being beholden to the current website's layout. This endpoint aims to provide a structured-data look at the shows' history.

## Contents
This repository hosts code meant to run on Google's Appspot. It can similarly work by downloading the [SDK](http://code.google.com/appengine/downloads.html) and running it locally, but why do this when it's already running at [wefunk-api.appspot.com](http://wefunk-api.appspot.com/)?

## The endpoints
### /shows/[total]/[starting_at]/

Return show metadata, optionally limiting it to `[total]` entries and beginning at `[starting_at]`. (I know this isn't an optimal endpoint description, but we're in alpha.)

## License
All code is GPL/MIT/Apache, take your pick.
