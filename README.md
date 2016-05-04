# revealjs_with_speech
Mashup of RevealJS with HTML5 Speech Synthesis

Started with [RevealJS](http://lab.hakim.se/reveal-js/) slides.

Wanted ability to add voice over to .png images generated from .pdf file.

Python code does this:
 * On Mac with **convert** (ImageMagik), generates .png from .pdf into deck folder.
 * Wraps .png files in an HTML file, nodes_form.htm, which allows typing in the script for the voice over on each slide.
 * Wraps the slide text and images in deck.html file.

A deck.html with folder and associated css, js, lib and plugin folders can be deployed on Firebase, like [this](http://makeitstick20160504.firebaseapp.com).

