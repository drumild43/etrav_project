let searcharray = [
    'Asian Future-01','Bourge ','Campus', 'Furo', 'Furios-89', 'Hravso Grsk', 'Lancer ',
     'Nivia Verdict', 'Reebok Revolution', 'Sparx Sx0414g', 'Bacca Bucci', 'Cebtrio', 
    
  
  ];
  
  const searchInput = document.getElementById('inputbar');
  const searchbar = document.querySelector('.searchbar');
  const resultsbar = document.querySelector('.results');
  
  searchInput.addEventListener('keyup', () => {
    let results = [];
    let input = searchInput.value;
    if (input.length) {
      results = searcharray.filter((item) => {
        return item.toLowerCase().includes(input.toLowerCase());
      });
    }
    renderResults(results);
  });
  
  function renderResults(results) {
    if (!results.length) {
      return searchbar.classList.remove('show');
    }
  
    const content = results
      .map((item) => {
        return `<li>${item}</li>`;
      })
      .join('');
  
    searchbar.classList.add('show');
    resultsbar.innerHTML = `<ul>${content}</ul>`;
  }
  
gsap.from(".logo", { opacity: 0, duration: 1, delay: 0.5, y: -10 });
gsap.from(".hamburger", { opacity: 0, duration: 1, delay: 1, x: 20 });
gsap.from(".h1", { opacity: 0, duration: 1, delay: 1.5, x: -200 });
gsap.from(".img-content h2", { opacity: 0, duration: 1, delay: 2, y: -50 });
gsap.from(".img-content h1", { opacity: 0, duration: 1, delay: 2.5, y: -45 });
gsap.from(".gimg", { opacity: 0, duration: 1, delay: 2.5, x: -45 });
gsap.from(".img-content a", { opacity: 0, duration: 1, delay: 3.5, y: 50 });
gsap.from(".box", { opacity: 0, duration: 0.5, delay: 1, x: -100 });

