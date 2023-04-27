const target = document.getElementById('target');

function addMetaData(item) {
    item.count = Object.entries(item.data).reduce((total, [keyword, sections]) => {
        const keyword_count = Object.values(sections).reduce((kw_total, arr) => kw_total + arr.length, 0); 
        return total + keyword_count;
    }, 0);
    return item;
}

function elementFromItem(item) {
    const row = document.createElement('tr');
    const code = document.createElement('td');
    const title = document.createElement('td');
    const details = document.createElement('td');

    const link = document.createElement('a');
    link.href = `./module.html?code=${item.code}`;
    link.textContent = `${item.code}`;
    code.append(link);
    title.textContent = `${item.title}`;
    details.textContent = item.count;
    if(item.count) {
        row.classList.add("found")
    }
    row.append(code, title, details);
    return row;
}

loadJSON('summary.json').then(data => {
    const articles = data.map(addMetaData).sort((a, b) => b.count - a.count).map(elementFromItem);
    target.append(...articles);
})