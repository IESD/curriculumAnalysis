const target = document.getElementById('target');

function elementFromItem(item) {
    console.log(item);
    const row = document.createElement('tr');
    const code = document.createElement('td');
    const title = document.createElement('td');
    const details = document.createElement('td');
    const link = document.createElement('a');

    link.href = `./module.html?code=${item.code}`;
    link.textContent = item.code;
    title.textContent = item.title;
    details.textContent = item.total;
    if(item.total) {
        row.classList.add("found")
    }

    code.append(link);
    row.append(code, title, details);
    return row;
}

loadJSON('summary.json').then(data => {
    const articles = data.sort((a, b) => b.total - a.total).map(elementFromItem);
    target.append(...articles);
})