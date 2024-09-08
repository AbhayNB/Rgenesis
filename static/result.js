document.querySelector('.collapsible-button').addEventListener('click', function() {
    const collapsible = document.querySelector('.collapsible');
    collapsible.style.display = collapsible.style.display === 'none' ? 'block' : 'none';
});