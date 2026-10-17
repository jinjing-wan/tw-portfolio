/*
 * 左侧导航交互（alabaster 主题）
 * 1) 分组标题（toctree :caption:）默认折叠，点击展开子页面。
 * 2) 当前页「本页目录」({{ toc }}) 从隐藏容器搬到「当前所在导航行」下方，
 *    形成 点击的页面 → 其下展示本页目录 的上下文式布局，而不是浮在导航上方。
 * 3) 例外：DEFAULT_OPEN 名单里的分组（参考）默认展开；其余一律折叠，
 *    当前页所在分组不再强制展开（页面进入时即折叠）。
 * 静态站点无状态，每次加载都重新计算。
 */
(function () {
  "use strict";

  // 默认展开的分组标题关键字（含其一即展开）。参考页面常驻展开方便查 API 树。
  var DEFAULT_OPEN = ["参考", "Reference"];

  function initSidebarCollapse() {
    var sidebar = document.querySelector(".sphinxsidebar");
    if (!sidebar) return;

    // --- 1) 分组折叠 ---
    var captions = sidebar.querySelectorAll("p.caption");
    for (var i = 0; i < captions.length; i++) {
      (function (cap) {
        if (cap.getAttribute("data-collapse-init")) return;
        cap.setAttribute("data-collapse-init", "1");

        var ul = cap.nextElementSibling;
        if (!ul || ul.tagName.toLowerCase() !== "ul") return;

        var label = (cap.textContent || "").trim();
        var shouldOpen = DEFAULT_OPEN.some(function (k) {
          return label.indexOf(k) >= 0;
        });

        cap.classList.toggle("open", shouldOpen);
        ul.style.display = shouldOpen ? "block" : "none"; // 默认折叠，参考例外

        cap.addEventListener("click", function () {
          var isOpen = cap.classList.toggle("open");
          ul.style.display = isOpen ? "block" : "none";
        });
      })(captions[i]);
    }

    // --- 2) 把本页目录搬到当前导航行下方（无论该分组是否折叠，均在 DOM 内完成）---
    var tocSrc = document.getElementById("localtoc-current");
    var curAnchor = sidebar.querySelector("a.current");
    var curLi = curAnchor ? curAnchor.parentElement : null;

    if (tocSrc && curLi) {
      var tocUl = tocSrc.querySelector("ul");
      if (tocUl) {
        tocUl.classList.add("localtoc-moved");
        curLi.appendChild(tocUl); // 直接挂到当前页那一行下面
      }
      if (tocSrc.parentNode) tocSrc.parentNode.removeChild(tocSrc);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSidebarCollapse);
  } else {
    initSidebarCollapse();
  }
})();
