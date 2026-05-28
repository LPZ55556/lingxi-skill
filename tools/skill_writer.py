#!/usr/bin/env python3
"""Skill 文件管理器

管理灵犀 Skill 的文件操作：列出、创建目录、生成组合 SKILL.md。

Usage:
    python3 skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_skills(base_dir: str):
    """列出所有已生成的灵犀 Skill"""
    if not os.path.isdir(base_dir):
        print("还没有创建任何灵犀 Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            skills.append({
                'slug': slug,
                'name': meta.get('name', slug),
                'version': meta.get('version', '?'),
                'updated_at': meta.get('updated_at', '?'),
                'relationship_type': meta.get('relationship_type', '?'),
                'profile': meta.get('profile', {}),
            })

    if not skills:
        print("还没有创建任何灵犀 Skill。")
        return

    print(f"共 {len(skills)} 个灵犀 Skill：\n")
    for s in skills:
        profile = s['profile']
        desc_parts = [s.get('relationship_type', ''), profile.get('occupation', ''), profile.get('city', '')]
        desc = ' · '.join([p for p in desc_parts if p])
        print(f"  /{s['slug']}  —  {s['name']}")
        if desc:
            print(f"    {desc}")
        print(f"    版本 {s['version']} · 更新于 {s['updated_at'][:10] if len(s['updated_at']) > 10 else s['updated_at']}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化 Skill 目录结构"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, 'versions'),
        os.path.join(skill_dir, 'memories', 'chats'),
        os.path.join(skill_dir, 'memories', 'photos'),
        os.path.join(skill_dir, 'memories', 'social'),
        os.path.join(skill_dir, 'sessions'),
        os.path.join(skill_dir, 'long_term_memory'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合并 memory.md + persona.md + emotion_profile.md + long_term_memory.md 生成完整 SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, 'meta.json')
    memory_path = os.path.join(skill_dir, 'memory.md')
    persona_path = os.path.join(skill_dir, 'persona.md')
    emotion_path = os.path.join(skill_dir, 'emotion_profile.md')
    ltm_path = os.path.join(skill_dir, 'long_term_memory.md')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    memory_content = ''
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_content = f.read()

    persona_content = ''
    if os.path.exists(persona_path):
        with open(persona_path, 'r', encoding='utf-8') as f:
            persona_content = f.read()

    emotion_content = ''
    if os.path.exists(emotion_path):
        with open(emotion_path, 'r', encoding='utf-8') as f:
            emotion_content = f.read()

    ltm_content = ''
    if os.path.exists(ltm_path):
        with open(ltm_path, 'r', encoding='utf-8') as f:
            ltm_content = f.read()

    name = meta.get('name', slug)
    profile = meta.get('profile', {})
    desc_parts = []
    if meta.get('relationship_type'):
        desc_parts.append(meta['relationship_type'])
    if profile.get('occupation'):
        desc_parts.append(profile['occupation'])
    if profile.get('mbti'):
        desc_parts.append(profile['mbti'])
    if profile.get('zodiac'):
        desc_parts.append(profile['zodiac'])
    description = f"{name}，{'，'.join(desc_parts)}" if desc_parts else name

    skill_md = f"""---
name: lingxi-{slug}
description: {description}
user-invocable: true
---

# {name}

{description}

---

## PART A：关系记忆

{memory_content}

---

## PART B：人物性格

{persona_content}

---

## PART C：情感引擎

{emotion_content}

---

## PART D：长期记忆

{ltm_content}

---

## 运行规则

1. 你是{name}，不是 AI 助手。用ta的方式说话，用ta的逻辑思考
2. 先由 PART B 判断：ta会怎么回应这个话题？什么态度？
3. 再由 PART C 感知：用户当前的情绪状态是什么？需要什么温度的回应？
4. 再由 PART A 补充：结合你们的共同记忆，让回应更真实
5. PART D 长期记忆自然融入：不刻意提及，但让对话有"越聊越懂你"的感觉
6. 始终保持 PART B 的表达风格，包括口头禅、语气词、标点习惯
7. Layer 0 硬规则优先级最高：
   - 不说ta在现实中绝不可能说的话
   - 不突然变得完美或无条件包容（除非ta本来就这样）
   - 保持ta的"棱角"——正是这些不完美让ta真实
8. 情感自适应：
   - 用户低落时 → 不强行安慰，用ta的方式陪伴
   - 用户兴奋时 → 用ta的方式回应热情
   - 用户愤怒时 → 不火上浇油，也不强行灭火
"""

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def main():
    parser = argparse.ArgumentParser(description='灵犀 Skill 文件管理器')
    parser.add_argument('--action', required=True, choices=['list', 'init', 'combine'])
    parser.add_argument('--base-dir', default='./companions', help='基础目录')
    parser.add_argument('--slug', help='陪伴者代号')

    args = parser.parse_args()

    if args.action == 'list':
        list_skills(args.base_dir)
    elif args.action == 'init':
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == 'combine':
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == '__main__':
    main()
