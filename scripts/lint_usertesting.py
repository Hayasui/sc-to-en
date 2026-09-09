#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_usertesting.py — 检查用研 md 英文版是否符合 UserTesting 平台限制与本地化规范。

用法:
    python lint_usertesting.py <英文版.md>
    python lint_usertesting.py <英文版.md> --sc <中文版.md>   # 额外做中英结构比对

检查项:
    [平台] Instruction/Navigation text 是否超 1000 字符
    [平台] 是否残留平台禁止的自填提示 (please specify / 请说明 ...)
    [平台] 量表题是否都有 Scale Labels; NPS 题不应有
    [本地化] 是否残留汉字 / 中文标点
    [本地化] 是否残留隐形字符（控制字符 / 零宽字符 / BOM / 替换字符 / 全角空格）
    [本地化] 章节序号是否还是中文 (一、二、)
    [结构] 题号是否连续 / 有无重复 (抓"误删标题行"类事故)
    [结构] 题号交叉引用是否指向存在的题（"见问题 9"）
    [结构] Task A Instruction/Navigation + Task B Page 是否齐全
    [结构] 有人版（环节 N）的环节是否连续
    [对齐] 中英题号数 / 每题选项数是否一致 (需 --sc)

退出码: 0 = 全部通过, 1 = 有问题
"""
import argparse
import re
import sys
from pathlib import Path

# ---------- 常量 ----------

CJK_RE = re.compile(r"[\u4e00-\u9fa5]")
CJK_PUNCT_RE = re.compile(r"[，。；：、（）《》！？「」『』]")
CN_SECTION_RE = re.compile(r"^##\s*[〇一二三四五六七八九十]+、")

# 隐形字符：肉眼看不见、但会污染文档或被平台吞掉。
# 覆盖：C0/C1 控制字符、零宽字符、BOM、替换字符。
# 2026-09-09 加：一次批量替换事故把 120 处题号写成了 \x01，
# 而当时 check_cjk 只查汉字/中文标点，纯英文行里的控制字符完全检不出。
# 注：全角空格 U+3000 不在此列——它是本文档题目标题的字段分隔符（`#### Q1　...`），
# 属于格式约定，报警会淹没真问题。
INVISIBLE_RE = re.compile(
    r"[\u0000-\u0008\u000b\u000c\u000e-\u001f"   # C0 控制字符（排除 \t \n \r）
    r"\u007f-\u009f"                              # DEL + C1 控制字符
    r"\u00a0"                                     # 不换行空格（从网页/邮件复制常带）
    r"\u200b-\u200f\u2028-\u202f\u2060-\u206f"   # 零宽字符 / 方向控制 / 不可见分隔
    r"\ufeff\ufffd"                               # BOM / 替换字符
    r"]"
)

# 平台禁止的自填提示（出现在选项/题干里）
FORBIDDEN_PROMPTS = [
    r"please\s+specify",
    r"please\s+name\s+it",
    r"please\s+tell\s+us\s+which",
    r"\(please\b",
    r"请说明",
    r"请填写",
    r"请写出",
    r"请注明",
]

CHAR_LIMIT = 1000

# 量表题标记
SCALE_TAG_RE = re.compile(r"`\[(Rating scale|Matrix)[^`]*\]`")
NPS_TAG_RE = re.compile(r"`\[NPS[^`]*\]`")
QUESTION_HEAD_RE = re.compile(r"^####\s+(?:Q|题|问题)\s*(\d+)", re.M)
SCALE_LABEL_RE = re.compile(r"\*\*(?:Scale Labels|量表标签)\*\*", re.I)


class Finding:
    def __init__(self, level, category, message):
        self.level = level      # "ERROR" | "WARN"
        self.category = category
        self.message = message

    def __str__(self):
        icon = "✗" if self.level == "ERROR" else "!"
        return f"  {icon} [{self.category}] {self.message}"


# ---------- 检查逻辑 ----------

def check_text_limits(lines):
    """检查 Instruction / Navigation 的文本块字符数。"""
    findings = []
    # 定位以 > 开头的连续引用块，按前面的小标题归类
    blocks = []
    current_title = None
    current_block = []
    for line in lines:
        if line.startswith("###") or line.startswith("####"):
            if current_block:
                blocks.append((current_title, current_block))
                current_block = []
            current_title = line.strip("# ").strip()
        elif line.startswith(">"):
            current_block.append(line.lstrip("> ").rstrip())
        else:
            if current_block:
                blocks.append((current_title, current_block))
                current_block = []
                current_title = None
    if current_block:
        blocks.append((current_title, current_block))

    for title, block in blocks:
        text = "\n".join(block)
        # 只检查 Instruction / Navigation 这两段
        if title and ("Instruction" in title or "Navigation" in title):
            n = len(text)
            if n > CHAR_LIMIT:
                findings.append(Finding(
                    "ERROR", "平台",
                    f"「{title}」文本 {n} 字符，超出 {CHAR_LIMIT} 上限"
                ))
    return findings


def check_forbidden_prompts(lines):
    """检查平台禁止的自填提示。

    只在「选项由平台渲染」的题型里查（Multiple Choice / Ranking），
    且覆盖其题干行与选项行。Verbal / Written response 题里出现
    "please tell us which..." 是合法的（玩家开口说/打字回答），不查。
    """
    findings = []
    current_type = None
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        # 遇到新题头，更新当前题型
        if stripped.startswith("####"):
            m = re.search(r"`\[([^`]*)\]`", line)
            current_type = m.group(1) if m else None
            continue
        if stripped.startswith(">"):
            continue  # 引用块（说明文字/内部备注）

        applies = current_type is not None and (
            "Multiple Choice" in current_type or "Ranking" in current_type
        )
        if not applies:
            continue

        is_option = stripped.startswith("- ")
        is_stem = stripped.startswith("**Stem**")
        if not (is_option or is_stem):
            continue

        for pat in FORBIDDEN_PROMPTS:
            if re.search(pat, line, re.I):
                findings.append(Finding(
                    "ERROR", "平台",
                    f"第 {i} 行出现平台禁止的自填提示 `{pat}`：{line.strip()[:70]}"
                ))
    return findings


def check_scale_labels(text):
    """检查每个量表题是否带 Scale Labels；NPS 题不应有。"""
    findings = []
    # 按题目切分
    parts = re.split(r"^(####\s+(?:Q|题|问题)\s*\d+.*)$", text, flags=re.M)
    # parts: [前言, 标题1, 正文1, 标题2, 正文2, ...]
    for idx in range(1, len(parts), 2):
        head = parts[idx]
        body = parts[idx + 1] if idx + 1 < len(parts) else ""
        qnum = re.search(r"(?:Q|问题|题)\s*(\d+)", head)
        label = f"题 {qnum.group(1)}" if qnum else head.strip()[:40]
        is_scale = SCALE_TAG_RE.search(head)
        is_nps = NPS_TAG_RE.search(head)
        has_label = SCALE_LABEL_RE.search(body)
        if is_scale and not has_label:
            findings.append(Finding(
                "ERROR", "量表",
                f"{label} 是量表题但缺少 Scale Labels"
            ))
        if is_nps and has_label:
            findings.append(Finding(
                "WARN", "量表",
                f"{label} 是 NPS 题，不应额外加 Scale Labels（NPS 自带量表）"
            ))
    return findings


def check_cjk(lines):
    """检查汉字 / 中文标点 / 中文章节序号 / 隐形字符。"""
    findings = []
    for i, line in enumerate(lines, 1):
        if CJK_RE.search(line):
            findings.append(Finding(
                "ERROR", "本地化",
                f"第 {i} 行残留汉字：{line.strip()[:70]}"
            ))
        if CJK_PUNCT_RE.search(line):
            findings.append(Finding(
                "ERROR", "本地化",
                f"第 {i} 行残留中文标点：{line.strip()[:70]}"
            ))
        if CN_SECTION_RE.search(line):
            findings.append(Finding(
                "ERROR", "本地化",
                f"第 {i} 行章节序号还是中文：{line.strip()[:70]}"
            ))
        inv = INVISIBLE_RE.findall(line)
        if inv:
            codes = ", ".join(sorted({f"U+{ord(c):04X}" for c in inv}))
            findings.append(Finding(
                "ERROR", "本地化",
                f"第 {i} 行含隐形字符（{codes}）：{line.strip()[:60]!r}"
            ))
    return findings


def parse_questions(text):
    """解析每题：(题号, 题型标记, 选项数, 量表端点集合)。

    选项计数兼容 `- ` 与 `1. ` 两种列表写法。
    量表端点从 `1 = xxx | 10 = yyy` 这类写法提取数值。
    """
    parts = re.split(r"^(####\s+(?:Q|题|问题)\s*\d+.*)$", text, flags=re.M)
    result = {}
    for idx in range(1, len(parts), 2):
        head = parts[idx]
        body = parts[idx + 1] if idx + 1 < len(parts) else ""
        # 正文只取到下一个二级/三级标题为止，避免最后一题吃到附录，
        # 把附录里的 `- ` 列表误算成选项。
        body = re.split(r"^#{2,3}\s+\S", body, flags=re.M)[0]
        qnum = re.search(r"(?:Q|问题|题)\s*(\d+)", head)
        if not qnum:
            continue
        num = int(qnum.group(1))
        tag = re.search(r"`\[([^`]*)\]`", head)
        # 选项数：优先数字列表，其次 `- ` 列表
        numbered = re.findall(r"^\s*\d+\.\s+\S", body, re.M)
        if numbered:
            options = len(numbered)
        else:
            options = len([
                l for l in body.splitlines()
                if l.strip().startswith("- ") and not l.strip().startswith("- [")
            ])
        # 量表端点：从 `N = 标签` 提取数值
        scales = re.findall(r"(\d+)\s*=\s*[^|｜\n]+", body)
        result[num] = {
            "type": tag.group(1) if tag else "",
            "options": options,
            "scales": set(int(s) for s in scales),
        }
    return result


def check_alignment(en_text, sc_text):
    """中英题号 / 选项数 / 量表端点对齐。"""
    findings = []
    en_q = parse_questions(en_text)
    sc_q = parse_questions(sc_text)
    only_en = sorted(set(en_q) - set(sc_q))
    only_sc = sorted(set(sc_q) - set(en_q))
    if only_en:
        findings.append(Finding("ERROR", "对齐", f"英文版有、中文版没有的题号：{only_en}"))
    if only_sc:
        findings.append(Finding("ERROR", "对齐", f"中文版有、英文版没有的题号：{only_sc}"))
    for num in sorted(set(en_q) & set(sc_q)):
        e, s = en_q[num], sc_q[num]
        if e["options"] != s["options"]:
            findings.append(Finding(
                "WARN", "对齐",
                f"题 {num} 选项数不一致：英文 {e['options']} / 中文 {s['options']}"
            ))
        # 量表端点数值比对（两端都写了才比）
        if e["scales"] and s["scales"] and e["scales"] != s["scales"]:
            findings.append(Finding(
                "WARN", "对齐",
                f"题 {num} 量表端点数值不一致：英文 {sorted(e['scales'])} / 中文 {sorted(s['scales'])}"
            ))
    return findings


def check_cross_references(text, label):
    """检查正文里的题号交叉引用是否指向真实存在的题。

    抓的是"题号顺移后，引用没跟着改"这类事故——
    比如把题 5-28 顺移成 6-29，正文里"见问题 9"却还指着原来的 8。

    只匹配明确的引用写法：中文 `问题 N`、英文 `Q N` / `QN`。
    排除 RQ（研究问题）、页码、金额等噪声。
    """
    findings = []
    defined = {int(m) for m in QUESTION_HEAD_RE.findall(text)}
    if not defined:
        return findings

    for i, line in enumerate(text.splitlines(), 1):
        # 题目标题行本身不算引用
        if QUESTION_HEAD_RE.match(line):
            continue
        # 中文引用：问题 N
        refs = [int(n) for n in re.findall(r"问题\s*(\d+)", line)]
        # 英文引用：Q N 或 QN，但不能是 RQ N
        for m in re.finditer(r"(?<![A-Za-z])(?:Q|q)\s*(\d+)", line):
            refs.append(int(m.group(1)))
        bad = sorted({n for n in refs if n not in defined})
        if bad:
            findings.append(Finding(
                "ERROR", "结构",
                f"{label} 第 {i} 行引用了不存在的题号 {bad}：{line.strip()[:70]}"
            ))
    return findings


def check_segment_sequence(text, label):
    """有人版（环节 N）的环节编号连续性。

    `check_task_structure` 只认无人版的 Task/Page 结构；
    有人版用 `### 环节 N`，需要单独查，否则它的结构错误无人兜底。
    """
    findings = []
    segs = [int(n) for n in re.findall(r"^###\s+环节\s*(\d+)", text, re.M)]
    if not segs:
        return findings
    uniq = sorted(set(segs))
    dupes = sorted({n for n in segs if segs.count(n) > 1})
    if dupes:
        findings.append(Finding("ERROR", "结构", f"{label} 环节编号重复：{dupes}"))
    missing = [n for n in range(uniq[0], uniq[-1] + 1) if n not in uniq]
    if missing:
        findings.append(Finding(
            "ERROR", "结构", f"{label} 环节编号不连续，缺失：{missing}"
        ))
    return findings


def check_question_sequence(text, label):
    """题号连续性 + 重复检查。

    抓的是"批量替换时误删了某一题的标题行"这类事故——
    题号会突然跳号（1,2,4,5），或同一题号出现两次。
    """
    findings = []
    nums = [int(m) for m in QUESTION_HEAD_RE.findall(text)]
    if not nums:
        return findings

    # 重复
    seen = {}
    for n in nums:
        seen[n] = seen.get(n, 0) + 1
    dupes = sorted(n for n, c in seen.items() if c > 1)
    if dupes:
        findings.append(Finding(
            "ERROR", "结构",
            f"{label} 题号重复：{dupes}（可能是批量替换误伤）"
        ))

    # 跳号
    uniq = sorted(seen)
    missing = [n for n in range(uniq[0], uniq[-1] + 1) if n not in seen]
    if missing:
        findings.append(Finding(
            "ERROR", "结构",
            f"{label} 题号不连续，缺失：{missing}（标题行可能被误删）"
        ))
    return findings


def check_task_structure(text, label):
    """Task / Question Page 结构完整性检查。

    只对**访谈大纲**类文档生效（含 Task A / Task B 结构）。
    甄别问卷这类没有 Task 结构的文档直接跳过，不误报。
    """
    findings = []
    # 先探测是否属于"访谈大纲"型文档
    has_task_a = bool(re.search(r"^###\s+Task A\s*·", text, re.M))
    has_task_b = bool(re.search(r"^###\s+Task B\s*·", text, re.M))
    if not (has_task_a or has_task_b):
        return findings  # 非访谈大纲，跳过

    has_instruction = bool(re.search(r"^###\s+Task A\s*·\s*Instruction", text, re.M))
    has_navigation = bool(re.search(r"^###\s+Task A\s*·\s*Navigation", text, re.M))
    pages = re.findall(r"^###\s+Task B\s*·\s*Page\s*(\d+)", text, re.M)

    if not has_instruction:
        findings.append(Finding("ERROR", "结构", f"{label} 缺少 Task A · Instruction 区块"))
    if not has_navigation:
        findings.append(Finding("ERROR", "结构", f"{label} 缺少 Task A · Navigation 区块"))
    if not pages:
        findings.append(Finding("WARN", "结构", f"{label} 未发现 Task B · Page N 区块"))
    else:
        nums = sorted(int(p) for p in pages)
        missing = [n for n in range(1, nums[-1] + 1) if n not in nums]
        if missing:
            findings.append(Finding(
                "ERROR", "结构",
                f"{label} Question Page 不连续，缺失：Page {missing}"
            ))
    return findings


# ---------- 主流程 ----------

def main():
    ap = argparse.ArgumentParser(description="检查用研 md 英文版是否符合 UserTesting 规范")
    ap.add_argument("en_file", help="英文版 md 文件")
    ap.add_argument("--sc", help="中文版 md 文件（可选，用于中英结构比对）", default=None)
    args = ap.parse_args()

    en_path = Path(args.en_file)
    if not en_path.exists():
        print(f"✗ 文件不存在：{en_path}")
        return 1
    en_text = en_path.read_text(encoding="utf-8")
    en_lines = en_text.splitlines()

    findings = []
    findings += check_cjk(en_lines)
    findings += check_forbidden_prompts(en_lines)
    findings += check_text_limits(en_lines)
    findings += check_scale_labels(en_text)
    findings += check_question_sequence(en_text, "英文版")
    findings += check_cross_references(en_text, "英文版")
    findings += check_segment_sequence(en_text, "英文版")
    findings += check_task_structure(en_text, "英文版")

    if args.sc:
        sc_path = Path(args.sc)
        if not sc_path.exists():
            print(f"✗ 中文版文件不存在：{sc_path}")
            return 1
        sc_text = sc_path.read_text(encoding="utf-8")
        findings += check_alignment(en_text, sc_text)
        findings += check_question_sequence(sc_text, "中文版")
        findings += check_cross_references(sc_text, "中文版")
        findings += check_segment_sequence(sc_text, "中文版")
        findings += check_task_structure(sc_text, "中文版")

    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]

    print(f"\n检查文件：{en_path.name}")
    if args.sc:
        print(f"对照文件：{Path(args.sc).name}")
    print(f"结果：{len(errors)} 个错误 / {len(warns)} 个警告\n")

    if not findings:
        print("✓ 全部通过\n")
        return 0

    for f in findings:
        print(f)

    print()
    if errors:
        print("请修复上述 ERROR 后再交付。\n")
        return 1
    print("没有错误，警告项请人工确认。\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
