(function () {
  'use strict';

  var stageButtons = document.querySelectorAll('.event-flow__button');
  var stageDetail = document.getElementById('event-stage-detail');

  if (!stageButtons.length || !stageDetail) return;

  stageButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      stageButtons.forEach(function (stageButton) {
        stageButton.setAttribute('aria-pressed', String(stageButton === button));
      });

      stageDetail.textContent = button.getAttribute('data-detail');
    });
  });
})();
