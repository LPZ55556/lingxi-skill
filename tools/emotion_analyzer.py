#!/usr/bin/env python3
"""情感分析器

从聊天记录中提取目标人物的情感表达模式，
构建情感映射表用于 Emotion Profile。

Usage:
    python3 emotion_analyzer.py --file <path> --target <name> --output <output_path>
"""

import argparse
import json
import re
import os
import sys
from collections import defaultdict


# 情绪关键词库
EMOTION_KEYWORDS = {
    'happy': ['哈哈', '嘻嘻', '嘿嘿', '开心', '高兴', '太好了', '爽', '棒', '赞', 'nice', '😂', '🤣', '😄', '😁', '😆'],
    'sad': ['唉', '哎', '难过', '伤心', '哭了', '呜呜', '心塞', '难受', '丧', '😢', '😭', '😞', '😔'],
    'angry': ['气死', '靠', '烦', '受不了', '凭什么', '太过分', '滚', '讨厌', '😤', '😡', '🤬', '💢'],
    'anxious': ['怎么办', '担心', '怕', '万一', '会不会', '焦虑', '慌', '紧张', '😰', '😨', '😥'],
    'caring': ['注意身体', '早点睡', '别太累', '吃了吗', '到家了吗', '小心', '记得', '别忘了'],
    'teasing': ['哈哈', '笑死', '绝了', '牛', '666', 'nb', '可以的', '行啊'],
    'intimate': ['想你', '喜欢', '爱你', '宝贝', '亲爱的', '❤️', '💕', '😘', '🥰', '😍'],
    'neutral': ['嗯', '哦', '好的', '知道了', '行', '可以', '随便', '无所谓'],
}

# 回应模式关键词
RESPONSE_PATTERNS = {
    'comfort': ['别难过', '没事的', '会好的', '别担心', '有我在', '慢慢来'],
    'advice': ['你应该', '我觉得', '建议', '不如', '试试', '要不'],
    'distraction': ['对了', '换个话题', '不说这个', '你知道吗', '说个好笑的'],
    'empathy': ['我懂', '理解', '确实', '换我也会', '正常', '谁都会'],
    'silent': [],  # 通过消息间隔检测
}


def detect_emotion(text: str) -> dict:
    """检测单条消息的情绪"""
    scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text)
        if count > 0:
            scores[emotion] = count
    return scores


def analyze_emotional_patterns(messages: list, target_name: str) -> dict:
    """分析目标人物的情感表达模式"""
    target_msgs = [m for m in messages if target_name in m.get('sender', '')]

    # 情绪分布统计
    emotion_counts = defaultdict(int)
    emotion_examples = defaultdict(list)

    for msg in target_msgs:
        content = msg.get('content', '')
        if not content:
            continue
        emotions = detect_emotion(content)
        for emotion, score in emotions.items():
            emotion_counts[emotion] += score
            if len(emotion_examples[emotion]) < 3:
                emotion_examples[emotion].append(content[:100])

    # 消息长度模式
    lengths = [len(m.get('content', '')) for m in target_msgs if m.get('content')]
    avg_length = sum(lengths) / len(lengths) if lengths else 0

    # 高频语气词
    all_text = ' '.join([m.get('content', '') for m in target_msgs if m.get('content')])
    particles = re.findall(r'[哈嗯哦噢嘿唉呜啊呀吧嘛呢吗么]+', all_text)
    particle_freq = defaultdict(int)
    for p in particles:
        particle_freq[p] += 1
    top_particles = sorted(particle_freq.items(), key=lambda x: -x[1])[:10]

    # 标点习惯
    punctuation = {
        '句号': all_text.count('。'),
        '感叹号': all_text.count('！') + all_text.count('!'),
        '问号': all_text.count('？') + all_text.count('?'),
        '省略号': all_text.count('...') + all_text.count('…'),
        '波浪号': all_text.count('～') + all_text.count('~'),
    }

    return {
        'emotion_distribution': dict(emotion_counts),
        'emotion_examples': {k: v for k, v in emotion_examples.items()},
        'avg_message_length': round(avg_length, 1),
        'message_style': 'short_burst' if avg_length < 20 else 'long_form',
        'top_particles': top_particles,
        'punctuation': punctuation,
    }


def generate_emotion_profile(analysis: dict, target_name: str) -> str:
    """生成 Emotion Profile markdown"""
    lines = [f"# {target_name} — Emotion Profile\n"]

    # 情绪分布
    dist = analysis.get('emotion_distribution', {})
    total = sum(dist.values()) if dist else 1
    lines.append("## 情绪表达分布\n")
    for emotion, count in sorted(dist.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        bar = '█' * int(pct / 5)
        lines.append(f"- {emotion}: {bar} {pct:.1f}%")
    lines.append("")

    # 说话风格
    lines.append("## 说话风格\n")
    style = analysis.get('message_style', 'unknown')
    lines.append(f"- 消息风格：{'短句连发型' if style == 'short_burst' else '长段落型'}")
    lines.append(f"- 平均消息长度：{analysis.get('avg_message_length', 'N/A')} 字")
    lines.append("")

    # 高频语气词
    particles = analysis.get('top_particles', [])
    if particles:
        lines.append("## 高频语气词\n")
        for word, count in particles:
            lines.append(f"- {word}: {count}次")
        lines.append("")

    # 标点习惯
    punct = analysis.get('punctuation', {})
    if any(v > 0 for v in punct.values()):
        lines.append("## 标点习惯\n")
        for name, count in punct.items():
            if count > 0:
                lines.append(f"- {name}: {count}次")
        lines.append("")

    # 情绪示例
    examples = analysis.get('emotion_examples', {})
    if examples:
        lines.append("## 情绪表达示例\n")
        for emotion, msgs in examples.items():
            lines.append(f"### {emotion}")
            for msg in msgs:
                lines.append(f"- \"{msg}\"")
            lines.append("")

    # 情感映射表模板
    lines.append("## 情感映射表\n")
    lines.append("### 用户开心/兴奋时")
    lines.append("- ta的回应方式：[待分析]")
    lines.append("")
    lines.append("### 用户低落/疲惫时")
    lines.append("- ta的回应方式：[待分析]")
    lines.append("")
    lines.append("### 用户焦虑/不安时")
    lines.append("- ta的回应方式：[待分析]")
    lines.append("")
    lines.append("### 用户愤怒时")
    lines.append("- ta的回应方式：[待分析]")
    lines.append("")
    lines.append("### 用户沉默/不想聊时")
    lines.append("- ta的回应方式：[待分析]")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='情感分析器')
    parser.add_argument('--file', required=True, help='聊天记录文件路径')
    parser.add_argument('--target', required=True, help='目标人物的名字/昵称')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    # 简单解析聊天记录
    messages = []
    msg_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)$')

    with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
        current_msg = None
        for line in f:
            line = line.rstrip('\n')
            match = msg_pattern.match(line)
            if match:
                if current_msg:
                    messages.append(current_msg)
                timestamp, sender = match.groups()
                current_msg = {'timestamp': timestamp, 'sender': sender.strip(), 'content': ''}
            elif current_msg and line.strip():
                if current_msg['content']:
                    current_msg['content'] += '\n'
                current_msg['content'] += line
    if current_msg:
        messages.append(current_msg)

    if not messages:
        print("警告：未能解析出消息，将使用纯文本模式", file=sys.stderr)
        with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        messages = [{'sender': args.target, 'content': content[:5000]}]

    # 分析
    analysis = analyze_emotional_patterns(messages, args.target)

    # 生成 profile
    profile = generate_emotion_profile(analysis, args.target)

    # 写入
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(profile)

    print(f"情感分析完成，结果已写入 {args.output}")


if __name__ == '__main__':
    main()
