#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_lint.py — lint_usertesting.py 的最小回归测试。

为什么需要：2026-09-09 一次批量替换事故把 120 处题号写成了 \\x01，
而当时的 lint 只查汉字/中文标点，纯英文行里的控制字符完全检不出；
同一轮里有人版（环节结构）也没进任何检查。改脚本时若不验证，
很可能"改好了 A、弄坏了 B"却毫无察觉。

用法:
    python test_lint.py

设计原则:
    - 每个用例只针对一个检查项，用最小输入，失败时能一眼看出是哪个检查失灵
    - 正例（应通过）和反例（应报错）成对出现，防止检查写得过严误报
    - 不依赖项目里的具体文档，用例自带输入，可在任何目录跑
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_lint():
    spec = importlib.util.spec_from_file_location(
        "lint_usertesting", HERE / "lint_usertesting.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LINT = load_lint()

# ---------- 测试框架（够用就好，不引第三方依赖） ----------

PASSED = []
FAILED = []


def check(name, condition, detail=""):
    if condition:
        PASSED.append(name)
        print(f"  ✓ {name}")
    else:
        FAILED.append((name, detail))
        print(f"  ✗ {name}  {detail}")


def has_error(findings, keyword=None):
    """findings 里是否有 ERROR；给了 keyword 则要求消息里含该词。"""
    errs = [f for f in findings if f.level == "ERROR"]
    if keyword is None:
        return bool(errs)
    return any(keyword in f.message for f in errs)


# ---------- 用例 ----------

def test_invisible_chars():
    """隐形字符必须被检出——这是 2026-09-09 事故的直接防线。"""
    print("\n[隐形字符]")
    cases = {
        "U+0001 控制字符": "#### Q5 hello \x01 world",
        "U+200B 零宽空格": "#### Q5 hello \u200b world",
        "U+200D 零宽连接符": "#### Q5 hello \u200d world",
        "U+FEFF BOM": "#### Q5 hello \ufeff world",
        "U+FFFD 替换字符": "#### Q5 hello \ufffd world",
        "U+00A0 不换行空格": "#### Q5 hello \u00a0 world",
    }
    for label, line in cases.items():
        r = LINT.check_cjk([line])
        check(f"检出 {label}", has_error(r, "隐形字符"), f"实际 findings={len(r)}")

    # 反例：正常的全角空格是题目标题的字段分隔符，不该报警
    r = LINT.check_cjk(["#### Q5\u3000Stem here"])
    check("全角空格不误报", not has_error(r), f"实际 findings={len(r)}")


def test_cross_references():
    """交叉引用指向不存在的题，必须被检出。"""
    print("\n[交叉引用]")
    text_ok = (
        "#### Q1　first\n\n> see Q2 for details\n\n"
        "#### Q2　second\n\nbody\n"
    )
    check("合法引用不报错", not has_error(LINT.check_cross_references(text_ok, "T")))

    text_bad = (
        "#### Q1　first\n\n> see Q9 for details\n\n"
        "#### Q2　second\n\nbody\n"
    )
    check(
        "悬空引用 Q9 被检出",
        has_error(LINT.check_cross_references(text_bad, "T"), "不存在的题号"),
    )

    # 中文侧：题号顺移后引用没跟着改，是真实踩过的坑
    text_cn_bad = (
        "#### 问题 1　第一题\n\n> 见问题 9\n\n"
        "#### 问题 2　第二题\n\n正文\n"
    )
    check(
        "中文悬空引用被检出",
        has_error(LINT.check_cross_references(text_cn_bad, "T"), "不存在的题号"),
    )

    # RQ1 / RQ2 不是题号引用，不能误报
    text_rq = "#### Q1　first\n\n> RQ1 and RQ4 are research questions\n"
    check("RQ1 不误报", not has_error(LINT.check_cross_references(text_rq, "T")))

    # 无人版的 Q1 是 Task A 的导航单元，只写在标题里，占号但不是问答题：
    # 正文里引用 Q1 是合法的，不能报成悬空引用（2026-09-11 实测踩到）
    text_nav = (
        "### Task A · Navigation (Download & Open the Game)　`Q1`\n\n"
        "> Q1 is the navigation unit, not a question.\n\n"
        "#### Q2　second\n\nbody\n"
    )
    check("标题里的 Q1 占号单元不误报",
          not has_error(LINT.check_cross_references(text_nav, "T")))

    # 题号区间是概述，端点不能算悬空引用
    text_range = (
        "#### Q2　first\n\n> All 34 questions: Q1-Q34.\n\n"
        "#### Q34　last\n\nbody\n"
    )
    check("题号区间端点不误报",
          not has_error(LINT.check_cross_references(text_range, "T")))

    # 区间之外的悬空引用仍然要报出来（防止放宽过头）
    text_out_of_range = (
        "> All 34 questions: Q1-Q34.\n\n"
        "#### Q2　first\n\n> see Q35 for details\n\n"
        "#### Q34　last\n\nbody\n"
    )
    check("区间之外仍被检出",
          has_error(LINT.check_cross_references(text_out_of_range, "T"), "不存在的题号"))


def test_segment_sequence():
    """有人版的环节编号连续性。"""
    print("\n[环节编号]")
    ok = "### 环节 1 · a\n\n### 环节 2 · b\n"
    check("连续环节不报错", not has_error(LINT.check_segment_sequence(ok, "T")))

    missing = "### 环节 1 · a\n\n### 环节 3 · c\n"
    check(
        "跳号被检出",
        has_error(LINT.check_segment_sequence(missing, "T"), "不连续"),
    )

    dup = "### 环节 1 · a\n\n### 环节 1 · a again\n"
    check(
        "重复被检出",
        has_error(LINT.check_segment_sequence(dup, "T"), "重复"),
    )

    # 无人版没有"环节"，不能误报
    none_doc = "### Task B · Page 1: x\n\n#### Q1　y\n"
    check("无环节结构不报错", not has_error(LINT.check_segment_sequence(none_doc, "T")))

    # 英文版有人大纲用 `### Segment N`，同样要查连续性
    en_ok = "### Segment 1 · a\n\n### Segment 2 · b\n"
    check("英文 Segment 连续不报错", not has_error(LINT.check_segment_sequence(en_ok, "T")))

    en_gap = "### Segment 1 · a\n\n### Segment 3 · c\n"
    check(
        "英文 Segment 跳号被检出",
        has_error(LINT.check_segment_sequence(en_gap, "T"), "不连续"),
    )


def test_question_sequence():
    """题号连续性与重复。"""
    print("\n[题号连续性]")
    ok = "#### Q1　a\n\n#### Q2　b\n"
    check("连续题号不报错", not has_error(LINT.check_question_sequence(ok, "T")))

    gap = "#### Q1　a\n\n#### Q3　c\n"
    check("跳号被检出", has_error(LINT.check_question_sequence(gap, "T"), "不连续"))

    dup = "#### Q1　a\n\n#### Q1　a\n"
    check("重复被检出", has_error(LINT.check_question_sequence(dup, "T"), "重复"))


def test_parse_questions_scope():
    """选项计数不能吃到附录——最后一题曾把附录的列表算成选项。"""
    print("\n[选项解析范围]")
    text = (
        "#### Q1　stem\n\n- a\n- b\n- c\n\n"
        "## Appendix\n\n- x\n- y\n- z\n- w\n"
    )
    q = LINT.parse_questions(text)
    check("选项数不含附录列表", q.get(1, {}).get("options") == 3,
          f"实际={q.get(1, {}).get('options')}")


def test_scale_labels():
    """量表题必须有 Scale Labels；NPS 若写标签须从 0 起算。"""
    print("\n[Scale Labels]")
    ok = (
        "#### Q1　`[Rating scale · 1-10 · required]`　x\n\n"
        "**Scale Labels**: **1 = low** | **10 = high**\n"
    )
    check("量表题有标签不报错", not has_error(LINT.check_scale_labels(ok)))

    missing = "#### Q1　`[Rating scale · 1-10 · required]`　x\n\nstem only\n"
    check(
        "量表题缺标签被检出",
        has_error(LINT.check_scale_labels(missing), "缺少 Scale Labels"),
    )

    nps_zero = (
        "#### Q1　`[NPS · 0-10 · required]`　x\n\n"
        "**Scale Labels**: **0 = low** | **10 = high**\n"
    )
    check("NPS 标签从 0 起算不报警",
          not any(f.level == "WARN" for f in LINT.check_scale_labels(nps_zero)))

    nps_one = (
        "#### Q1　`[NPS · 0-10 · required]`　x\n\n"
        "**Scale Labels**: **1 = low** | **10 = high**\n"
    )
    check("NPS 标签从 1 起算被警告",
          any(f.level == "WARN" for f in LINT.check_scale_labels(nps_one)))


def test_forbidden_prompts():
    """平台禁止的自填提示，只在选项由平台渲染的题型里查。"""
    print("\n[禁止自填提示]")
    mc_bad = [
        "#### Q1　`[Multiple Choice · single · required]`　x",
        "**Stem**: pick one",
        "- Other (please specify)",
    ]
    check("多选里的 please specify 被检出",
          has_error(LINT.check_forbidden_prompts(mc_bad), "禁止的自填提示"))

    verbal_ok = [
        "#### Q1　`[Verbal response · required]`　x",
        "**Stem**: please tell us which game you mean",
    ]
    check("Verbal 题里的 please tell us 不报错",
          not has_error(LINT.check_forbidden_prompts(verbal_ok)))


def test_text_limits():
    """Instruction / Navigation 的 1000 字符上限。"""
    print("\n[字符上限]")
    short = ["### Task A · Instruction", "> short text"]
    check("短文本不报错", not has_error(LINT.check_text_limits(short)))

    long_block = ["### Task A · Instruction"] + ["> " + "x" * 200] * 6
    check("超 1000 字符被检出",
          has_error(LINT.check_text_limits(long_block), "上限"))


def main():
    print("=" * 56)
    print("lint_usertesting.py 回归测试")
    print("=" * 56)

    test_invisible_chars()
    test_cross_references()
    test_segment_sequence()
    test_question_sequence()
    test_parse_questions_scope()
    test_scale_labels()
    test_forbidden_prompts()
    test_text_limits()

    print("\n" + "=" * 56)
    total = len(PASSED) + len(FAILED)
    print(f"结果：{len(PASSED)} / {total} 通过")
    if FAILED:
        print("\n失败用例：")
        for name, detail in FAILED:
            print(f"  ✗ {name}  {detail}")
        return 1
    print("✓ 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
