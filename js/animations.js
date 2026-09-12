/**
 * Fu-Glide Shared Entrance Animations
 * Observes .animate-in elements with IntersectionObserver,
 * automatically calculating incremental stagger delays for sibling elements (80ms apart).
 */
(function () {
  'use strict';

  var observer = null;

  function isReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function applySiblingStaggers(elements) {
    var parentMap = new Map();

    elements.forEach(function (el) {
      // If the element already has custom stagger delay defined inline, skip
      if (el.style.getPropertyValue('--stagger-delay') || el.style.transitionDelay) {
        return;
      }

      var parent = el.parentElement;
      if (!parent) return;

      if (!parentMap.has(parent)) {
        parentMap.set(parent, []);
      }
      parentMap.get(parent).push(el);
    });

    parentMap.forEach(function (siblings) {
      if (siblings.length > 1) {
        siblings.forEach(function (el, index) {
          el.style.setProperty('--stagger-delay', (index * 80) + 'ms');
        });
      }
    });
  }

  function setupObserver() {
    if (observer) return observer;

    var observerOptions = {
      root: null,
      rootMargin: '0px 0px 50px 0px',
      threshold: 0.02
    };

    observer = new IntersectionObserver(function (entries, obsInstance) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obsInstance.unobserve(entry.target);
        }
      });
    }, observerOptions);

    return observer;
  }

  function initAnimations() {
    var elements = Array.prototype.slice.call(document.querySelectorAll('.animate-in:not(.is-visible)'));
    if (!elements.length) return;

    if (isReducedMotion()) {
      elements.forEach(function (el) {
        el.classList.add('is-visible');
      });
      return;
    }

    applySiblingStaggers(elements);

    var obs = setupObserver();
    elements.forEach(function (el) {
      obs.observe(el);
    });
  }

  // Initialize as early as DOM is interactive
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnimations);
  } else {
    initAnimations();
  }

  // Also re-run on window load and export global hook
  window.addEventListener('load', initAnimations);
  window.initScrollAnimations = initAnimations;

  // Observe dynamically injected DOM nodes (e.g. modular headers/footers)
  if (window.MutationObserver) {
    var domObserver = new MutationObserver(function (mutations) {
      var hasNewAnimateNodes = false;
      mutations.forEach(function (mutation) {
        for (var i = 0; i < mutation.addedNodes.length; i++) {
          var node = mutation.addedNodes[i];
          if (node.nodeType === 1) { // ELEMENT_NODE
            if (node.classList && node.classList.contains('animate-in')) {
              hasNewAnimateNodes = true;
              break;
            }
            if (node.querySelector && node.querySelector('.animate-in')) {
              hasNewAnimateNodes = true;
              break;
            }
          }
        }
      });
      if (hasNewAnimateNodes) {
        initAnimations();
      }
    });

    if (document.body) {
      domObserver.observe(document.body, { childList: true, subtree: true });
    } else {
      document.addEventListener('DOMContentLoaded', function () {
        domObserver.observe(document.body, { childList: true, subtree: true });
      });
    }
  }
})();
