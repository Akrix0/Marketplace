(function () {
  "use strict";

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

  document.addEventListener("DOMContentLoaded", function () {
    initGallery();
    initImageUpload();
    initInfiniteScroll();
  });
})();
