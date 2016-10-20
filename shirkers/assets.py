from django_assets import Bundle, register

css_files = [
    'static/jquery-ui.min.css',
    'static/pure/base-min.css',
    'static/pure/forms-min.css',
    'static/custom.css',
]

js_files = [
    'static/jquery.js',
    'static/jquery-ui.min.js',
]

js = Bundle(*js_files, filters='jsmin', output='static/scripts.js')
css = Bundle(*css_files, filters='cssmin', output='static/styles.css')

register('js_all', js)
register('styles_all', css)
