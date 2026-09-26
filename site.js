/* Native navigation and clipboard feedback shared by every locale and season. */
(() => {
  'use strict';
  window.lucide?.createIcons();
  const menus = [...document.querySelectorAll('.nav-picker')];
  menus.forEach((menu) => {
    menu.addEventListener('toggle', () => {
      if (menu.open) menus.forEach((other) => { if (other !== menu) other.open = false; });
    });
    menu.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.open) {
        event.preventDefault();
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
    menu.addEventListener('focusout', (event) => {
      if (!menu.contains(event.relatedTarget)) menu.open = false;
    });
  });
  document.addEventListener('click', (event) => menus.forEach((menu) => {
    if (!menu.contains(event.target)) menu.open = false;
  }));
  // Follow the existing calculator's selection without changing its formula.
  const stakeButtons = [...document.querySelectorAll('#s1StakeToggle button')];
  stakeButtons.forEach((button) => button.addEventListener('click', () => {
    stakeButtons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
  }));
  const lang = document.documentElement.lang.split('-')[0];
  const [done, error] = ({
    zh: ['已复制', '复制失败，请选中文本手动复制。'],
    en: ['Copied', 'Copy failed. Select the text and copy it manually.'],
    ja: ['コピー済み', 'コピーできませんでした。テキストを選択してコピーしてください。'],
    ko: ['복사됨', '복사하지 못했습니다. 텍스트를 선택하여 직접 복사해 주세요.']
  })[lang] || ['Copied', 'Copy failed. Select and copy the text manually.'];
  const buttons = document.querySelectorAll('.copy-id,.addr-btn,.cb-copy');
  if (!buttons.length) return;
  let feedback = document.getElementById('copy-feedback');
  if (!feedback) {
    feedback = document.createElement('p');
    feedback.id = 'copy-feedback';
    feedback.className = 'sr-only';
    feedback.setAttribute('role', 'status');
    feedback.setAttribute('aria-atomic', 'true');
    document.body.append(feedback);
  }
  function selectionCopy(text) {
    const field = document.createElement('textarea');
    const focused = document.activeElement;
    field.value = text;
    field.readOnly = true;
    field.style.cssText = 'position:fixed;top:0;left:-9999px;font-size:16px;';
    document.body.append(field);
    try {
      field.select();
      if (!document.execCommand('copy')) throw new Error('Copy unavailable');
    } finally {
      field.remove();
      focused?.focus({preventScroll:true});
    }
  }
  buttons.forEach((button) => {
    const textElement = button.querySelector('code,.addr') || button.closest('.codeblock')?.querySelector('code');
    if (!textElement) return;
    const text = textElement.textContent.trim();
    const cell = button.closest('.model-id-cell');
    const label = button.querySelector('.cb-lbl');
    const original = label?.textContent;
    let pending = false;
    let timer;
    button.disabled = false;
    button.title = button.getAttribute('aria-label') || text;
    button.addEventListener('click', async () => {
      if (pending) return;
      pending = true;
      clearTimeout(timer);
      feedback.textContent = '';
      feedback.classList.remove('copy-error');
      button.classList.remove('done');
      cell?.classList.remove('is-copied');
      button.setAttribute('aria-busy', 'true');
      try {
        try {
          if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(text);
        } catch {
          selectionCopy(text);
        }
        button.classList.add('done');
        cell?.classList.add('is-copied');
        if (label) label.textContent = done;
        feedback.textContent = `${done}: ${text}`;
      } catch {
        feedback.textContent = error;
        feedback.classList.add('copy-error');
      } finally {
        pending = false;
        button.removeAttribute('aria-busy');
        timer = setTimeout(() => {
          button.classList.remove('done');
          cell?.classList.remove('is-copied');
          if (label) label.textContent = original;
        }, 2200);
      }
    });
  });
})();
