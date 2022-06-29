# Easy Compare
> A text compare lib based google's 'diff_match_patch' lib.
> By this, you can easily to make a Human readable result in html. 
> And you can click 'next diff' button easily to see the next difference.

## Compare Result Example
![example img](https://user-images.githubusercontent.com/34443073/173779126-b0c86330-e239-4842-8553-5a1ad1eb61a4.png)


## Install
```commandline
pip install ez-compare
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
