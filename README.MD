# Easy Compare
> Easy to compare two text or text file by google's 'diff_match_patch' lib.
> By this, you can easily to make a Human readable result in html.

## Install
```commandline
pip install ez_compare
```

## Usage
```python
from ez_compare.core import TextCompare


result = TextCompare.compare("your_file_one.txt", "your_file_two.txt")

```

## Html Result Example
```python
from ez_compare.example import generate_compare_result


html_str = generate_compare_result("your_file_one.txt", "your_file_two.txt")
with open("example.html", "w", encoding="utf-8") as f:
    f.write(html_str)
    # then you can open 'example.html' file by you browser.
```
