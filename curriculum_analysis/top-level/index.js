const target = document.getElementById('target');

function elementFromItem(item) {
    const row = document.createElement('tr');
    const url = document.createElement('td');

    const link = document.createElement('a');
    link.href = item.url;
    link.textContent = item.title;
    url.append(link);
    row.append(url);
    return row;
}

loadJSON('summary.json').then(data => {
    const articles = data.map(elementFromItem);
    target.append(...articles);
})