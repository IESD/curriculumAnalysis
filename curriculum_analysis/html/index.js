const target = document.getElementById('target');

async function loadJSON(url) {
    const response = await fetch(url);
    return response.json();
}


function elementFromItem(item) {
    console.log(item);
    const result = document.createElement('tr');
    const code = document.createElement('td');
    code.textContent = `${item.code}`;
    result.append(code)
    const title = document.createElement('td');
    title.textContent = `${item.title}`;
    result.append(title);
    return result;
}

loadJSON('summary.json').then(data => {
    const articles = data.map(elementFromItem);
    target.append(...articles);
})