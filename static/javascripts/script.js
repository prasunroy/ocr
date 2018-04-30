// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// OCR front-end client interface.
// Created on Mon Jul 10 11:00:00 2017
// Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
// GitHub: https://github.com/prasunroy/ocr
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


// --------------------------------------------------------------------------------
// initialization
// --------------------------------------------------------------------------------

// get canvas
var canvas = document.querySelector('canvas');

// setup canvas
canvas.width = canvas.parentNode.getBoundingClientRect().width - canvas.offsetLeft * 2 - 2;
canvas.height = canvas.parentNode.getBoundingClientRect().height;

// get context of canvas
context = canvas.getContext('2d');

// setup background of canvas
context.fillStyle = 'rgb(255, 240, 165)';
context.fillRect(0, 0, canvas.width, canvas.height);

// mouse object
var mouse = {
    prevX: undefined,
    prevY: undefined,
    active: false
};

// touch object
var touch = {
    prevX: undefined,
    prevY: undefined,
    active: false
};

// options object
var options = {
    activeView: 'embedded-view',
    segmentationMode: 'contour',
    recognitionEngine: 'en-numbers',
    restEndpoint: 'http://localhost:5000/recognize'
};


// --------------------------------------------------------------------------------
// mouse events on canvas
// --------------------------------------------------------------------------------

canvas.addEventListener('mouseup', function(event) {
    mouse.prevX = undefined;
    mouse.prevY = undefined;
    mouse.active = false;
}, false);

canvas.addEventListener('mousedown', function(event) {
    mouse.active = true;
}, false);

canvas.addEventListener('mousemove', function(event) {
    if(!mouse.active)
        return;

    if(mouse.prevX == undefined)
        mouse.prevX = event.x;
    if(mouse.prevY == undefined)
        mouse.prevY = event.y;

    var offsetX = canvas.getBoundingClientRect().left;
    var offsetY = canvas.getBoundingClientRect().top;

    context.beginPath();
    context.arc(mouse.prevX - offsetX, mouse.prevY - offsetY, 1.6, 0, 2*Math.PI);
    context.fillStyle = '#000000';
    context.fill();

    context.beginPath();
    context.moveTo(mouse.prevX - offsetX, mouse.prevY - offsetY);
    context.lineTo(event.x - offsetX, event.y - offsetY);
    context.lineWidth = 4;
    context.stroke();

    mouse.prevX = event.x;
    mouse.prevY = event.y;
}, false);


// --------------------------------------------------------------------------------
// touch events on canvas
// --------------------------------------------------------------------------------

canvas.addEventListener('touchend', function(event) {
    touch.prevX = undefined;
    touch.prevY = undefined;
    touch.active = false;
}, false);

canvas.addEventListener('touchstart', function(event) {
    touch.active = true;
}, false);

canvas.addEventListener('touchmove', function(event) {
    if(!touch.active)
        return;

    if(touch.prevX == undefined)
        touch.prevX = event.touches[0].clientX;
    if(touch.prevY == undefined)
        touch.prevY = event.touches[0].clientY;

    var offsetX = canvas.getBoundingClientRect().left;
    var offsetY = canvas.getBoundingClientRect().top;

    context.beginPath();
    context.arc(touch.prevX - offsetX, touch.prevY - offsetY, 1.6, 0, 2*Math.PI);
    context.fillStyle = '#000000';
    context.fill();

    context.beginPath();
    context.moveTo(touch.prevX - offsetX, touch.prevY - offsetY);
    context.lineTo(event.touches[0].clientX - offsetX, event.touches[0].clientY - offsetY);
    context.lineWidth = 4;
    context.stroke();

    touch.prevX = event.touches[0].clientX;
    touch.prevY = event.touches[0].clientY;
}, false);

// prevent scrolling when touching the canvas
document.body.addEventListener('touchend', function(event) {
    if(event.target == canvas)
        event.preventDefault();
}, false);

document.body.addEventListener('touchstart', function(event) {
    if(event.target == canvas)
        event.preventDefault();
}, false);

document.body.addEventListener('touchmove', function(event) {
    if(event.target == canvas)
        event.preventDefault();
}, false);


// --------------------------------------------------------------------------------
// resize event
// --------------------------------------------------------------------------------

window.addEventListener('resize', function(event) {
    canvas.width = canvas.parentNode.getBoundingClientRect().width - canvas.offsetLeft * 2 - 2;

    // setup background of canvas
    context.fillStyle = 'rgb(255, 240, 165)';
    context.fillRect(0, 0, canvas.width, canvas.height);

    // reset animation and textarea
    outputRenderer(hideAnim=true, hideText=true, text='', triggerFloatingViewMode=false);
}, false);


// --------------------------------------------------------------------------------
// clear button
// --------------------------------------------------------------------------------

var clear = document.getElementById('clear');

clear.onclick = function(event) {
    context.clearRect(0, 0, canvas.width, canvas.height);

    // setup background of canvas
    context.fillStyle = 'rgb(255, 240, 165)';
    context.fillRect(0, 0, canvas.width, canvas.height);

    // reset animation and textarea
    outputRenderer(hideAnim=true, hideText=true, text='', triggerFloatingViewMode=false);
};


// --------------------------------------------------------------------------------
// recognize button
// --------------------------------------------------------------------------------

var recognize = document.getElementById('recognize');

recognize.onclick = function(event) {
    // show animation and hide textarea
    outputRenderer(hideAnim=false, hideText=true, text='');

    // convert canvas data to base64 encoded image data
    var canvasData = canvas.toDataURL('image/png');

    // transmit encoded image to recognition api end-point
    $.ajax({
        type: 'POST',
        url: options.restEndpoint,
        data: {
            imageBase64: canvasData,
            segmentationMode: options.segmentationMode,
            recognitionEngine: options.recognitionEngine
        }
    }).done(function(response) {
        // hide animation and show textarea
        outputRenderer(hideAnim=true, hideText=false, text=response);
    });
};


// --------------------------------------------------------------------------------
// browse button
// --------------------------------------------------------------------------------

var browse = document.getElementById('browse');
var imfile = null;

browse.onchange = function(event) {
    imfile = event.target.files[0];

    // verify whether image file
    var iminfo = '';

    if(imfile && imfile.type.match('image.*'))
        iminfo = imfile.name + '\t' + Math.ceil(imfile.size / 1024).toString() + ' KB';
    else
        imfile = null;

    document.getElementById('fileinfo').value = iminfo;
};


// --------------------------------------------------------------------------------
// upload button
// --------------------------------------------------------------------------------

var upload = document.getElementById('upload');

upload.onclick = function(event) {
    // create a file reader
    var reader = new FileReader();

    // transmit encoded image to recognition api end-point after reading
    reader.onload = function (event) {
        $.ajax({
            type: 'POST',
            url: options.restEndpoint,
            data: {
                imageBase64: reader.result,
                segmentationMode: options.segmentationMode,
                recognitionEngine: options.recognitionEngine
            }
        }).done(function(response) {
            // hide animation and show textarea
            outputRenderer(hideAnim=true, hideText=false, text=response);
        });
    };

    if(imfile) {
        // show animation and hide textarea
        outputRenderer(hideAnim=false, hideText=true, text='');

        // read image file as base64 encoded image data
        reader.readAsDataURL(imfile);
    }
};


// --------------------------------------------------------------------------------
// menu controllers
// --------------------------------------------------------------------------------

var menu = document.getElementById('menu');
var viewOption = menu.getElementsByClassName('view-option');
var prevViewOp = menu.getElementsByClassName('view-option selected')[0];
var segmOption = menu.getElementsByClassName('segm-option');
var prevSegmOp = menu.getElementsByClassName('segm-option selected')[0];
var engnOption = menu.getElementsByClassName('re-option');
var prevEngnOp = menu.getElementsByClassName('re-option selected')[0];

// do not automatically hide dropdown menu when clicked
menu.onclick = function(event) {
    event.stopPropagation();
};

// view controller
for(var i = 0; i < viewOption.length; i++) {
    viewOption[i].onclick = function(event) {
        prevViewOp.classList.remove('selected');
        this.classList.add('selected');
        prevViewOp = this;
        options.activeView = this.id;
    };
}

// segmentation controller
for(var i = 0; i < segmOption.length; i++) {
    segmOption[i].onclick = function(event) {
        prevSegmOp.classList.remove('selected');
        this.classList.add('selected');
        prevSegmOp = this;
        options.segmentationMode = this.id;
    };
}

// engine controller
for(var i = 0; i < engnOption.length; i++) {
    engnOption[i].onclick = function(event) {
        prevEngnOp.classList.remove('selected');
        this.classList.add('selected');
        prevEngnOp = this;
        options.recognitionEngine = this.id;
    };
}


// --------------------------------------------------------------------------------
// output renderer
// --------------------------------------------------------------------------------

function outputRenderer(hideAnim=true, hideText=true, text='', triggerFloatingViewMode=true) {
    // setup view
    if(options.activeView == 'embedded-view') {
        document.getElementById('anim').hidden = hideAnim;
        document.getElementById('text').hidden = hideText;
        document.getElementById('text').innerHTML = text;
        document.getElementById('modal-anim').hidden = true;
        document.getElementById('modal-text').hidden = true;
        document.getElementById('modal-text').innerHTML = '';
    }
    else if(options.activeView == 'floating-view') {
        document.getElementById('anim').hidden = true;
        document.getElementById('text').hidden = true;
        document.getElementById('text').innerHTML = '';
        document.getElementById('modal-anim').hidden = hideAnim;
        document.getElementById('modal-text').hidden = hideText;
        document.getElementById('modal-text').innerHTML = text;

        // control floating view mode
        if(triggerFloatingViewMode)
            $('#modal').modal();
        else
            $('#modal').modal('hide');
    }
}


// --------------------------------------------------------------------------------
// loading screen controller
// --------------------------------------------------------------------------------

$(document).ready(function() {
    // hide the loading screen
    $('.loader').fadeOut(1000);
});
