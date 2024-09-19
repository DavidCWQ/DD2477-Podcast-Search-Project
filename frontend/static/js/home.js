// home.js

document.addEventListener('DOMContentLoaded', function () {
  const backgroundImage = document.getElementById('background-image');
  backgroundImage.addEventListener('click', function () {
    window.location.href = '/search';
  });
});