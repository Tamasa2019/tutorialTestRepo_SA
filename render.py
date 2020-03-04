import base64

def image(width, height, pixels):
    """
    Generate an HTML document containing a single grayscale image.

    Parameters
    ----------
    width : int
        the image width in pixels
    height : int
        the image height in pixels
    pixels : list of int
        the grayscale values of the pixels, in row-major ordering
        the pixel with coordinates (x, y) has the index (x + y * width)
        each value must be in the range [0, 255]
        there must be exactly (width * height) elements in the list

    Returns
    -------
    string
        the generated HTML content
    """
    assert isinstance(width, int)
    assert isinstance(height, int)
    assert width > 0
    assert height > 0
    assert isinstance(pixels, list)
    assert len(pixels) == width * height
    encoded_pixels = base64.b64encode(bytes(pixels)).decode()
    return f'''
    <html>
        <head>
            <meta charset="UTF-8">
            <style>
                html, body {{
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    overflow: hidden;
                }}
                canvas {{
                    position: absolute;
                    display: inline-block;
                    image-rendering: optimizeSpeed;
                    image-rendering: -moz-crisp-edges;
                    image-rendering: -webkit-optimize-contrast;
                    image-rendering: -o-crisp-edges;
                    image-rendering: pixelated;
                    -ms-interpolation-mode: nearest-neighbor;
                }}
            </style>
        </head>
        <body>
            <canvas id="canvas" width="{width}" height="{height}"></canvas>
            <script>
                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                var pixels = atob('{encoded_pixels}');
                var image = context.createImageData(canvas.width, canvas.height);
                for (var y = 0; y < canvas.height; ++y) {{
                    for (var x = 0; x < canvas.width; ++x) {{
                        var index = x + y * canvas.width;
                        image.data[index * 4] = pixels.charCodeAt(index);
                        image.data[index * 4 + 1] = pixels.charCodeAt(index);
                        image.data[index * 4 + 2] = pixels.charCodeAt(index);
                        image.data[index * 4 + 3] = 255;
                    }}
                }}
                context.putImageData(image, 0, 0);
                function px(value) {{
                    return value.toString() + 'px';
                }}
                function setSize() {{
                    if (canvas.width * window.innerHeight > canvas.height * window.innerWidth) {{
                        var visual_height = window.innerWidth / canvas.width * canvas.height;
                        canvas.style.width = px(window.innerWidth);
                        canvas.style.height = px(visual_height);
                        canvas.style.left = px(0);
                        canvas.style.top = px((window.innerHeight - visual_height) / 2);
                    }} else {{
                        var visual_width = window.innerHeight / canvas.height * canvas.width;
                        canvas.style.height = px(window.innerHeight);
                        canvas.style.width = px(visual_width);
                        canvas.style.top = px(0);
                        canvas.style.left = px((window.innerWidth - visual_width) / 2);
                    }}
                }}
                setSize();
                window.addEventListener('resize', setSize);
            </script>
        </body>
    </html>
    '''
