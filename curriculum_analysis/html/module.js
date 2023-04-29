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
    itemCode.textContent = item.code;
    itemName.textContent = item.title;

    const results = Object.entries(item.results).filter(([section, {keywords, tokens, total}]) => {
        return tokens.length;
    })
    
    console.log(results);

    const articles = results.map(([section, {keywords, tokens, total}]) => {
        const result = document.createElement('article');
        const h2 = document.createElement("h2");
        const pills = document.createElement("div");
        const highlightedText = document.createElement("p");
        const totalSpan = document.createElement('span');

        pills.classList.add("pills");
        h2.textContent = section
        totalSpan.textContent = `(found ${total})`;

        const hueStep = 360 / Object.keys(keywords).length;
        let hue = 0;

        Object.entries(keywords).forEach(([kw, indices]) => {
            hue += hueStep;
            for(const index of indices) {
                tokens[index] = `<span class="keyword" style="background: hsl(${hue}, 50%, 70%)">${tokens[index]}</span>`;
            }
            if(indices.length) {
                const pill = document.createElement('span');
                const count = document.createElement('span');
                pill.classList.add('pill');
                count.classList.add('count');
                pill.textContent = kw;
                pill.style.background = `hsl(${hue}, 50%, 70%)`;
                count.textContent = indices.length;
                pill.append(count);
                pills.append(pill);
            }
        });
        text = tokens.join(' ');
        highlightedText.innerHTML = text;
        result.append(h2, pills, highlightedText);
        return result;
    })
    target.append(...articles);

    // const data = Object.entries(item.summary).filter(([kw, count]) => {
    //     return count;
    // }).map(([kw, count]) => {
    //     return Object.entries(item.data[kw]).filter(([location, instances]) => instances.length).map(([location, instances]) => {
    //         return {location: location, text: item.raw[location], keyword: kw}
    //     }).flat();
    // }).flat();
    // target.append(sectionFromData(data));
}

loadJSON('summary.json').then(data => {
    const item = data.find(item => item.code == code);
    generatePage(item);
})