from core import TextCompare, SimpleHtmlTag


def generate_compare_result():
    # you can change the default html color
    # SimpleHtmlTag.Color.ChangedColor = ("background color", "front color")
    # SimpleHtmlTag.Color.AddedColor = ("background color", "front color")
    # SimpleHtmlTag.Color.DeletedColor = ("background color", "front color")
    result = TextCompare.compare("test_data/old.txt", "test_data/new.txt")
    with open("test_data/compare_result_template.html", "r", encoding="utf-8") as template:
        result = template.read().replace(
            "{left}", result.left_html).replace(
            "{right}", result.right_html).replace(
            "{compare_diff_ids}", str(list(range(result.diff_count))))
        return result
