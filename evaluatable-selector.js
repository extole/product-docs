(function () {
  var TITLES_BY_COUNT = {
    3: [
      "Static Value",
      "Buildtime - Handlebars",
      "Buildtime - Javascript",
    ],
    5: [
      "Static Value",
      "Buildtime - Handlebars",
      "Buildtime - Javascript",
      "Runtime - Handlebars",
      "Runtime - Javascript",
    ],
  };

  var TYPE_CHIP_RE =
    /^(string|object|array|integer|boolean|number|Static Value)(\s*·\s*\w+)?$/i;

  function labelOf(tab) {
    var btn = tab.querySelector('[data-component-part="tab-button"]');
    return ((btn && btn.textContent) || tab.textContent || "")
      .trim()
      .replace(/\s+/g, " ");
  }

  function tabNodes(list) {
    var tabs = list.querySelectorAll('[data-component-part="tab"]');
    if (tabs.length) return tabs;
    return list.querySelectorAll('[role="tab"]');
  }

  function textOf(el) {
    return ((el && el.textContent) || "").trim().replace(/\s+/g, " ");
  }

  function isEvaluatableLabels(labels) {
    if (!labels || labels.length < 2 || labels.length > 8) return false;
    var joined = labels.join("\n");
    if (!/Static Value/i.test(joined)) return false;
    return /Handlebars|Javascript/i.test(joined);
  }

  function optionTexts(sel) {
    var out = [];
    for (var i = 0; i < sel.options.length; i++) {
      var opt = sel.options[i];
      if (opt.disabled && !opt.value) continue;
      var t = (opt.textContent || opt.label || "").trim().replace(/\s+/g, " ");
      if (!t) continue;
      if (/^select /i.test(t)) continue;
      out.push({ index: i, text: t });
    }
    return out;
  }

  function cleanTitle(text) {
    return text
      .replace(/\s*·\s*(object|string|integer|boolean|array|number)\s*$/i, "")
      .trim();
  }

  function isTypeLike(text) {
    return (
      TYPE_CHIP_RE.test(text) ||
      /^(Static Value|Buildtime - Handlebars|Buildtime - Javascript|Runtime - Handlebars|Runtime - Javascript)$/i.test(
        text
      )
    );
  }

  function isEvaluatableSelect(items) {
    if (!items || items.length < 2 || items.length > 8) return false;
    var texts = items.map(function (it) {
      return it.text;
    });
    var hasStatic = texts.some(function (t) {
      return /Static Value/i.test(t);
    });
    var hasExpr = texts.some(function (t) {
      return /Handlebars|Javascript|Buildtime|Runtime/i.test(t);
    });
    var stringCount = 0;
    var typeLikeCount = 0;
    for (var i = 0; i < texts.length; i++) {
      if (/^string(\s*·|$)/i.test(texts[i]) || texts[i] === "string") {
        stringCount++;
      }
      if (isTypeLike(texts[i])) typeLikeCount++;
    }
    if (hasStatic && (hasExpr || stringCount >= 2)) return true;
    if (
      typeLikeCount === texts.length &&
      (texts.length === 3 || texts.length === 5) &&
      (hasStatic || stringCount === texts.length || stringCount >= 2)
    ) {
      return true;
    }
    return false;
  }

  function titlesForSelect(items) {
    var cleaned = items.map(function (it) {
      return cleanTitle(it.text);
    });
    var hasExpr = cleaned.some(function (t) {
      return /Handlebars|Javascript|Buildtime|Runtime/i.test(t);
    });
    if (hasExpr) return cleaned;
    return TITLES_BY_COUNT[items.length] || cleaned;
  }

  function setSelectIndex(sel, index) {
    var opt = sel.options[index];
    if (!opt) return;
    var desc = Object.getOwnPropertyDescriptor(
      HTMLSelectElement.prototype,
      "value"
    );
    desc.set.call(sel, opt.value);
    sel.selectedIndex = index;
    sel.dispatchEvent(new Event("input", { bubbles: true }));
    sel.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function playgroundHash(tab) {
    if (!tab || !tab.id) return "";
    if (tab.id.indexOf("_R_") === 0) return "";
    return tab.id;
  }

  function clickTab(tab) {
    var btn = tab.querySelector('[data-component-part="tab-button"]') || tab;
    try {
      btn.focus();
    } catch (err) {}
    btn.dispatchEvent(
      new PointerEvent("pointerdown", { bubbles: true, cancelable: true })
    );
    btn.dispatchEvent(
      new PointerEvent("pointerup", { bubbles: true, cancelable: true })
    );
    btn.click();
    if (tab !== btn) tab.click();
  }

  function setNodeLabel(el, title) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    var last = null;
    var n;
    while ((n = walker.nextNode())) {
      if (n.nodeValue && n.nodeValue.trim()) last = n;
    }
    if (last) last.nodeValue = title;
    else el.appendChild(document.createTextNode(title));
  }

  function buildSelect(titles, selected, ariaLabel) {
    var ui = document.createElement("div");
    ui.className = "extole-eval-combo";
    ui.innerHTML =
      '<div class="extole-eval-combo-wrap">' +
      '<select class="extole-eval-combo-select"></select></div>';
    var sel = ui.querySelector("select");
    sel.setAttribute("aria-label", ariaLabel);
    for (var i = 0; i < titles.length; i++) {
      var opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = titles[i];
      sel.appendChild(opt);
    }
    sel.selectedIndex = selected;
    return { ui: ui, sel: sel };
  }

  function enhanceTabs(list) {
    if (list.dataset.extoleEval || list.dataset.extoleCombo) return;
    var tabs = tabNodes(list);
    if (tabs.length < 2) return;
    var inField = !!list.closest(".object-param-field");
    var inDialog = !!list.closest('[role="dialog"]');
    if (!inField && !inDialog) return;

    var labels = [];
    var selected = 0;
    for (var i = 0; i < tabs.length; i++) {
      labels.push(labelOf(tabs[i]));
      if (tabs[i].getAttribute("aria-selected") === "true") selected = i;
    }
    if (!isEvaluatableLabels(labels)) return;

    list.dataset.extoleEval = "1";
    var root = list.parentElement;
    if (!root) return;

    var built = buildSelect(labels, selected, "Evaluatable value");
    built.sel.addEventListener("change", function () {
      var idx = +built.sel.value;
      var tab = tabs[idx];
      if (!tab) return;
      clickTab(tab);
      var hash = playgroundHash(tab);
      if (inDialog && hash) {
        setTimeout(function () {
          if (location.hash !== "#" + hash) location.hash = hash;
        }, 400);
      }
    });

    new MutationObserver(function () {
      if (!list.isConnected) return;
      for (var j = 0; j < tabs.length; j++) {
        if (tabs[j].getAttribute("aria-selected") === "true") {
          if (built.sel.selectedIndex !== j) built.sel.selectedIndex = j;
          break;
        }
      }
    }).observe(list, {
      attributes: true,
      subtree: true,
      attributeFilter: ["aria-selected"],
    });

    root.insertBefore(built.ui, list);
  }

  function enhanceNativeSelect(sel) {
    if (sel.dataset.extoleEval) return;
    if (
      sel.closest(".extole-eval-combo") ||
      sel.closest(".extole-type-combo") ||
      sel.closest(".extole-eval-map")
    ) {
      return;
    }
    var items = optionTexts(sel);
    if (!isEvaluatableSelect(items)) return;

    sel.dataset.extoleEval = "1";
    var titles = titlesForSelect(items);
    for (var t = 0; t < items.length && t < titles.length; t++) {
      sel.options[items[t].index].textContent = titles[t];
    }
    var selected = 0;
    for (var i = 0; i < items.length; i++) {
      if (sel.selectedIndex === items[i].index) {
        selected = i;
        break;
      }
    }

    var built = buildSelect(titles, selected, "Evaluatable value");
    built.sel.addEventListener("change", function () {
      var idx = +built.sel.value;
      var item = items[idx];
      if (!item) return;
      setSelectIndex(sel, item.index);
    });

    sel.classList.add("extole-eval-native-hidden");
    sel.setAttribute("aria-hidden", "true");
    if (!sel.parentElement) return;
    sel.parentElement.insertBefore(built.ui, sel);
  }

  function typedNodes(list) {
    var nodes = [];
    for (var i = 0; i < list.length; i++) {
      if (isTypeLike(textOf(list[i]))) nodes.push(list[i]);
    }
    if (nodes.length >= 2 && nodes.length <= 8) return nodes;
    return [];
  }

  function collectMenuOptions(root) {
    if (!root || !root.querySelectorAll) return [];
    var roles = typedNodes(
      root.querySelectorAll('[role="option"], [role="menuitem"]')
    );
    if (roles.length) return roles;
    return typedNodes(root.querySelectorAll("button"));
  }

  function visibleTypeOptions() {
    var nodes = document.querySelectorAll("button, [role='option'], [role='menuitem']");
    var cands = [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.closest(".extole-eval-combo") || el.closest(".extole-eval-native-hidden")) {
        continue;
      }
      if (!isTypeLike(textOf(el))) continue;
      var r = el.getBoundingClientRect();
      if (r.height < 8 || r.width < 8 || r.y < 0) continue;
      cands.push({ el: el, x: Math.round(r.x), y: r.y });
    }
    if (cands.length < 2) return [];
    cands.sort(function (a, b) {
      return a.y - b.y;
    });
    var best = [];
    for (var s = 0; s < cands.length; s++) {
      var run = [cands[s]];
      for (var j = s + 1; j < cands.length; j++) {
        if (Math.abs(cands[j].x - cands[s].x) > 40) continue;
        if (cands[j].y - run[run.length - 1].y > 48) break;
        run.push(cands[j]);
      }
      if (run.length > best.length) best = run;
    }
    if (best.length < 2 || best.length > 8) return [];
    return best.map(function (c) {
      return c.el;
    });
  }

  function menuItems(nodes) {
    var items = [];
    for (var i = 0; i < nodes.length; i++) {
      items.push({ index: i, text: textOf(nodes[i]), node: nodes[i] });
    }
    return items;
  }

  function selectedMenuIndex(nodes) {
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.getAttribute("aria-selected") === "true") return i;
      if (el.getAttribute("data-headlessui-state") &&
          /selected/.test(el.getAttribute("data-headlessui-state"))) {
        return i;
      }
      if (el.querySelector("svg") && /Static Value|string|object|Handlebars/.test(textOf(el))) {
        var cls = (el.className || "").toString();
        if (/bg-|ring-|checked|selected/.test(cls)) return i;
      }
    }
    return 0;
  }

  function expandedChip() {
    var dialog = document.querySelector('[role="dialog"]');
    if (!dialog) return null;
    var buttons = dialog.querySelectorAll("button[aria-expanded='true']");
    for (var i = 0; i < buttons.length; i++) {
      if (isTypeChip(buttons[i])) return buttons[i];
    }
    return null;
  }

  function isTypeChip(btn) {
    if (!btn || btn.closest(".extole-eval-combo") || btn.closest(".extole-type-combo")) {
      return false;
    }
    if (!btn.closest('[role="dialog"]')) return false;
    if (!TYPE_CHIP_RE.test(textOf(btn))) return false;
    var wrap = btn.parentElement;
    if (!wrap) return false;
    var cls = (wrap.className || "").toString();
    return /\brelative\b/.test(cls) && /\bflex\b/.test(cls);
  }

  function polishChip(chip) {
    if (!chip) return;
    var t = textOf(chip);
    var stored = chip.dataset.extoleEvalTitles;
    var idx = chip.dataset.extoleEvalIndex;
    if (stored && idx != null) {
      try {
        var titles = JSON.parse(stored);
        var title = titles[+idx];
        if (title && t !== title) setNodeLabel(chip, title);
        return;
      } catch (err) {}
    }
    if (/^Static Value ·/i.test(t)) setNodeLabel(chip, cleanTitle(t));
  }

  function relabelMenu(root, allowVisibleFallback) {
    var nodes = collectMenuOptions(root);
    if (nodes.length < 2 && allowVisibleFallback) nodes = visibleTypeOptions();
    var items = menuItems(nodes);
    if (!isEvaluatableSelect(items)) return false;
    var titles = titlesForSelect(items);
    for (var i = 0; i < nodes.length && i < titles.length; i++) {
      setNodeLabel(nodes[i], titles[i]);
    }
    var selected = selectedMenuIndex(nodes);
    var chip = expandedChip();
    if (chip) {
      chip.dataset.extoleEvalTitles = JSON.stringify(titles);
      chip.dataset.extoleEvalIndex = String(selected);
      setNodeLabel(chip, titles[selected] || titles[0]);
    }
    return true;
  }

  function enhanceEvalMenus(base) {
    if (!base || !base.querySelectorAll) return;
    if (base.matches && (base.matches('[role="listbox"]') || base.matches('[role="menu"]'))) {
      relabelMenu(base);
    }
    var menus = base.querySelectorAll('[role="listbox"], [role="menu"]');
    for (var i = 0; i < menus.length; i++) relabelMenu(menus[i]);
    if (base !== document && base !== document.documentElement && base !== document.body) {
      relabelMenu(base);
    }
  }

  function enhanceChips(base) {
    var scope = base && base.querySelectorAll ? base : document;
    var dialog =
      (scope.closest && scope.closest('[role="dialog"]')) ||
      (scope.querySelector && scope.querySelector('[role="dialog"]')) ||
      document.querySelector('[role="dialog"]');
    if (!dialog) return;
    var buttons = dialog.querySelectorAll("button");
    for (var i = 0; i < buttons.length; i++) {
      if (isTypeChip(buttons[i])) polishChip(buttons[i]);
    }
  }

  function scan(root) {
    var base = root && root.nodeType === 1 ? root : document;
    var lists = [];
    if (base.matches && base.matches('[data-component-part="tabs-list"]')) {
      lists.push(base);
    }
    if (base.querySelectorAll) {
      var found = base.querySelectorAll('[data-component-part="tabs-list"]');
      for (var i = 0; i < found.length; i++) lists.push(found[i]);
    }
    for (var j = 0; j < lists.length; j++) enhanceTabs(lists[j]);

    if (!base.querySelectorAll) return;
    var selects = base.querySelectorAll("select");
    if (base.matches && base.matches("select")) enhanceNativeSelect(base);
    for (var k = 0; k < selects.length; k++) enhanceNativeSelect(selects[k]);

    enhanceEvalMenus(base);
    enhanceChips(base);
  }

  var lastTypeChip = null;

  scan(document);
  document.addEventListener(
    "click",
    function (e) {
      if (document.documentElement.getAttribute("data-extole-driving")) return;
      if (e.target && e.target.closest && e.target.closest(".extole-eval-map")) {
        return;
      }
      var item =
        e.target && e.target.closest && e.target.closest('[role="menuitem"]');
      if (item && lastTypeChip) {
        var menu = item.closest('[role="menu"]') || item.parentElement;
        var nodes = collectMenuOptions(menu);
        var items = menuItems(nodes);
        if (isEvaluatableSelect(items)) {
          var idx = nodes.indexOf(item);
          if (idx < 0) {
            for (var n = 0; n < nodes.length; n++) {
              if (nodes[n].contains(item) || item.contains(nodes[n])) {
                idx = n;
                break;
              }
            }
          }
          if (idx >= 0) {
            var titles = titlesForSelect(items);
            lastTypeChip.dataset.extoleEvalTitles = JSON.stringify(titles);
            lastTypeChip.dataset.extoleEvalIndex = String(idx);
            var chip = lastTypeChip;
            var apply = function () {
              setNodeLabel(chip, titles[idx]);
            };
            apply();
            setTimeout(apply, 0);
            setTimeout(apply, 80);
          }
        }
      }
      var btn = e.target && e.target.closest && e.target.closest("button");
      if (!btn || !isTypeChip(btn)) return;
      lastTypeChip = btn;
      var relabel = function () {
        enhanceEvalMenus(document.body);
        relabelMenu(document.body, true);
      };
      setTimeout(relabel, 0);
      setTimeout(relabel, 80);
    },
    true
  );
  new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i++) {
      var nodes = mutations[i].addedNodes;
      for (var j = 0; j < nodes.length; j++) {
        if (nodes[j].nodeType === 1) scan(nodes[j]);
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
