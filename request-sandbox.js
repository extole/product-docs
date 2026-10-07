(function () {
  "use strict";

  var modal;
  var dialog;
  var form;
  var lastTrigger;
  var hiddenSiblings = [];
  // Set true after enabling Salesforce Web-to-Lead reCAPTCHA enforcement.
  var captchaEnabled = false;

  function triggerLinks() {
    return document.querySelectorAll('a[href="#request-sandbox"]');
  }

  function returnUrl() {
    var url = new URL(window.location.href);
    url.searchParams.set("sandbox-request", "submitted");
    url.hash = "";
    return url.toString();
  }

  function setReturnUrl() {
    form.querySelector('[name="retURL"]').value = returnUrl();
  }

  function setNameFields() {
    var fullName = form.querySelector('[name="full_name"]').value.trim();
    var parts = fullName.split(/\s+/);
    var lastName = parts.pop();
    form.querySelector('[name="first_name"]').value = parts.join(" ");
    form.querySelector('[name="last_name"]').value = lastName;
  }

  function updateCaptchaTimestamp() {
    if (!captchaEnabled) return;

    var response = form.querySelector('[name="g-recaptcha-response"]');
    if (response && response.value.trim()) return;
    var settings = form.querySelector('[name="captcha_settings"]');
    var values = JSON.parse(settings.value);
    values.ts = JSON.stringify(new Date().getTime());
    settings.value = JSON.stringify(values);
  }

  function resetCaptcha() {
    if (
      captchaEnabled &&
      window.grecaptcha &&
      typeof window.grecaptcha.reset === "function"
    ) {
      window.grecaptcha.reset();
    }
  }

  function loadCaptcha() {
    if (document.querySelector('script[src="https://www.google.com/recaptcha/api.js"]')) return;
    var script = document.createElement("script");
    script.src = "https://www.google.com/recaptcha/api.js";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }

  function submitToSalesforce(event) {
    event.preventDefault();
    setNameFields();
    setReturnUrl();

    if (captchaEnabled) {
      updateCaptchaTimestamp();

      var captchaResponse = form.querySelector(
        '[name="g-recaptcha-response"]'
      );
      if (!captchaResponse || !captchaResponse.value.trim()) {
        showSubmissionError("Complete the reCAPTCHA verification to continue.");
        return;
      }
    }

    clearSubmissionError();
    var formData = new URLSearchParams(new FormData(form));
    var button = form.querySelector('[type="submit"]');
    button.disabled = true;
    button.textContent = "Sending…";

    fetch(form.action, {
      body: formData,
      method: "POST",
      mode: "no-cors",
    })
      .then(showSubmissionConfirmation)
      .catch(function () {
        showSubmissionError(
          "We couldn’t confirm that your request was sent. Please wait a few minutes before trying again."
        );
      })
      .finally(resetSubmitButton);
  }

  function showSubmissionConfirmation() {
    modal.querySelector("#extole-sandbox-title").textContent = "Request sent";
    modal.querySelector("#extole-sandbox-description").textContent =
      "We’ve sent your details for review. We’ll email you with next steps.";
    form.hidden = true;
    modal.querySelector(".extole-sandbox-success").hidden = false;
  }

  function showSubmissionError(message) {
    var error = modal.querySelector(".extole-sandbox-error");
    error.textContent = message;
    error.hidden = false;
  }

  function clearSubmissionError() {
    var error = modal.querySelector(".extole-sandbox-error");
    error.textContent = "";
    error.hidden = true;
  }

  function resetSubmitButton() {
    var button = form.querySelector('[type="submit"]');
    button.disabled = false;
    button.textContent = "Request sandbox";
  }

  function resetModal() {
    form.reset();
    resetCaptcha();
    clearSubmissionError();
    resetSubmitButton();
    form.hidden = false;
    modal.querySelector(".extole-sandbox-success").hidden = true;
    modal.querySelector("#extole-sandbox-title").textContent = "Request a Sandbox";
    modal.querySelector("#extole-sandbox-description").textContent =
      "Tell us about yourself and we’ll help you get started.";
  }

  function hideBackground() {
    var children = document.body.children;
    hiddenSiblings = [];
    for (var i = 0; i < children.length; i++) {
      if (children[i] === modal) continue;
      hiddenSiblings.push({
        node: children[i],
        value: children[i].getAttribute("aria-hidden"),
      });
      children[i].setAttribute("aria-hidden", "true");
    }
  }

  function restoreBackground() {
    for (var i = 0; i < hiddenSiblings.length; i++) {
      var item = hiddenSiblings[i];
      if (item.value === null) item.node.removeAttribute("aria-hidden");
      else item.node.setAttribute("aria-hidden", item.value);
    }
    hiddenSiblings = [];
  }

  function openModal(trigger) {
    lastTrigger = trigger || document.activeElement;
    setReturnUrl();
    modal.hidden = false;
    document.documentElement.classList.add("extole-sandbox-open");
    hideBackground();
    var focusTarget = form.hidden
      ? modal.querySelector(".extole-sandbox-close")
      : form.querySelector('[name="full_name"]');
    focusTarget.focus();
  }

  function closeModal() {
    resetModal();
    modal.hidden = true;
    document.documentElement.classList.remove("extole-sandbox-open");
    restoreBackground();
    if (lastTrigger && typeof lastTrigger.focus === "function") lastTrigger.focus();
  }

  function trapFocus(event) {
    if (event.key !== "Tab") return;
    var focusable = dialog.querySelectorAll(
      'button:not([disabled]), input:not([disabled]), [href], [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function addModal() {
    if (document.getElementById("extole-request-sandbox-modal")) return;
    var wrapper = document.createElement("div");
    var captchaMarkup = "";

    if (captchaEnabled) {
      captchaMarkup =
        '<input type="hidden" name="captcha_settings" value=\'{"keyname":"Developer_Docs_WebToLead_v2","fallback":"true","orgId":"00D400000009iMx","ts":""}\'>' +
        '<div class="extole-sandbox-captcha"><div class="g-recaptcha" data-sitekey="6LecTeItAAAAAJ92rFMWrCosWV7_AWzWpgwIYeIk"></div></div>';
    }

    wrapper.className = "extole-sandbox-modal";
    wrapper.id = "extole-request-sandbox-modal";
    wrapper.hidden = true;
    wrapper.innerHTML =
      '<div class="extole-sandbox-dialog" role="dialog" aria-modal="true" aria-labelledby="extole-sandbox-title" aria-describedby="extole-sandbox-description">' +
      '<button class="extole-sandbox-close" type="button" aria-label="Close request sandbox form">×</button>' +
      '<h2 id="extole-sandbox-title">Request a Sandbox</h2>' +
      '<p id="extole-sandbox-description">Tell us about yourself and we’ll help you get started.</p>' +
      '<form class="extole-sandbox-form" method="post" action="https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8&orgId=00D400000009iMx">' +
      '<input type="hidden" name="oid" value="00D400000009iMx">' +
      '<input type="hidden" name="Campaign__c" value="Developer Docs">' +
      '<input type="hidden" name="lead_source" value="Inbound - Organic">' +
      captchaMarkup +
      '<input type="hidden" name="first_name">' +
      '<input type="hidden" name="last_name">' +
      '<input type="hidden" name="retURL">' +
      '<div class="extole-sandbox-field"><label for="extole-sandbox-name">Name</label><input id="extole-sandbox-name" name="full_name" autocomplete="name" required></div>' +
      '<div class="extole-sandbox-field"><label for="extole-sandbox-title-field">Title</label><input id="extole-sandbox-title-field" name="title" autocomplete="organization-title" required></div>' +
      '<div class="extole-sandbox-field"><label for="extole-sandbox-company">Company</label><input id="extole-sandbox-company" name="company" autocomplete="organization" required></div>' +
      '<div class="extole-sandbox-field"><label for="extole-sandbox-email">Email</label><input id="extole-sandbox-email" name="email" type="email" autocomplete="email" required></div>' +
      '<p class="extole-sandbox-error" aria-live="assertive" hidden></p>' +
      '<button class="extole-sandbox-submit" type="submit">Request sandbox</button>' +
      '</form>' +
      '<div class="extole-sandbox-success" aria-live="polite" hidden><span class="extole-sandbox-success-icon" aria-hidden="true">✓</span><div class="extole-sandbox-success-copy"><h3>In the meantime</h3><p>Explore the documentation while we prepare your sandbox.</p></div><button class="extole-sandbox-submit" type="button">Return to documentation</button></div>' +
      '</div>';
    document.body.appendChild(wrapper);
    modal = wrapper;
    dialog = wrapper.querySelector(".extole-sandbox-dialog");
    form = wrapper.querySelector("form");
    if (captchaEnabled) {
      loadCaptcha();
      window.setInterval(updateCaptchaTimestamp, 500);
    }

    form.addEventListener("submit", submitToSalesforce);
    wrapper.querySelector(".extole-sandbox-close").addEventListener("click", closeModal);
    wrapper.querySelector(".extole-sandbox-success button").addEventListener("click", closeModal);
    wrapper.addEventListener("click", function (event) {
      if (event.target === wrapper) closeModal();
    });
    dialog.addEventListener("keydown", trapFocus);
    document.addEventListener("keydown", function (event) {
      if (!modal.hidden && event.key === "Escape") closeModal();
    });
  }

  function bindTriggers(root) {
    var links = root && root.querySelectorAll ? root.querySelectorAll('a[href="#request-sandbox"]') : triggerLinks();
    for (var i = 0; i < links.length; i++) {
      if (links[i].dataset.extoleSandboxTrigger) continue;
      links[i].dataset.extoleSandboxTrigger = "true";
      links[i].addEventListener("click", function (event) {
        event.preventDefault();
        openModal(event.currentTarget);
      });
    }
  }

  addModal();
  bindTriggers();
  if (new URLSearchParams(window.location.search).get("sandbox-request") === "submitted") {
    window.history.replaceState({}, "", window.location.pathname + window.location.hash);
    showSubmissionConfirmation();
    openModal();
  }
  new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i++) {
      for (var j = 0; j < mutations[i].addedNodes.length; j++) {
        var node = mutations[i].addedNodes[j];
        if (node.nodeType === 1) bindTriggers(node);
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
