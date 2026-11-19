import pytest
from load_scores import load_scores
from load_scores import load_scores
from helpers import 쓰기


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

def test_일부러_틀린_테스트():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 99


def test_빈_줄은_건너뛴다(tmp_path):
    with open("scores.csv", encoding="utf-8-sig") as f:
        내용 = f.read()

    파일 = tmp_path / "빈줄.csv"
    파일.write_text(
        "\n\n".join(내용.splitlines()) + "\n\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(str(파일))
    assert (len(kept), len(skipped)) == (5, 0)


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    with open("scores.csv", encoding="utf-8-sig") as f:
        헤더 = f.readline()

    파일 = tmp_path / "이름쉼표.csv"
    파일.write_text(
        헤더.rstrip("\r\n") + '\n"김, 하나",88\n',
        encoding="utf-8"
    )

    kept, skipped = load_scores(str(파일))
    assert kept == [("김, 하나", 88)]

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

def test_경계_0점():
    쓰기("임시.csv", 0)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept), len(skipped)) == (1, 0)

def test_경계_100점():
    쓰기("임시.csv", 100)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept), len(skipped)) == (1, 0)

def test_경계_101점():
    쓰기("임시.csv", 101)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept), len(skipped)) == (0, 1)

def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(점수, 유효한가):
    쓰기(f"임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가