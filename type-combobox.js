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

  function enhance(list) {
    if (list.dataset.extoleCombo || !list.closest(".object-param-field")) return;
    var tabs = list.querySelectorAll('[data-component-part="tab"]');
    if (!tabs.length) return;
    list.dataset.extoleCombo = "1";

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

    function apply(i) {
      selected = i;
      var btn = tabs[i].querySelector('[data-component-part="tab-button"]');
      (btn || tabs[i]).click();
      input.value = labels[i];
      setOpen(false);
    }

    function pick(i) {
      apply(i);
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

    root.insertBefore(ui, list);
  }

  function scan(root) {
    var base = root && root.nodeType === 1 ? root : document;
    if (
      base.matches &&
      base.matches('[data-component-part="tabs-list"]') &&
      base.closest(".object-param-field")
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
