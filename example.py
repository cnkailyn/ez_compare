from core import TextCompare


def generate_compare_result():
    result = TextCompare.compare("test_data/old.txt", "test_data/new.txt")
    with open("test_data/compare_result_template.html", "r", encoding="utf-8") as template:
        result = template.read().replace(
            "{left}", result.left_html).replace(
            "{right}", result.right_html).replace(
            "{compare_diff_ids}", str(list(range(result.diff_count))))
        return result
