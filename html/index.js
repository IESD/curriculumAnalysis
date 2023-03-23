const target = document.getElementById('target');

async function loadJSON(url) {
    const response = await fetch(url);
    return response.json();
}


function elementFromItem(item) {
    console.log(item);
    const result = document.createElement('li');
    const title = document.createElement('span');
    title.textContent = `${item.code} ${item.title}`;   
    // const h2 = document.createElement('h2');
    // h2.textContent = item.code;
    result.append(title);
    return result;
}

loadJSON('summary.json').then(data => {
    const articles = data.map(elementFromItem);
    target.append(...articles);
})