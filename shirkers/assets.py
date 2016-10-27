from django_assets import Bundle, register

css_files = [
    'static/jquery-ui.min.css',
    'static/pure/base-min.css',
    'static/pure/forms-min.css',
    'static/custom.css',
    'static/fragment.css',
]

embed_css_files = [
    'static/jquery-ui.min.css',
    'static/fragment.css',
]

js_files = [
    'static/jquery.js',
    'static/jquery-ui.min.js',
]

embed_js_files = [
    'static/jquery.js',
    'static/jquery-ui.min.js',
    'static/loader.js',
]

js = Bundle(*js_files, filters='jsmin', output='static/scripts.js')
css = Bundle(*css_files, filters='cssmin', output='static/styles.css')

embed_js = Bundle(*embed_js_files, filters='jsmin', output='static/embed.js')
embed_css = Bundle(*embed_css_files, filters='cssmin',
                   output='static/embed.css')

register('js_all', js)
register('styles_all', css)
register('embed_js', embed_js)
register('embed_styles', embed_css)
