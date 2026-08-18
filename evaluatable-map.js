(function () {
  var TITLES = [
    "Static Value",
    "Buildtime - Handlebars",
    "Buildtime - Javascript",
    "Runtime - Handlebars",
    "Runtime - Javascript",
  ];

  var TYPES = [
    { prefix: "", pattern: null, placeholder: "value", example: "" },
    {
      prefix: "handlebars@buildtime:",
      pattern: /^handlebars@buildtime:/,
      placeholder: "{{name}}",
      example: "{{name}}",
    },
    {
      prefix: "javascript@buildtime:",
      pattern: /^javascript@buildtime:/,
      placeholder: "function() { ... }",
      example: "",
    },
    {
      prefix: "handlebars@runtime:",
      pattern: /^handlebars@runtime:/,
      placeholder: "{{name}}",
      example: "{{name}}",
    },
    {
      prefix: "javascript@runtime:",
      pattern: /^javascript@runtime:/,
      placeholder: "function() { ... }",
      example: "",
    },
  ];

  function waitFor(pred, ms) {
    return new Promise(function (resolve) {
      var start = Date.now();
      (function tick() {
        var found = pred();
        if (found) return resolve(found);
        if (Date.now() - start > (ms || 2000)) return resolve(null);
        setTimeout(tick, 30);
      })();
    });
  }

  function driving(job) {
    var active = document.activeElement;
    document.documentElement.setAttribute("data-extole-driving", "1");
    return Promise.resolve()
      .then(job)
      .finally(function () {
        document.documentElement.removeAttribute("data-extole-driving");
        if (
          active &&
          active !== document.body &&
          typeof active.focus === "function"
        ) {
          try {
            active.focus();
          } catch (err) {}
        }
      });
  }

  function setValue(el, value) {
    if (!el) return;
    var proto =
      el.tagName === "TEXTAREA"
        ? HTMLTextAreaElement.prototype
        : HTMLInputElement.prototype;
    var desc = Object.getOwnPropertyDescriptor(proto, "value");
    var tracker = el._valueTracker;
    if (tracker) tracker.setValue("");
    desc.set.call(el, value);
    var inputEv;
    try {
      inputEv = new InputEvent("input", {
        bubbles: true,
        cancelable: true,
        composed: true,
        inputType: "insertText",
        data: value,
      });
    } catch (err) {
      inputEv = new Event("input", { bubbles: true, cancelable: true });
    }
    el.dispatchEvent(inputEv);
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function enterKey(el) {
    var opts = {
      key: "Enter",
      code: "Enter",
      keyCode: 13,
      which: 13,
      bubbles: true,
      cancelable: true,
    };
    el.dispatchEvent(new KeyboardEvent("keydown", opts));
    el.dispatchEvent(new KeyboardEvent("keypress", opts));
    el.dispatchEvent(new KeyboardEvent("keyup", opts));
  }

  function visible(el) {
    if (!el || !el.getBoundingClientRect) return false;
    var r = el.getBoundingClientRect();
    return r.width > 24 && r.height > 16;
  }

  function addButton(field) {
    return field.querySelector(
      '[data-testid$="values.additional-property-button"]'
    );
  }

  function pendingKeyInput(field) {
    return field.querySelector(
      'input[placeholder="Enter key of new property"]'
    );
  }

  function nativeEntry(field, key) {
    var dels = field.querySelectorAll('[aria-label="Delete item"]');
    for (var i = 0; i < dels.length; i++) {
      var block = dels[i].closest(".py-5") || dels[i].parentElement;
      if (block && (block.innerText || "").indexOf("values." + key) !== -1) {
        return block;
      }
    }
    return null;
  }

  function typeChip(block) {
    if (!block) return null;
    var buttons = block.querySelectorAll("button");
    for (var i = 0; i < buttons.length; i++) {
      if (buttons[i].getAttribute("aria-label") === "Delete item") continue;
      if (buttons[i].getAttribute("data-testid")) continue;
      return buttons[i];
    }
    return null;
  }

  function nativeValueInput(field, key) {
    var block = nativeEntry(field, key);
    var scoped = block || field;
    return (
      scoped.querySelector('input[placeholder="enter ' + key + '"]') ||
      scoped.querySelector('input[aria-label="Enter ' + key + '"]') ||
      scoped.querySelector('textarea[placeholder="enter ' + key + '"]') ||
      scoped.querySelector('textarea[aria-label="Enter ' + key + '"]')
    );
  }

  function spec(row) {
    return TYPES[+row.querySelector("select").value] || TYPES[0];
  }

  function keyOf(row) {
    return (row.querySelector(".extole-eval-map-key").value || "").trim();
  }

  function suffixOf(row) {
    return row.querySelector(".extole-eval-map-input").value;
  }

  function fullValue(row) {
    var s = spec(row);
    var raw = suffixOf(row);
    if (!s.prefix) return raw;
    if (raw.indexOf(s.prefix) === 0) return raw;
    return s.prefix + raw;
  }

  function paint(row) {
    var s = spec(row);
    var prefix = row.querySelector(".extole-eval-map-prefix");
    var input = row.querySelector(".extole-eval-map-input");
    var wrap = row.querySelector(".extole-eval-map-val");
    var hint = row.querySelector(".extole-eval-map-hint");
    prefix.textContent = s.prefix;
    prefix.hidden = !s.prefix;
    wrap.classList.toggle("has-prefix", !!s.prefix);
    input.placeholder = s.placeholder;
    if (s.prefix && input.value.indexOf(s.prefix) === 0) {
      input.value = input.value.slice(s.prefix.length);
    }
    var ok = true;
    var msg = "";
    if (s.pattern && !s.pattern.test(fullValue(row))) {
      ok = false;
      msg = "Must start with " + s.prefix;
    }
    wrap.classList.toggle("is-invalid", !ok);
    hint.textContent = msg;
    hint.hidden = !msg;
  }

  function queue(field, job) {
    field._extoleMapQ = (field._extoleMapQ || Promise.resolve())
      .then(function () {
        return driving(job);
      })
      .catch(function () {});
    return field._extoleMapQ;
  }

  function commitPendingKey(field, key) {
    var input = pendingKeyInput(field);
    if (!input) return Promise.resolve(null);
    setValue(input, key);
    enterKey(input);
    return waitFor(function () {
      return nativeEntry(field, key);
    });
  }

  function ensureNativeKey(field, row, key) {
    if (nativeEntry(field, key)) {
      row.dataset.nativeKey = key;
      return Promise.resolve(nativeEntry(field, key));
    }
    var pending = pendingKeyInput(field);
    if (pending) {
      return commitPendingKey(field, key).then(function (block) {
        if (block) row.dataset.nativeKey = key;
        return block;
      });
    }
    var add = addButton(field);
    if (!add) return Promise.resolve(null);
    add.click();
    return waitFor(function () {
      return pendingKeyInput(field);
    }).then(function () {
      return commitPendingKey(field, key);
    }).then(function (block) {
      if (block) row.dataset.nativeKey = key;
      return block;
    });
  }

  function ensureNativeType(field, row, key, idx) {
    if (row.dataset.nativeType === String(idx)) return Promise.resolve();
    var block = nativeEntry(field, key);
    var chip = typeChip(block);
    if (!chip) return Promise.resolve();
    chip.click();
    return waitFor(function () {
      var items = document.querySelectorAll('[role="menuitem"]');
      return items.length >= 3 ? items : null;
    }).then(function (items) {
      if (!items || !items[idx]) return;
      items[idx].click();
      row.dataset.nativeType = String(idx);
    });
  }

  function fillNativeValue(field, row, key) {
    var s = spec(row);
    if (!s.prefix) return Promise.resolve();
    var want = fullValue(row);
    return waitFor(function () {
      return nativeValueInput(field, key);
    }).then(function (input) {
      if (!input) return;
      if (input.value === want) return;
      setValue(input, want);
    });
  }

  function syncRow(field, row) {
    paint(row);
    var key = keyOf(row);
    if (!key) return;
    var idx = +row.querySelector("select").value;
    queue(field, function () {
      var prev = row.dataset.nativeKey;
      if (prev && prev !== key) {
        var old = nativeEntry(field, prev);
        var del = old && old.querySelector('[aria-label="Delete item"]');
        if (del) del.click();
        row.dataset.nativeKey = "";
        row.dataset.nativeType = "";
      }
      return ensureNativeKey(field, row, key)
        .then(function () {
          return ensureNativeType(field, row, key, idx);
        })
        .then(function () {
          return fillNativeValue(field, row, key);
        });
    });
  }

  function maybePrefill(row) {
    var s = spec(row);
    var input = row.querySelector(".extole-eval-map-input");
    if (s.example && !input.value) input.value = s.example;
  }

  function bindRow(field, row) {
    var keyEl = row.querySelector(".extole-eval-map-key");
    var typeEl = row.querySelector("select");
    var valEl = row.querySelector(".extole-eval-map-input");
    var remove = row.querySelector(".extole-eval-map-remove");
    var timer = null;
    paint(row);

    function bumpKey() {
      if (!keyOf(row) && (suffixOf(row) || spec(row).prefix)) {
        keyEl.value = "default";
      }
    }

    function syncSoon() {
      bumpKey();
      paint(row);
      clearTimeout(timer);
      timer = setTimeout(function () {
        syncRow(field, row);
      }, 80);
    }

    keyEl.addEventListener("input", syncSoon);
    keyEl.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        clearTimeout(timer);
        syncRow(field, row);
      }
    });
    keyEl.addEventListener("blur", function () {
      clearTimeout(timer);
      syncRow(field, row);
    });
    typeEl.addEventListener("change", function () {
      maybePrefill(row);
      bumpKey();
      row.dataset.nativeType = "";
      paint(row);
      clearTimeout(timer);
      syncRow(field, row);
    });
    valEl.addEventListener("input", syncSoon);
    valEl.addEventListener("blur", function () {
      clearTimeout(timer);
      syncRow(field, row);
    });
    remove.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var rows = field.querySelectorAll(".extole-eval-map-row");
      queue(field, function () {
        var block = nativeEntry(field, row.dataset.nativeKey);
        var del = block && block.querySelector('[aria-label="Delete item"]');
        if (del) del.click();
      }).then(function () {
        if (rows.length <= 1) {
          keyEl.value = "";
          valEl.value = "";
          typeEl.selectedIndex = 0;
          row.dataset.nativeKey = "";
          row.dataset.nativeType = "";
          paint(row);
          return;
        }
        row.remove();
      });
    });
  }

  function buildRow() {
    var row = document.createElement("div");
    row.className = "extole-eval-map-row";
    var opts = TITLES.map(function (t, i) {
      return '<option value="' + i + '">' + t + "</option>";
    }).join("");
    row.innerHTML =
      '<input class="extole-eval-map-key" type="text" spellcheck="false" autocomplete="off" placeholder="default" aria-label="Map key">' +
      '<select class="extole-eval-map-type" aria-label="Value type">' +
      opts +
      "</select>" +
      '<label class="extole-eval-map-val">' +
      '<span class="extole-eval-map-prefix" hidden></span>' +
      '<input class="extole-eval-map-input" type="text" spellcheck="false" autocomplete="off" aria-label="Map value">' +
      "</label>" +
      '<button type="button" class="extole-eval-map-remove" aria-label="Remove entry">×</button>' +
      '<p class="extole-eval-map-hint" hidden></p>';
    return row;
  }

  function enhance(field) {
    if (!field || !visible(field)) return;
    if (!field.closest('[role="dialog"]')) return;
    if (!addButton(field)) return;
    if (field.querySelector(":scope > .extole-eval-map")) return;

    var ui = document.createElement("div");
    ui.className = "extole-eval-map";
    function stopBubble(e) {
      e.stopPropagation();
    }
    ui.addEventListener("pointerdown", stopBubble);
    ui.addEventListener("mousedown", stopBubble);
    ui.addEventListener("click", stopBubble);
    ui.addEventListener("keydown", stopBubble);

    var list = document.createElement("div");
    list.className = "extole-eval-map-list";
    var row = buildRow();
    list.appendChild(row);

    var more = document.createElement("button");
    more.type = "button";
    more.className = "extole-eval-map-add";
    more.textContent = "+ add another entry";
    more.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var next = buildRow();
      list.appendChild(next);
      bindRow(field, next);
      next.querySelector(".extole-eval-map-key").focus();
    });

    ui.appendChild(list);
    ui.appendChild(more);

    var grid = field.querySelector(":scope > .grid");
    if (grid && grid.parentElement === field) field.insertBefore(ui, grid);
    else field.appendChild(ui);

    bindRow(field, row);
  }

  function scan() {
    var fields = document.querySelectorAll('[data-testid="api-input-values"]');
    for (var i = 0; i < fields.length; i++) enhance(fields[i]);
  }

  scan();
  new MutationObserver(function () {
    scan();
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
