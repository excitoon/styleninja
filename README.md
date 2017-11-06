### Introduction

C++ code style checker for styles I use. Compatible with C++11 raw literals.

### Command-line options

```
styleninja [--squeeze] [paths]
```

Specify `paths` to scan specific files and directories instead of current directory.
Specify `--squeeze` to remove extra whitespaces and comments instead of checking (warning, that will rewrite files in-place).

### Configuration

Configuration file lies in `~/.styleninjarc`.

#### `extensions`

List of file extensions which are to be processed.

Example:
```
[ "*.c", "*.cpp", "*.cxx", "*.h", "*.hpp" ]
```

#### `namespace_indent`

Indent of namespace block.

#### `big_indent`

Double indent (occurs approximately on first multiline block in round brackets).

### See also

* https://github.com/google/styleguide/tree/gh-pages/cpplint
* https://clang.llvm.org/docs/ClangFormat.html
* http://kitware.github.io/KWStyle/
* https://bitbucket.org/verateam/vera/overview
* http://astyle.sourceforge.net/
* https://code.google.com/archive/p/nsiqcppstyle/
