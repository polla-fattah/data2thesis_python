import os
import re
from bs4 import BeautifulSoup

def clean_chapter_content(soup, soup_main, is_subpath=True):
    # Remove breadcrumbs and title-block-header navigation
    for el in soup_main.find_all('nav', class_=lambda c: c and 'quarto-page-breadcrumbs' in c):
        el.decompose()
    for el in soup_main.find_all('header', id='title-block-header'):
        el.decompose()
    
    # Remove internal chapter title since we provide our own header in the card
    h1 = soup_main.find('h1')
    if h1:
        h1.decompose()
        
    # Remove page navigation footer links if present
    for el in soup_main.find_all('nav', class_=lambda c: c and 'page-navigation' in c):
        el.decompose()
        
    # Fix image sources if in a subdirectory like full/
    prefix = '../' if is_subpath else ''
    for img in soup_main.find_all('img'):
        src = img.get('src', '')
        if src and not src.startswith(('http://', 'https://', 'data:', '/')):
            img['src'] = prefix + src
            
    # Wrap standard pre / code tags if not already wrapped
    for code_cell in soup_main.find_all('div', class_=lambda c: c and 'sourceCode' in c):
        if code_cell.find_parent('div', class_='code-block-wrapper'):
            continue
        pre = code_cell.find('pre')
        if not pre:
            continue
            
        # Determine language
        lang = 'PYTHON'
        classes = pre.get('class', []) + (pre.find('code').get('class', []) if pre.find('code') else [])
        for c in classes:
            if 'bash' in c or 'sh' in c:
                lang = 'BASH'
            elif 'python' in c:
                lang = 'PYTHON'
            elif 'r' in c:
                lang = 'R'
            elif 'json' in c:
                lang = 'JSON'
            elif 'yaml' in c:
                lang = 'YAML'
                
        # Remove default quarto copy button to use our modern one
        for btn in code_cell.find_all('button', class_=lambda c: c and 'code-copy-button' in c):
            btn.decompose()
            
        wrapper = soup.new_tag('div', attrs={'class': 'code-block-wrapper'})
        header = soup.new_tag('div', attrs={'class': 'code-header-bar'})
        
        lang_label = soup.new_tag('span', attrs={'class': 'code-lang-label'})
        dot = soup.new_tag('span', attrs={'class': 'code-lang-dot'})
        lang_label.append(dot)
        lang_label.append(f" {lang}")
        
        copy_btn = soup.new_tag('button', attrs={
            'class': 'copy-code-btn',
            'onclick': 'copyCode(this)',
            'title': 'Copy code',
            'type': 'button'
        })
        copy_btn.append(BeautifulSoup('<i class="fa-regular fa-copy"></i> <span>Copy</span>', 'html.parser'))
        
        header.append(lang_label)
        header.append(copy_btn)
        
        code_cell.wrap(wrapper)
        wrapper.insert(0, header)

    # Wrap tables in table-responsive
    for table in soup_main.find_all('table'):
        if not table.find_parent('div', class_='table-responsive'):
            resp = soup.new_tag('div', attrs={'class': 'table-responsive'})
            table.wrap(resp)

    return str(soup_main)

def build_full_book():
    print("Building Full Book Online Edition...")
    
    chapter_defs = [
        # (id, filename, badge, title, part_name)
        ('chapter-01', '01-getting-started.html', 'CH 01', 'Getting Started with Python', 'Part I: Foundations of Python Programming'),
        ('chapter-02', '02-data-structures.html', 'CH 02', 'Data Structures in Python', 'Part I: Foundations of Python Programming'),
        ('chapter-03', '03-data-manipulation.html', 'CH 03', 'Data Manipulation with pandas', 'Part I: Foundations of Python Programming'),
        ('chapter-04', '04-data-visualization.html', 'CH 04', 'Data Visualization with Seaborn', 'Part I: Foundations of Python Programming'),
        ('chapter-05', '05-research-question.html', 'CH 05', 'From Research Question to Data', 'Part II: Statistical Analysis for Research'),
        ('chapter-06', '06-descriptive-statistics.html', 'CH 06', 'Descriptive Statistics & EDA', 'Part II: Statistical Analysis for Research'),
        ('chapter-07', '07-hypothesis-testing.html', 'CH 07', 'Hypothesis Testing & Inference', 'Part II: Statistical Analysis for Research'),
        ('chapter-08', '08-anova-regression.html', 'CH 08', 'ANOVA and Linear Regression', 'Part II: Statistical Analysis for Research'),
        ('chapter-09', '09-multivariate.html', 'CH 09', 'Multivariate Statistical Methods', 'Part II: Statistical Analysis for Research'),
        ('chapter-10', '10-mixed-models.html', 'CH 10', 'Mixed-Effects Models', 'Part II: Statistical Analysis for Research'),
        ('chapter-11', '11-machine-learning.html', 'CH 11', 'Foundations of Machine Learning', 'Part III: Machine Learning with Python'),
        ('chapter-12', '12-classification.html', 'CH 12', 'Classification Models', 'Part III: Machine Learning with Python'),
        ('chapter-13', '13-predictive-regression.html', 'CH 13', 'Predictive Regression', 'Part III: Machine Learning with Python'),
        ('chapter-14', '14-advanced-clustering.html', 'CH 14', 'Advanced Clustering (GMM & DBSCAN)', 'Part III: Machine Learning with Python'),
        ('chapter-15', '15-neural-networks.html', 'CH 15', 'Neural Networks and Deep Learning', 'Part III: Machine Learning with Python'),
        ('chapter-16', '16-time-series.html', 'CH 16', 'Time Series Analysis & Forecasting', 'Part III: Machine Learning with Python'),
        ('chapter-17', '17-reproducible-research.html', 'CH 17', 'Reproducible Research with Quarto', 'Part IV: Reproducible Research & Applications'),
        ('chapter-18', '18-ai.html', 'CH 18', 'AI-Assisted Data Analysis', 'Part IV: Reproducible Research & Applications'),
        ('chapter-19', '19-putting-it-together.html', 'CH 19', 'Putting It All Together: Thesis Workflow', 'Part IV: Reproducible Research & Applications'),
        ('references', 'references.html', 'REF', 'References & Bibliography', 'References'),
        ('appendix-a', 'a-installation.html', 'APP A', 'Installing Python, VS Code, and Quarto', 'Appendices'),
        ('appendix-b', 'b-glossary.html', 'APP B', 'Glossary of Key Terms', 'Appendices'),
        ('appendix-c', 'c-packages.html', 'APP C', 'Essential Python Packages Reference', 'Appendices'),
        ('appendix-d', 'd-common-errors.html', 'APP D', 'Troubleshooting and Common Python Errors', 'Appendices'),
        ('appendix-e', 'e-resources.html', 'APP E', 'Further Resources & Reading', 'Appendices'),
    ]

    base_dir = '_site/content/book'
    chapters_data = []

    for idx, (cid, filename, badge, display_title, part_name) in enumerate(chapter_defs):
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found!")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        main = soup.find('main')
        if not main:
            continue
            
        # Extract title from original H1 if available
        orig_h1 = main.find('h1')
        title_text = display_title
        if orig_h1:
            raw_title = orig_h1.get_text(strip=True)
            # Remove leading numbers from raw_title if duplicate
            clean_title = re.sub(r'^\d+\s*', '', raw_title)
            if clean_title:
                title_text = clean_title
                
        # Clean content
        content_html = clean_chapter_content(soup, main, is_subpath=True)
        
        chapters_data.append({
            'id': cid,
            'filename': filename,
            'badge': badge,
            'title': title_text,
            'part': part_name,
            'content': content_html,
            'index': idx
        })

    # Read Foreword markdown
    foreword_html = ""
    if os.path.exists('content/book/foreword.qmd'):
        with open('content/book/foreword.qmd', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        body_lines = []
        for line in lines:
            if line.startswith('# Foreword') or line.startswith('```{=typst}') or line.startswith('```') or line.startswith('#v('):
                continue
            if line.startswith('### '):
                body_lines.append(f"<h3>{line[4:].strip()}</h3>")
            elif line.startswith('> '):
                body_lines.append(f'<div class="callout callout-note"><div class="callout-body">{line[2:].strip()}</div></div>')
            elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                body_lines.append(f"<li style='margin-left: 20px;'>{line.strip()}</li>")
            elif line.strip():
                # bold
                txt = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line.strip())
                txt = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', txt)
                body_lines.append(f"<p>{txt}</p>")
        foreword_html = "\n".join(body_lines)

    total_chapters = 19
    total_appendices = 5

    # Generate HTML content
    full_html = generate_template(chapters_data, foreword_html, total_chapters, total_appendices)

    # Write destinations
    targets = [
        'content/book/full/index.html',
        '_site/content/book/full/index.html',
        '_site/content/book/full.html',
        '_site/book/full/index.html',
        '_site/book/full.html',
    ]

    for target in targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        # For root-level full.html vs full/index.html, adjust asset paths
        if target.endswith('full.html'):
            content = full_html.replace('../0', '0').replace('../../images/', '../images/').replace('../../../downloads/', '../downloads/')
        else:
            content = full_html
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {target} ({len(content):,} bytes)")

def generate_template(chapters_data, foreword_html, total_chapters, total_appendices):
    # Group chapters by Part for sidebar and TOC
    parts_map = {}
    for ch in chapters_data:
        p = ch['part']
        if p not in parts_map:
            parts_map[p] = []
        parts_map[p].append(ch)

    # Build Sidebar Links
    sidebar_items_html = []
    # Front matter in sidebar
    sidebar_items_html.append('''
      <div class="sidebar-section-title">Front Matter</div>
      <li class="sidebar-toc-item" data-target="dedication">
        <a href="#dedication"><span class="sidebar-num-badge">DED</span> Dedication</a>
      </li>
      <li class="sidebar-toc-item" data-target="foreword">
        <a href="#foreword"><span class="sidebar-num-badge">FWD</span> Foreword by Dr. Polla Fattah</a>
      </li>
    ''')

    for part_name, ch_list in parts_map.items():
        sidebar_items_html.append(f'<div class="sidebar-section-title">{part_name}</div>')
        for ch in ch_list:
            sidebar_items_html.append(f'''
              <li class="sidebar-toc-item" data-target="{ch['id']}">
                <a href="#{ch['id']}">
                  <span class="sidebar-num-badge">{ch['badge']}</span>
                  <span class="sidebar-item-label">{ch['title']}</span>
                </a>
              </li>
            ''')

    # Build Chapter Switcher Options
    select_options = [
        '<option value="table-of-contents">⚡ Jump to Chapter / Topic...</option>',
        '<optgroup label="Front Matter">',
        '  <option value="dedication">Dedication</option>',
        '  <option value="foreword">Foreword by Dr. Polla Fattah</option>',
        '</optgroup>'
    ]

    for part_name, ch_list in parts_map.items():
        select_options.append(f'<optgroup label="{part_name}">')
        for ch in ch_list:
            select_options.append(f'  <option value="{ch["id"]}">{ch["badge"]}: {ch["title"]}</option>')
        select_options.append('</optgroup>')

    # Build Visual TOC Cards
    toc_cards_html = []
    for part_name, ch_list in parts_map.items():
        toc_cards_html.append(f'<div class="toc-part-group"><div class="toc-part-heading">{part_name}</div><div class="book-toc-grid">')
        for ch in ch_list:
            toc_cards_html.append(f'''
              <a href="#{ch['id']}" class="book-toc-card">
                <span class="toc-card-pill">{ch['badge']}</span>
                <span class="toc-card-title">{ch['title']}</span>
              </a>
            ''')
        toc_cards_html.append('</div></div>')

    # Build Articles for Chapters
    articles_html = []

    # 1. Dedication
    articles_html.append('''
      <article class="chapter-article" id="dedication">
        <div class="chapter-header" style="text-align: center; border-bottom: none; padding: 40px 20px;">
          <div class="chapter-pill-badge" style="background: rgba(37,99,235,0.08); color: var(--primary);">Dedication</div>
          <div style="font-size: 1.8rem; font-style: italic; color: var(--text-main); margin-top: 24px; font-weight: 500;">
            "Dedicated to Tano"
          </div>
        </div>
        <footer class="chapter-footer-nav">
          <a href="#table-of-contents" class="pager-btn pager-btn-toc"><i class="fa-solid fa-list-ol"></i> Table of Contents</a>
          <a href="#foreword" class="pager-btn pager-btn-next">Foreword <i class="fa-solid fa-arrow-right"></i></a>
        </footer>
      </article>
    ''')

    # 2. Foreword
    articles_html.append(f'''
      <article class="chapter-article" id="foreword">
        <div class="chapter-header">
          <div class="chapter-pill-badge">PREFACE &amp; FOREWORD</div>
          <h1 class="chapter-main-title">Foreword</h1>
          <div class="chapter-meta-banner">
            By <strong>Dr. Polla Abdulhamid Fattah</strong> · Lecturer at Salahaddin University-Erbil (SUE) &amp; Director/Founding Member at AIIC, University of Kurdistan Hewlêr
          </div>
        </div>
        <div class="chapter-body">
          {foreword_html}
        </div>
        <footer class="chapter-footer-nav">
          <a href="#dedication" class="pager-btn pager-btn-prev"><i class="fa-solid fa-arrow-left"></i> Dedication</a>
          <a href="#table-of-contents" class="pager-btn pager-btn-toc"><i class="fa-solid fa-list-ol"></i> Table of Contents</a>
          <a href="#chapter-01" class="pager-btn pager-btn-next">Chapter 01 <i class="fa-solid fa-arrow-right"></i></a>
        </footer>
      </article>
    ''')

    # 3. All Chapters, References, Appendices
    for i, ch in enumerate(chapters_data):
        prev_target = "foreword" if i == 0 else chapters_data[i-1]['id']
        prev_label = "Foreword" if i == 0 else chapters_data[i-1]['badge']
        
        has_next = i < len(chapters_data) - 1
        next_target = chapters_data[i+1]['id'] if has_next else "back-cover"
        next_label = chapters_data[i+1]['badge'] if has_next else "Back Cover"

        pencil_button_html = ""
        if ch['id'].startswith('chapter-'):
            qmd_name = ch['filename'].replace('.html', '.qmd')
            pencil_button_html = f'''
              <div style="margin-top: 8px;">
                <a href="https://github.com/polla-fattah/data2thesis_python/edit/main/content/book/{qmd_name}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 7px; padding: 4px 12px; font-size: 0.82rem; font-weight: 600; color: var(--brand-copper, #b4762e); background: rgba(180, 118, 46, 0.08); border: 1px solid rgba(180, 118, 46, 0.25); border-radius: 6px; text-decoration: none;">
                  <i class="fa-solid fa-pen-to-square"></i> Amendments are welcomed
                </a>
              </div>
            '''

        articles_html.append(f'''
          <article class="chapter-article" id="{ch['id']}" data-chapter="{ch['badge']}">
            <div class="chapter-header">
              <div class="chapter-pill-badge">
                <i class="fa-solid fa-bookmark" style="font-size: 0.75rem;"></i>
                <span>{ch['part']} · {ch['badge']}</span>
              </div>
              <h1 class="chapter-main-title">{ch['title']}</h1>
              {pencil_button_html}
              <div class="chapter-meta-banner">
                FROM DATA TO THESIS: Using Python for Non-Technical · Comprehensive Online Reader
              </div>
            </div>
            
            <div class="chapter-body">
              {ch['content']}
            </div>

            <footer class="chapter-footer-nav">
              <a href="#{prev_target}" class="pager-btn pager-btn-prev">
                <i class="fa-solid fa-arrow-left"></i> {prev_label}
              </a>
              <a href="#table-of-contents" class="pager-btn pager-btn-toc">
                <i class="fa-solid fa-list-ol"></i> Table of Contents
              </a>
              <a href="#{next_target}" class="pager-btn pager-btn-next">
                {next_label} <i class="fa-solid fa-arrow-right"></i>
              </a>
            </footer>
          </article>
        ''')

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FROM DATA TO THESIS: Using Python for Non-Technical (Full Book)</title>
  <meta name="description" content="Complete textbook 'FROM DATA TO THESIS: Using Python for Non-Technical' by Dr. Polla Abdulhamid Fattah and Collection of LLMs. Read all 19 chapters, references, and appendices online." />
  
  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="../../images/logo.svg" />
  <link rel="alternate icon" type="image/png" href="../../images/cover-front.png" />

  <!-- FontAwesome 6 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  
  <!-- MathJax 3 for Equations -->
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js" type="text/javascript"></script>

  <!-- Modern Styling -->
  <style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;1,400&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

:root {{
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-dark: #1e3a8a;
  --primary-light: #eff6ff;
  --primary-border: #bfdbfe;
  --accent-emerald: #059669;
  --accent-emerald-light: #ecfdf5;
  --accent-amber: #d97706;
  --accent-amber-light: #fffbeb;
  --accent-rose: #e11d48;
  --accent-rose-light: #fff1f2;
  --text-main: #0f172a;
  --text-body: #334155;
  --text-muted: #64748b;
  --text-subtle: #94a3b8;
  --bg-page: #f8fafc;
  --bg-card: #ffffff;
  --bg-sidebar: #ffffff;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --code-bg: #0f172a;
  --code-header-bg: #1e293b;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.06), 0 1px 2px 0 rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
}}

[data-theme="dark"] {{
  --primary: #38bdf8;
  --primary-hover: #60a5fa;
  --primary-dark: #0284c7;
  --primary-light: rgba(56, 189, 248, 0.12);
  --primary-border: rgba(56, 189, 248, 0.28);
  --accent-emerald: #34d399;
  --accent-emerald-light: rgba(52, 211, 153, 0.12);
  --accent-amber: #fbbf24;
  --accent-amber-light: rgba(251, 191, 36, 0.12);
  --accent-rose: #f87171;
  --accent-rose-light: rgba(248, 113, 113, 0.12);
  --text-main: #f8fafc;
  --text-body: #cbd5e1;
  --text-muted: #94a3b8;
  --text-subtle: #64748b;
  --bg-page: #0b1120;
  --bg-card: #151f32;
  --bg-sidebar: #0f172a;
  --border: #1e293b;
  --border-strong: #334155;
  --code-bg: #070d19;
  --code-header-bg: #0f172a;
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.6);
}}

*, *::before, *::after {{
  box-sizing: border-box;
}}

html {{
  scroll-behavior: smooth;
  font-size: 16px;
  -webkit-text-size-adjust: 100%;
}}

body {{
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--text-body);
  background-color: var(--bg-page);
  line-height: 1.75;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background-color 200ms ease, color 200ms ease;
}}

/* Reading Progress Bar */
#reading-progress-bar {{
  position: fixed;
  top: 0;
  left: 0;
  height: 3.5px;
  background: linear-gradient(90deg, #38bdf8 0%, #2563eb 50%, #1e40af 100%);
  width: 0%;
  z-index: 2000;
  transition: width 80ms ease-out;
}}

/* Sticky Top Navigation Bar */
.book-navbar {{
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  transition: background-color 200ms ease, border-color 200ms ease;
}}

[data-theme="dark"] .book-navbar {{
  background: rgba(15, 23, 42, 0.92);
}}

.book-nav-left {{
  display: flex;
  align-items: center;
  gap: 14px;
}}

.book-nav-brand {{
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-main);
  font-weight: 700;
  font-size: 0.98rem;
  transition: opacity 160ms ease;
}}

.book-nav-brand:hover {{
  opacity: 0.85;
}}

.book-nav-logo {{
  width: 32px;
  height: 32px;
  border-radius: 6px;
  object-fit: cover;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}}

.book-brand-badge {{
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  padding: 2px 8px;
  border-radius: 9999px;
  background: var(--primary-light);
  color: var(--primary);
  border: 1px solid var(--primary-border);
}}

.book-nav-center {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  max-width: 520px;
  margin: 0 16px;
}}

.chapter-switcher-select {{
  width: 100%;
  padding: 7px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-main);
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  transition: border-color 160ms ease, box-shadow 160ms ease;
}}

.chapter-switcher-select:focus,
.chapter-switcher-select:hover {{
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}}

.book-nav-actions {{
  display: flex;
  align-items: center;
  gap: 10px;
}}

.nav-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 160ms ease;
  white-space: nowrap;
  cursor: pointer;
}}

.nav-btn-ghost {{
  color: var(--text-body);
  border: 1px solid var(--border);
  background: var(--bg-card);
}}

.nav-btn-ghost:hover {{
  color: var(--primary);
  border-color: var(--primary);
  background: var(--primary-light);
}}

.nav-btn-primary {{
  background: var(--primary);
  color: #ffffff !important;
  border: 1px solid var(--primary);
}}

.nav-btn-primary:hover {{
  background: var(--primary-hover);
  border-color: var(--primary-hover);
}}

.theme-toggle-btn {{
  background: none;
  border: 1px solid var(--border);
  padding: 6px 11px;
  border-radius: var(--radius-sm);
  color: var(--text-main);
  cursor: pointer;
  transition: all 160ms ease;
}}

.theme-toggle-btn:hover {{
  background: var(--primary-light);
  color: var(--primary);
  border-color: var(--primary);
}}

.sidebar-toggle-btn {{
  display: none;
  background: none;
  border: 1px solid var(--border);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  color: var(--text-main);
  font-size: 1.1rem;
  cursor: pointer;
}}

/* App Master Layout */
.book-shell {{
  display: flex;
  max-width: 1560px;
  margin: 0 auto;
  min-height: calc(100vh - 58px);
}}

/* Sticky Chapter Sidebar */
.book-sidebar {{
  width: 320px;
  flex-shrink: 0;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  position: sticky;
  top: 58px;
  height: calc(100vh - 58px);
  overflow-y: auto;
  padding: 20px 16px 40px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: background-color 200ms ease, border-color 200ms ease;
}}

.book-sidebar::-webkit-scrollbar {{
  width: 6px;
}}

.book-sidebar::-webkit-scrollbar-thumb {{
  background: var(--border-strong);
  border-radius: 3px;
}}

.sidebar-header {{
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}}

.sidebar-title {{
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--text-muted);
  margin-bottom: 8px;
}}

.sidebar-search-box {{
  width: 100%;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  font-family: inherit;
  font-size: 0.85rem;
  background: var(--bg-page);
  color: var(--text-main);
  outline: none;
  transition: all 160ms ease;
}}

.sidebar-search-box:focus {{
  background: var(--bg-card);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}}

.sidebar-section-title {{
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  padding: 10px 8px 4px 8px;
}}

.sidebar-toc-list {{
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}}

.sidebar-toc-item a {{
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 7px 10px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  color: var(--text-body);
  font-size: 0.86rem;
  font-weight: 500;
  transition: all 140ms ease;
  border-left: 3px solid transparent;
}}

.sidebar-toc-item a:hover {{
  background: var(--primary-light);
  color: var(--primary);
}}

.sidebar-toc-item.active a {{
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700;
  border-left-color: var(--primary);
}}

.sidebar-num-badge {{
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  padding: 1px 5px;
  border-radius: 4px;
  flex-shrink: 0;
}}

.sidebar-toc-item.active .sidebar-num-badge {{
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}}

/* Main Reading Area */
.book-main {{
  flex: 1;
  min-width: 0;
  padding: 32px 48px 100px 48px;
  max-width: 1060px;
  margin: 0 auto;
}}

/* Hero & Front Cover Card */
.book-hero-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 40px;
  margin-bottom: 44px;
  box-shadow: var(--shadow-md);
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 36px;
  align-items: center;
  transition: background-color 200ms ease, border-color 200ms ease;
}}

.book-hero-cover {{
  text-align: center;
}}

.book-cover-img {{
  width: 100%;
  max-width: 280px;
  height: auto;
  border-radius: var(--radius-md);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 0, 0, 0.08);
}}

.book-hero-meta {{
  display: flex;
  flex-direction: column;
  gap: 12px;
}}

.hero-kicker {{
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--primary);
}}

.hero-main-title {{
  font-size: 2.35rem;
  font-weight: 800;
  line-height: 1.2;
  color: var(--text-main);
  margin: 0;
  letter-spacing: -0.02em;
}}

.hero-subtitle {{
  font-size: 1.15rem;
  color: var(--text-muted);
  font-weight: 500;
  line-height: 1.5;
  margin: 0;
}}

.hero-author-box {{
  padding: 12px 16px;
  background: var(--bg-page);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-top: 6px;
}}

.hero-author-name {{
  font-weight: 700;
  color: var(--text-main);
  font-size: 1rem;
}}

.hero-author-affil {{
  font-size: 0.86rem;
  color: var(--text-muted);
  line-height: 1.4;
  margin-top: 2px;
}}

.hero-details-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 6px;
}}

.hero-badge-pill {{
  font-size: 0.78rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 9999px;
  background: var(--bg-page);
  border: 1px solid var(--border);
  color: var(--text-muted);
}}

.hero-actions-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}}

/* Visual Table of Contents Section */
.book-toc-section {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px 36px 40px 36px;
  margin-bottom: 50px;
  box-shadow: var(--shadow-sm);
  transition: background-color 200ms ease, border-color 200ms ease;
}}

.book-toc-header {{
  border-bottom: 2px solid var(--primary);
  padding-bottom: 14px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.book-toc-title {{
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--text-main);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}}

.toc-part-group {{
  margin-bottom: 24px;
}}

.toc-part-heading {{
  font-size: 0.88rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--primary);
  margin-bottom: 10px;
  padding-bottom: 4px;
  border-bottom: 1px dashed var(--border);
}}

.book-toc-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 10px;
  list-style: none;
  padding: 0;
  margin: 0;
}}

.book-toc-card {{
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  background: var(--bg-page);
  border: 1px solid var(--border);
  text-decoration: none;
  color: var(--text-main);
  transition: all 160ms ease;
}}

.book-toc-card:hover {{
  background: var(--bg-card);
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
  color: var(--primary);
}}

.toc-card-pill {{
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  padding: 2px 7px;
  border-radius: 4px;
  flex-shrink: 0;
}}

.toc-card-title {{
  font-weight: 600;
  font-size: 0.92rem;
  line-height: 1.4;
}}

/* Chapter Article Block */
.chapter-article {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 44px 44px;
  margin-bottom: 50px;
  box-shadow: var(--shadow-md);
  position: relative;
  transition: background-color 200ms ease, border-color 200ms ease;
}}

.chapter-header {{
  border-bottom: 2px solid var(--border);
  padding-bottom: 22px;
  margin-bottom: 32px;
}}

.chapter-pill-badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--primary);
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  padding: 4px 12px;
  border-radius: 9999px;
  margin-bottom: 12px;
}}

.chapter-main-title {{
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.25;
  margin: 0 0 14px 0;
  letter-spacing: -0.02em;
}}

.chapter-meta-banner {{
  background: var(--bg-page);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.5;
  font-style: italic;
}}

/* Chapter Body Typography */
.chapter-body {{
  color: var(--text-body);
  font-size: 1.04rem;
  line-height: 1.8;
}}

.chapter-body h2 {{
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-main);
  margin-top: 2.4rem;
  margin-bottom: 0.8rem;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
  letter-spacing: -0.01em;
  scroll-margin-top: 80px;
}}

.chapter-body h3 {{
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  margin-top: 1.8rem;
  margin-bottom: 0.6rem;
  scroll-margin-top: 80px;
}}

.chapter-body h4 {{
  font-size: 1.08rem;
  font-weight: 700;
  color: var(--text-muted);
  margin-top: 1.4rem;
  margin-bottom: 0.5rem;
  scroll-margin-top: 80px;
}}

.chapter-body p {{
  margin: 1.2em 0;
}}

.chapter-body strong {{
  color: var(--text-main);
  font-weight: 700;
}}

.chapter-body ul, 
.chapter-body ol {{
  margin: 1.2em 0;
  padding-left: 28px;
}}

.chapter-body li {{
  margin-bottom: 0.45em;
}}

.chapter-body a {{
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  border-bottom: 1px solid transparent;
  transition: border-color 140ms ease;
}}

.chapter-body a:hover {{
  border-bottom-color: var(--primary);
}}

/* Inline Code */
.chapter-body code:not([class*="sourceCode"]):not(pre code) {{
  font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
  font-size: 0.88em;
  font-weight: 500;
  color: var(--primary);
  background-color: var(--primary-light);
  border: 1px solid var(--primary-border);
  padding: 0.18em 0.45em;
  border-radius: 4px;
  word-break: break-word;
}}

/* Code Block Containers */
.code-block-wrapper {{
  background: var(--code-bg);
  border: 1px solid var(--code-header-bg);
  border-radius: var(--radius-md);
  margin: 1.6em 0;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}}

.code-header-bar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: var(--code-header-bg);
  border-bottom: 1px solid #334155;
}}

.code-lang-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 8px;
}}

.code-lang-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary);
}}

.copy-code-btn {{
  background: #334155;
  color: #e2e8f0;
  border: 1px solid #475569;
  border-radius: 4px;
  padding: 3px 9px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: inherit;
  transition: all 140ms ease;
}}

.copy-code-btn:hover {{
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
}}

.code-block-wrapper pre {{
  margin: 0;
  padding: 16px 20px;
  font-family: 'JetBrains Mono', 'Fira Code', Consolas, Monaco, monospace;
  font-size: 0.91rem;
  line-height: 1.6;
  color: #f8fafc;
  overflow-x: auto;
  background: transparent;
}}

.code-block-wrapper pre code {{
  font-family: inherit;
  font-size: inherit;
  color: inherit;
  background: none;
  border: none;
  padding: 0;
}}

/* Terminal / Output Styling */
.cell-output {{
  margin: 0.8em 0 1.6em 0;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: var(--radius-md);
  padding: 12px 18px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  color: #a5f3fc;
  overflow-x: auto;
}}

.cell-output pre {{
  margin: 0;
  padding: 0;
  background: transparent;
  color: inherit;
}}

/* Syntax Highlighting Tokens */
code span.kw {{ color: #38bdf8; font-weight: 600; }}
code span.cf {{ color: #38bdf8; font-weight: 600; }}
code span.dt {{ color: #f472b6; }}
code span.dv, code span.fl, code span.bn {{ color: #fb923c; }}
code span.ch, code span.st {{ color: #4ade80; }}
code span.co, code span.cv, code span.do {{ color: #94a3b8; font-style: italic; }}
code span.fu {{ color: #60a5fa; font-weight: 600; }}
code span.bu {{ color: #c084fc; font-weight: 600; }}
code span.va {{ color: #e2e8f0; }}
code span.op {{ color: #94a3b8; }}
code span.sc {{ color: #fb7185; }}

/* Tables */
.table-responsive {{
  width: 100%;
  overflow-x: auto;
  margin: 1.6em 0;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.94rem;
  background: var(--bg-card);
  margin: 0;
}}

th {{
  background-color: var(--bg-page);
  color: var(--text-main);
  font-weight: 700;
  text-align: left;
  padding: 12px 16px;
  border-bottom: 2px solid var(--border);
}}

td {{
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  color: var(--text-body);
}}

tr:last-child td {{
  border-bottom: none;
}}

tr:hover td {{
  background-color: var(--primary-light);
}}

/* Callout Alerts - High Contrast & Maximum Readability */
.callout {{
  border-radius: var(--radius-md);
  padding: 16px 20px;
  margin: 1.8em 0;
  border-left: 4px solid var(--primary);
  border-top: 1px solid var(--border);
  border-right: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  background: var(--bg-card);
}}

.callout .callout-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 750;
  font-size: 0.96rem;
  letter-spacing: -0.01em;
  margin-bottom: 8px;
}}

.callout .callout-title-container {{
  font-weight: 750;
  font-size: 0.98rem;
  color: var(--text-main);
}}

.callout .callout-icon-container {{
  display: inline-flex;
  align-items: center;
  font-size: 1.1rem;
}}

.callout .callout-body,
.callout .callout-body-container {{
  font-size: 0.96rem;
  line-height: 1.7;
  color: var(--text-body);
}}

.callout .callout-body p,
.callout .callout-body-container p {{
  color: inherit !important;
  margin: 0.6em 0;
}}

.callout .callout-body p:first-child,
.callout .callout-body-container p:first-child {{
  margin-top: 0;
}}

.callout .callout-body p:last-child,
.callout .callout-body-container p:last-child {{
  margin-bottom: 0;
}}

.callout .callout-body strong,
.callout .callout-body-container strong {{
  color: var(--text-main);
  font-weight: 700;
}}

.callout code:not([class*="sourceCode"]) {{
  background-color: rgba(0, 0, 0, 0.06) !important;
  color: var(--text-main) !important;
  border: 1px solid rgba(0, 0, 0, 0.1) !important;
}}

/* Callout Themes - Light Mode */
.callout-tip {{
  border-left-color: #059669 !important;
  background-color: #f0fdf4 !important;
  border-color: #bbf7d0 #bbf7d0 #bbf7d0 #059669 !important;
}}
.callout-tip .callout-header,
.callout-tip .callout-title-container,
.callout-tip .callout-icon {{
  color: #065f46 !important;
}}
.callout-tip .callout-body,
.callout-tip .callout-body-container {{
  color: #064e3b !important;
}}

.callout-note {{
  border-left-color: #2563eb !important;
  background-color: #eff6ff !important;
  border-color: #bfdbfe #bfdbfe #bfdbfe #2563eb !important;
}}
.callout-note .callout-header,
.callout-note .callout-title-container,
.callout-note .callout-icon {{
  color: #1e40af !important;
}}
.callout-note .callout-body,
.callout-note .callout-body-container {{
  color: #1e3a8a !important;
}}

.callout-important, 
.callout-warning {{
  border-left-color: #d97706 !important;
  background-color: #fffbeb !important;
  border-color: #fde68a #fde68a #fde68a #d97706 !important;
}}
.callout-important .callout-header,
.callout-important .callout-title-container,
.callout-important .callout-icon,
.callout-warning .callout-header,
.callout-warning .callout-title-container,
.callout-warning .callout-icon {{
  color: #92400e !important;
}}
.callout-important .callout-body,
.callout-important .callout-body-container,
.callout-warning .callout-body,
.callout-warning .callout-body-container {{
  color: #78350f !important;
}}

.callout-caution {{
  border-left-color: #e11d48 !important;
  background-color: #fff1f2 !important;
  border-color: #fecdd3 #fecdd3 #fecdd3 #e11d48 !important;
}}
.callout-caution .callout-header,
.callout-caution .callout-title-container,
.callout-caution .callout-icon {{
  color: #9f1239 !important;
}}
.callout-caution .callout-body,
.callout-caution .callout-body-container {{
  color: #881337 !important;
}}

/* Callout Themes - Dark Mode */
[data-theme="dark"] .callout {{
  background-color: #131d2e !important;
}}

[data-theme="dark"] .callout code:not([class*="sourceCode"]) {{
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #f8fafc !important;
  border-color: rgba(255, 255, 255, 0.18) !important;
}}

[data-theme="dark"] .callout-tip {{
  border-left-color: #10b981 !important;
  background-color: rgba(16, 185, 129, 0.14) !important;
  border-color: rgba(16, 185, 129, 0.28) rgba(16, 185, 129, 0.28) rgba(16, 185, 129, 0.28) #10b981 !important;
}}
[data-theme="dark"] .callout-tip .callout-header,
[data-theme="dark"] .callout-tip .callout-title-container,
[data-theme="dark"] .callout-tip .callout-icon {{
  color: #6ee7b7 !important;
}}
[data-theme="dark"] .callout-tip .callout-body,
[data-theme="dark"] .callout-tip .callout-body-container {{
  color: #ecfdf5 !important;
}}

[data-theme="dark"] .callout-note {{
  border-left-color: #38bdf8 !important;
  background-color: rgba(56, 189, 248, 0.14) !important;
  border-color: rgba(56, 189, 248, 0.28) rgba(56, 189, 248, 0.28) rgba(56, 189, 248, 0.28) #38bdf8 !important;
}}
[data-theme="dark"] .callout-note .callout-header,
[data-theme="dark"] .callout-note .callout-title-container,
[data-theme="dark"] .callout-note .callout-icon {{
  color: #7dd3fc !important;
}}
[data-theme="dark"] .callout-note .callout-body,
[data-theme="dark"] .callout-note .callout-body-container {{
  color: #f0f9ff !important;
}}

[data-theme="dark"] .callout-important,
[data-theme="dark"] .callout-warning {{
  border-left-color: #fbbf24 !important;
  background-color: rgba(251, 191, 36, 0.14) !important;
  border-color: rgba(251, 191, 36, 0.28) rgba(251, 191, 36, 0.28) rgba(251, 191, 36, 0.28) #fbbf24 !important;
}}
[data-theme="dark"] .callout-important .callout-header,
[data-theme="dark"] .callout-important .callout-title-container,
[data-theme="dark"] .callout-important .callout-icon,
[data-theme="dark"] .callout-warning .callout-header,
[data-theme="dark"] .callout-warning .callout-title-container,
[data-theme="dark"] .callout-warning .callout-icon {{
  color: #fde68a !important;
}}
[data-theme="dark"] .callout-important .callout-body,
[data-theme="dark"] .callout-important .callout-body-container,
[data-theme="dark"] .callout-warning .callout-body,
[data-theme="dark"] .callout-warning .callout-body-container {{
  color: #fffbeb !important;
}}

[data-theme="dark"] .callout-caution {{
  border-left-color: #f43f5e !important;
  background-color: rgba(244, 63, 94, 0.14) !important;
  border-color: rgba(244, 63, 94, 0.28) rgba(244, 63, 94, 0.28) rgba(244, 63, 94, 0.28) #f43f5e !important;
}}
[data-theme="dark"] .callout-caution .callout-header,
[data-theme="dark"] .callout-caution .callout-title-container,
[data-theme="dark"] .callout-caution .callout-icon {{
  color: #fda4af !important;
}}
[data-theme="dark"] .callout-caution .callout-body,
[data-theme="dark"] .callout-caution .callout-body-container {{
  color: #fff1f2 !important;
}}

/* Images Inside Chapter */
.chapter-body img {{
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-md);
  display: block;
  margin: 1.8em auto;
}}

.quarto-figure {{
  text-align: center;
  margin: 2em 0;
}}

.quarto-figure figcaption {{
  font-size: 0.88rem;
  color: var(--text-muted);
  margin-top: 8px;
  font-style: italic;
}}

/* Chapter Footer Pager */
.chapter-footer-nav {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  border-top: 1px solid var(--border);
  padding-top: 24px;
  margin-top: 40px;
}}

.pager-btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 140ms ease;
}}

.pager-btn-prev {{
  background: var(--bg-card);
  color: var(--text-body);
  border: 1px solid var(--border);
}}

.pager-btn-prev:hover {{
  background: var(--primary-light);
  color: var(--primary);
  border-color: var(--primary);
}}

.pager-btn-toc {{
  color: var(--text-muted);
  font-weight: 500;
  text-decoration: none;
}}

.pager-btn-toc:hover {{
  color: var(--primary);
}}

.pager-btn-next {{
  background: var(--primary);
  color: #ffffff !important;
  border: 1px solid var(--primary);
}}

.pager-btn-next:hover {{
  background: var(--primary-hover);
  border-color: var(--primary-hover);
}}

/* Back Cover Card */
.book-back-cover-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 40px;
  margin-top: 20px;
  margin-bottom: 40px;
  box-shadow: var(--shadow-md);
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 36px;
  align-items: center;
  transition: background-color 200ms ease, border-color 200ms ease;
}}

/* Floating Return to Top Button */
.floating-top-btn {{
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 999;
  background: var(--primary);
  color: #ffffff;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.45);
  text-decoration: none;
  font-size: 1.1rem;
  transition: transform 160ms ease, background 160ms ease, opacity 200ms ease;
  opacity: 0;
  pointer-events: none;
}}

.floating-top-btn.visible {{
  opacity: 1;
  pointer-events: auto;
}}

.floating-top-btn:hover {{
  transform: translateY(-3px);
  background: var(--primary-hover);
  color: #ffffff;
}}

/* Responsive Media Queries */
@media (max-width: 1100px) {{
  .book-shell {{
    flex-direction: column;
  }}
  
  .book-sidebar {{
    display: none;
    position: fixed;
    top: 58px;
    left: 0;
    width: 300px;
    z-index: 1500;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  }}
  
  .book-sidebar.open {{
    display: flex;
  }}
  
  .sidebar-toggle-btn {{
    display: inline-block;
  }}
  
  .book-main {{
    padding: 24px 20px 80px 20px;
  }}
  
  .book-hero-card,
  .book-back-cover-card {{
    grid-template-columns: 1fr;
    text-align: center;
    padding: 28px 20px;
  }}
  
  .book-cover-img {{
    margin: 0 auto;
  }}
  
  .hero-details-row,
  .hero-actions-row {{
    justify-content: center;
  }}
}}

@media (max-width: 640px) {{
  .chapter-article {{
    padding: 28px 18px;
  }}
  
  .book-toc-grid {{
    grid-template-columns: 1fr;
  }}
  
  .book-nav-center {{
    display: none;
  }}
  
  .chapter-main-title {{
    font-size: 1.75rem;
  }}
}}
  </style>
</head>
<body>

  <!-- Top Progress Bar -->
  <div id="reading-progress-bar"></div>

  <!-- Sticky Navbar -->
  <header class="book-navbar">
    <div class="book-nav-left">
      <button class="sidebar-toggle-btn" onclick="toggleSidebar()" title="Toggle chapters sidebar" aria-label="Toggle chapters menu">
        <i class="fa-solid fa-bars"></i>
      </button>
      <a href="../../index.html" class="book-nav-brand">
        <img src="../../images/logo.svg" alt="Python Logo" class="book-nav-logo" />
        <span>From Data to Thesis</span>
      </a>
      <span class="book-brand-badge">Full Book</span>
    </div>

    <div class="book-nav-center">
      <select id="header-chapter-select" class="chapter-switcher-select" onchange="onChapterSelectChange(this)">
        {''.join(select_options)}
      </select>
    </div>

    <div class="book-nav-actions">
      <button class="theme-toggle-btn" onclick="toggleTheme()" title="Toggle Dark/Light Mode" aria-label="Toggle theme">
        <i class="fa-solid fa-moon" id="theme-icon"></i>
      </button>
      <a href="#table-of-contents" class="nav-btn nav-btn-ghost">
        <i class="fa-solid fa-list-ol"></i> Contents
      </a>
      <a href="../../../downloads/From-Data-to-Thesis.pdf" class="nav-btn nav-btn-primary" download>
        <i class="fa-solid fa-file-pdf"></i> Download PDF
      </a>
    </div>
  </header>

  <!-- Shell Layout -->
  <div class="book-shell">
    
    <!-- Sidebar -->
    <aside class="book-sidebar" id="book-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-title">Book Contents</div>
        <input 
          type="text" 
          class="sidebar-search-box" 
          placeholder="Filter chapters..." 
          oninput="onSidebarSearch(this)"
          aria-label="Filter book chapters"
        />
      </div>
      <ul class="sidebar-toc-list" id="sidebar-toc-list">
        {''.join(sidebar_items_html)}
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="book-main">
      
      <!-- Hero Card -->
      <section class="book-hero-card" id="book-hero">
        <div class="book-hero-cover">
          <img src="../../images/cover-front.png" alt="FROM DATA TO THESIS: Using Python for Non-Technical Cover" class="book-cover-img" />
        </div>
        <div class="book-hero-meta">
          <div class="hero-kicker">Complete Textbook Online Edition</div>
          <h1 class="hero-main-title">From Data to Thesis</h1>
          <p class="hero-subtitle">Using Python for Non-Technical</p>
          
          <div class="hero-author-box">
            <div class="hero-author-name">Dr. Polla Abdulhamid Fattah &amp; Collection of LLMs</div>
            <div class="hero-author-affil">Lecturer at Salahaddin University-Erbil (SUE)</div>
            <div class="hero-author-affil">Director &amp; Founding Member, AIIC, University of Kurdistan Hewlêr (UKH)</div>
          </div>

          <div class="hero-details-row">
            <span class="hero-badge-pill"><i class="fa-solid fa-book-open"></i> {total_chapters} Chapters</span>
            <span class="hero-badge-pill"><i class="fa-solid fa-paperclip"></i> {total_appendices} Appendices</span>
            <span class="hero-badge-pill"><i class="fa-solid fa-file-pdf"></i> Companion PDF</span>
            <span class="hero-badge-pill"><i class="fa-solid fa-code"></i> Quarto &amp; Python 3.12</span>
            <span class="hero-badge-pill"><i class="fa-solid fa-database"></i> 600-Student Case Study</span>
          </div>

          <div class="hero-actions-row">
            <a href="#chapter-01" class="nav-btn nav-btn-primary">
              <i class="fa-solid fa-play"></i> Start Reading (Chapter 1)
            </a>
            <a href="../../../downloads/From-Data-to-Thesis.pdf" class="nav-btn nav-btn-ghost" download>
              <i class="fa-solid fa-file-pdf"></i> Download PDF (14.8 MB)
            </a>
            <a href="../../index.html" class="nav-btn nav-btn-ghost">
              <i class="fa-solid fa-house"></i> Course Home
            </a>
          </div>
        </div>
      </section>

      <!-- Visual Table of Contents -->
      <section class="book-toc-section" id="table-of-contents">
        <div class="book-toc-header">
          <h2 class="book-toc-title"><i class="fa-solid fa-table-list"></i> Table of Contents</h2>
          <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted);">COMPLETE 4-PART CURRICULUM</span>
        </div>
        {''.join(toc_cards_html)}
      </section>

      <!-- Articles Stream -->
      {''.join(articles_html)}

      <!-- Back Cover Section -->
      <section class="book-back-cover-card" id="back-cover">
        <div class="book-hero-cover">
          <img src="../../images/cover-back.jpg" alt="FROM DATA TO THESIS: Using Python for Non-Technical Back Cover" class="book-cover-img" />
        </div>
        <div class="book-hero-meta">
          <div class="hero-kicker">About this Publication</div>
          <h2 class="hero-main-title" style="font-size: 1.8rem;">End of Book Edition</h2>
          <p class="hero-subtitle">
            You have reached the end of <em>FROM DATA TO THESIS: Using Python for Non-Technical</em>.
            May this research journey empower your thesis defense and future scientific publications.
          </p>
          <div class="hero-author-box">
            <div class="hero-author-name">Dr. Polla Abdulhamid Fattah</div>
            <div class="hero-author-affil">Lecturer at Salahaddin University-Erbil (SUE)</div>
            <div class="hero-author-affil">Director &amp; Founding Member, AIIC, UKH</div>
          </div>
          <div class="hero-actions-row">
            <a href="#table-of-contents" class="nav-btn nav-btn-primary">
              <i class="fa-solid fa-arrow-up"></i> Return to Table of Contents
            </a>
            <a href="../../index.html" class="nav-btn nav-btn-ghost">
              <i class="fa-solid fa-house"></i> Return to Course Home
            </a>
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- Floating Back to Top Button -->
  <a href="#table-of-contents" class="floating-top-btn" id="floating-top-btn" title="Back to Table of Contents" aria-label="Back to Table of Contents">
    <i class="fa-solid fa-arrow-up"></i>
  </a>

  <!-- Embedded Client JavaScript -->
  <script>
// Theme Management (Light / Dark)
function initTheme() {{
  const saved = localStorage.getItem('d2t-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(saved);
}}

function applyTheme(theme) {{
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('d2t-theme', theme);
  const icon = document.getElementById('theme-icon');
  if (icon) {{
    icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
  }}
}}

function toggleTheme() {{
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}}

initTheme();

// Reading Progress Indicator
window.addEventListener('scroll', () => {{
  const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
  const bar = document.getElementById('reading-progress-bar');
  if (bar) bar.style.width = scrolled + '%';

  // Floating Back to Top Button
  const topBtn = document.getElementById('floating-top-btn');
  if (topBtn) {{
    if (winScroll > 450) {{
      topBtn.classList.add('visible');
    }} else {{
      topBtn.classList.remove('visible');
    }}
  }}

  // Scrollspy
  updateActiveChapter();
}});

// Update active chapter on scroll
function updateActiveChapter() {{
  const chapters = document.querySelectorAll('.chapter-article');
  let currentId = '';
  const scrollPos = window.scrollY + 140;

  chapters.forEach(ch => {{
    if (ch.offsetTop <= scrollPos) {{
      currentId = ch.getAttribute('id');
    }}
  }});

  if (currentId) {{
    // Update sidebar active link
    document.querySelectorAll('.sidebar-toc-item').forEach(item => {{
      item.classList.remove('active');
      if (item.dataset.target === currentId) {{
        item.classList.add('active');
      }}
    }});

    // Update switcher select
    const select = document.getElementById('header-chapter-select');
    if (select && select.value !== currentId) {{
      select.value = currentId;
    }}
  }}
}}

// Chapter switch dropdown handler
function onChapterSelectChange(select) {{
  const targetId = select.value;
  if (targetId) {{
    const el = document.getElementById(targetId);
    if (el) {{
      el.scrollIntoView({{ behavior: 'smooth' }});
    }}
  }}
}}

// Sidebar Search Filter
function onSidebarSearch(input) {{
  const q = input.value.toLowerCase().trim();
  const items = document.querySelectorAll('.sidebar-toc-item');
  items.forEach(item => {{
    const text = item.textContent.toLowerCase();
    if (!q || text.includes(q)) {{
      item.style.display = 'block';
    }} else {{
      item.style.display = 'none';
    }}
  }});
}}

// Mobile sidebar toggle
function toggleSidebar() {{
  const sb = document.getElementById('book-sidebar');
  if (sb) {{
    sb.classList.toggle('open');
  }}
}}

// Copy Code Button
function copyCode(btn) {{
  const wrapper = btn.closest('.code-block-wrapper');
  if (!wrapper) return;
  const pre = wrapper.querySelector('pre');
  if (!pre) return;
  
  const text = pre.innerText;
  navigator.clipboard.writeText(text).then(() => {{
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-check"></i> <span>Copied!</span>';
    btn.style.background = '#059669';
    btn.style.borderColor = '#059669';
    btn.style.color = '#ffffff';
    setTimeout(() => {{
      btn.innerHTML = original;
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
    }}, 2000);
  }}).catch(() => {{
    // Fallback if clipboard API fails
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    btn.innerHTML = '<i class="fa-solid fa-check"></i> <span>Copied!</span>';
    setTimeout(() => {{ btn.innerHTML = original; }}, 2000);
  }});
}}

// Typeset MathJax if loaded
window.addEventListener('load', () => {{
  if (window.MathJax && window.MathJax.typesetPromise) {{
    window.MathJax.typesetPromise();
  }}
}});
  </script>
</body>
</html>
'''

if __name__ == '__main__':
    build_full_book()
