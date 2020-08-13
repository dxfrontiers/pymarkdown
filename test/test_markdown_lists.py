"""
https://github.github.com/gfm/#lists
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_list_items_281():
    """
    Test case 281:  (part 1) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
- bar
+ baz"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[ulist(3,1):+::2:]",
        "[para(3,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_281a():
    """
    Test case 281a:  variation on 281 with second item indented
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
  * bar
* baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_281b():
    """
    Test case 281b:  variation on 281 with second item indented and third with different list start
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
  * bar
+ baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[ulist(3,1):+::2:]",
        "[para(3,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_281c():
    """
    Test case 281c:  variation on 281b with third item indented, and a following list item for the parent
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
  * bar
  + baz
* boffo"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[ulist(3,3):+::4:  ]",
        "[para(3,5):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text:boffo:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar</li>
</ul>
<ul>
<li>baz</li>
</ul>
</li>
<li>boffo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_281d():
    """
    Test case 281d:  variation on 281
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
  * bar
    * boffo
  + baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[ulist(3,5):*::6:    ]",
        "[para(3,7):]",
        "[text:boffo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[ulist(4,3):+::4:  ]",
        "[para(4,5):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>boffo</li>
</ul>
</li>
</ul>
<ul>
<li>baz</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_281e():
    """
    Test case 281e:  variation on 281
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
  * bar
    * boffo
+ baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[ulist(3,5):*::6:    ]",
        "[para(3,7):]",
        "[text:boffo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
        "[ulist(4,1):+::2:]",
        "[para(4,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>boffo</li>
</ul>
</li>
</ul>
</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_282():
    """
    Test case 282:  (part 2) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. foo
2. bar
3) baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):3::2]",
        "[para(2,4):]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
        "[olist(3,1):):3:3:]",
        "[para(3,4):]",
        "[text:baz:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_283():
    """
    Test case 283:  In CommonMark, a list can interrupt a paragraph. That is, no blank line is needed to separate a paragraph from a following list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
- bar
- baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:Foo:]",
        "[end-para]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text:bar:]",
        "[end-para]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<p>Foo</p>
<ul>
<li>bar</li>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_284():
    """
    Test case 284:  In order to solve of unwanted lists in paragraphs with hard-wrapped numerals, we allow only lists starting with 1 to interrupt paragraphs. Thus,
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """The number of windows in my house is
14.  The number of doors is 6."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:The number of windows in my house is\n14.  The number of doors is 6.::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>The number of windows in my house is
14.  The number of doors is 6.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_285():
    """
    Test case 285:  We may still get an unintended result in cases like
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """The number of windows in my house is
1.  The number of doors is 6."""
    expected_tokens = [
        "[para(1,1):]",
        "[text:The number of windows in my house is:]",
        "[end-para]",
        "[olist(2,1):.:1:4:]",
        "[para(2,5):]",
        "[text:The number of doors is 6.:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<p>The number of windows in my house is</p>
<ol>
<li>The number of doors is 6.</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_286():
    """
    Test case 286:  (part 1) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo

- bar


- baz"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>bar</p>
</li>
<li>
<p>baz</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_287():
    """
    Test case 287:  (part 2) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
  - bar
    - baz


      bim"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[ulist(3,5):-::6:    :      ]",
        "[para(3,7):]",
        "[text:baz:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
        "[para(6,7):]",
        "[text:bim:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>
<p>baz</p>
<p>bim</p>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_288():
    """
    Test case 288:  (part 1) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
- bar

<!-- -->

- baz
- bim"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[end-ulist]",
        "[html-block(4,1)]",
        "[text:<!-- -->:]",
        "[end-html-block]",
        "[BLANK(5,1):]",
        "[ulist(6,1):-::2:]",
        "[para(6,3):]",
        "[text:baz:]",
        "[end-para]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text:bim:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
</ul>
<!-- -->
<ul>
<li>baz</li>
<li>bim</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_289():
    """
    Test case 289:  (part 2) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-   foo

    notcode

-   foo

<!-- -->

    code"""
    expected_tokens = [
        "[ulist(1,1):-::4::    ]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,5):]",
        "[text:notcode:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[li(5,1):4::]",
        "[para(5,5):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(6,1):]",
        "[end-ulist]",
        "[html-block(7,1)]",
        "[text:<!-- -->:]",
        "[end-html-block]",
        "[BLANK(8,1):]",
        "[icode-block(9,5):    :]",
        "[text:code:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<p>notcode</p>
</li>
<li>
<p>foo</p>
</li>
</ul>
<!-- -->
<pre><code>code
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_290():
    """
    Test case 290:  (part 1) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
 - b
  - c
   - d
  - e
 - f
- g"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text:b:]",
        "[end-para]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text:c:]",
        "[end-para]",
        "[li(4,4):5:   :]",
        "[para(4,6):]",
        "[text:d:]",
        "[end-para]",
        "[li(5,3):4:  :]",
        "[para(5,5):]",
        "[text:e:]",
        "[end-para]",
        "[li(6,2):3: :]",
        "[para(6,4):]",
        "[text:f:]",
        "[end-para]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text:g:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
<li>e</li>
<li>f</li>
<li>g</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_291():
    """
    Test case 291:  (part 2) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a

  2. b

   3. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[li(3,3):5:  :2]",
        "[para(3,6):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[li(5,4):6:   :3]",
        "[para(5,7):]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
<li>
<p>c</p>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_292():
    """
    Test case 292:  Note, however, that list items may not be indented more than three spaces. Here - e is treated as a paragraph continuation line, because it is indented more than three spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
 - b
  - c
   - d
    - e"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text:b:]",
        "[end-para]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text:c:]",
        "[end-para]",
        "[li(4,4):5:   :]",
        "[para(4,6):\n\x04]",
        "[text:d\n- e::\n]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d
- e</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown, show_debug=False)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_292a():
    """
    Test case 292a:  Variation on 292
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
 - b
  - c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text:b:]",
        "[end-para]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text:c:]",
        "[end-para]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_292b():
    """
    Test case 292b:  Variation on 292
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
 - b
  - c
   - d
- e"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text:b:]",
        "[end-para]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text:c:]",
        "[end-para]",
        "[li(4,4):5:   :]",
        "[para(4,6):]",
        "[text:d:]",
        "[end-para]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text:e:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
<li>e</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293():
    """
    Test case 293:  And here, 3. c is treated as in indented code block, because it is indented four spaces and preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a

  2. b

    3. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[li(3,3):5:  :2]",
        "[para(3,6):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[end-olist]",
        "[icode-block(5,5):    :]",
        "[text:3. c:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<ol>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
</ol>
<pre><code>3. c
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293a():
    """
    Test case 293a:  variation on 293
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a
  1. b
    1. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,3):5:  :1]",
        "[para(2,6):\n ]",
        "[text:b\n1. c::\n]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>a</li>
<li>b
1. c</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293b():
    """
    Test case 293b:  variation on 293
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a
   1. b
1. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text:b:]",
        "[end-para]",
        "[end-olist]",
        "[li(3,1):3::1]",
        "[para(3,4):]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b</li>
</ol>
</li>
<li>c</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293c():
    """
    Test case 293c:  variation on 293
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a
   1. b
1) c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text:b:]",
        "[end-para]",
        "[end-olist]",
        "[end-olist]",
        "[olist(3,1):):1:3:]",
        "[para(3,4):]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b</li>
</ol>
</li>
</ol>
<ol>
<li>c</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293d():
    """
    Test case 293d:  variation on 293
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a
   1. b
   1) c
1. d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text:b:]",
        "[end-para]",
        "[end-olist]",
        "[olist(3,4):):1:6:   ]",
        "[para(3,7):]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
        "[li(4,1):3::1]",
        "[para(4,4):]",
        "[text:d:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b</li>
</ol>
<ol>
<li>c</li>
</ol>
</li>
<li>d</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293e():
    """
    Test case 293e:  variation on 293
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a
   1. b
      1. c
   1) d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text:b:]",
        "[end-para]",
        "[olist(3,7):.:1:9:      ]",
        "[para(3,10):]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
        "[end-olist]",
        "[olist(4,4):):1:6:   ]",
        "[para(4,7):]",
        "[text:d:]",
        "[end-para]",
        "[end-olist]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b
<ol>
<li>c</li>
</ol>
</li>
</ol>
<ol>
<li>d</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_293f():
    """
    Test case 293f:  variation on 293
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. a
   1. b
      1. c
1) d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:a:]",
        "[end-para]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text:b:]",
        "[end-para]",
        "[olist(3,7):.:1:9:      ]",
        "[para(3,10):]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
        "[end-olist]",
        "[end-olist]",
        "[olist(4,1):):1:3:]",
        "[para(4,4):]",
        "[text:d:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b
<ol>
<li>c</li>
</ol>
</li>
</ol>
</li>
</ol>
<ol>
<li>d</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_294():
    """
    Test case 294:  This is a loose list, because there is a blank line between two of the list items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
- b

- c"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
<li>
<p>c</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_295():
    """
    Test case 295:  So is this, with a empty second item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* a
*

* c"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[BLANK(2,2):]",
        "[BLANK(3,1):]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li></li>
<li>
<p>c</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_296():
    """
    Test case 296:  (part 1) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
- b

  c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,3):]",
        "[text:c:]",
        "[end-para]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<p>c</p>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_297():
    """
    Test case 297:  (part 2) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
- b

  [ref]: /url
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,3):True::ref:: :/url:::::]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_298():
    """
    Test case 298:  This is a tight list, because the blank lines are in a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
- ```
  b


  ```
- c"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[fcode-block(2,3):`:3::::::]",
        "[text:b\n\x03\n\x03:]",
        "[end-fcode-block::3]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>
<pre><code>b


</code></pre>
</li>
<li>c</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_299():
    """
    Test case 299:  This is a tight list, because the blank line is between two paragraphs of a sublist. So the sublist is loose while the outer list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
  - b

    c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,5):]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>
<p>b</p>
<p>c</p>
</li>
</ul>
</li>
<li>d</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_300():
    """
    Test case 300:  This is a tight list, because the blank line is inside the block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* a
  > b
  >
* c"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[block-quote(2,3):  :  > \n  >]",
        "[para(2,5):]",
        "[text:b:]",
        "[end-para]",
        "[BLANK(3,4):]",
        "[end-block-quote]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
</li>
<li>c</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_301():
    """
    Test case 301:  This list is tight, because the consecutive block elements are not separated by blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
  > b
  ```
  c
  ```
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text:b:]",
        "[end-para]",
        "[end-block-quote]",
        "[fcode-block(3,3):`:3::::::]",
        "[text:c:]",
        "[end-fcode-block::3]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
<pre><code>c
</code></pre>
</li>
<li>d</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_302():
    """
    Test case 302:  (part 1) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_303():
    """
    Test case 303:  (part 2) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
  - b"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text:b:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_304():
    """
    Test case 304:  This list is loose, because of the blank line between the two block elements in the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. ```
   foo
   ```

   bar"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[fcode-block(1,4):`:3::::::]",
        "[text:foo:]",
        "[end-fcode-block::3]",
        "[BLANK(4,1):]",
        "[para(5,4):]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>foo
</code></pre>
<p>bar</p>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_305():
    """
    Test case 305:  (part 1) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
  * bar

  baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[end-ulist]",
        "[para(4,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<ul>
<li>bar</li>
</ul>
<p>baz</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


def test_list_items_305a():
    """
    Test case 305a:  variation on 305
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
* foogle    
  * bar

  baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):2::]",
        "[para(2,3)::    ]",
        "[text:foogle:]",
        "[end-para]",
        "[ulist(3,3):*::4:  ]",
        "[para(3,5):]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[end-ulist]",
        "[para(5,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>foogle</p>
<ul>
<li>bar</li>
</ul>
<p>baz</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


def test_list_items_305b():
    """
    Test case 305b:  variation on 305
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* foo
 * foogle    
   * bar

   baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,2):3: :]",
        "[para(2,4)::    ]",
        "[text:foogle:]",
        "[end-para]",
        "[ulist(3,4):*::5:   ]",
        "[para(3,6):]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[end-ulist]",
        "[para(5,4):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>foogle</p>
<ul>
<li>bar</li>
</ul>
<p>baz</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_items_306():
    """
    Test case 306:  (part 2) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a
  - b
  - c

- d
  - e
  - f"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:a:]",
        "[end-para]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text:b:]",
        "[end-para]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text:c:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[end-ulist]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text:d:]",
        "[end-para]",
        "[ulist(6,3):-::4:  ]",
        "[para(6,5):]",
        "[text:e:]",
        "[end-para]",
        "[li(7,3):4:  :]",
        "[para(7,5):]",
        "[text:f:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
<ul>
<li>b</li>
<li>c</li>
</ul>
</li>
<li>
<p>d</p>
<ul>
<li>e</li>
<li>f</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
