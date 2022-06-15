from ez_compare.core import TextCompare


def generate_compare_result():
    result = TextCompare.compare("old.txt", "new.txt")
    with open("compare_result_template.html", "r", encoding="utf-8") as template:
        result = template.read().replace(
            "{left}", result.left_html).replace(
            "{right}", result.right_html).replace(
            "{compare_diff_ids}", str(list(range(result.diff_count))))
        with open("result.html", "w", encoding="utf-8") as f:
            f.write(result)


if __name__ == "__main__":
    generate_compare_result()
