var cardDrop = document.getElementById('card-dropdown');
var activeDropdown;
cardDrop.addEventListener('click', function () {
  var node;
  for (var i = 0; i < this.childNodes.length - 1; i++) {if (window.CP.shouldStopExecution(0)) break;
    node = this.childNodes[i];}window.CP.exitedLoop(0);
  if (node.className === 'dropdown-select') {
    node.classList.add('visible');
    activeDropdown = node;
  };
});

window.onclick = function (e) {
  console.log(e.target.tagName);
  console.log('dropdown');
  console.log(activeDropdown);
  if (e.target.tagName === 'LI' && activeDropdown) {
    if (e.target.innerHTML === 'Master Card') {
      document.getElementById('credit-card-image').src = {% static "images/MasterCard_Logo.png" %};
      activeDropdown.classList.remove('visible');
      activeDropdown = null;
      e.target.innerHTML = document.getElementById('current-card').innerHTML;
      document.getElementById('current-card').innerHTML = 'Master Card';
    } else
    if (e.target.innerHTML === 'American Express') {
      document.getElementById('credit-card-image').src = {% static "images/amex-logo.png" %};
      activeDropdown.classList.remove('visible');
      activeDropdown = null;
      e.target.innerHTML = document.getElementById('current-card').innerHTML;
      document.getElementById('current-card').innerHTML = 'American Express';
    } else
    if (e.target.innerHTML === 'Visa') {
      document.getElementById('credit-card-image').src = {% static "images/visa_logo.png" %};
      activeDropdown.classList.remove('visible');
      activeDropdown = null;
      e.target.innerHTML = document.getElementById('current-card').innerHTML;
      document.getElementById('current-card').innerHTML = 'Visa';
    }
  } else
  if (e.target.className !== 'dropdown-btn' && activeDropdown) {
    activeDropdown.classList.remove('visible');
    activeDropdown = null;
  }
};