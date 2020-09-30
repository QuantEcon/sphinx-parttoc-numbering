# sphinx-parttoc-numbering

[![Github-CI][github-ci]][github-link]
[![Coverage Status][codecov-badge]][codecov-link]

**An extension for continuous numbering of toctree elements across multiple toctrees**.

This package contains a [Sphinx](http://www.sphinx-doc.org/en/master/) extension to continuously number sections across multiple toctrees present in the same document. Also quite useful in [jupyter-book](https://jupyterbook.org/) projects for continuous numbering of chapters across different parts.

## Get started

To get started with `sphinx-multitoc-numbering`, first install it through `pip`:

```
pip install sphinx-multitoc-numbering
```

then, add `sphinx_multitoc_numbering` to your sphinx `extensions` in the `conf.py`

```python
...
extensions = ["sphinx_multitoc_numbering"]
...
```

## Contributing

We welcome all contributions! See the [EBP Contributing Guide](https://executablebooks.org/en/latest/contributing.html) for general details.

[github-ci]: https://github.com/executablebooks/sphinx-multitoc-numbering/workflows/continuous-integration/badge.svg?branch=master
[github-link]: https://github.com/executablebooks/sphinx-multitoc-numbering
[codecov-badge]: https://codecov.io/gh/executablebooks/sphinx-multitoc-numbering/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/executablebooks/sphinx-multitoc-numbering
