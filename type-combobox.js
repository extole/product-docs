(function () {
  var pending = new WeakMap();

  function labelOf(tab) {
    var btn = tab.querySelector('[data-component-part="tab-button"]');
    return ((btn && btn.textContent) || tab.textContent || "")
      .trim()
      .replace(/\s+/g, " ");
  }

  function shouldEnhance(list, tabCount) {
    if (list.closest(".object-param-field")) return tabCount >= 2;
    if (list.closest('[role="dialog"]')) return tabCount >= 8;
    return false;
  }

  function tabNodes(list) {
    var tabs = list.querySelectorAll('[data-component-part="tab"]');
    if (tabs.length) return tabs;
    return list.querySelectorAll('[role="tab"]');
  }

  function inDialog(el) {
    return !!(el && el.closest && el.closest('[role="dialog"]'));
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

  function selectedIndex(tabs) {
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].getAttribute("aria-selected") === "true") return i;
    }
    return 0;
  }

  function indexFromHash(tabs) {
    var hash = (location.hash || "").replace(/^#/, "");
    if (!hash) return -1;
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].id === hash) return i;
    }
    return -1;
  }

  function syncSelect(select, tabs) {
    var fromHash = indexFromHash(tabs);
    var idx = fromHash >= 0 ? fromHash : selectedIndex(tabs);
    if (String(idx) !== select.value) select.value = String(idx);
  }

  function activate(list, tabs, idx, dialogScoped) {
    var tab = tabs[idx];
    if (!tab) return;
    var hash = playgroundHash(tab);
    if (dialogScoped && hash) {
      if (location.hash === "#" + hash) {
        location.hash = "";
        location.hash = hash;
      } else {
        location.hash = hash;
      }
      return;
    }
    clickTab(tab);
  }

  function enhance(list) {
    if (list.dataset.extoleTypeSelect) return;
    var tabs = tabNodes(list);
    if (!shouldEnhance(list, tabs.length)) return;
    list.dataset.extoleTypeSelect = "1";

    var root = list.parentElement;
    if (!root) return;
    var dialogScoped = inDialog(list);

    var selectId =
      "extole-type-select-" + Math.random().toString(36).slice(2, 9);
    var ui = document.createElement("div");
    ui.className = "extole-type-select";
    ui.innerHTML =
      "<label>Type</label><select aria-label=\"Schema type\"></select>";

    var select = ui.querySelector("select");
    var labelEl = ui.querySelector("label");
    select.id = selectId;
    labelEl.setAttribute("for", selectId);

    for (var i = 0; i < tabs.length; i++) {
      var opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = labelOf(tabs[i]);
      select.appendChild(opt);
    }
    syncSelect(select, tabs);

    select.addEventListener("change", function () {
      activate(list, tabs, +select.value, dialogScoped);
    });

    if (dialogScoped) {
      window.addEventListener("hashchange", function () {
        if (!list.isConnected) return;
        syncSelect(select, tabs);
      });
    }

    new MutationObserver(function () {
      if (!list.isConnected) return;
      syncSelect(select, tabs);
    }).observe(list, {
      attributes: true,
      subtree: true,
      attributeFilter: ["aria-selected"],
    });

    root.insertBefore(ui, list);
  }

  function queueEnhance(list) {
    if (!list || list.dataset.extoleTypeSelect) return;
    var prev = pending.get(list);
    if (prev) clearTimeout(prev);
    pending.set(
      list,
      setTimeout(function () {
        pending.delete(list);
        enhance(list);
      }, 50)
    );
  }

  function scan(root) {
    var base = root && root.nodeType === 1 ? root : document;
    if (base.closest) {
      var near = base.closest('[data-component-part="tabs-list"]');
      if (near) queueEnhance(near);
    }
    if (
      base.matches &&
      base.matches('[data-component-part="tabs-list"]')
    ) {
      queueEnhance(base);
    }
    var lists = base.querySelectorAll
      ? base.querySelectorAll('[data-component-part="tabs-list"]')
      : [];
    for (var i = 0; i < lists.length; i++) queueEnhance(lists[i]);
  }

  scan(document);
  new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i++) {
      var nodes = mutations[i].addedNodes;
      for (var j = 0; j < nodes.length; j++) {
        if (nodes[j].nodeType === 1) scan(nodes[j]);
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
