(function () {
  "use strict";

  var STATIC_VERSION = "3";

  function boot() {
    initGallery();
    initImageUpload();
    initInfiniteScroll();

    var badge = document.querySelector("[data-cart-count]");
    if (badge) {
      var count = parseInt(badge.textContent, 10) || 0;
      badge.classList.toggle("is-zero", count === 0);
    }
  }

  function initGallery() {
    var mainImage = document.getElementById("gallery-main-image");
    var thumbs = document.querySelectorAll("[data-gallery-thumb]");

    if (!mainImage || !thumbs.length) {
      return;
    }

    thumbs.forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        var nextSrc = thumb.getAttribute("data-full-src");

        if (!nextSrc || thumb.classList.contains("is-active")) {
          return;
        }

        mainImage.classList.add("is-changing");

        window.setTimeout(function () {
          mainImage.src = nextSrc;
          mainImage.classList.remove("is-changing");
        }, 120);

        thumbs.forEach(function (item) {
          item.classList.remove("is-active");
          item.setAttribute("aria-pressed", "false");
        });

        thumb.classList.add("is-active");
        thumb.setAttribute("aria-pressed", "true");
      });
    });
  }

  function initImageUpload() {
    var uploadZone = document.querySelector("[data-upload-zone]");
    var fileInput = document.querySelector("[data-image-input]");
    var previewList = document.querySelector("[data-upload-preview]");

    if (!uploadZone || !fileInput || !previewList) {
      return;
    }

    function renderPreview(files) {
      previewList.innerHTML = "";

      if (!files.length) {
        previewList.hidden = true;
        return;
      }

      previewList.hidden = false;

      Array.from(files).forEach(function (file, index) {
        if (!file.type.startsWith("image/")) {
          return;
        }

        var item = document.createElement("li");
        item.className = "upload-preview__item";
        item.style.animationDelay = index * 40 + "ms";

        var image = document.createElement("img");
        image.alt = file.name;

        var caption = document.createElement("span");
        caption.className = "upload-preview__name";
        caption.textContent = file.name;

        item.appendChild(image);
        item.appendChild(caption);
        previewList.appendChild(item);

        var reader = new FileReader();
        reader.onload = function (event) {
          image.src = event.target.result;
        };
        reader.readAsDataURL(file);
      });
    }

    fileInput.addEventListener("change", function () {
      renderPreview(fileInput.files);
    });

    ["dragenter", "dragover"].forEach(function (eventName) {
      uploadZone.addEventListener(eventName, function (event) {
        event.preventDefault();
        uploadZone.classList.add("is-dragover");
      });
    });

    ["dragleave", "drop"].forEach(function (eventName) {
      uploadZone.addEventListener(eventName, function (event) {
        event.preventDefault();
        uploadZone.classList.remove("is-dragover");
      });
    });

    uploadZone.addEventListener("drop", function (event) {
      var files = event.dataTransfer.files;

      if (!files.length) {
        return;
      }

      fileInput.files = files;
      renderPreview(files);
    });
  }

  function initInfiniteScroll() {
    var grid = document.querySelector("[data-infinite-grid]");
    var wrapper = document.querySelector("[data-infinite-scroll]");
    var nextLink = document.querySelector("[data-infinite-next]");
    var status = document.querySelector("[data-infinite-status]");

    if (!grid || !wrapper || !nextLink || !("IntersectionObserver" in window) || !("fetch" in window)) {
      return;
    }

    var isLoading = false;
    nextLink.hidden = true;

    function setStatus(message) {
      if (status) {
        status.textContent = message;
      }
    }

    function loadNextPage() {
      var nextUrl = nextLink.getAttribute("href");

      if (isLoading || !nextUrl) {
        return;
      }

      isLoading = true;
      setStatus("Loading more products...");

      fetch(nextUrl, {
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      })
        .then(function (response) {
          if (!response.ok) {
            throw new Error("Unable to load products");
          }

          return response.text();
        })
        .then(function (html) {
          var parser = new DOMParser();
          var doc = parser.parseFromString(html, "text/html");
          var nextGrid = doc.querySelector("[data-infinite-grid]");
          var nextPageLink = doc.querySelector("[data-infinite-next]");

          if (!nextGrid) {
            wrapper.remove();
            return;
          }

          Array.from(nextGrid.children).forEach(function (item) {
            grid.appendChild(item);
          });

          if (nextPageLink) {
            nextLink.setAttribute("href", nextPageLink.getAttribute("href"));
            setStatus("");
          } else {
            wrapper.remove();
          }
        })
        .catch(function () {
          setStatus("Could not load more products.");
        })
        .finally(function () {
          isLoading = false;
        });
    }

    var observer = new IntersectionObserver(function (entries) {
      if (entries.some(function (entry) { return entry.isIntersecting; })) {
        loadNextPage();
      }
    }, {
      rootMargin: "240px 0px"
    });

    observer.observe(wrapper);
  }

  function getCsrfToken() {
    var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input && input.value) {
      return input.value;
    }

    var meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.getAttribute("content")) {
      return meta.getAttribute("content");
    }

    var match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function parseJsonResponse(response) {
    return response.text().then(function (text) {
      var data;
      try {
        data = JSON.parse(text);
      } catch (error) {
        throw new Error("Invalid server response");
      }

      if (!response.ok || !data.ok) {
        throw new Error((data && data.error) || "Request failed");
      }

      return data;
    });
  }

  function updateCartCount(count) {
    var badges = document.querySelectorAll("[data-cart-count]");
    badges.forEach(function (badge) {
      badge.textContent = count;
      badge.classList.toggle("is-zero", count === 0);
    });

    var triggers = document.querySelectorAll("[data-cart-trigger]");
    triggers.forEach(function (trigger) {
      trigger.setAttribute("aria-label", "Cart, " + count + " items");
    });
  }

  function animateCartAdded() {
    var trigger = document.querySelector("[data-cart-trigger]");
    var flash = document.querySelector("[data-cart-flash]");

    if (!trigger) {
      return;
    }

    trigger.classList.remove("is-added");
    window.requestAnimationFrame(function () {
      trigger.classList.add("is-added");
    });

    if (flash) {
      flash.classList.remove("is-visible");
      window.requestAnimationFrame(function () {
        flash.classList.add("is-visible");
      });
    }

    window.setTimeout(function () {
      trigger.classList.remove("is-added");
      if (flash) {
        flash.classList.remove("is-visible");
      }
    }, 900);
  }

  function postFormAjax(form) {
    var body = new FormData(form);

    return fetch(form.getAttribute("action"), {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCsrfToken()
      },
      body: body
    }).then(parseJsonResponse);
  }

  function getCartRow(form) {
    return form.closest("[data-cart-item-row]");
  }

  function updateRowSubtotal(row, quantity, currency) {
    var subtotalEl = row ? row.querySelector("[data-item-subtotal]") : null;
    var unitPrice = row ? parseFloat(row.getAttribute("data-unit-price") || "0") : 0;

    if (!subtotalEl) {
      return;
    }

    var subtotal = (unitPrice * quantity).toFixed(2);
    subtotalEl.innerHTML = subtotal + ' <span class="cart-item__currency">' + currency + "</span>";
  }

  function syncRowQuantityForms(row, quantity) {
    if (!row) {
      return;
    }

    row.querySelectorAll("[data-qty-form]").forEach(function (form) {
      var action = form.getAttribute("data-qty-action");
      var quantityInput = form.querySelector("input[name='quantity']");
      var button = form.querySelector("button[type='submit']");

      if (!quantityInput) {
        return;
      }

      if (action === "decrease") {
        quantityInput.value = String(Math.max(quantity - 1, 0));
        if (button) {
          button.disabled = quantity <= 1;
        }
      } else if (action === "increase") {
        quantityInput.value = String(Math.min(quantity + 1, 99));
      } else if (action === "remove") {
        quantityInput.value = "0";
      } else if (action === "set") {
        quantityInput.value = String(quantity);
      }
    });
  }

  function handleCartItemRemoved(row) {
    if (!row) {
      window.location.reload();
      return;
    }

    row.classList.add("is-removing");
    window.setTimeout(function () {
      row.remove();
      var list = document.querySelector("[data-cart-list]");
      if (list && !list.children.length) {
        window.location.reload();
      }
    }, 220);
  }

  function handleCartFormSubmit(form) {
    var row = getCartRow(form);
    if (row) {
      row.classList.add("is-updating");
    }

    return postFormAjax(form)
      .then(function (data) {
        updateCartCount(data.cart_count);

        if (data.removed) {
          handleCartItemRemoved(row);
          return;
        }

        syncRowQuantityForms(row, data.quantity);
        updateRowSubtotal(row, data.quantity, data.currency);
      })
      .catch(function () {
        window.alert("Could not update cart.");
      })
      .finally(function () {
        if (row) {
          row.classList.remove("is-updating");
        }
      });
  }

  document.addEventListener("submit", function (event) {
    var form = event.target;

    if (form && form.matches && form.matches("[data-add-to-cart]")) {
      event.preventDefault();

      var button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
      }

      postFormAjax(form)
        .then(function (data) {
          updateCartCount(data.cart_count);
          animateCartAdded();
        })
        .catch(function () {
          window.alert("Could not add product to cart.");
        })
        .finally(function () {
          if (button) {
            button.disabled = false;
          }
        });
      return;
    }

    if (!form || !form.matches || !form.matches("[data-qty-form]")) {
      return;
    }

    if (!window.fetch) {
      return;
    }

    event.preventDefault();
    handleCartFormSubmit(form);
  });

  document.addEventListener("change", function (event) {
    var input = event.target;
    if (!input || !input.matches || !input.matches("[data-qty-action='set'] input[name='quantity']")) {
      return;
    }

    var value = parseInt(input.value, 10);
    if (Number.isNaN(value) || value < 1) {
      input.value = "1";
      value = 1;
    }
    if (value > 99) {
      input.value = "99";
      value = 99;
    }

    var form = input.closest("[data-qty-form]");
    if (!form || !window.fetch) {
      return;
    }

    handleCartFormSubmit(form);
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.MarketplaceStaticVersion = STATIC_VERSION;
})();
