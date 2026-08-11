(function () {
  var registry = [];

  function labelOf(tab) {
    var btn = tab.querySelector('[data-component-part="tab-button"]');
    return ((btn && btn.textContent) || tab.textContent || "")
      .trim()
      .replace(/\s+/g, " ");
  }

  function sameLabels(a, b) {
    if (a.length !== b.length) return false;
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
    return true;
  }

  function tabNodes(list) {
    var tabs = list.querySelectorAll('[data-component-part="tab"]');
    if (tabs.length) return tabs;
    return list.querySelectorAll('[role="tab"]');
  }

  function playgroundHash(tab) {
    if (!tab || !tab.id) return "";
    if (tab.id.indexOf("_R_") === 0) return "";
    return tab.id;
  }

  function shouldEnhance(list, tabCount) {
    if (list.closest(".object-param-field")) return tabCount >= 2;
    if (list.closest('[role="dialog"]')) return tabCount >= 2;
    return false;
  }

  function setSelectValue(sel, value) {
    sel.disabled = false;
    var desc = Object.getOwnPropertyDescriptor(
      HTMLSelectElement.prototype,
      "value"
    );
    desc.set.call(sel, value);
    sel.dispatchEvent(new Event("input", { bubbles: true }));
    sel.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function enhance(list) {
    if (list.dataset.extoleCombo) return;
    var tabs = tabNodes(list);
    if (!shouldEnhance(list, tabs.length)) return;
    list.dataset.extoleCombo = "1";

    var dialogScoped = !!list.closest('[role="dialog"]');
    var scope = dialogScoped ? list.closest('[role="dialog"]') : document;
    var labels = [];
    var selected = 0;
    for (var i = 0; i < tabs.length; i++) {
      labels.push(labelOf(tabs[i]));
      if (tabs[i].getAttribute("aria-selected") === "true") selected = i;
    }

    var root = list.parentElement;
    if (!root) return;

    var ui = document.createElement("div");
    ui.className = "extole-type-combo";
    ui.innerHTML =
      "<label>Type</label>" +
      '<div class="extole-type-combo-wrap">' +
      '<input type="text" autocomplete="off" spellcheck="false" aria-label="Search schema types" role="combobox" aria-autocomplete="list" aria-expanded="false">' +
      '<div class="extole-type-combo-menu" role="listbox" hidden></div></div>' +
      '<span class="extole-type-combo-meta"></span>';

    var input = ui.querySelector("input");
    var menu = ui.querySelector(".extole-type-combo-menu");
    var meta = ui.querySelector(".extole-type-combo-meta");
    input.value = labels[selected];
    meta.textContent = tabs.length + "/" + tabs.length + " variants";

    var fillTimer = null;
    var fillGen = 0;

    function setOpen(open) {
      menu.hidden = !open;
      input.setAttribute("aria-expanded", open ? "true" : "false");
      if (!open) meta.textContent = tabs.length + "/" + tabs.length + " variants";
    }

    function paint(query) {
      var q = (query || "").toLowerCase();
      var html = "";
      var n = 0;
      for (var i = 0; i < labels.length; i++) {
        if (q && labels[i].toLowerCase().indexOf(q) === -1) continue;
        n++;
        html +=
          '<button type="button" role="option" data-i="' +
          i +
          '"' +
          (i === selected ? ' aria-selected="true"' : "") +
          ">" +
          labels[i] +
          "</button>";
      }
      menu.innerHTML =
        html || '<div class="extole-type-combo-empty">No matching types</div>';
      meta.textContent = n + "/" + tabs.length + " variants";
      setOpen(true);
    }

    function activeTypeSelect() {
      var selectedTab =
        list.querySelector('[role="tab"][aria-selected="true"]') ||
        tabs[selected];
      if (!selectedTab) return null;
      var controls = selectedTab.getAttribute("aria-controls");
      if (!controls) return null;
      var panel = scope.querySelector("#" + CSS.escape(controls));
      if (!panel) return null;
      return panel.querySelector('[data-testid="api-input-type"] select');
    }

    function typeSelectHas(sel, label) {
      if (!sel) return false;
      for (var o = 0; o < sel.options.length; o++) {
        if (sel.options[o].value === label) return true;
      }
      return false;
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

    function lockTypeSelect(sel) {
      if (!sel || !ui.isConnected) return;
      sel.disabled = true;
      sel.setAttribute("aria-disabled", "true");
      sel.title = "Choose the type from the Type dropdown above";
    }

    function syncTypeToLabel(label) {
      var sel = activeTypeSelect();
      if (!typeSelectHas(sel, label)) return false;
      if (sel.value !== label) setSelectValue(sel, label);
      lockTypeSelect(sel);
      return sel.value === label;
    }

    function scheduleTypeSync(label) {
      if (!dialogScoped || !ui.isConnected) return;
      if (fillTimer) clearInterval(fillTimer);
      var gen = ++fillGen;
      var tries = 0;
      fillTimer = setInterval(function () {
        if (gen !== fillGen || !list.isConnected || !ui.isConnected) {
          clearInterval(fillTimer);
          fillTimer = null;
          return;
        }
        tries++;
        if (syncTypeToLabel(label) || tries > 40) {
          clearInterval(fillTimer);
          fillTimer = null;
        }
      }, 50);
    }

    function apply(i) {
      selected = i;
      var tab = tabs[i];
      var label = labels[i];
      var hash = playgroundHash(tab);

      clickTab(tab);
      if (dialogScoped && hash) {
        setTimeout(function () {
          if (location.hash !== "#" + hash) location.hash = hash;
          scheduleTypeSync(label);
        }, 400);
      }

      input.value = label;
      setOpen(false);
    }

    function pick(i) {
      apply(i);
      if (dialogScoped) return;
      var label = labels[i];
      for (var r = 0; r < registry.length; r++) {
        var other = registry[r];
        if (other.list === list || !sameLabels(labels, other.labels)) continue;
        other.applyByLabel(label);
      }
    }

    var api = {
      list: list,
      labels: labels,
      applyByLabel: function (label) {
        var idx = labels.indexOf(label);
        if (idx < 0 || idx === selected) {
          if (idx >= 0) input.value = labels[idx];
          return;
        }
        apply(idx);
      },
    };
    registry.push(api);

    function syncFromDom(alsoFillType) {
      var hash = (location.hash || "").replace(/^#/, "");
      var idx = -1;
      if (dialogScoped && hash) {
        for (var i = 0; i < tabs.length; i++) {
          if (tabs[i].id === hash) {
            idx = i;
            break;
          }
        }
      }
      if (idx < 0) {
        for (var j = 0; j < tabs.length; j++) {
          if (tabs[j].getAttribute("aria-selected") === "true") {
            idx = j;
            break;
          }
        }
      }
      if (idx < 0) return;
      selected = idx;
      if (document.activeElement !== input) input.value = labels[idx];
      if (alsoFillType && dialogScoped) scheduleTypeSync(labels[idx]);
    }

    function enterSearch() {
      input.value = "";
      paint("");
    }

    input.addEventListener("pointerdown", enterSearch);
    input.addEventListener("focus", enterSearch);
    input.addEventListener("input", function () {
      paint(input.value);
    });
    input.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      input.value = labels[selected];
      setOpen(false);
      input.blur();
    });
    input.addEventListener("blur", function () {
      setTimeout(function () {
        setOpen(false);
        if (!input.value.trim()) input.value = labels[selected];
      }, 0);
    });
    menu.addEventListener("pointerdown", function (e) {
      var t = e.target.closest("button[data-i]");
      if (!t) return;
      e.preventDefault();
      pick(+t.getAttribute("data-i"));
    });

    if (dialogScoped) {
      window.addEventListener("hashchange", function () {
        if (!list.isConnected) return;
        syncFromDom(true);
      });
      new MutationObserver(function () {
        if (!list.isConnected || !ui.isConnected) return;
        lockTypeSelect(activeTypeSelect());
      }).observe(scope, { childList: true, subtree: true });
    }

    new MutationObserver(function () {
      if (!list.isConnected) return;
      syncFromDom(false);
    }).observe(list, {
      attributes: true,
      subtree: true,
      attributeFilter: ["aria-selected"],
    });

    root.insertBefore(ui, list);
    syncFromDom(dialogScoped);
  }

  function scan(root) {
    var base = root && root.nodeType === 1 ? root : document;
    if (base.closest) {
      var near = base.closest('[data-component-part="tabs-list"]');
      if (near) enhance(near);
    }
    if (
      base.matches &&
      base.matches('[data-component-part="tabs-list"]')
    ) {
      enhance(base);
    }
    var lists = base.querySelectorAll
      ? base.querySelectorAll('[data-component-part="tabs-list"]')
      : [];
    for (var i = 0; i < lists.length; i++) enhance(lists[i]);
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
