# Renormalized

Welcome to my personal site. While I am not particularly interested in writing much, occasionally I will use this to say things that I feel need to be said, usually relating to topics in physics, music, and computer science. The primary goal of the site, however, is for me to get some hands on experience in developing a lean, optimized, yet feature-rich, static site.

## Setting Up the Repo

First, you need to install [RubyGems](https://rubygems.org/), clone this repo, and navigate into it. Then, execute these commands:

```commandline
gem install bundler jekyll
bundle install
```

If you do not have permissions to write to your RubyGems directory, either run the install with `sudo` or use a virtual environment. How to set up the virutal environment, if you choose to go that route, is on you.

## Building the Site

To give space for the local build approach taken on this site, the default branch for development is `src`. The `master` branch is a subtree based off the dist directory. This logic is handled entirely by the `build` and `deploy` scripts in the root directory.

To build the site, execute:

```commandline
./build
```

To run the site (you can see it at http://localhost:4000), execute:

```commandline
./serve
```

To deploy the site, which includes a push to `origin/master`, execute:

```commandline
./deploy
```

## Goals

### Long-term

- Styling
- Service workers
- Javascript science demos (double pendulum, Ising model)

### Short-term

- Meta tags (Done, mostly)
- Decisions regarding images (idea: default profile for no image, otherwise use big image twitter card and use that)
- Decisions regarding categories (will probably be fairly general)
- Style tables
- Style block quotes
- Decision regarding blog and main page (samples of blog, dev, and music posts?)
- Footer
- Prev/next buttons
- Read-more buttons for posts
- Image left right asymmetry
- About page
- Home page
- Come up with good handling for categories
