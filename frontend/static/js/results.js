// results.js

document.addEventListener('DOMContentLoaded', function () {
  const homeIcon = document.getElementById('home-icon');
  const totalCnt = document.getElementById('total-counts');
  const pageInfo = document.getElementById('page-info');
  const resultsContainer = document.getElementById('result-details');
  const backIcon = document.getElementById('back-icon');
  const nextIcon = document.getElementById('next-icon');

  // Initialize search results data
  const searchResults = JSON.parse(resultsContainer.textContent);
  const itemsPerPage = 10;
  const totalResults = searchResults.length;
  let currentItems;
  let currentPage = 1;
  let totalPages = Math.ceil(totalResults / itemsPerPage);

  function navToSearchPage() {
    window.location.href = '/search';
  }

  function handlePrevious() {
    if (currentPage > 1)
      currentPage--;
    renderResults();
    window.scrollTo(0, 0);
  }

  function handleNext() {
    if (currentPage < totalPages)
      currentPage++;
    renderResults();
    window.scrollTo(0, 0);
  }

  function renderResults() {
    function truncateText(text, length) {
      // Check if the length of the text exceeds given characters
      if (text.length > length) return text.substring(0, length-4) + "...";
      else return text;
    }
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    currentItems = searchResults.slice(start, end);

    // Insert resultItems into HTML
    resultsContainer.innerHTML = '';
    currentItems.forEach(item => {
      const title = `<h3>${truncateText(item.title, 68)}</h3>`;
      const div = document.createElement('div');
      div.className = 'result-item';
      // Define result text components
      let idInfo = `<div class="info"><p><b>ID:</b> ${item.id}`;
      let content = `<div class="text"><b>Contents:</b> ${item.content}</div></p>`;
      let timeInfo = `<div class="info">`;
      let audioInfo = ``;
      // Append result text components
      if ('score' in item)
        idInfo += `&emsp;&emsp; <b>Score:</b> ${item['score']}`;
      if ('start@' in item && 'end@' in item) {
        const startTime = new Date(item[`start@`] * 1000).toISOString().slice(11, 19);
        const endAtTime = new Date(item[`end@`] * 1000).toISOString().slice(11, 19);
        timeInfo += `<b>Start:</b> <font face="Arial">${startTime}</font>
        &emsp;&emsp;<b>End at:</b> <font face="Arial">${endAtTime}</font>`;
      }
      idInfo += `&emsp;&emsp; <b>Rank:</b> ${item[`rank`]}</p></div><p>`;
      // Metadata update (v2.0)
      if ('episode' in item) {
        const linkName = truncateText(`${item[`episode`]}`, 48);
        timeInfo += `&emsp;&emsp; <b>Audio: <font color="#3779c9">${linkName}</font></b>`;
      }
      timeInfo += `</p></div><p>`;
      if ('url' in item) {
        audioInfo += `<audio id="audioPlayer${item[`rank`]}" controls style="width: 440px; height: 6%;">
          <source src="${item[`url`]}" type="audio/mpeg">
          &emsp; Your browser does not support the audio element.
        </audio></p><p>`;
      }
      function audioClip(startTime) {
        const audio = document.getElementById('audioPlayer'.concat(item[`rank`]));
        if (audio !== null) {
          audio.currentTime = startTime;
        }
      }
      // Replace text of innerHTML with resultItems
      div.innerHTML = title.concat(idInfo, audioInfo, timeInfo, content);
      resultsContainer.appendChild(div);
      audioClip(item['start@'])
    });

    pageInfo.innerHTML = `<i>Showing Page</i> ${currentPage} of ${totalPages}`;
    totalCnt.innerHTML = `<b>Top ${totalResults} search ${totalResults === 1?'result':'results'}</b>`;
  }

  renderResults();
  homeIcon.addEventListener('click', navToSearchPage);
  backIcon.addEventListener('click', handlePrevious);
  nextIcon.addEventListener('click', handleNext);
  console.log(searchResults);
});