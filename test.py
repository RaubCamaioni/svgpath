import svgtrace

xml = """<?xml version="1.0" encoding="iso-8859-1"?>
<svg>		
  <path d="M11.298,8.02c1.295-0.587,1.488-5.055,0.724-6.371c-0.998-1.718-5.742-1.373-7.24-0.145
    C4.61,2.114,4.628,3.221,4.636,4.101h4.702v0.412H4.637c0,0.006-2.093,0.013-2.093,0.013c-3.609,0-3.534,7.838,1.228,7.838
    c0,0,0.175-1.736,0.481-2.606C5.198,7.073,9.168,8.986,11.298,8.02z M6.375,3.465c-0.542,0-0.981-0.439-0.981-0.982
    c0-0.542,0.439-0.982,0.981-0.982c0.543,0,0.982,0.44,0.982,0.982C7.358,3.025,6.918,3.465,6.375,3.465z"/>
  <path d="M13.12,4.691c0,0-0.125,1.737-0.431,2.606c-0.945,2.684-4.914,0.772-7.045,1.738
    C4.35,9.622,4.155,14.09,4.92,15.406c0.997,1.719,5.741,1.374,7.24,0.145c0.172-0.609,0.154-1.716,0.146-2.596H7.603v-0.412h4.701
    c0-0.006,2.317-0.013,2.317-0.013C17.947,12.53,18.245,4.691,13.12,4.691z M10.398,13.42c0.542,0,0.982,0.439,0.982,0.982
    c0,0.542-0.44,0.981-0.982,0.981s-0.981-0.439-0.981-0.981C9.417,13.859,9.856,13.42,10.398,13.42z"/>
</svg>"""

tree = list(svgtrace.parse(xml))


from svgtrace import (
    tree_to_paths,
    path_absolute_tokens,
)

# expand generator of generators (only needed to compair generator outputs)
paths = [[token for token in path] for path in tree_to_paths(tree)]
apaths = [[token for token in path] for path in path_absolute_tokens(paths)]

for i, (path, apath) in enumerate(zip(paths, apaths)):
    print(f"Path: {i}")
    for token, atoken in zip(path, apath):
        print(f"  {token} {atoken}")

from matplotlib import pyplot as plt
from svgtrace import (
    tree_to_paths,
    paths_to_points,
)

paths = list(tree_to_paths(tree))

_, ax = plt.subplots()
ax.invert_yaxis()
for path in paths_to_points(paths, resolution=100):
    for trace in path:
        ax.plot(trace[:, 0], trace[:, 1])
plt.show()
