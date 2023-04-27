const target = document.getElementById('target');
const itemCode = document.getElementById('itemCode');
const itemName = document.getElementById('itemName');

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const code = urlParams.get('code');

function sectionFromData(data) {
    const section = document.createElement("section");
    const articles = data.map(articleFromInstance)
    section.append(...articles);
    return section;
}

function articleFromInstance({keyword, location, text}) {
    const article = document.createElement("article");
    const h2 = document.createElement("h2");
    const kwSpan = document.createElement("span");
    const locSpan = document.createElement("span");
    const p = document.createElement("p");
    kwSpan.classList.add("keyword")
    locSpan.classList.add("location")
    kwSpan.textContent = keyword;
    locSpan.textContent = location;
    h2.append("keyword: ", kwSpan, " found in ", locSpan);
    console.log(text.split(/\n/));
    const re = RegExp(keyword.toLowerCase(), 'g');
    console.log(re);
    p.innerHTML = text.toLowerCase().replace(re, `<span class="keyword">${keyword}</span>`);
    article.append(h2, p);
    return article;
}

function generatePage(item) {
    console.log(item);
    itemCode.textContent = `${item.code}`;
    itemName.textContent = `${item.title}`;

    const data = Object.entries(item.summary).filter(([kw, count]) => {
        return count;
    }).map(([kw, count]) => {
        return Object.entries(item.data[kw]).filter(([location, instances]) => instances.length).map(([location, instances]) => {
            return {location: location, text: item.raw[location], keyword: kw}
        }).flat();
    }).flat();
    target.append(sectionFromData(data));
}

loadJSON('summary.json').then(data => {
    const item = data.find(item => item.code == code);
    generatePage(item);
})