import sys
import json
import time
import shutil
import tempfile
import os
import codecs
import webbrowser


from flask import Flask, request
from flask.ext.cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def hello():
    texts = []
    images = []
    for item in request.form.items():
        if item[0].startswith("text"):
            texts.append((int(item[0][4:]), item[1]))
        else: # image
            images.append((int(item[0][5:]), item[1]))
    texts.sort(key=lambda tup: tup[0])
    images.sort(key=lambda tup: tup[0])
    # get deck name from image URL
    deck = images[0][1].split("/")[-2]
    with open("{}.html".format(deck), "w") as f:
        f.write(top_of_index)
        slide_data = []
        for index, item in enumerate(texts):
            slide_item = '\n{"text":"'+ item[1] + '","image":"'+ os.path.join(deck, images[index][1].split("/")[-1]) + '"}'
            slide_data.append(slide_item)
        f.write(",".join(slide_data))
        f.write(bottom_of_index)
    webbrowser.open( os.path.join("file://{}".format(os.getcwd()), "{}.html#test".format(deck)) )
    os._exit(1)

#### Prepare form with images    

html_file_name = 'nodes_form.htm'

def stem(file_name_or_path):
    head, file_name = os.path.split(file_name_or_path)
    return ".".join(file_name.split(".")[0:len(file_name.split("."))-1])


class Slides():
    def read_and_parse(self, file_path, files):
        image_urls = ["file://{}/{}".format(file_path, item) for item in files]

        htmlFile = codecs.open(os.path.join(os.getcwd(), html_file_name), encoding='utf-8', mode='w+')
        writeHtmlHeader2(htmlFile)
        for index, image_url in enumerate(image_urls):
            writeSlide2(htmlFile, image_url, index)
        writeHtmlFooter2(htmlFile)
        htmlFile.close()
        print("Created {}".format(html_file_name))
        webbrowser.open( os.path.join("file://{}".format(os.getcwd()), html_file_name) )


def writeHtmlHeader2(htmlFile):
    htmlFile.write('''<!doctype html>
<html lang="en">

    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://cdn.firebase.com/js/client/2.4.2/firebase.js"></script>
<style type="text/css">
textarea {
   font-size: 20pt;
   font-family: Arial;
}

button {
   font-size: 20pt;
   font-family: Arial;
   height:300px;
   width:100px;
}

.save_button {
   margin-left: 2px;
   height:100px;
   width:100%;
}
</style>
    </head>

    <body>
<script>
function play_text(id) {
 speak(document.getElementById("textarea"+id).value);
}

function speak(text) {
    // text can contain <break/> tags for pauses
    var lines = text.split('<break/>').reverse();  // ['is a test', 'This']
    step_through_lines(lines);
}

function step_through_lines(lines) {
    // When there are no lines
    if (!lines || lines.length == 0) {
        return;
    }
    var speak_text = new SpeechSynthesisUtterance(lines.pop());
    speak_text.onend = function(e) {
        step_through_lines(lines);
    };
    window.utterances = [];
    utterances.push( speak_text );
    speechSynthesis.speak(speak_text);
}

function save_slide_texts() {
    var newSlideTexts = {};
    var images = $( "img" );
    $( "textarea" ).each(function( index ) {
      newSlideTexts["text"+index] = $( this ).val();
      newSlideTexts["image"+index] = images[index].src;
    });
    $.post('http://localhost:5000/', newSlideTexts);
}
</script>
<button class="save_button" onclick="save_slide_texts();">Save</button>
    <div id="playid"></div>
<table>''')

def writeSlide2(htmlFile, image_file_name, number):
    htmlFile.write("""<tr><td valign="top"><img src="{image_file_name}" height="300px"></td>
<td valign="top"><button onclick="play_text({number})">Play</button></td>
<td valign="top"><textarea id="textarea{number}" rows="8" cols="50" tabindex={number_plus_one}></textarea></td>
</tr>
""".format(image_file_name=image_file_name, number=number, number_plus_one=number + 1))


def writeHtmlFooter2(htmlFile):
    htmlFile.write("""
    </table>
    </body>
</html>
""")


### Prepare static index.html to play slides

top_of_index = """
<!doctype html>
<html lang="en">

    <head>
        <meta charset="utf-8">

        <title>reveal.js – The HTML Presentation Framework</title>

        <meta name="description" content="A framework for easily creating beautiful presentations using HTML">
        <meta name="author" content="Hakim El Hattab">

        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, minimal-ui">

        <link rel="stylesheet" href="css/reveal.css">
        <link rel="stylesheet" href="css/theme/black.css" id="theme">

        <!-- Code syntax highlighting -->
        <link rel="stylesheet" href="lib/css/zenburn.css">

        <!-- Printing and PDF exports -->
        <script>
            var link = document.createElement( 'link' );
            link.rel = 'stylesheet';
            link.type = 'text/css';
            link.href = window.location.search.match( /print-pdf/gi ) ? 'css/print/pdf.css' : 'css/print/paper.css';
            document.getElementsByTagName( 'head' )[0].appendChild( link );
        </script>
    <script   src="https://code.jquery.com/jquery-2.2.3.min.js"   integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo="   crossorigin="anonymous"></script>

        <!--[if lt IE 9]>
        <script src="lib/js/html5shiv.js"></script>
        <![endif]-->
    </head>

    <body onload="fetch_slides();">


        <div class="reveal">

            <!-- Any section element inside of this container is displayed as a slide -->
            <div class="slides" id="slides">

            </div>

        </div>

        <script src="lib/js/head.min.js"></script>
        <script src="js/reveal.js"></script>

    <script type="text/javascript">
        function fetch_slides() {
            var hash = window.location.href.split('#')[1];
            if (hash == "test" || window.location.href.startsWith('file:') == false) {
            var data = ["""

bottom_of_index = """]
                for (var i = 0; i < data.length; i++) {
                    var section_node = document.createElement("section");                 // Create a <section> node
                    if (data[i]["text"].length > 0) section_node.setAttribute("title", data[i]["text"]);
                    var img_node = document.createElement("img");         // Create a <img> node
                    img_node.setAttribute("src", data[i]["image"])
                    section_node.appendChild(img_node); 
                    document.getElementById("slides").appendChild(section_node);
                }
}

                // Full list of configuration options available at:
                // https://github.com/hakimel/reveal.js#configuration
                Reveal.initialize({
                    controls: true,
                    progress: true,
                    history: true,
                    center: true,

                    transition: 'slide', // none/fade/slide/convex/concave/zoom

                    // Optional reveal.js plugins
                    dependencies: [
                        { src: 'lib/js/classList.js', condition: function() { return !document.body.classList; } },
                        { src: 'plugin/markdown/marked.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                        { src: 'plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                        { src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
                        { src: 'plugin/zoom-js/zoom.js', async: true },
                        { src: 'plugin/notes/notes.js', async: true }
                    ]
                });
            }
    </script>

    </body>
</html>
"""


def main(argv):
    if len(argv) < 2:
        print( """
Usage: python add_script_to_local_png.py <path to png folder>
       or 
       python add_script_to_local_png.py <full path to pdf file>

Notes: If <full path to pdf file>, then convert will generate .png files.
       Images will be copied to local deck<timestamp> folder.
       deck<timestamp>.html and folder can be deployed to firebase.
""")
    else:
        time_stamp = time.time()
        deck_folder = "deck{}".format(int(time_stamp))
        os.mkdir(deck_folder)
        file_path = os.path.abspath(argv[1])
        if file_path.endswith(".pdf"):
            with tempfile.TemporaryDirectory() as tmpdirname:
                print('created temporary directory', tmpdirname)
                path, file = os.path.split(file_path)
                shutil.copyfile(file_path, os.path.join(tmpdirname, file))
                current_working_directory = os.getcwd()
                os.chdir(tmpdirname)
                file_stem, file_ext = os.path.splitext(file)
                os.system('convert "{}" "{}.png"'.format(file, file_stem))
                files = os.listdir(tmpdirname)
                files = [item for item in files if item[-4:] in [".png",".jpg"]]
                files.sort(key=lambda x: int(x.split("-")[-1].split(".")[0]))
                print( "\nUsing {} files from {}\n".format(len(files), tmpdirname))
                for file in files:
                    shutil.copyfile(os.path.join(tmpdirname, file), os.path.join(current_working_directory, deck_folder, file))
                os.chdir(current_working_directory)
        else:
            files = os.listdir(file_path)
            files = [item for item in files if item[-4:] in [".png",".jpg"]]
            print( "\nUsing {} files from {}\n".format(len(files), file_path))
            for file in files:
                shutil.copyfile(os.path.join(file_path, file), os.path.join(deck_folder, file))
        try:
            os.remove(os.path.join(deck_folder, "index.html"))
        except OSError:
            pass
        slides = Slides()
        slides.read_and_parse(os.path.abspath(deck_folder), files)
        app.run()


if __name__ == "__main__":
    main(sys.argv)
