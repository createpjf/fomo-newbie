/* Shared behavior for all four S3 locales. Charts show scores, never payouts. */
(() => {
  'use strict';
  if (window.lucide) window.lucide.createIcons();
  const copy = JSON.parse(document.getElementById('s3-copy').textContent);
  const byId = (id) => document.getElementById(id);
  const format = (value, digits = 3) => new Intl.NumberFormat(copy.lang, {
    minimumFractionDigits: digits, maximumFractionDigits: digits
  }).format(value);
  const announcement = byId('lab-announcement');
  function announce(message) { announcement.textContent = message; }

  // Copy the complete MT address or API ID; model names remain reference text.
  function copyWithSelection(text) {
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
      focused?.focus({ preventScroll: true });
    }
  }
  const copyFeedback = byId('copy-feedback');
  document.querySelectorAll('.copy-id').forEach((button) => {
    const cell = button.closest('.model-id-cell');
    const id = cell.querySelector('code').textContent;
    let resetTimer;
    let pending = false;
    button.hidden = false;
    button.disabled = false;
    button.title = button.getAttribute('aria-label');
    button.addEventListener('click', async () => {
      if (pending) return;
      pending = true;
      clearTimeout(resetTimer);
      cell.classList.remove('is-copied');
      copyFeedback.textContent = '';
      button.setAttribute('aria-busy', 'true');
      try {
        try {
          if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(id);
        } catch {
          copyWithSelection(id);
        }
        cell.classList.add('is-copied');
        const success = button.dataset.copyKind === 'address' ? copy.modelCopy.addressSuccess : copy.modelCopy.success;
        copyFeedback.textContent = success.replace('{id}', id);
        resetTimer = setTimeout(() => cell.classList.remove('is-copied'), 2200);
      } catch {
        copyFeedback.textContent = copy.modelCopy.error;
      } finally {
        pending = false;
        button.removeAttribute('aria-busy');
      }
    });
  });

  // Native disclosure navigation keeps hidden links out of the tab order.
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

  const tabs = [...document.querySelectorAll('[role="tab"]')];
  const panels = [...document.querySelectorAll('[role="tabpanel"]')];
  function selectTab(tab, focus = false) {
    announcement.textContent = '';
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    panels.forEach((panel) => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        selectTab(tabs[next], true);
      }
    });
  });
  selectTab(tabs[0]);
  document.querySelector('.lab-tabs').hidden = false;
  document.querySelectorAll('.lab [disabled]').forEach((control) => { control.disabled = false; });

  let eligibility = [true, false, false];
  let scene = null;
  function setEligibility(index) {
    eligibility = index === 0 ? [true, false, false] : index === 1 ? [true, true, true] : [false, false, false];
    document.querySelectorAll('[data-pool]').forEach((pool, i) => {
      pool.dataset.eligible = String(eligibility[i]);
      pool.querySelector('[data-status-text]').textContent = eligibility[i] ? copy.yes : copy.no;
      pool.querySelector('[data-status-icon]').textContent = eligibility[i] ? '✓' : '−';
    });
    document.querySelectorAll('.pool-fallback span').forEach((pool, i) => { pool.dataset.lit = String(eligibility[i]); });
    byId('eligibility-result').textContent = copy.eligibilityText[index];
    if (scene) scene.setEligibility(eligibility);
  }
  document.querySelectorAll('input[name="participation"]').forEach((input) => {
    input.addEventListener('change', () => {
      setEligibility(Number(input.value));
      announce(copy.eligibilityText[Number(input.value)]);
    });
  });

  // Coordinates are normalized so the plot stays legible at narrow widths.
  const px = (share) => 8 + 584 * share;
  const py = (value, min, max) => 190 - 180 * (value - min) / (max - min);
  function plot(svg, fn, min, max, series = 'primary') {
    const d = Array.from({ length: 121 }, (_, i) => {
      const x = i / 120;
      return `${i ? 'L' : 'M'}${px(x).toFixed(2)} ${py(fn(x), min, max).toFixed(2)}`;
    }).join(' ');
    svg.querySelector(`[data-curve="${series}"]`).setAttribute('d', d);
  }
  function point(svg, share, value, min, max, series = 'primary') {
    const dot = svg.querySelector(`[data-point="${series}"]`);
    dot.setAttribute('cx', px(share));
    dot.setAttribute('cy', py(value, min, max));
    svg.querySelector('[data-guide]').setAttribute('d', `M${px(share)} 10 V190`);
  }
  function fillRange(input) { input.style.setProperty('--fill', `${input.value}%`); }
  const stake = byId('stake-range');
  const alpha = byId('alpha');
  const stakeChart = byId('stake-chart');
  function scoreStatus(prefix) {
    return copy.scoreStatus.replace('{global}', byId(`${prefix}-global`).textContent)
      .replace('{incentive}', byId(`${prefix}-incentive`).textContent);
  }
  function updateStake() {
    const s = Number(stake.value) / 100;
    const a = Number(alpha.value);
    // Fixed example: usage share = 0.5 and gmFLOCK multiplier = 1.
    const globalScore = (share) => 0.5 * (a + (1 - a) * Math.sqrt(share));
    const incentiveScore = (share) => 0.5 * share;
    byId('stake-value').textContent = `${stake.value}%`;
    byId('stake-global').textContent = format(globalScore(s));
    byId('stake-incentive').textContent = format(incentiveScore(s));
    byId('stake-result').textContent = copy.stakeNotes[s === 0 ? 0 : 1];
    plot(stakeChart, globalScore, 0, 0.5);
    plot(stakeChart, incentiveScore, 0, 0.5, 'secondary');
    point(stakeChart, s, globalScore(s), 0, 0.5);
    point(stakeChart, s, incentiveScore(s), 0, 0.5, 'secondary');
    fillRange(stake);
  }
  [stake, alpha].forEach((input) => {
    input.addEventListener('input', updateStake);
    input.addEventListener('change', () => {
      updateStake();
      announce(scoreStatus('stake'));
    });
  });

  const gm = byId('gm-range');
  const gmUsed = byId('gm-used');
  const gmStaked = byId('gm-staked');
  const gmChart = byId('gm-chart');
  // Illustration only. The protocol's balance normalization is not published
  // precisely enough to infer a wallet balance → multiplier conversion.
  const illustrativeMultiplier = (position) => 1 + Math.log1p(9 * position) / Math.log(10);
  function updateGm() {
    const position = Number(gm.value) / 100;
    const multiplier = illustrativeMultiplier(position);
    const usage = gmUsed.checked ? 0.5 : 0;
    const share = gmStaked.checked ? 0.1 : 0;
    const level = copy.gmScale[position < 0.2 ? 0 : position < 0.7 ? 1 : 2];
    byId('gm-level').textContent = level;
    gm.setAttribute('aria-valuetext', level);
    byId('gm-multiplier').textContent = `${format(multiplier, 2)}×`;
    byId('gm-global').textContent = format(usage * (0.9 + 0.1 * Math.sqrt(share)) * multiplier);
    byId('gm-incentive').textContent = format(usage * share * multiplier);
    byId('gm-result').textContent = copy.gmNotes[!gmUsed.checked ? 2 : gmStaked.checked ? 1 : 0];
    plot(gmChart, illustrativeMultiplier, 1, 2);
    point(gmChart, position, multiplier, 1, 2);
    fillRange(gm);
  }
  [gm, gmUsed, gmStaked].forEach((input) => {
    input.addEventListener('input', updateGm);
    input.addEventListener('change', () => {
      updateGm();
      announce(`${copy.boostStatus.replace('{boost}', byId('gm-multiplier').textContent)} ${scoreStatus('gm')}`);
    });
  });
  document.querySelectorAll('.scores output, .range-heading output, #gm-multiplier').forEach((output) => output.setAttribute('aria-live', 'off'));
  document.querySelector('#stake-chart').parentElement.parentElement.setAttribute('aria-describedby', 'stake-value stake-global stake-incentive stake-chart-caption');
  document.querySelector('#gm-chart').parentElement.parentElement.setAttribute('aria-describedby', 'gm-multiplier gm-chart-caption');
  updateStake();
  updateGm();

  // Keep markers circular when the SVG stretches with its container.
  const chartResize = new ResizeObserver((entries) => entries.forEach(({ target, contentRect }) => {
    if (!contentRect.width || !contentRect.height) return;
    target.querySelectorAll('.chart-point').forEach((marker) => {
      marker.setAttribute('rx', 5 * 600 / contentRect.width);
      marker.setAttribute('ry', 5 * 200 / contentRect.height);
    });
  }));
  [stakeChart, gmChart].forEach((svg) => chartResize.observe(svg));

  // Three.js is a progressive enhancement: only fetch it when the scene is
  // visible. Text, scores, SVG charts and controls never depend on WebGL.
  const container = byId('pool-scene');
  let requested = false;
  const loader = new IntersectionObserver(async (entries) => {
    if (!entries.some((entry) => entry.isIntersecting) || requested) return;
    requested = true;
    loader.disconnect();
    try {
      const { createPoolScene } = await import('/season-3-scene.js?v=20260923-brand');
      scene = createPoolScene(container, eligibility);
    } catch (error) {
      // The local SVG/CSS and text alternatives remain fully usable.
      container.dataset.ready = 'false';
      console.warn('S3: keeping the static reward-pool illustration.', error.message);
    }
  });
  loader.observe(container);
})();
