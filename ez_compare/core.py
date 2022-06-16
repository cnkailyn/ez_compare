from typing import List
import diff_match_patch as dmp_module
import os


class SimpleHtmlTag(object):
    class Color(object):
        ChangedColor = ("#f0f9fe", "#009df6")
        DeletedColor = ("#fff5f8", "#f1416c")
        AddedColor = ("#e8fff3", "#50cd89")

    class Tag(object):
        def __init__(self, tag_name: str, text: str, style=None, id_=None):
            self.id = id_
            self.tag = tag_name
            self.text = text
            self.style = style

        def get_html(self) -> str:
            _style = f' style="{self.style}"' if self.style else ''
            _id = f" id='{self.id}'" if self.id is not None else ''
            html = f'<{self.tag}{_id}{_style}>{self.text}</{self.tag}>'
            return html

    @classmethod
    def is_same_tag(cls, tag1: Tag, tag2: Tag):
        return tag1.tag == tag2.tag and tag1.style == tag2.style and tag1.id == tag2.id

    @classmethod
    def gen_changed_tag(cls, s: str, id_=None) -> Tag:
        """
        blue
        """
        color = cls.Color.ChangedColor
        return SimpleHtmlTag.Tag("span", s, f"background-color: {color[0]}; color: {color[1]}", id_)

    @classmethod
    def gen_deleted_tag(cls, s: str, id_=None) -> Tag:
        """
        red
        """
        color = cls.Color.DeletedColor
        return SimpleHtmlTag.Tag("del", s, f"background-color: {color[0]}; color: {color[1]}", id_)

    @classmethod
    def gen_new_added_tag(cls, s: str, id_=None) -> Tag:
        """
        green
        """
        color = cls.Color.AddedColor
        return SimpleHtmlTag.Tag("span", s, f"background-color: {color[0]}; color: {color[1]}", id_)

    @staticmethod
    def gen_normal_tag(s: str) -> Tag:
        return SimpleHtmlTag.Tag("span", s)

    @staticmethod
    def merge_same_tag(tags: List[Tag]) -> List[Tag]:
        """
        merge the same and continued tags to one to reduce text length
        """
        new_tag_list = []
        if len(tags) <= 1:
            return tags
        new_tag_list.append(tags[0])
        for tag in tags[1:]:
            # move first '\n' to previous line element, usually there will not multi '\n'
            if tag.text.startswith("\n"):
                tag.text = tag.text[1:]
                new_tag_list[-1].text += "\n"
            if SimpleHtmlTag.is_same_tag(tag, new_tag_list[-1]):
                new_tag_list[-1].text += tag.text
            else:
                new_tag_list.append(tag)
        return new_tag_list

    @staticmethod
    def move_out_break_line(tags: List[Tag]) -> List[Tag]:
        """
        move out the start and end break line out the diff tag
        """
        new_tag_list = []
        for tag in tags:
            l_strip = tag.text.lstrip("\n")
            l_len_count = len(tag.text) - len(l_strip)
            r_strip = tag.text.rstrip("\n")
            r_len_count = len(tag.text) - len(r_strip)
            if l_len_count != 0:
                new_tag_list.append(SimpleHtmlTag.gen_normal_tag("\n"*l_len_count))
            tag.text = tag.text.strip("\n")
            new_tag_list.append(tag)
            if r_len_count != 0:
                new_tag_list.append(SimpleHtmlTag.gen_normal_tag("\n"*r_len_count))

        return new_tag_list


class CompareResult(object):
    left_tags: List[SimpleHtmlTag.Tag]
    right_tags: List[SimpleHtmlTag.Tag]
    left_html: str
    right_html: str
    diff_count: str


class TextCompare(object):
    @staticmethod
    def compare(content_left: str, content_right: str) -> CompareResult:
        """
        compare two text.
        the result will keep two text have both lines to looks more intuitively
        """
        if os.path.isfile(content_left):
            with open(content_left, "r", encoding="utf-8") as f:
                content_left = f.read()
        if os.path.isfile(content_right):
            with open(content_right, "r", encoding="utf-8") as f:
                content_right = f.read()

        dmp = dmp_module.diff_match_patch()

        diff = dmp.diff_main(content_left, content_right)
        dmp.diff_cleanupSemantic(diff)
        diff = list(diff)
        result_left: List[SimpleHtmlTag.Tag] = []
        result_right: List[SimpleHtmlTag.Tag] = []
        changed_count = 0
        # recognize the change status
        i = 0
        while i < len(diff):
            item = diff[i]
            if item[1] == "":
                i += 1
                continue
            if item[0] == 0:  # not changed
                result_left.append(SimpleHtmlTag.gen_normal_tag(item[1]))
                result_right.append(SimpleHtmlTag.gen_normal_tag(item[1]))
            elif item[0] == -1:  # deleted
                result_left.append(SimpleHtmlTag.gen_normal_tag(item[1]))
                if i + 1 < len(diff):
                    if diff[i + 1][0] == 1:  # changed
                        if diff[i + 1][1].strip() == "":  # special
                            i += 2
                            result_right.append(SimpleHtmlTag.gen_deleted_tag(item[1]))
                            continue

                        left_break_line_count = item[1].count("\n")
                        right_break_line_count = diff[i + 1][1].count("\n")
                        diff_count = right_break_line_count - left_break_line_count
                        # just when -+ is happened on same line, we think they are changed,
                        # otherwise, it's delete and add
                        if diff_count == 0:
                            result_left.append(SimpleHtmlTag.gen_normal_tag("\n" * left_break_line_count))
                            result_right.append(SimpleHtmlTag.gen_deleted_tag(diff[i][1]))
                            result_right.append(SimpleHtmlTag.gen_changed_tag(diff[i + 1][1], changed_count))
                            changed_count += 1
                            i += 2
                            continue

                result_right.append(SimpleHtmlTag.gen_deleted_tag(item[1], changed_count))
                changed_count += 1

            else:  # added
                break_line_count = item[1].count("\n")
                # last line not endswith '\n', and we need 2 black line, we should set 3 '\n'
                if result_left and not result_left[-1].text.endswith("\n") and i > 0 and diff[i - 1][0] != -1 and \
                        break_line_count != 0:
                    break_line_count += 1
                result_left.append(SimpleHtmlTag.gen_normal_tag("\n" * break_line_count))
                result_right.append(SimpleHtmlTag.gen_new_added_tag(item[1], changed_count))
                changed_count += 1
            i += 1

        # For the continuity same tag, need to be merged to reduce the html size
        result_left = SimpleHtmlTag.move_out_break_line(SimpleHtmlTag.merge_same_tag(result_left))
        result_right = SimpleHtmlTag.move_out_break_line(SimpleHtmlTag.merge_same_tag(result_right))

        result = CompareResult()
        result.left_tags = result_left
        result.right_tags = result_right
        result.left_html = "".join([i.get_html() for i in result_left]).replace("\n", "<br>")
        result.right_html = "".join([i.get_html() for i in result_right]).replace("\n", "<br>")
        result.diff_count = changed_count

        return result
