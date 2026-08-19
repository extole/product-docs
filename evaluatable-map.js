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
        scanSoon();
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

  function isEvaluatableLabels(labels) {
    if (!labels || labels.length < 2 || labels.length > 8) return false;
    var joined = labels.join("\n");
    if (!/Static Value/i.test(joined)) return false;
    return /Handlebars|Javascript/i.test(joined);
  }

  function isStaticPlusStringUnion(labels) {
    if (!labels || labels.length < 4 || labels.length > 8) return false;
    var strings = 0;
    var hasStatic = false;
    for (var i = 0; i < labels.length; i++) {
      if (/Static Value/i.test(labels[i]) || /^object(\s|$)/i.test(labels[i])) {
        hasStatic = true;
      }
      if (/^string(\s*·|$)/i.test(labels[i])) strings += 1;
    }
    return hasStatic && strings >= 3;
  }

  function isEvaluatableValueType(labels) {
    return isEvaluatableLabels(labels) || isStaticPlusStringUnion(labels);
  }

  function collectTypeLabels(root) {
    if (!root) return [];
    var out = [];
    var seen = {};
    function add(text) {
      var t = (text || "").trim().replace(/\s+/g, " ");
      if (!t || seen[t]) return;
      if (/^add new property$/i.test(t)) return;
      if (/^select /i.test(t)) return;
      seen[t] = 1;
      out.push(t);
    }
    var tabs = root.querySelectorAll(
      '[data-component-part="tab"], [role="tab"], [data-component-part="tab-button"]'
    );
    for (var i = 0; i < tabs.length; i++) add(tabs[i].textContent);
    var opts = root.querySelectorAll("option");
    for (var j = 0; j < opts.length; j++) add(opts[j].textContent);
    var items = root.querySelectorAll('[role="option"], [role="menuitem"]');
    for (var k = 0; k < items.length; k++) add(items[k].textContent);
    return out;
  }

  function nativeMapRoot(field) {
    var clone = field.cloneNode(true);
    var ours = clone.querySelectorAll(".extole-eval-map");
    for (var i = 0; i < ours.length; i++) ours[i].remove();
    return clone;
  }

  function unionLooksEvaluatable(root) {
    if (!root) return false;
    var selects = root.querySelectorAll("select");
    for (var i = 0; i < selects.length; i++) {
      var labels = [];
      for (var o = 0; o < selects[i].options.length; o++) {
        var t = (selects[i].options[o].textContent || "").trim().replace(/\s+/g, " ");
        if (t && !/^select /i.test(t)) labels.push(t);
      }
      if (isEvaluatableValueType(labels)) return true;
    }
    var lists = root.querySelectorAll('[data-component-part="tabs-list"]');
    for (var j = 0; j < lists.length; j++) {
      if (isEvaluatableValueType(collectTypeLabels(lists[j]))) return true;
    }
    return false;
  }

  function isComponentSettingBody(body) {
    if (!body) return false;
    var text = body.innerText || body.textContent || "";
    return (
      /ADMIN_ICON/.test(text) &&
      /BROWSER_SIDE_JAVASCRIPT/.test(text) &&
      /STRING_MAP/.test(text)
    );
  }

  function nativeLooksLikePlainMap(labels) {
    if (!labels || !labels.length) return false;
    if (isEvaluatableValueType(labels)) return false;
    return true;
  }

  function isEvaluatableValuesMap(field) {
    var native = nativeMapRoot(field);
    var nativeLabels = collectTypeLabels(native);
    if (unionLooksEvaluatable(native) || isEvaluatableValueType(nativeLabels)) {
      return true;
    }
    if (nativeLooksLikePlainMap(nativeLabels)) return false;
    var text = native.innerText || native.textContent || "";
    if (/Choose between static or dynamic values/i.test(text)) return true;
    if (/Open map of setting values/i.test(text)) return true;
    var body =
      field.closest('[data-testid="api-input-section-Body"]') ||
      field.closest('[role="dialog"]');
    return isComponentSettingBody(body);
  }

  function pendingKeyInput(field) {
    return field.querySelector(
      'input[placeholder="Enter key of new property"]'
    );
  }

  function nativeEntry(field, key) {
    var marker = "values." + key;
    var dels = field.querySelectorAll('[aria-label="Delete item"]');
    for (var i = 0; i < dels.length; i++) {
      var block = dels[i].closest(".py-5") || dels[i].parentElement;
      if (!block) continue;
      var text = (block.innerText || block.textContent || "").replace(/\s+/g, " ");
      var at = text.indexOf(marker);
      if (at === -1) continue;
      var next = text.charAt(at + marker.length);
      if (next && /[a-z0-9_]/.test(next)) continue;
      return block;
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
    var escaped = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    var re = new RegExp("(^|\\s)enter\\s+" + escaped + "$", "i");
    var nodes = scoped.querySelectorAll("input, textarea");
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].closest(".extole-eval-map")) continue;
      var ph = nodes[i].placeholder || "";
      var aria = nodes[i].getAttribute("aria-label") || "";
      if (re.test(ph.trim()) || re.test(aria.trim())) return nodes[i];
    }
    return null;
  }

  function parsedStatic(raw) {
    if (!(raw || "").trim()) return { kind: "empty" };
    try {
      var parsed = JSON.parse(raw);
      if (parsed !== null && typeof parsed === "object") {
        return { kind: "object", raw: raw };
      }
    } catch (err) {}
    return { kind: "scalar", raw: raw };
  }

  function nativeTypeIndex(row) {
    var idx = +row.querySelector("select").value;
    if (idx !== 0) return idx;
    return parsedStatic(suffixOf(row)).kind === "scalar" ? 1 : 0;
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

  function wantedValue(row) {
    var s = spec(row);
    var want = s.prefix ? fullValue(row) : suffixOf(row);
    if (!s.prefix && parsedStatic(want).kind === "empty") want = "{}";
    return want;
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
    var existing = nativeEntry(field, key);
    if (existing) {
      row.dataset.nativeKey = key;
      return Promise.resolve(existing);
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

  function nativeValueKind(field, key) {
    var input = nativeValueInput(field, key);
    if (!input) return "";
    return input.tagName === "TEXTAREA" ? "object" : "string";
  }

  function typeMenuItem(idx) {
    var title = TITLES[idx];
    var items = document.querySelectorAll('[role="menuitem"]');
    for (var i = 0; i < items.length; i++) {
      var text = (items[i].textContent || "").trim().replace(/\s+/g, " ");
      if (text === title || text.indexOf(title) === 0) return items[i];
    }
    return null;
  }

  function mapAlreadyOnType(field, idx) {
    var rows = field.querySelectorAll(".extole-eval-map-row");
    for (var i = 0; i < rows.length; i++) {
      if (rows[i].dataset.nativeType === String(idx)) return true;
    }
    return false;
  }

  function ensureNativeType(field, row, key, idx) {
    var wantString = idx !== 0;
    var kind = nativeValueKind(field, key);
    if (row.dataset.nativeType === String(idx) && kind) return Promise.resolve();
    if (mapAlreadyOnType(field, idx) && wantString && kind === "string") {
      row.dataset.nativeType = String(idx);
      return Promise.resolve();
    }
    if (mapAlreadyOnType(field, idx) && !wantString && kind === "object") {
      row.dataset.nativeType = String(idx);
      return Promise.resolve();
    }
    var block = nativeEntry(field, key);
    var chip = typeChip(block);
    if (!chip) return Promise.resolve();
    chip.click();
    return waitFor(function () {
      return typeMenuItem(idx);
    }).then(function (item) {
      if (!item) return;
      item.click();
      row.dataset.nativeType = String(idx);
    });
  }

  function restoreOtherValues(field, current) {
    var rows = field.querySelectorAll(".extole-eval-map-row");
    var chain = Promise.resolve();
    for (var i = 0; i < rows.length; i++) {
      (function (other) {
        if (other === current) return;
        var key = other.dataset.nativeKey;
        if (!key) return;
        chain = chain.then(function () {
          return fillNativeValue(field, other, key);
        });
      })(rows[i]);
    }
    return chain;
  }

  function fillNativeValue(field, row, key) {
    var want = wantedValue(row);
    return waitFor(function () {
      return nativeValueInput(field, key);
    }, 3000).then(function (input) {
      if (!input) return;
      setValue(input, want);
      enterKey(input);
      if (typeof input.blur === "function") input.blur();
    });
  }

  function snapshot(row) {
    return (
      keyOf(row) +
      "\0" +
      row.querySelector("select").value +
      "\0" +
      fullValue(row)
    );
  }

  function setSaveState(row, dirty) {
    var save = row.querySelector(".extole-eval-map-save");
    if (!save) return;
    save.disabled = !dirty;
    save.setAttribute("aria-disabled", dirty ? "false" : "true");
    save.classList.toggle("is-active", !!dirty);
  }

  function markDirty(row) {
    paint(row);
    setSaveState(row, snapshot(row) !== (row.dataset.saved || ""));
  }

  function markSaved(row) {
    row.dataset.saved = snapshot(row);
    setSaveState(row, false);
  }

  function syncRow(field, row) {
    paint(row);
    var key = keyOf(row);
    if (!key) return Promise.resolve();
    var idx = nativeTypeIndex(row);
    return queue(field, function () {
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
        })
        .then(function () {
          return restoreOtherValues(field, row);
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
    var save = row.querySelector(".extole-eval-map-save");
    var remove = row.querySelector(".extole-eval-map-remove");
    paint(row);
    if (!row.dataset.saved) row.dataset.saved = snapshot(row);
    markDirty(row);

    function bumpKey() {
      if (!keyOf(row) && (suffixOf(row) || spec(row).prefix)) {
        keyEl.value = "default";
      }
    }

    function noteEdit() {
      bumpKey();
      markDirty(row);
    }

    function saveRow() {
      bumpKey();
      paint(row);
      if (!keyOf(row)) return;
      save.disabled = true;
      return syncRow(field, row).then(function () {
        var key = keyOf(row);
        if (row.dataset.nativeKey !== key) {
          setSaveState(row, true);
          return;
        }
        var input = nativeValueInput(field, key);
        if (input && input.value === wantedValue(row)) markSaved(row);
        else setSaveState(row, true);
      });
    }

    keyEl.addEventListener("input", noteEdit);
    keyEl.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        saveRow();
      }
    });
    typeEl.addEventListener("change", function () {
      maybePrefill(row);
      row.dataset.nativeType = "";
      noteEdit();
    });
    valEl.addEventListener("input", noteEdit);
    valEl.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        saveRow();
      }
    });
    save.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      saveRow();
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
          row.dataset.saved = "";
          paint(row);
          row.dataset.saved = snapshot(row);
          markDirty(row);
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
      '<button type="button" class="extole-eval-map-save" aria-label="OK" title="OK" disabled>✓</button>' +
      '<button type="button" class="extole-eval-map-remove" aria-label="Remove entry">×</button>' +
      '<p class="extole-eval-map-hint" hidden></p>';
    return row;
  }

  function enhance(field) {
    if (!field || !visible(field)) return;
    if (!field.closest('[role="dialog"]')) return;
    if (!addButton(field)) return;
    if (field.dataset.extoleEvalMap === "no") {
      var skipped = field.querySelector(":scope > .extole-eval-map");
      if (skipped) skipped.remove();
      field.classList.remove("extole-eval-map-on");
      return;
    }
    if (!isEvaluatableValuesMap(field)) {
      var nativeLabels = collectTypeLabels(nativeMapRoot(field));
      if (nativeLabels.length) {
        field.dataset.extoleEvalMap = "no";
        var wrong = field.querySelector(":scope > .extole-eval-map");
        if (wrong) wrong.remove();
        field.classList.remove("extole-eval-map-on");
      }
      return;
    }
    var existing = field.querySelector(":scope > .extole-eval-map");
    if (existing) {
      if (existing.querySelector(".extole-eval-map-save")) return;
      existing.remove();
    }

    var ui = document.createElement("div");
    ui.className = "extole-eval-map";
    function stopBubble(e) {
      e.stopPropagation();
    }
    ui.addEventListener("pointerdown", stopBubble);
    ui.addEventListener("mousedown", stopBubble);
    ui.addEventListener("click", stopBubble);
    ui.addEventListener("keydown", stopBubble);
    ui.addEventListener("input", stopBubble);
    ui.addEventListener("change", stopBubble);

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

    if (field.querySelector(":scope > .extole-eval-map")) return;

    var grid = field.querySelector(":scope > .grid");
    if (grid && grid.parentElement === field) field.insertBefore(ui, grid);
    else field.appendChild(ui);

    field.classList.add("extole-eval-map-on");
    field.dataset.extoleEvalMap = "yes";
    bindRow(field, row);
  }

  function scan() {
    if (document.documentElement.getAttribute("data-extole-driving")) return;
    var fields = document.querySelectorAll(
      '[role="dialog"] [data-testid="api-input-values"]'
    );
    for (var i = 0; i < fields.length; i++) enhance(fields[i]);
  }

  var scanTimer = 0;
  function scanSoon() {
    if (scanTimer) return;
    scanTimer = setTimeout(function () {
      scanTimer = 0;
      scan();
    }, 50);
  }

  scan();
  new MutationObserver(scanSoon).observe(document.documentElement, {
    childList: true,
    subtree: true,
  });
})();
