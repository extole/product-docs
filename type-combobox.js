(function () {
  var MIN_TABS = 1;
  var enhancing = false;
  var scheduled = null;

  var TOOLBAR =
    "mb-3 flex flex-wrap items-center gap-2";
  var LABEL =
    "text-xs font-semibold text-stone-500 dark:text-stone-400";
  var META =
    "text-xs text-stone-500 dark:text-stone-400";
  var COMBO =
    "relative min-w-64 flex-1 basis-72";
  var INPUT =
    "w-full min-w-64 max-w-full appearance-none rounded-lg border border-stone-300 bg-white px-3 py-2 font-mono text-sm leading-5 text-inherit outline-none focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-violet-700/35 dark:border-stone-700 dark:bg-stone-900";
  var MENU =
    "absolute left-0 right-0 top-full z-40 mt-1 max-h-72 overflow-auto rounded-lg border border-stone-300 bg-white shadow-lg dark:border-stone-700 dark:bg-stone-900";
  var OPTION =
    "block w-full cursor-pointer border-0 bg-transparent px-3 py-2 text-left font-mono text-xs text-inherit hover:bg-violet-700/10 hover:text-violet-700";
  var OPTION_ACTIVE =
    "bg-violet-700/10 text-violet-700";
  var EMPTY =
    "px-3 py-3 text-xs text-stone-500 dark:text-stone-400";

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
    var toolbar = el("div", TOOLBAR, {
      "data-extole-type-ui": "combobox",
    });
    toolbar.appendChild(el("span", LABEL, { text: "Type" }));

    var combo = el("div", COMBO);
    var input = el("input", INPUT, {
      type: "search",
      placeholder: "Search types…",
      "aria-label": "Search schema types",
      autocomplete: "off",
    });
    var menu = el("div", MENU);
    menu.hidden = true;
    var meta = el("span", META);

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
        menu.appendChild(el("div", EMPTY, { text: "No matching types" }));
        menu.hidden = false;
        return;
      }
      matches.forEach(function (tab) {
        var isActive = tab.getAttribute("aria-selected") === "true";
        var option = el("button", OPTION + (isActive ? " " + OPTION_ACTIVE : ""), {
          type: "button",
          text: tabLabel(tab),
        });
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
