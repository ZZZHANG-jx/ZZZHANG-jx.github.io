---
layout: home
permalink: /
title: ""
redirect_from:
  - /about/
  - /about.html
---

<section class="profile" id="about" aria-label="About Jiaxin Zhang">
  <div class="profile-bio">
    <h1 class="profile-name">Jiaxin Zhang</h1>
    <p>
      I am a researcher working on <strong>document image analysis</strong>,
      <strong>optical character recognition (OCR)</strong>, and
      <strong>multimodal document understanding</strong>. My goal is to make machines read
      the way people do — handling a document that is photographed at an angle, folded,
      shadowed, or written in an unfamiliar layout, and turning it into structured,
      machine-readable content.
    </p>
    <p>
      My recent work spans document image restoration and dewarping
      (<a href="https://openaccess.thecvf.com/content/CVPR2024/html/Zhang_DocRes_A_Generalist_Model_Toward_Unifying_Document_Image_Restoration_Tasks_CVPR_2024_paper.html">DocRes</a>,
      CVPR 2024;
      <a href="https://doi.org/10.1145/3503161.3548214">Marior</a>), unified pixel-level OCR
      (<a href="https://proceedings.mlr.press/v235/peng24e.html">UPOCR</a>, ICML 2024), large
      multimodal models for visual document understanding
      (<a href="https://ojs.aaai.org/index.php/AAAI/article/view/33076">DocKylin</a>, AAAI 2025),
      and datasets and benchmarks that push the field forward
      (<a href="https://openaccess.thecvf.com/content/CVPR2023/html/Cheng_M6Doc_A_Large-Scale_Multi-Format_Multi-Type_Multi-Layout_Multi-Language_Multi-Annotation_Category_Dataset_CVPR_2023_paper.html">M6Doc</a>,
      CVPR 2023; <a href="https://arxiv.org/abs/2507.15085">OCRGenBench</a>). Several of these
      are widely used as standard baselines for document AI.
    </p>
    <p>
      I did my research training at South China University of Technology, and I currently work
      as a researcher in industry.
    </p>

    <p class="profile-links">
      <span>eejxzhang@gmail.com</span>
      <span class="sep">/</span>
      <a href="https://scholar.google.com/citations?user=pXh33zUAAAAJ&amp;hl=zh-CN">Google Scholar</a>
      <span class="sep">/</span>
      <a href="https://github.com/ZZZHANG-jx">GitHub</a>
    </p>
  </div>
  <figure class="profile-photo">
    <img src="../images/me.jpg" alt="Portrait of Jiaxin Zhang" width="208" height="208" decoding="async">
  </figure>
</section>

<hr>

<section id="news">
  <h2>News</h2>
  <ul class="news">
    <li><span class="news-date">2026</span><strong>Q-DRFormer</strong> accepted to <em>ACM Transactions on Graphics</em>.</li>
    <li><span class="news-date">2026</span>Three papers accepted to <em>Pattern Recognition</em>: DocAligner, AutoScaler, and Text Prior-Guided Cell Alignment.</li>
  </ul>
</section>

<hr>

<section id="papers">
  <h2>Papers</h2>
  {% include papers.html %}
</section>

<hr>

<section id="service">
  <h2>Academic Service</h2>
  {% include service.html %}
</section>
