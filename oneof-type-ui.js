(function () {
  var MIN_TABS = 1;
  var enhancing = false;
  var scheduled = null;

  function el(tag, className, attrs) {
    var node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (attrs) {
      Object.keys(attrs).forEach(function (key) {
        if (key === "text") {
          node.textContent = attrs[key];
          return;
        }
        node.setAttribute(key, attrs[key]);
      });
    }
    return node;
  }

  function tabLabel(tab) {
    var button = tab.querySelector('[data-component-part="tab-button"]');
    return ((button && button.textContent) || tab.textContent || "")
      .trim()
      .replace(/\s+/g, " ");
  }

  function selectedIndex(tabs) {
    for (var i = 0; i < tabs.length; i += 1) {
      if (tabs[i].getAttribute("aria-selected") === "true") {
        return i;
      }
    }
    return 0;
  }

  function activateTab(tab) {
    var button = tab.querySelector('[data-component-part="tab-button"]');
    (button || tab).click();
  }

  function clearEnhancements(list) {
    var root = list.parentElement;
    if (!root) {
      return;
    }
    root.querySelectorAll("[data-extole-type-ui]").forEach(function (node) {
      node.remove();
    });
    list.classList.remove("extole-type-ui-hidden");
    list.removeAttribute("data-extole-enhanced");
  }

  function buildCombobox(root, list, tabs) {
    var toolbar = el("div", "extole-type-ui-toolbar", {
      "data-extole-type-ui": "combobox",
    });
    toolbar.appendChild(el("span", "extole-type-ui-label", { text: "Type" }));

    var combo = el("div", "extole-type-ui-combo");
    var input = el("input", "extole-type-ui-combo-input", {
      type: "search",
      placeholder: "Search types…",
      "aria-label": "Search schema types",
      autocomplete: "off",
    });
    var menu = el("div", "extole-type-ui-combo-menu");
    menu.hidden = true;
    var meta = el("span", "extole-type-ui-meta");

    var active = tabs[selectedIndex(tabs)];
    var selectedLabel = tabLabel(active);
    input.value = selectedLabel;
    meta.textContent = tabs.length + " variants";

    function renderMenu(query) {
      menu.innerHTML = "";
      var q = (query || "").trim().toLowerCase();
      var matches = tabs.filter(function (tab) {
        return !q || tabLabel(tab).toLowerCase().indexOf(q) !== -1;
      });
      if (!matches.length) {
        menu.appendChild(
          el("div", "extole-type-ui-combo-empty", { text: "No matching types" })
        );
        menu.hidden = false;
        return;
      }
      matches.forEach(function (tab) {
        var option = el("button", "extole-type-ui-combo-option", {
          type: "button",
          text: tabLabel(tab),
        });
        if (tab.getAttribute("aria-selected") === "true") {
          option.setAttribute("data-active", "true");
        }
        option.addEventListener("mousedown", function (event) {
          event.preventDefault();
          activateTab(tab);
          selectedLabel = tabLabel(tab);
          input.value = selectedLabel;
          menu.hidden = true;
        });
        menu.appendChild(option);
      });
      menu.hidden = false;
    }

    input.addEventListener("focus", function () {
      input.value = "";
      renderMenu("");
    });
    input.addEventListener("input", function () {
      renderMenu(input.value);
    });
    input.addEventListener("blur", function () {
      window.setTimeout(function () {
        menu.hidden = true;
        if (!input.value.trim()) {
          input.value = selectedLabel;
        }
      }, 120);
    });

    combo.appendChild(input);
    combo.appendChild(menu);
    toolbar.appendChild(combo);
    toolbar.appendChild(meta);
    root.insertBefore(toolbar, list);
    list.classList.add("extole-type-ui-hidden");
  }

  function enhanceList(list, force) {
    var tabs = list.querySelectorAll('[data-component-part="tab"]');
    if (tabs.length < MIN_TABS) {
      clearEnhancements(list);
      return;
    }
    if (!force && list.getAttribute("data-extole-enhanced") === "combobox") {
      return;
    }
    clearEnhancements(list);
    var root = list.parentElement;
    if (!root) {
      return;
    }
    buildCombobox(root, list, Array.prototype.slice.call(tabs));
    list.setAttribute("data-extole-enhanced", "combobox");
  }

  function enhanceAll(force) {
    if (enhancing) {
      return;
    }
    enhancing = true;
    try {
      document
        .querySelectorAll('[data-component-part="tabs-list"]')
        .forEach(function (list) {
          enhanceList(list, force);
        });
    } finally {
      enhancing = false;
    }
  }

  function schedule() {
    if (scheduled) {
      return;
    }
    scheduled = window.setTimeout(function () {
      scheduled = null;
      enhanceAll(false);
    }, 50);
  }

  enhanceAll(true);
  document.addEventListener("DOMContentLoaded", schedule);

  var observer = new MutationObserver(function (mutations) {
    if (enhancing) {
      return;
    }
    for (var i = 0; i < mutations.length; i += 1) {
      var mutation = mutations[i];
      for (var j = 0; j < mutation.addedNodes.length; j += 1) {
        var node = mutation.addedNodes[j];
        if (!(node instanceof Element)) {
          continue;
        }
        if (
          node.matches('[data-component-part="tabs-list"]') ||
          node.querySelector('[data-component-part="tabs-list"]')
        ) {
          schedule();
          return;
        }
      }
    }
  });
  observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
  });
})();
