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
    "relative min-w-64 flex-1 basis-72 cursor-pointer";
  var INPUT =
    "w-full min-w-64 max-w-full cursor-pointer appearance-none rounded-lg border border-stone-300 bg-white py-2 pl-3 pr-10 font-mono text-sm leading-5 text-inherit outline-none focus:cursor-text focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-violet-700/35 dark:border-stone-700 dark:bg-stone-900";
  var ARROW =
    "pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 cursor-pointer text-stone-500 dark:text-stone-400";
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

  function dropdownArrow() {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", ARROW);
    svg.setAttribute("viewBox", "0 0 20 20");
    svg.setAttribute("fill", "currentColor");
    svg.setAttribute("aria-hidden", "true");
    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("fill-rule", "evenodd");
    path.setAttribute("clip-rule", "evenodd");
    path.setAttribute(
      "d",
      "M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
    );
    svg.appendChild(path);
    return svg;
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
      type: "text",
      role: "combobox",
      "aria-autocomplete": "list",
      "aria-expanded": "false",
      placeholder: "Search types…",
      "aria-label": "Search schema types",
      autocomplete: "off",
    });
    var menu = el("div", MENU, {
      role: "listbox",
    });
    menu.hidden = true;
    var meta = el("span", META);

    var active = tabs[selectedIndex(tabs)];
    var selectedLabel = tabLabel(active);
    input.value = selectedLabel;
    meta.textContent = tabs.length + " variants";

    function setExpanded(open) {
      input.setAttribute("aria-expanded", open ? "true" : "false");
    }

    function renderMenu(query) {
      menu.innerHTML = "";
      var q = (query || "").trim().toLowerCase();
      var matches = tabs.filter(function (tab) {
        return !q || tabLabel(tab).toLowerCase().indexOf(q) !== -1;
      });
      if (!matches.length) {
        menu.appendChild(el("div", EMPTY, { text: "No matching types" }));
        menu.hidden = false;
        setExpanded(true);
        return;
      }
      matches.forEach(function (tab) {
        var isActive = tab.getAttribute("aria-selected") === "true";
        var option = el("button", OPTION + (isActive ? " " + OPTION_ACTIVE : ""), {
          type: "button",
          role: "option",
          text: tabLabel(tab),
        });
        option.addEventListener("mousedown", function (event) {
          event.preventDefault();
          activateTab(tab);
          selectedLabel = tabLabel(tab);
          input.value = selectedLabel;
          menu.hidden = true;
          setExpanded(false);
        });
        menu.appendChild(option);
      });
      menu.hidden = false;
      setExpanded(true);
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
        setExpanded(false);
        if (!input.value.trim()) {
          input.value = selectedLabel;
        }
      }, 120);
    });

    combo.appendChild(input);
    combo.appendChild(dropdownArrow());
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
