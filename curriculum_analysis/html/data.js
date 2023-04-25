async function loadJSON(url) {
    const response = await fetch(url);
    return response.json();
}
