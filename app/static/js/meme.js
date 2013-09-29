/*
Meme.js
=======

Use one function to generate a meme.

You can call it all with strings:

     Meme('dog.jpg', 'canvasID', 'Buy pizza, 'Pay in snakes');

Or with a selected canvas element:

     var canvas = document.getElementById('canvasID');
     Meme('wolf.jpg', canvas, 'The time is now', 'to take what\'s yours');

Or with a jQuery/Zepto selection:

     Meme('spidey.jpg', $('#canvasID'), 'Did someone say', 'Spiderman JS?');

You can also pass in an image:

     var img = new Image();
     img.src = 'insanity.jpg';
     var can = document.getElementById('canvasID');
     Meme(img, can, 'you ignore my calls', 'I ignore your screams of mercy');

********************************************************************************

Copyright (c) 2012 BuddyMeme

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/


/*
function fileSelect(evt) {
    var files = evt.target.files;
    var selectedFile = evt.target.files[0];
    var p = document.getElementById('placeholder');
    var c = document.getElementById('canvas');
    var ctx = c.getContext("2d");

    var reader = new FileReader();

    //once data is read, load data into canvas
    reader.onload = function(event) {
        var c = document.getElementById('canvas');
        var img = new Image();
        img.src = event.target.result;

        c.width = img.width;    c.height = img.height;
        var ctx = c.getContext("2d")
        ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, img.width, img.height);
    };

    reader.readAsDataURL(selectedFile);

    var result = '';
    var file;
    for (var i = 0; file = files[i]; i++) {
        result += '<li>' + file.name + ' ' + file.size + ' bytes</li>';
    }
    document.getElementById('filesInfo').innerHTML = '<ul>' + result + '</ul>';

    c.style.display="block";
    p.style.display="none";
}

document.getElementById('filesToUpload').addEventListener('change', fileSelect, false);

function post_image(evt) {
    //transform canvas into img tag
}

document.getElementById('image_post_button').addEventListener('click', fileSelect, false);
*/


function meme_me() {
    //get img tag
    var preview = document.getElementById("img_preview");
    var img = preview.childNodes[0];
    if(!img)
        return;

    //create virtual canvas
    //var canvas = document.createElement('canvas');
    var canvas = document.getElementById("img_canvas");
    if(!canvas)
        return;

    var meme1 = document.getElementById("meme1").value;
    if(!meme1)
        meme1 = 'you ignore my calls';

    var meme2 = document.getElementById("meme2").value;
    if(!meme2)
        meme2 = 'I ignore your screams of mercy';

    var image = new Image();
    image.src = img.src;
    Meme(image, canvas, meme1, meme2);

    preview.removeChild(img);

    //img.remove();
    /*
    var new_image = new Image();
    new_image.src = canvas.toDataURL("image/png");
    preview.appendChild(new_image);
*/

    var new_image = new Image();
    setTimeout(function() {
        var url = canvas.toDataURL("image/png");
        new_image.src = url;
        preview.appendChild(new_image);
        var new_meow_image = document.getElementById("new_meow_image");
        new_meow_image.src = url;
    }, 100);
}

window.Meme = function(image, canvas, top, bottom) {

	/*
	Default top and bottom
	*/

	top = top || '';
	bottom = bottom || '';

	/*
	Deal with the canvas
	*/

	// If it's nothing, set it to a dummy value to trigger error
	if (!canvas)
		canvas = 0;

	// If it's a string, conver it
	if (canvas.toUpperCase)
		canvas = document.getElementById(canvas);

	// If it's jQuery or Zepto, convert it
	if (($) && (canvas instanceof $))
		canvas = canvas[0];

	// Throw error
	if (!(canvas instanceof HTMLCanvasElement))
		throw new Error('No canvas selected');

	// Get context
	var context = canvas.getContext('2d');

	/*
	Deal with the image
	*/

	// If there's no image, set it to a dummy value to trigger an error
	if (!image)
		image = 0;

	// Convert it from a string
	if (image.toUpperCase) {
		var src = image;
		image = new Image();
		image.src = src;
	}

	// Set the proper width and height of the canvas
	var setCanvasDimensions = function(w, h) {
		canvas.width = w;
		canvas.height = h;
	};
	setCanvasDimensions(image.width, image.height);

	/*
	Draw a centered meme string
	*/

	var drawText = function(text, topOrBottom, y) {

		// Variable setup
		topOrBottom = topOrBottom || 'top';
		var fontSize = (canvas.height / 8);
		var x = canvas.width / 2;
		if (typeof y === 'undefined') {
			y = fontSize;
			if (topOrBottom === 'bottom')
				y = canvas.height - 10;
		}

		// Should we split it into multiple lines?
		if (context.measureText(text).width > (canvas.width * 1.1)) {

			// Split word by word
			var words = text.split(' ');
			var wordsLength = words.length;

			// Start with the entire string, removing one word at a time. If
			// that removal lets us make a line, place the line and recurse with
			// the rest. Removes words from the back if placing at the top;
			// removes words at the front if placing at the bottom.
			if (topOrBottom === 'top') {
				var i = wordsLength;
				while (i --) {
					var justThis = words.slice(0, i).join(' ');
					if (context.measureText(justThis).width < (canvas.width * 1.0)) {
						drawText(justThis, topOrBottom, y);
						drawText(words.slice(i, wordsLength).join(' '), topOrBottom, y + fontSize);
						return;
					}
				}
			}
			else if (topOrBottom === 'bottom') {
				for (var i = 0; i < wordsLength; i ++) {
					var justThis = words.slice(i, wordsLength).join(' ');
					if (context.measureText(justThis).width < (canvas.width * 1.0)) {
						drawText(justThis, topOrBottom, y);
						drawText(words.slice(0, i).join(' '), topOrBottom, y - fontSize);
						return;
					}
				}
			}

		}

		// Draw!
		context.fillText(text, x, y, canvas.width * .9);
		context.strokeText(text, x, y, canvas.width * .9);

	};

	/*
	Do everything else after image loads
	*/

	image.onload = function() {

		// Set dimensions
		setCanvasDimensions(this.width, this.height);

		// Draw the image
		context.drawImage(image, 0, 0);

		// Set up text variables
		context.fillStyle = 'white';
		context.strokeStyle = 'black';
		context.lineWidth = 2;
		var fontSize = (canvas.height / 8);
		context.font = fontSize + 'px Impact';
		context.textAlign = 'center';

		// Draw them!
		drawText(top, 'top');
		drawText(bottom, 'bottom');

	};

};