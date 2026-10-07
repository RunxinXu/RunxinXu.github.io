---
layout: academic
title: Runxin Xu
meta-title: Runxin Xu (许润昕)
meta-description: >-
  Runxin Xu (许润昕) is a researcher at DeepSeek, working on large language
  models and reasoning on the path to AGI.
share-img: /img/profile.jpg
page-nav:
  - name: About
    url: "#about"
  - name: Publications
    url: "#publications"
  - name: Experience
    url: "#experience"
  - name: Education
    url: "#education"
    secondary: true
  - name: Honours
    url: "#honours"
    secondary: true
---

<header class="wrap profile">
  <div class="profile-text">
    <h1 class="name">Runxin Xu<span class="name-cn">许润昕</span></h1>
    <p class="role">
      Researcher at <a href="https://www.deepseek.com/">DeepSeek</a><br />
      Large language models &middot; Reasoning &middot; Post-training
    </p>
    <p class="contact">runxinxu <span class="obf">AT</span> gmail <span class="obf">DOT</span> com</p>
    <ul class="linkrow">
      <li><a href="https://scholar.google.com/citations?hl=en&amp;user=dRp21l4AAAAJ">Google Scholar</a></li>
      <li><a href="https://x.com/pigjunebaba">Twitter</a></li>
    </ul>
  </div>
  <figure class="profile-figure">
    <img src="{{ '/img/profile.jpg' | prepend: site.baseurl }}" alt="Portrait of Runxin Xu" width="800" height="1000" />
  </figure>
</header>

<section class="wrap section prose" id="about" markdown="1">

<h2 class="section-title">About</h2>

I am a researcher at [DeepSeek](https://www.deepseek.com/), where I have been
deeply involved in the DeepSeek model series —
[V1](https://arxiv.org/abs/2401.02954) /
[V2](https://arxiv.org/abs/2405.04434) /
[V3](https://arxiv.org/abs/2412.19437) / V3.1 /
[V3.2](https://arxiv.org/abs/2512.02556) /
[V4](https://arxiv.org/abs/2606.19348) /
[V4.1](https://arxiv.org/abs/2609.19969), the
[R1](https://www.nature.com/articles/s41586-025-09422-z) reasoning models, and
the [Math](https://arxiv.org/abs/2402.03300),
[Coder](https://arxiv.org/abs/2406.11931), and
[MoE](https://arxiv.org/abs/2401.06066) lines.

My long-term research interest lies in AGI: pushing the boundaries of machine
intelligence with methods that are simple, scalable, and effective. I keep
reminding myself to re-read [The Bitter
Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html).

Before DeepSeek, I was a master's student at the [Institute of Computational
Linguistics](https://icl.pku.edu.cn/), [School of EECS, Peking
University](https://eecs.pku.edu.cn/), advised by [Baobao
Chang](https://icl.pku.edu.cn/cy/cbb/index.htm) and [Zhifang
Sui](https://icl.pku.edu.cn/cy/szf/ywb/index.htm). Prior to that I received my
bachelor's degree from [Shanghai Jiao Tong University](https://www.sjtu.edu.cn).

</section>

<section class="wrap section" id="publications">
  <h2 class="section-title">Selected Publications</h2>
  {%- assign has_figures = false -%}
  {%- for pub in site.data.publications -%}
    {%- if pub.figure -%}{%- assign has_figures = true -%}{%- endif -%}
  {%- endfor -%}
  <ol class="pub-list{% if has_figures %} has-figures{% endif %}">
    {%- for pub in site.data.publications %}
    <li class="pub">
      <div class="pub-venue">{{ pub.venue }}</div>
      <div>
        <div class="pub-title">
          {%- if pub.links and pub.links.first -%}
          <a href="{{ pub.links.first.url }}">{{ pub.title }}</a>
          {%- else -%}
          {{ pub.title }}
          {%- endif -%}
        </div>
        <p class="pub-authors">{{ pub.authors }}</p>
        {%- if pub.note %}
        <span class="pub-flag">{{ pub.note }}</span>
        {%- endif %}
        {%- if pub.links %}
        <p class="pub-links">
          {%- for link in pub.links -%}
          {%- unless forloop.first %}<span class="pub-sep">·</span>{% endunless -%}
          <a href="{{ link.url }}">{{ link.name }}</a>
          {%- endfor -%}
        </p>
        {%- endif %}
      </div>
      {%- if pub.figure %}
      <figure class="pub-fig">
        {%- if pub.links and pub.links.first %}<a href="{{ pub.links.first.url }}">{% endif -%}
        <img src="{{ pub.figure | prepend: site.baseurl }}" alt="{{ pub.alt | default: pub.title }}" loading="lazy" />
        {%- if pub.links and pub.links.first %}</a>{% endif -%}
      </figure>
      {%- endif %}
    </li>
    {%- endfor %}
  </ol>
  <p class="section-note">
    A full list is available on
    <a href="https://scholar.google.com/citations?hl=en&amp;user=dRp21l4AAAAJ">Google Scholar</a>.
  </p>
</section>

<section class="wrap section" id="experience">
  <h2 class="section-title">Experience</h2>
  <ol class="cv-list">
    <li class="cv-item">
      <div class="cv-org"><a href="https://www.deepseek.com/">DeepSeek</a></div>
      <div class="cv-date">Aug 2023 — Present</div>
      <p class="cv-detail">Researcher. Large language models on the path to AGI.</p>
    </li>
    <li class="cv-item">
      <div class="cv-org"><a href="https://www.metabit-trading.com/home">Metabit Trading</a></div>
      <div class="cv-date">Nov 2022 — Mar 2023</div>
      <p class="cv-detail">Quantitative researcher. Advised by Bowei Ma and An Ju.</p>
    </li>
    <li class="cv-item">
      <div class="cv-org">ByteDance Search</div>
      <div class="cv-date">Jan 2022 — Sep 2022</div>
      <p class="cv-detail">Search engine for Douyin Mall. Advised by Shian Chen, Zhe Chen, and <a href="https://scholar.google.com/citations?user=5oUR6xIAAAAJ&amp;hl=en">Pengcheng Yang</a>.</p>
    </li>
    <li class="cv-item">
      <div class="cv-org"><a href="https://damo.alibaba.com/">Alibaba DAMO Academy</a></div>
      <div class="cv-date">Mar 2021 — Dec 2021</div>
      <p class="cv-detail">Effective and efficient language models. Advised by <a href="https://www.linkedin.com/in/songfang">Songfang Huang</a> and <a href="https://luofuli.github.io">Fuli Luo</a>.</p>
    </li>
    <li class="cv-item">
      <div class="cv-org"><a href="https://ailab.bytedance.com">ByteDance AI Lab</a></div>
      <div class="cv-date">Nov 2019 — Jan 2021</div>
      <p class="cv-detail">Information extraction and machine translation. Advised by <a href="https://lileicc.github.io">Lei Li</a>, <a href="https://mingxuan.github.io">Mingxuan Wang</a>, and Jun Cao.</p>
    </li>
    <li class="cv-item">
      <div class="cv-org">Microsoft C+AI</div>
      <div class="cv-date">Jul 2019 — Oct 2019</div>
      <p class="cv-detail">Built the <a href="https://github.com/microsoft/vscode-maven/graphs/contributors">vscode-maven</a> extension. Advised by <a href="https://github.com/akaroml">Rome Li</a>, <a href="https://github.com/testforstephen">Jinbo Wang</a>, and <a href="https://github.com/Eskibear">Yan Zhang</a>.</p>
    </li>
  </ol>
</section>

<section class="wrap section" id="education">
  <h2 class="section-title">Education</h2>
  <ol class="cv-list">
    <li class="cv-item">
      <div class="cv-org"><a href="https://www.pku.edu.cn/">Peking University</a></div>
      <div class="cv-date">Sep 2020 — Jun 2023</div>
      <p class="cv-detail">M.S., <a href="https://eecs.pku.edu.cn/">School of EECS</a>. Advised by <a href="https://icl.pku.edu.cn/cy/cbb/index.htm">Baobao Chang</a> and <a href="https://icl.pku.edu.cn/cy/szf/ywb/index.htm">Zhifang Sui</a> at the <a href="https://icl.pku.edu.cn/">Institute of Computational Linguistics</a>.</p>
    </li>
    <li class="cv-item">
      <div class="cv-org"><a href="https://www.sjtu.edu.cn/">Shanghai Jiao Tong University</a></div>
      <div class="cv-date">Sep 2016 — Jun 2020</div>
      <p class="cv-detail">B.Eng., <a href="https://infosec.sjtu.edu.cn/">School of Cyber Science and Engineering</a>.</p>
    </li>
  </ol>
</section>

<section class="wrap section" id="honours">
  <h2 class="section-title">Honours &amp; Awards</h2>
  <ul class="award-list">
    <li><span>National Scholarship</span><span class="award-year">2018, 2019, 2021</span></li>
    <li><span><a href="https://cs.pku.edu.cn/info/1428/3643.htm">Huatai Securities Technology Scholarship</a> (华泰证券科技奖学金)</span><span class="award-year">2022</span></li>
    <li><span>Outstanding Graduate, Shanghai Jiao Tong University</span><span class="award-year">2020</span></li>
    <li><span>A-class Scholarship, Shanghai Jiao Tong University (1st in major)</span><span class="award-year">2018</span></li>
    <li><span>B-class Scholarship, Shanghai Jiao Tong University</span><span class="award-year">2017, 2019</span></li>
    <li><span><a href="http://www.tangfoundation.org.cn/">Cyrus Tang Scholarship</a> (唐仲英德育奖学金)</span><span class="award-year">2018, 2019</span></li>
    <li><span><a href="https://jjh.jinlongyu.cn/project/index.aspx?NC=105003002">Arawana Scholarship</a> (金龙鱼奖学金)</span><span class="award-year">2017</span></li>
    <li><span><a href="https://www.comap.com/undergraduate/contests/">Meritorious Winner, Interdisciplinary Contest in Modeling</a> (top 8% of 11,262 teams)</span><span class="award-year">2018</span></li>
  </ul>
</section>
