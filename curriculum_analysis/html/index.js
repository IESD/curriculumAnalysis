const target = document.getElementById('target');

function addMetaData(item) {
    item.count = Object.entries(item.data).reduce((total, [keyword, sections]) => {
        const keyword_count = Object.values(sections).reduce((kw_total, arr) => kw_total + arr.length, 0); 
        return total + keyword_count;
    }, 0);
    return item;
}

function elementFromItem(item) {
    const result = document.createElement('tr');
    const code = document.createElement('td');
    code.textContent = `${item.code}`;
    const title = document.createElement('td');
    title.textContent = `${item.title}`;
    const details = document.createElement('td');
    details.textContent = item.count;
    if(item.count) {
        result.classList.add("found")
    }
    result.append(code, title, details);
    return result;
}

loadJSON('summary.json').then(data => {
    const articles = data.map(addMetaData).map(elementFromItem);
    target.append(...articles);
})