import pytest
from comment import Comment

def test_comment_initialization():

    comment_id = 1
    comment_text = "Este é um comentário de teste."
    score_value = 4.5

    comment = Comment(comment_id, comment_text, score_value)

    assert comment.id == comment_id
    assert comment.comment == comment_text
    assert comment.score == score_value

def test_comment_properties():

    comment_id = 2
    comment_text = "Outro comentário de teste."
    score_value = 3.0

    comment = Comment(comment_id, comment_text, score_value)

    assert comment.id == 2
    assert comment.comment == "Outro comentário de teste."
    assert comment.score == 3.0

def test_comment_to_dict():

    comment_id = 3
    comment_text = "Comentário para teste de dicionário."
    score_value = 4.0

    comment = Comment(comment_id, comment_text, score_value)

    expected_dict = {
        "id": comment_id,
        "comment": comment_text,
        "score": score_value
    }
    assert comment.to_dict() == expected_dict
