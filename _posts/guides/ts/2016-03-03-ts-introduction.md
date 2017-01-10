---
title: Preface
categories: guides ts
permalink: /guides/ts/introduction.html
layout: default
---

On your path to becoming a typesetter, the most important change you will see is that you will begin to have a clear vision of what you want to do, and hopefully why you want to do it. The questions I ask and attempt to answer here are a good place to start figuring out how you want to do things.

### What is typesetting?

Typesetting in general is a very broad field, but within the context of anime fansubbing it generally corresponds to aligning text and drawings on the anime video in order to translate certain signs in an effort to allow non-Japanese viewers to understand the non-verbal ways in which the show communicates with the viewer. That is a very long sentence that boils down to: "We translate Japanese signs by putting text on the screen." 

### What do we use to typeset?

Before I start talking about the standard tools used in fansubbing currently, I should mention that what you use to typeset depends on what you want the end-result to be like. If you as a typesetter (and the rest of your group) are satisfied with encoding your subtitles over the Japanese video, the tool you should be using is Adobe After Effects, and this guide will not help you with that. However, should you desire to do your work in a format that is rendered in real-time along with the video, Aegisub is the tool for you. 

### What is Aegisub?

The format for subtitle files is called the ASS format (short for Alpha Sub Station). Aegisub is the only editor for this format that allows you to render the subs in the editor and offers several graphical tools to assist the user in setting up the subs the way they want. In addition, it supports the use of user-installed Lua and Moon scripts, which allows the user to expand the functionality of Aegisub significantly. It is worth mentioning that any .ass file is simply a text file following a specific format, and, if you wanted to, you could simply work in your text editor. However, if you wanted to test how something would look, you would need to set up something to show the video and the subtitles at the frames you are interested in. This is exactly what Aegisub does for you, so I'm not sure why you would do that.

### How does this text become what shows up when I play the video?

To make a very long story short, the video player has a subtitle renderer that works with the .ass file after it is split from the rest of the .mkv file. Currently, there are two leading renderers. There is libass, which comes with almost every video player that supports subtitle rendering (though most of them come with some older version). libass comes with the nice benefits that it is cross-platform and that there is active development on it and it is continually being improved in order to achieve faster and more consistent performance. The other general renderer is vs-filter, which has several variants, which are for all intents and purposes the same thing. vs-filter only supports Windows. It is also no longer being developed. libass and vs-filter behave identically (with a few notable exceptions that I will explain when they come up).
